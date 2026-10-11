"""Create the actual data-driven district comparison and threshold retention plots."""
import pandas as pd,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import BASE

def main():
 f=BASE/'results/city_predictions_unique_ids.csv'
 if not f.exists():
  raise FileNotFoundError('This figure requires authorized building-level predictions, retained outside the public repo.')
 d=pd.read_csv(f); y='y_hat_retrained_footprint_saga'
 agg=d.groupby('z_admin')[y].agg(['mean','count']).sort_values('mean')
 agg['p10']=d.groupby('z_admin')[y].quantile(.1)
 agg['p90']=d.groupby('z_admin')[y].quantile(.9)
 n=len(agg); fig,ax=plt.subplots(figsize=(9,5))
 ypos=np.arange(n);m=agg['mean'].to_numpy()
 colors=plt.cm.viridis(np.linspace(.15,.85,n))
 ax.hlines(ypos,agg.p10,agg.p90,color='0.7',linewidth=2)
 ax.scatter(m,ypos,s=90,c=colors,zorder=3)
 ax.axvline(d[y].mean(),color='0.3',linestyle='--',label='City mean')
 ax.set_yticks(ypos,agg.index);ax.set_xlabel('Predicted SAGA irradiation proxy (kWh m$^{-2}$ yr$^{-1}$)')
 ax.legend(frameon=False);fig.tight_layout()
 fig.savefig(BASE/'figures/district_mean_p10_p90.pdf');plt.close(fig)
 q3=d[y].quantile(.75); q4=d[d[y]>q3]
 xs=np.arange(0,5.001,.5); vals=[100*(q4[y]>=q3*(1+x/100)).mean() for x in xs]
 fig,ax=plt.subplots(figsize=(7.5,4.5));ax.plot(xs,vals,'o-',color='#21618c')
 ax.fill_between(xs,vals,alpha=.13,color='#21618c')
 ax.set(xlabel='Increase above Q3 threshold (%)',ylabel='Original Q4 retained (%)',ylim=(0,105),xlim=(0,5))
 ax.grid(alpha=.15);fig.tight_layout()
 fig.savefig(BASE/'figures/threshold_sensitivity.pdf');plt.close(fig)
 print('Threshold Q3=',q3, 'retained +1%, +2%=',vals[2],vals[4])
if __name__=='__main__':main()
