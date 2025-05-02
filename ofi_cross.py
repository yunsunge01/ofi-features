from __future__ import annotations
import pandas as pd


def pivot_cross_asset(df_ofi: pd.DataFrame,
                      value_col: str = "integrated_ofi") -> pd.DataFrame:
    pivot = (
        df_ofi
        .pivot_table(index="timestamp",
                     columns="symbol",
                     values=value_col,
                     fill_value=0.0)
        .sort_index()
    )
    
    pivot.columns = [f"{sym}_{value_col}" for sym in pivot.columns]
    return pivot.reset_index()
