from __future__ import annotations
import joblib
from pathlib import Path
from typing import Sequence

import pandas as pd
from sklearn.decomposition import PCA


def fit_pca(df_multi: pd.DataFrame,
            level_cols: Sequence[str] | None = None,
            n_components: int = 1,
            save_path: str | Path | None = None) -> pd.Series:
   
    if level_cols is None:
        level_cols = [c for c in df_multi.columns if c.startswith("ofi_lvl_")]

    X = df_multi[level_cols].values
    pca = PCA(n_components=n_components)
    pca.fit(X)

    w = pca.components_[0]
    # normalize l1‑norm = 1 
    w = w / abs(w).sum()

    weights = pd.Series(w, index=level_cols, name="pca_weight")

    if save_path is not None:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(weights, save_path)
        print(f"[+] PCA weights saved → {save_path}")

    return weights


def integrated_ofi(df_multi: pd.DataFrame,
                   weights: pd.Series) -> pd.DataFrame:
    
    common_cols = weights.index.tolist()
    df = df_multi.copy()
    df["integrated_ofi"] = (df[common_cols] * weights).sum(axis=1)
    return df
