"""Exact fractional raster-cell-overlap means for original footprint polygons.

To generate the full 48,688-row reference, use the unique source OSM polygons matched
to archived inference IDs; this may take several minutes on a local machine.
"""
import argparse
from pathlib import Path
import numpy as np,pandas as pd,geopandas as gpd,rasterio
from rasterio.features import geometry_mask
from rasterio.windows import from_bounds, Window
from shapely.geometry import box
from common import BASE

def footprint_mean(geom, src, data):
 if geom is None or geom.is_empty: return float('nan')
 win=from_bounds(*geom.bounds,transform=src.transform)
 col0=max(0,int(np.floor(win.col_off))-1)
 row0=max(0,int(np.floor(win.row_off))-1)
 col1=min(src.width,int(np.ceil(win.col_off+win.width))+1)
 row1=min(src.height,int(np.ceil(win.row_off+win.height))+1)
 if col0>=col1 or row0>=row1:return float('nan')
 block=data[row0:row1,col0:col1]
 transform=src.window_transform(Window(col0,row0,col1-col0,row1-row0))
 mask=geometry_mask([geom],out_shape=block.shape,transform=transform,invert=True,all_touched=True)
 valid=mask & np.isfinite(block)
 if src.nodata is not None: valid &= block!=src.nodata
 masses=[];vals=[]
 for rr,cc in np.argwhere(valid):
  x0,y0=transform*(int(cc),int(rr));x1,y1=transform*(int(cc)+1,int(rr)+1)
  cell=box(min(x0,x1),min(y0,y1),max(x0,x1),max(y0,y1))
  area=geom.intersection(cell).area
  if area>1.e-12:masses.append(area);vals.append(block[rr,cc])
 return float(np.average(vals,weights=masses)) if masses else float('nan')

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--all',action='store_true',help='Process all 48,688 inference rows (slow)')
 args=parser.parse_args()
 inp=BASE/'data/local_inputs'
 orig=gpd.read_file(inp/'roof_blocks_s1.gpkg')
 orig=orig[['roof_id','geometry']].drop_duplicates('roof_id').set_index('roof_id')
 ids=(pd.read_csv(inp/'inference_features.csv',usecols=['roof_id']).roof_id if args.all
      else pd.read_csv(inp/'train_dataset.csv',usecols=['roof_id']).roof_id)
 assert len(ids)==48688 if args.all else len(ids)==1525
 geoms=orig.loc[ids].geometry
 raster=inp/'G_year_kWh_clip.tif';out=BASE/'results/recomputed';out.mkdir(exist_ok=True)
 with rasterio.open(raster) as ds:
  assert ds.crs.to_epsg()==25832
  band=ds.read(1)
  result=[footprint_mean(x,ds,band) for x in geoms]
 name='full_city_reference_recomputed.csv' if args.all else 'sample_reference_recomputed.csv'
 pd.DataFrame({'roof_id':ids.to_numpy(),'area_weighted_saga':result}).to_csv(out/name,index=False)
 print('Wrote',out/name,'n',len(ids))
if __name__=='__main__': main()
