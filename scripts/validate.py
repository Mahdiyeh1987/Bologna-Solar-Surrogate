"""Re-train/evaluate 15-feature LightGBM, ridge and mean baselines on exact published splits.

Requires the separate LOCAL input bundle in data/local_inputs. This script does NOT
reproduce the original preprocessed DEM, SAGA irradiation model, or GIS features.
"""
import argparse, json
import numpy as np,pandas as pd,geopandas as gpd
from sklearn.model_selection import KFold,GroupKFold
from sklearn.metrics import r2_score,mean_squared_error,mean_absolute_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.dummy import DummyRegressor
from lightgbm import LGBMRegressor
from common import BASE,FEATURES,PARAMS

def load():
 inputs=BASE/'data/local_inputs'
 train=pd.read_csv(inputs/'train_dataset.csv')
 target_file=BASE/'results/recomputed/sample_reference_recomputed.csv'
 if not target_file.exists():
  raise FileNotFoundError('Run python scripts/extract_reference.py with local inputs first to create corrected sample reference.')
 target=pd.read_csv(target_file,usecols=['roof_id','area_weighted_saga'])
 train=train.merge(target,on='roof_id',validate='one_to_one')
 assert len(train)==1525 and train.roof_id.is_unique
 assert np.isfinite(train[FEATURES].to_numpy(dtype=float)).all()
 assert train.area_weighted_saga.notna().all()
 return train

def fold_definitions(train,orig):
 coords=orig.set_index('roof_id').loc[train.roof_id].geometry.centroid
 xx=coords.x.to_numpy(); yy=coords.y.to_numpy()
 block=(np.floor((xx-xx.min())/1500).astype(int).astype(str)+'_'+
        np.floor((yy-yy.min())/1500).astype(int).astype(str))
 grouped=(train.z_admin.astype(str)+'|'+train.z_morph_k4.astype(str)).to_numpy()
 y=train.area_weighted_saga.to_numpy()
 X=train[FEATURES].to_numpy()
 splits={
  'Shuffled 10-fold':list(KFold(n_splits=10,shuffle=True,random_state=42).split(X,y)),
  'District-morphology grouped 5-fold':list(GroupKFold(n_splits=5).split(X,y,groups=grouped)),
  'Spatial block 1500m 5-fold':list(GroupKFold(n_splits=5).split(X,y,groups=block)),
  'LOZO six districts':[(np.flatnonzero(train.z_admin.to_numpy()!=v),np.flatnonzero(train.z_admin.to_numpy()==v)) for v in np.unique(train.z_admin)],
  'LOCO four clusters':[(np.flatnonzero(train.z_morph_k4.to_numpy()!=v),np.flatnonzero(train.z_morph_k4.to_numpy()==v)) for v in np.unique(train.z_morph_k4)]}
 return splits

def main():
 p=argparse.ArgumentParser(); p.add_argument('--out',default=str(BASE/'results/recomputed'));a=p.parse_args()
 out=__import__('pathlib').Path(a.out);out.mkdir(parents=True,exist_ok=True)
 train=load();X=train[FEATURES].to_numpy(dtype=float);y=train.area_weighted_saga.to_numpy()
 orig=gpd.read_file(BASE/'data/local_inputs/roof_blocks_s1.gpkg')[['roof_id','geometry']].drop_duplicates('roof_id')
 assert orig.crs.to_epsg()==25832
 folds=fold_definitions(train,orig)
 factories={'LightGBM':lambda:LGBMRegressor(**PARAMS),
            'Ridge':lambda:make_pipeline(StandardScaler(),Ridge(alpha=10.0)),
            'Mean baseline':lambda:DummyRegressor(strategy='mean')}
 rows=[];oofs=[]
 for protocol,splits in folds.items():
  for model_name,factory in factories.items():
   oof=np.full(len(y),np.nan)
   for k,(tr,te) in enumerate(splits):
    model=factory().fit(X[tr],y[tr]);pred=model.predict(X[te]);oof[te]=pred
    rows.append(dict(protocol=protocol,model=model_name,fold=k,test_n=len(te),
      r2=float(r2_score(y[te],pred)),rmse=float(mean_squared_error(y[te],pred)**.5),
      mae=float(mean_absolute_error(y[te],pred))))
   assert np.isfinite(oof).all()
   oofs.append(pd.DataFrame(dict(roof_id=train.roof_id,y_original_footprint_saga=y,
               prediction_oof=oof,protocol=protocol,model=model_name)))
 pd.DataFrame(rows).to_csv(out/'fold_metrics_recomputed.csv',index=False)
 pd.concat(oofs,ignore_index=True).to_csv(out/'out_of_fold_predictions_recomputed.csv',index=False)
 final=LGBMRegressor(**PARAMS).fit(X,y)
 final.booster_.save_model(str(out/'footprint_lightgbm_15features_recomputed.txt'))
 saved=pd.read_csv(BASE/'results/fold_metrics.csv')
 reconstructed=pd.DataFrame(rows)
 assert (saved[['protocol','model','fold','test_n']].astype(str).values == 
  reconstructed[['protocol','model','fold','test_n']].astype(str).values).all()
 print('Mean fold R2 reproduced by protocol:')
 print(reconstructed[reconstructed.model=='LightGBM'].groupby('protocol').r2.mean().round(4))
 print('Fold outputs written to:',out)
if __name__=='__main__':main()
