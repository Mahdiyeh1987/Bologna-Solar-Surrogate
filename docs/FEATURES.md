# Fifteen predictors: raw field name → scientific meaning

- `area_m2`: horizontal area of original footprint (m²)
- `slpmean`: mean slope derived from processed DEM, **not roof pitch**
- `asinmean`: mean sine of DEM aspect, circular orientation encoding
- `acosmean`: mean cosine of DEM aspect, circular orientation encoding
- `svf_mean`: average DEM-derived sky view factor
- `shadow_mean`: four-direction hillshade index (four azimuths, 45° solar altitude)
- `relief_mean`: elevation-range terrain descriptor within 21-cell focal window
- `rbwc50_pct`: percentage of ESA WorldCover class 50 built-up cells in 50 m context buffer
- `rbtcd10_pct`: percentage of cells with Tree Cover Density >=10% in 50 m buffer
- `ua_rbua50_2018_11210_pct`: Urban Atlas 2018 dense discontinuous urban fabric (50–80% soil sealing) (%)
- `ua_rbua50_2018_11220_pct`: Urban Atlas 2018 medium discontinuous urban fabric (30–50% soil sealing) (%)
- `ua_rbua50_2018_11230_pct`: Urban Atlas 2018 low-density urban fabric (10–30% soil sealing) (%)
- `ua_rbua50_2018_12100_pct`: Urban Atlas 2018 industrial/commercial/public/military/private units (%)
- `ua_rbua50_2018_13400_pct`: Urban Atlas 2018 land without current use (%)
- `ua_rbua50_2018_14100_pct`: Urban Atlas 2018 green urban areas (%)

The six Urban Atlas variables are land-use shares in the 50 m contextual neighbourhood.
Aspect sine and cosine have orientation-proxy meaning and **do not** encode measured roof azimuth.
Climate baseline values are constant across Bologna and excluded from modelling.
