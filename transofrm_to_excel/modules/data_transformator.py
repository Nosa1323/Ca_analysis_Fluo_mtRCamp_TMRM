import pandas as pd
import glob
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os
from scipy.signal import savgol_filter
from scipy.signal import find_peaks

def max_find_filt(data, filt_param, peaks_parametrs, window):
    if 'norm_time' in data.columns:
        data.drop(columns = ['norm_time'], inplace=True)
    if data.iloc[:,0].mean().item() < (-50):
        data = data*(-1)
    filt_df = data.apply(savgol_filter, args = (filt_param[0],filt_param[1]))
    peaks_raw= filt_df.iloc[window[0]:window[1], :].apply(find_peaks, 
                                        prominence=peaks_parametrs[0],
                                        width=peaks_parametrs[1], 
                                        height=peaks_parametrs[2])
    max_values = pd.melt(peaks_raw.iloc[1:,], value_name= 'max_val')
    max_values ['max_peaks'] = max_values.iloc[:,1].map(lambda x: max(x.get('peak_heights')) )
    max_values.drop('max_val', axis =1, inplace = True)

    not_mull_mask = filt_df.isin(max_values ['max_peaks'].values)
    filt_dendro_not_null = filt_df[not_mull_mask]
    filt_dendro_not_null.dropna(how='all', inplace=True)

    max_values ['id_max_peaks'] = filt_dendro_not_null.idxmax().values
    
    return max_values,filt_df

def data_to_long(data, type):
    out = pd.melt(data, id_vars='norm_time', value_name='Signal')
    out['type'] = type
    return out