from __future__ import annotations
import pandas as pd


def _apply_side_sign(df_long: pd.DataFrame) -> pd.Series:
    sign = df_long["side"].map({"B": 1, "A": -1})
    return df_long["dq"] * sign


def best_ofi(delta_q: pd.DataFrame,
             freq: str = "1S") -> pd.DataFrame:
    lvl0 = delta_q[delta_q["level"] == 0].copy()
    lvl0["signed_dq"] = _apply_side_sign(lvl0)

    best = (
        lvl0
        .set_index("ts_event")
        .groupby("symbol")
        .resample(freq)["signed_dq"]
        .sum()
        .reset_index()
        .rename(columns={"signed_dq": "best_ofi",
                         "ts_event":  "timestamp"})
    )
    return best


def multi_ofi(delta_q: pd.DataFrame,
              freq: str = "1S") -> pd.DataFrame:
    delta_q["signed_dq"] = _apply_side_sign(delta_q)

   
    agg = (
        delta_q
        .set_index("ts_event")
        .groupby(["symbol", "level"])        
        .resample(freq.lower())["signed_dq"] 
        .sum()
        .reset_index()
    )

    multi = (
        agg.pivot_table(index=["ts_event", "symbol"],
                        columns="level",
                        values="signed_dq",
                        fill_value=0)
        .reset_index()
    )
    multi.columns = (["timestamp", "symbol"]
                     + [f"ofi_lvl_{int(c)}" for c in multi.columns[2:]])
    return multi
