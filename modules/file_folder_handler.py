import pandas as pd
import glob
import numpy as np
import os


def file_extraction(search_string): 
    filepaths = glob.glob(search_string)
    df = pd.DataFrame()
    save_directory = {}
    type_list = set()
    for find_files in filepaths:
        
        f = pd.read_csv(find_files, sep =';', decimal= ',')

        output_folder_list = find_files.split('\\')
        filename = str(output_folder_list[2].split('.')[0])
        signal_type = str(output_folder_list[1].split('.')[0].split(' ')[0])
        type_list.add(signal_type)

        if signal_type=='Small' or signal_type=='ATP_mtRCaMP_Ctrl':
            array = np.arange(0.01,len(f)*0.01, 0.01)
        else:
            array = np.arange(0,len(f)*0.01, 0.01)

        f ['filename'] = filename
        f ['norm_time'] = pd.Series(array)
        f ['signal_type'] = signal_type

        df = pd.concat ([df, f])
        
        save_directory[filename] = f'fig/{signal_type}/{filename}'
    return(df, type_list,save_directory)

def file_folder_creator(save_directory):
    for save_path in save_directory.values():
        if not os.path.exists(save_path):
            os.makedirs(save_path)
    return 'Folder created'








    