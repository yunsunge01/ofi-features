from pathlib import Path
import pandas as pd


def load_events(csv_path: str | Path,
                parse_dates: list[str] = ("ts_event",),
                cols_keep: list[str] | None = None) -> pd.DataFrame:
    df = pd.read_csv(csv_path, low_memory=False, parse_dates=list(parse_dates))
    if cols_keep is not None:
        df = df[cols_keep]
    df = df.sort_values("ts_event").reset_index(drop=True)
    return df


def resample_bucket(df_evt: pd.DataFrame,
                    freq: str = "1S") -> pd.DataFrame:
    df_grp = (
        df_evt
        .set_index("ts_event")
        .groupby("symbol", group_keys=False)
        .resample(freq)
    )
    return df_grp


def save_timeseries(df_ts: pd.DataFrame,
                    out_csv: str | Path,
                    index: bool = False) -> None:
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    df_ts.to_csv(out_csv, index=index)
    print(f"[+] Saved: {out_csv}")
