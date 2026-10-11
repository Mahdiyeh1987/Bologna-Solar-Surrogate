"""Predict final city inventory from optional local feature table.

Outputs remain local; this public repo does not disclose building-linked rows.
"""
import numpy as np,pandas as pd,lightgbm as lgb
from common import BASE,FEATURES,MODEL

def main():
    inp=BASE/'data/local_inputs/inference_features.csv'
    if not inp.exists():
        raise FileNotFoundError('Unpack authorized private input archive into data/local_inputs/ before running inventory.py')
    infer=pd.read_csv(inp)
    assert len(infer)==48688
    model=lgb.Booster(model_file=str(MODEL))
    assert model.num_feature()==15
    pred=model.predict(infer[FEATURES].to_numpy(dtype=float),num_threads=1)
    scores=pd.DataFrame({'roof_id':infer.roof_id,'prediction':pred})
    scores=scores.drop_duplicates('roof_id',keep='first')
    assert len(scores)==48687
    q3=scores.prediction.quantile(.75)
    print('Unique IDs:',len(scores),'Q3:',q3,'Q4 size:',int((scores.prediction>q3).sum()))
    out=BASE/'results/recomputed';out.mkdir(parents=True,exist_ok=True)
    scores.to_csv(out/'inventory_recomputed.csv',index=False)
    print('Local, unpublished building-linked scores saved to',out)
if __name__=='__main__':main()
