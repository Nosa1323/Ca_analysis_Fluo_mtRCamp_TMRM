
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from modules.data_transformator import max_find_filt

def signal_shifting(shifting_df, maximum): 

    filename = shifting_df.columns
    if 'norm_time' in filename:
        shifting_df.drop(columns = ['norm_time'], inplace=True)
    shifted_signal = pd.DataFrame()
    col = shifting_df.columns
    for count, i in enumerate(filename):   
        if count<=len(col)-1 and i==col[count]:
            start_signal = maximum.iloc[count,4]
            if start_signal>=0:
                container1 = pd.Series(shifting_df.iloc [start_signal:,count].values)
                container1.name = i
                shifted_signal = pd.concat([shifted_signal, container1], axis = 1)
            else:
                delta = pd.Series([0 for _ in range(abs(start_signal))])
                container2 = pd.Series(shifting_df.iloc[:,count].values)
                container2 = pd.concat([delta, container2])
                container2.name = i
                container2.reset_index(drop=True, inplace=True)
                shifted_signal = pd.concat([shifted_signal, container2],  axis = 1)
    return shifted_signal


def mit_follow_Ca (dendro_df, mit_df, filt_param, peaks_parametrs_dendro, window):
    maximum,filt_dendro =  max_find_filt(dendro_df, filt_param, peaks_parametrs_dendro, window)

    one_col_signal = pd.melt(filt_dendro, value_vars= filt_dendro.columns, ignore_index = False)
    one_col_signal.drop(columns = ['filename'], inplace=True)

    max_id_from_all_traces, _ = max_find_filt(one_col_signal, filt_param, peaks_parametrs_dendro, window)
    maximum ['id_all_traces'] = int(max_id_from_all_traces['id_max_peaks'])
    maximum ['delta_shift'] = maximum.iloc[:, 2] - maximum.iloc[:, 3]
    
    shifted_dendro, shifted_mit   = signal_shifting(dendro_df, maximum),signal_shifting(mit_df,maximum)
    return   shifted_dendro, shifted_mit

def ca_follow_mit (dendro_df, mit_df, filt_param, peaks_parametrs, window):
    maximum,filt_mit = max_find_filt(mit_df, filt_param,peaks_parametrs, window)

    one_col_signal = pd.melt(filt_mit, value_vars=filt_mit.columns, ignore_index = False)
    one_col_signal.drop(columns = ['filename'], inplace=True)

    max_id_from_all_traces, _ = max_find_filt(one_col_signal, filt_param, peaks_parametrs, window)
    maximum ['id_all_traces'] = int(max_id_from_all_traces['id_max_peaks'])
    maximum ['delta_shift'] = maximum.iloc[:, 2] - maximum.iloc[:, 3]
    
    shifted_dendro, shifted_mit  = signal_shifting(dendro_df, maximum),signal_shifting(mit_df,maximum)
    return   shifted_dendro, shifted_mit

def independent (dendro_df, mit_df, filt_param_dendro,filt_param_mit, peaks_parametrs_dendro, peaks_parametrs_mit, window):
    maximum_dendro,filt_dendro =  max_find_filt(dendro_df, filt_param_dendro, peaks_parametrs_dendro, window)

    one_col_signal = pd.melt(filt_dendro, value_vars= filt_dendro.columns, ignore_index = False)
    one_col_signal.drop(columns = ['filename'], inplace=True)

    max_id_from_all_traces, _ = max_find_filt(one_col_signal, filt_param_dendro, peaks_parametrs_dendro, window)
    maximum_dendro ['id_all_traces'] = int(max_id_from_all_traces['id_max_peaks'])
    maximum_dendro ['delta_shift'] = maximum_dendro.iloc[:, 2] - maximum_dendro.iloc[:, 3]
    
    
    
    maximum_mit,filt_mit = max_find_filt(mit_df, filt_param_mit,peaks_parametrs_mit, window)

    one_col_signal = pd.melt(filt_mit, value_vars=filt_mit.columns, ignore_index = False)
    one_col_signal.drop(columns = ['filename'], inplace=True)

    max_id_from_all_traces, _ = max_find_filt(one_col_signal, filt_param_mit, peaks_parametrs_mit, window)
    maximum_mit ['id_all_traces'] = int(max_id_from_all_traces['id_max_peaks'])
    maximum_mit ['delta_shift'] = maximum_mit.iloc[:, 2] - maximum_mit.iloc[:, 3]
    


    shifted_dendro, shifted_mit  = signal_shifting(dendro_df, maximum_dendro),signal_shifting(mit_df,maximum_mit)
    return   shifted_dendro, shifted_mit, maximum_dendro, maximum_mit