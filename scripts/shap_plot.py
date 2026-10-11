"""Reproduce 15-feature SHAP summary with human-readable names, using saved FINAL model."""
from pathlib import Path
import numpy as np,pandas as pd,lightgbm as lgb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import shap
from common import BASE,MODEL,FEATURES
LABELS={
'area_m2':'Footprint area',
'slpmean':'Mean DEM slope',
'asinmean':'Aspect sine',
'acosmean':'Aspect cosine',
'svf_mean':'Sky view factor',
'shadow_mean':'Hillshade index',
'relief_mean':'Local relief',
'rbwc50_pct':'Built-up share (50 m)',
'rbtcd10_pct':'Tree-cover share >=10%',
'ua_rbua50_2018_11210_pct':'Dense urban fabric (UA 11210)',
'ua_rbua50_2018_11220_pct':'Medium urban fabric (UA 11220)',
'ua_rbua50_2018_11230_pct':'Low-density urban fabric (UA 11230)',
'ua_rbua50_2018_12100_pct':'Industrial/commercial/public (UA 12100)',
'ua_rbua50_2018_13400_pct':'Land without current use (UA 13400)',
'ua_rbua50_2018_14100_pct':'Urban green areas (UA 14100)'}

def main():
 data_file=BASE/'data/training_1525_corrected.csv'
 if data_file.exists():
  data=pd.read_csv(data_file)
 else:
  src_file=BASE/'data/local_inputs/train_dataset.csv'
  if not src_file.exists():
   raise FileNotFoundError('SHAP requires authorized research features; supply data/local_inputs/train_dataset.csv (not published)')
  data=pd.read_csv(src_file)
 assert len(data)==1525
 booster=lgb.Booster(model_file=str(MODEL));assert booster.num_feature()==15
 X=data[FEATURES]
 contrib=booster.predict(X.to_numpy(dtype=float),pred_contrib=True,num_threads=1)
 pred=booster.predict(X.to_numpy(dtype=float),num_threads=1)
 assert contrib.shape==(len(X),16)
 assert max(abs(pred-contrib.sum(axis=1)))<1.e-5
 importance=pd.DataFrame(dict(feature=FEATURES,mean_absolute_shap=np.abs(contrib[:,:-1]).mean(axis=0)))
 importance=importance.sort_values('mean_absolute_shap',ascending=False)
 out=BASE/'figures';out.mkdir(exist_ok=True)
 importance.to_csv(out/'shap_importance_recomputed.csv',index=False)
 X_plot=X.rename(columns=LABELS)
 np.random.seed(42)
 plt.figure(figsize=(11.5,8.1),dpi=160)
 shap.summary_plot(contrib[:,:-1],X_plot,show=False,max_display=15,plot_size=None)
 fig=plt.gcf();ax=fig.axes[0]
 ax.set_xlabel('SHAP value (kWh m$^{-2}$ yr$^{-1}$)')
 ax.axvline(0,linewidth=.8,color='gray',zorder=0)
 ax.grid(axis='x',alpha=.12)
 fig.subplots_adjust(left=.40,right=.9,bottom=.10,top=.98)
 fig.savefig(out/'shap_recomputed.pdf',bbox_inches='tight')
 fig.savefig(out/'shap_recomputed.png',dpi=300,bbox_inches='tight')
 plt.close(fig)
 print('Wrote figures and SHAP means:',out)
if __name__=='__main__':main()
