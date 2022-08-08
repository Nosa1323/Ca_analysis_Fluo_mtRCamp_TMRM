from cProfile import label
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os
import re
from scipy.signal import savgol_filter
from scipy.signal import find_peaks
from modules.data_transformator import data_to_long

def lineplot_graph(data, x, y):
    sns.set_theme(font_scale=0.7, style="ticks",context="poster")
    return sns.relplot(data=data, x=x, y=y, col_wrap=4, col="filename", height=5, kind="line")


def one_trace_plot(df, type, save_directory):
    filename = df.filename.unique() 
    plt.figure(figsize=(5,1.5))
    for i in filename:
        mask = (df['filename'] == i)
        line_df = df.loc[mask]
        plot = lineplot_graph(line_df ,"norm_time", type)
        plot.refline (y= line_df[type].mean(), color = 'red')
        plot.refline (y= line_df[type].std()*2 + line_df[type].mean(), color = 'purple')
        plot.refline (y= line_df[type].mean() - line_df[type].std()*2, color = 'purple')

        plt.tight_layout() 

        path = save_directory.setdefault(i.split('.')[0])
        fig_name = f'{path}/{type}.tif'
        plot.savefig(fig_name)
        plt.rc('figure', max_open_warning = 0)
    return


def line_graph(graph_df, figname, type_list):
    filename = graph_df.columns
    if 'norm_time' not  in filename:
        graph_df ['norm_time'] = np.arange(0.01, len(graph_df)*0.01, 0.01)
    graph_df = pd.melt(graph_df, id_vars='norm_time', value_vars = filename, 
                    var_name=['filename'], value_name='Signal')
                
    plt.figure(figsize=(10,4))
    custom_params = {"axes.spines.right": False, "axes.spines.top": False}
    sns.set_theme(font_scale=1,context = 'notebook', style="ticks", rc= custom_params)

    sns.lineplot(data=graph_df, x = 'norm_time', y ='Signal', hue = 'filename')
    plt.legend(loc=1, bbox_to_anchor=(1.4, 1.05), ncol = 5)
    
    for i in type_list:
        if i==filename[0].split(' ')[0]:
            figname = f'fig/{i}/{figname}'
    plt.tight_layout()
    plt.savefig(f'{figname}.png') 


def peak_detect_graph(x, peaks, properties, window): 
    plt.figure(figsize=(10,5))
    sns.set_theme(font_scale=2, style="ticks",context="notebook")
    plt.plot(x)
    plt.title(f'{pd.Series(x).name}')
    plt.plot(peaks, x[peaks], "x")
    plt.vlines(window[0], x.min(), x.max(),  color = sns.xkcd_rgb['dusty red'], linestyle='--')
    plt.vlines(window[1], x.min(), x.max(), color = sns.xkcd_rgb['dusty red'], linestyle='--')
    plt.vlines(x=peaks, ymin=x[peaks] - properties["prominences"],
            ymax = x[peaks], color = "C1")
    plt.hlines(y=properties["width_heights"], xmin=properties["left_ips"],
            xmax=properties["right_ips"], color = "C1")
    plt.grid(b=True, ls=':', color='#606060')
    plt.tight_layout()


def peaks_raw_vs_filt_graph(data, filt_param, peaks_parametrs, window, type):
    if type == 'mit' and data.iloc[:,0].mean().item() < (-50):
        data = data*(-1)
    for i in data:
        folder_type = re.split(r'[. ]\s*', i)[0]
        save_path = f'fig/{folder_type}/{folder_type}_peak_fig'
        sample_name = i.split('.')[0]
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        plt.figure(figsize=(10,5))
        peaks, properties = find_peaks(data[i],prominence=peaks_parametrs[0],
                                                width=peaks_parametrs[1],
                                                height=peaks_parametrs[2])
        peak_detect_graph(data[i], peaks, properties, window)
        figname = f'{save_path}/{sample_name}_{type}_raw.png'
        plt.tight_layout()
        plt.savefig(figname)


        sg_filt = savgol_filter(data[i],filt_param[0], filt_param[1])
        peaks, properties = find_peaks(sg_filt,prominence=peaks_parametrs[0],
                                                width=peaks_parametrs[1],
                                                height=peaks_parametrs[2])
        sg_filt = pd.Series(sg_filt)
        sg_filt.rename(f'{data[i].name} - sg_filt', inplace=True)
        peak_detect_graph (sg_filt, peaks, properties, window)


        figname = f'{save_path}/{sample_name}_{type}_sg_filt.png'
        plt.tight_layout()
        plt.savefig(figname)
        plt.rc('figure', max_open_warning = 0)
    print('Figures', type, 'saved successful')

def line_graph_mean(dendro_input, mit_input, type, figname, type_list):

    dendro_df = data_to_long(dendro_input, type[0])
    mit_df = data_to_long(mit_input,type[1])

    graph_df = pd.concat([dendro_df,mit_df])
    graph_df.reset_index(inplace=True)

    plt.figure(figsize=(8,5))
    custom_params = {"axes.spines.right": False, "axes.spines.top": False}
    sns.set_theme(font_scale=1,context = 'notebook', style="ticks", rc= custom_params)
    sns.lineplot(data=graph_df, x = 'norm_time', y ='Signal', hue = 'type', ci=None, estimator='mean')
    plt.legend(bbox_to_anchor=(1.1, 1.05))
    plt.tight_layout()
    for i in type_list:
        figname = f'fig/{i}/{figname}'

    plt.savefig(f'{figname}.png')