# Validation evidence available in public repository

The public release includes **90 genuine fold-level summary rows** in `results/fold_metrics.csv`: LightGBM, ridge and mean-baseline metrics for 30 folds over five validation protocols (10+5+5+6+4). These rows contain protocol, model, fold index, test-set size, R², RMSE and MAE; no building-level identifiers or per-record predictions are exposed.

Only aggregate geometry audit, feature-ablation, SHAP importance, and threshold sensitivity results are released. Building-linked training records, 22,875 original out-of-fold prediction rows, and 48,687 unique building-linked predictions are retained outside the public repo pending a separate dataset licence audit. The code's optional full-data steps require the independent local input archive.

**Numerical consistency warning:** the previous bundled `results/validation_metadata.json` gave 47,163 as the unlabelled sample count, whereas the deduplicated study inventory yields 47,162. That inconsistent JSON has been excluded pending a controlled recalculation. Do not silently use its counts in the manuscript.
