"""Validate public **aggregate** fold table and 15-feature model.

Full building-level consistency checks require optional local research inputs.
"""
import sys
from pathlib import Path
import pandas as pd
import lightgbm as lgb
from common import BASE, FEATURES, MODEL

def main():
    folds = pd.read_csv(BASE / 'results/fold_metrics.csv')
    assert len(folds) == 90, f'Expected 90 fold-level rows, got {len(folds)}'
    assert sorted(folds['model'].unique()) == ['LightGBM','Mean baseline','Ridge']
    assert len(folds['protocol'].unique()) == 5
    assert folds[['r2','rmse','mae','test_n']].notna().all().all()
    m = lgb.Booster(model_file=str(MODEL))
    assert m.num_feature() == len(FEATURES) == 15
    assert m.num_trees() == 800
    print('Verified public aggregate metrics: 90 rows, 5 protocols, 3 models')
    print('Verified saved model: 15 predictors and 800 trees')
    print(folds[folds.model == 'LightGBM'].groupby('protocol').r2.mean().round(4).to_string())
    print('Note: per-building source records deliberately not in public release.')
if __name__=='__main__': main()
