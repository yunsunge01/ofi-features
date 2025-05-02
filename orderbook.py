from __future__ import annotations
from typing import Literal

import pandas as pd
import numpy as np

# 0 ~ 9 (10 levels of deph)
_LEVELS = list(range(10))       
    
BID_COLS = [f"bid_sz_0{k}" for k in _LEVELS]
ASK_COLS = [f"ask_sz_0{k}" for k in _LEVELS]


def _melt_snapshot(df: pd.DataFrame,
                   side: Literal["bid", "ask"]) -> pd.DataFrame:
    cols = BID_COLS if side == "bid" else ASK_COLS
    out = (
        df[["ts_event", "symbol"] + cols]
        .melt(id_vars=["ts_event", "symbol"],
              value_vars=cols,
              var_name="col",
              value_name="qty")
    )
    out["level"] = out["col"].str.extract(r"(\d)$").astype(int)
    out.drop(columns="col", inplace=True)
    out["side"] = "B" if side == "bid" else "A"
    return out


def calc_delta_q(df_evt: pd.DataFrame) -> pd.DataFrame:
    bid_long = _melt_snapshot(df_evt, "bid")
    ask_long = _melt_snapshot(df_evt, "ask")
    long_df = pd.concat([bid_long, ask_long], ignore_index=True)
    long_df.sort_values(["symbol", "level", "side", "ts_event"],
                        inplace=True)
    long_df["dq"] = (
        long_df.groupby(["symbol", "level", "side"])["qty"]
               .diff()
               .fillna(long_df["qty"])    
    )
    return long_df.drop(columns="qty")
