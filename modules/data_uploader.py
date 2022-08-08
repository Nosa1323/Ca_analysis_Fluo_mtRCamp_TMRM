import numpy as np
import pandas as pd
from scipy.signal import find_peaks

def max_value_from_raw_find (raw_df,peaks_parametrs):
    properties = raw_df.iloc[:, :-1].apply(find_peaks, prominence=peaks_parametrs[0],
                                                        width=peaks_parametrs[1], 
                                                        height=peaks_parametrs[2])
    values_list = pd.melt(properties.iloc[1:,])
    values_list ['max_peaks'] = values_list.iloc[:,1].map(lambda x: max(x.get('peak_heights')) )
    return values_list

def features_out (df, peaks_parametrs):
    for_sd_df = pd.DataFrame()
    dendro = pd.pivot_table(df, index = 'index', columns = 'filename', values = 'dendro')
    dendro['norm_time'] = np.arange(0,len(dendro)*0.02, 0.02)

    mit = pd.pivot_table(df, index = 'index', columns = 'filename', values = 'mit')
    mit['norm_time'] = np.arange(0,len(mit)*0.02, 0.02)

    for_sd_df ['dendro_mean'] = df.groupby('filename').mean()['dendro'] 
    for_sd_df ['dendro_peak'] = max_value_from_raw_find(dendro, peaks_parametrs[0]).iloc[:,-1].values

    mask = (df['index']>15)&(df['index']<30)
    for_sd_df ['dendro_baseline'] =  df[mask].groupby('filename').mean()['dendro'] 
    
    
    for_sd_df ['mit_mean'] = df.groupby('filename').mean()['mit']
    if for_sd_df ['mit_mean'].mean().item() < (-50):
        data = data*(-1)
        for_sd_df ['mit_peak'] = ((max_value_from_raw_find(mit, peaks_parametrs[1])).iloc[:,-1].values)*(-1)
    for_sd_df ['mit_peak'] = (max_value_from_raw_find(mit, peaks_parametrs[1])).iloc[:,-1].values

    for_sd_df ['mit_baseline'] =  df[mask].groupby('filename').mean()['mit'] 
    
    return for_sd_df