from pathlib import Path
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent/'source_data';SEEDS=[42,123,456]
def empirical_cdf(values):
    x=np.asarray(values,dtype=float);assert x.ndim==1 and np.isfinite(x).all()
    return np.sort(x),np.arange(1,len(x)+1)/len(x)
def load_main_data():
    d={name:pd.read_csv(HERE/(name+'.csv')) for name in ['gradient','rank','correlations','counts','intervention','nodes']}
    d['clouds']={};d['input_hashes']={}
    for seed in SEEDS:
        for view in ['spatial','historical']:
            xs=[];ys=[]
            for batch in range(5):
                with np.load(HERE/('cloud_s%d_b%d_%s.npz'%(seed,batch,view))) as z:x,y=z['distance'].ravel(),z['error'].ravel()
                assert x.shape==y.shape==(6496,)
                reference=d['correlations'].query('seed==@seed and view==@view and batch==@batch').pearson.item()
                np.testing.assert_allclose(np.corrcoef(x,y)[0,1],reference,atol=1e-6,rtol=0)
                xs.append(x);ys.append(y)
            d['clouds'][seed,view]=np.concatenate(xs),np.concatenate(ys)
    np.testing.assert_allclose(d['nodes'].delta_mae,d['nodes'].mae_on-d['nodes'].mae_off,atol=1e-14,rtol=0)
    np.testing.assert_allclose(d['gradient'].area_within_pt2,24*d['gradient'].weighted_aux_norm/d['gradient'].groupby('loss').weighted_aux_norm.transform('median'))
    return d
