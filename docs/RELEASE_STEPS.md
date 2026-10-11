# New repository public code-only release

1. This directory is intended for a **new** repository, e.g. `Mahdiyeh1987/Bologna-Solar-Surrogate`. Do not overwrite the historical v1.0.0 thesis repository or its Zenodo archive.
2. Upload the **contents of this ZIP**, not the ZIP itself, preserving nested folder paths.
3. The building-level CSV tables and raw/intermediate geospatial files are deliberately absent from this package. Keep the private/local input ZIP off a public GitHub repository unless provenance and per-dataset publication licences are separately checked.
4. Run `python scripts/verify.py` and `pytest tests/test_quick.py`; these only verify the public model and aggregate fold results, and do not claim full end-to-end reproducibility without local inputs.
5. Before public release, obtain all coauthors' consent and confirm repository citation metadata / copyright.
6. If/when an approved code release is archived at Zenodo, update Data Availability in the manuscript to cite the actual **new** DOI. Do not cite the historical Zenodo DOI as though it contains the corrected footprint-target analysis.
7. This release preserves OSM, Copernicus, WorldCover and Comune di Bologna attribution in `docs/ATTRIBUTION.md`. The MIT licence applies to code, not externally sourced geographic datasets.
