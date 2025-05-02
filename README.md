# ofi-features

Before start
Download the packages in requirements.txt if needed.

Run to
python run.py
with the csv file in the same folder.

How each OFI is built

Outline
  Δq (quantity change)
  For every event snapshot,
  Δq = (current size − previous size) at each level & side.
  Bid Δq → +, Ask Δq → −
Best‑Level OFI
  ofi_basic.best_ofi
  Within a chosen time bucket (1s by default):
  best_ofi = Σ (Bid_Δq_lvl0 − Ask_Δq_lvl0)
Multi‑Level OFI
  ofi_basic.multi_ofi
  Same as above for each level 0‑9 → 10‑D vector ofi_lvl_0 … ofi_lvl_9
Integrated OFI
  ofi_integrated.fit_pca + integrated_ofi
  Fit PCA on historical Multi‑Level matrix.
  Keep first PC w (explain ≥ 89 % variance).
  integrated_ofi = wᵀ · multi_ofi (L¹‑norm of w = 1)
Cross‑Asset OFI
  ofi_cross.pivot_cross_asset
  Pivot Integrated‑OFI long table:
  index = timestamp, columns = symbol,
  values = integrated_ofi → wide matrix
  It will only show AAPL because the data given to use was only based on that.
