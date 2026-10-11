import sys
from pathlib import Path
import pandas as pd,lightgbm as lgb
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from common import BASE,FEATURES,MODEL

def test_public_aggregate_release():
    fold=pd.read_csv(BASE/'results/fold_metrics.csv')
    model=lgb.Booster(model_file=str(MODEL))
    assert len(fold)==90
    assert fold['protocol'].nunique()==5 and fold['model'].nunique()==3
    assert len(FEATURES)==15 and model.num_feature()==15 and model.num_trees()==800
