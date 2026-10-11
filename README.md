# Bologna building-footprint SAGA irradiation surrogate — corrected analysis code (2026)

Research code and **aggregate** results for: *Machine-Learning Surrogate for Building-Footprint Solar Irradiation Screening in a Dense European City* (Tabatabaei, Antonini, Gaspari; manuscript under preparation/review; no journal acceptance implied).

## Scope

The target is annual SAGA/DEM irradiation averaged, using fractional cell-area overlaps, over **original horizontal building footprints**. It is **not** measured rooftop irradiance, PV electricity output, or demonstrated computational savings. The historical 2026 thesis archive `10.5281/zenodo.22018674` concerns a 50-m-buffer target and should **not** be cited as a new corrected release.

The corrected LightGBM model uses **15 features and 800 trees**. The source dataset has 1,525 labelled footprints; the inventory has 48,687 unique IDs, with 47,162 outside the sample. Scores against the completed SAGA reference are surrogate-to-reference agreement, **not independent physical validation**.

## Public files and reproducibility

- `scripts/`: code for area-weighted reference extraction, 5 cross-validation protocols, final-inventory inference, SHAP and plotting. GIS features and original SAGA simulations were created upstream; this repository does **not** rebuild all raw source layers from scratch.
- `model/footprint_lightgbm_15features.txt`: final fitted LightGBM Booster (15 inputs; 800 trees).
- `results/fold_metrics.csv`: 90 **fold-level aggregate** metrics, LightGBM/ridge/mean across all five protocols.
- `results/`: geometry audit, feature-family ablation, mean absolute SHAP and threshold summaries.
- `figures/`: corrected SHAP plot; regenerated versions need the separate research inputs.
- `docs/FEATURES.md`: exact predictor definitions; `docs/ATTRIBUTION.md`: third-party provenance and licence notices.

### Deliberately not public here

Per-building training/inference/reference tables, OOF prediction rows, original building polygons, SAGA raster and GIS intermediates are **not contained in this public code-only release**. This is a conservative temporary publication choice while derivative-data licensing and data-release permissions are checked. Those research inputs are required for complete end-to-end reproduction of the reported numerical results. Aggregate statistics and the saved model can still be examined independently.

See `data/README.md` for the local input inventory and the difference between old `label_mean` (buffer target) and corrected `area_weighted_saga` (original-footprint target). Do not silently reconstruct missing rows or reclassify the old target as the corrected one.

## Quick checks (public files only)

```bash
python -m pip install -r requirements.txt
python scripts/verify.py
pytest tests/test_quick.py
```

To rerun correction, cross-validation and interpretation, obtain the internal input archive with appropriate data-use permissions, put its files under `data/local_inputs/`, then run:

```bash
python scripts/extract_reference.py
python scripts/validate.py
python scripts/inventory.py
python scripts/shap_plot.py
python scripts/plot_screening.py
```

The scripts distinguish the historical buffer labels from corrected SAGA footprint references and write regenerated results separately where feasible. The optional `data/local_inputs/` path is excluded by `.gitignore`.

## Provenance and licence

**MIT applies only to the original software code**, not to third-party datasets or any derived database subject to ODbL and other source licences. The model was trained using features derived in part from OpenStreetMap building footprints and public geospatial products. See `docs/ATTRIBUTION.md` for required source attribution. The model and research figures should be accompanied by this documentation when redistributed.

## Publication / archive

This is a code-and-aggregate release **pending coauthor review and a new archive identifier**. No DOI is assigned to this corrected package. The pre-existing Zenodo DOI `10.5281/zenodo.22018674` belongs only to the historical thesis version. Do not substitute the legacy DOI for a new archive citation.
