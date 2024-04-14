#%%
import os
import numpy as np
import pandas as pd
from glob import glob
import os.path as op
from pathlib import Path
import pandas as pd
from scipy.stats import zscore
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import seaborn as sns

#%%

# you will always have 7 spreadsheets less because we erased 7 files on accident
# at the beginning of the study

raw_file_list = []

for raw_file in os.listdir("/home/data/madlab/mvrn_ESI_study/raw_pilot_subs"):
    if ".csv" in raw_file:
        # getting the subject IDs for each raw file
        raw_file = raw_file.split("_Test1")[0]
        raw_file_list.append(raw_file)

# raw_file_list
#%%
clean_file_list = []
for clean_file in os.listdir("/home/data/madlab/mvrn_ESI_study/clean_pilot_subs"):
    if ".csv" in clean_file:
        # getting the subject IDs for each raw file
        clean_file = clean_file.split("_esi")[0]
        clean_file_list.append(clean_file)


#%%
'''
Final list of uncleaned files: compares the full list of files 
in the raw_file_list to the clean_file_list and returns the files
NOT found in the clean_data_list.
'''

uncleaned_list = list(sorted(set(raw_file_list).difference(clean_file_list)))
uncleaned_list

#%%
total_subjs_list = sorted(uncleaned_list + clean_file_list)
total_subjs_list
len(total_subjs_list)
# %%
