"""Fixed final 2026 LightGBM configuration and feature order."""
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
FEATURES=[
 'area_m2','slpmean','asinmean','acosmean','svf_mean','shadow_mean',
 'relief_mean','rbwc50_pct','rbtcd10_pct',
 'ua_rbua50_2018_11210_pct','ua_rbua50_2018_11220_pct',
 'ua_rbua50_2018_11230_pct','ua_rbua50_2018_12100_pct',
 'ua_rbua50_2018_13400_pct','ua_rbua50_2018_14100_pct']
PARAMS=dict(n_estimators=800,learning_rate=.03,num_leaves=63,subsample=.9,
 colsample_bytree=.9,reg_lambda=.6,min_child_samples=20,min_data_in_bin=10,
 feature_pre_filter=False,random_state=42,n_jobs=1,verbosity=-1)
MODEL=BASE/'model/footprint_lightgbm_15features.txt'
