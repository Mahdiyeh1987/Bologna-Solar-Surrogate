# Data provenance and restricted public subset

The public GitHub release intentionally **omits building-level data** until licences governing derived OSM geometry and ancillary inputs are reviewed for a dataset release. The code/data split is a precaution, not an assertion that these datasets cannot be published.

## Optional local archive (NOT for automatic public upload)

Unpack `Bologna_Local_Inputs.zip` into `data/local_inputs/` on your own machine; do not commit that folder.

- `roof_blocks_s1.gpkg`: OSM-derived Bologna polygon inventory (51,980 clipped polygons)
- `roof_step7_1525.gpkg`: historical 50 m buffers for 1,525 sampled footprints
- `G_year_kWh_clip.tif`: precomputed SAGA annual irradiation raster from Copernicus GLO-30 inputs
- `train_dataset.csv`: historical 1,525-row features and buffered `label_mean` (not corrected target)
- `inference_features.csv`: 48,688 inventory feature rows, one repeated roof ID
- `city_footprints_revised.gpkg`: 48,687 distinct final footprints and outputs

The corrected response must be derived as `area_weighted_saga` from the SAGA raster and the **original polygon geometry**, not from `label_mean`.

## Licences and required credit

See `../docs/ATTRIBUTION.md`. OpenStreetMap data are ODbL 1.0; derived databases may carry share-alike/availability obligations on public use. ESA WorldCover 2021 and Comune di Bologna quartieri data are CC BY 4.0. Copernicus Land Monitoring Service products are open with source and modification notices. Copernicus GLO-30 has a separate official attribution requirement. Do not construe MIT licensing for original Python code as licensing of the source or derived geospatial databases.
