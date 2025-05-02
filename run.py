RAW_CSV     = "first_25000_rows.csv"      
OUT_CSV     = "out/ofi_features.csv"      
BUCKET_FREQ = "1s"
#bucket for timestamp.
# For example, 1s is for 1 second timestamp, 1m is for 1 minute.                        
PCA_HIST_N  = None                        

def main() -> None:
    from pathlib import Path
    from io_utils       import load_events, save_timeseries
    from orderbook      import calc_delta_q
    from ofi_basic      import best_ofi, multi_ofi
    from ofi_integrated import fit_pca, integrated_ofi
    from ofi_cross      import pivot_cross_asset

    bid_cols = [f"bid_sz_0{k}" for k in range(10)]
    ask_cols = [f"ask_sz_0{k}" for k in range(10)]
    use_cols = ["ts_event", "symbol"] + bid_cols + ask_cols
    events   = load_events(RAW_CSV, cols_keep=use_cols)
    print(f"[1] Loaded {len(events):,} events")

    delta_q  = calc_delta_q(events)
    print("[2] Δq calculated")

    best_df  = best_ofi(delta_q,  freq=BUCKET_FREQ)
    multi_df = multi_ofi(delta_q, freq=BUCKET_FREQ)
    print("[3] Best‑Level & Multi‑Level OFI done")

    hist_df  = multi_df if PCA_HIST_N is None else multi_df.head(PCA_HIST_N)
    weights  = fit_pca(hist_df)
    integ_df = integrated_ofi(multi_df, weights)
    print("[4] Integrated OFI done")

    cross_df = pivot_cross_asset(integ_df, "integrated_ofi")
    print("[5] Cross‑Asset OFI pivot complete")

    per_symbol = (
        best_df
        .merge(multi_df, on=["timestamp", "symbol"], how="left")
        .merge(integ_df[["timestamp", "symbol", "integrated_ofi"]],
               on=["timestamp", "symbol"], how="left")
    )

    final = cross_df.merge(per_symbol, on="timestamp", how="left")

    Path(OUT_CSV).parent.mkdir(parents=True, exist_ok=True)
    save_timeseries(final, OUT_CSV)
    print(f"[+] All four OFIs saved to {OUT_CSV} ({len(final):,} rows)")

if __name__ == "__main__":
    main()
