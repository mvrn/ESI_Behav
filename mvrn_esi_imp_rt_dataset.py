#%%
import os
import numpy as np
import pandas as pd
from glob import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import seaborn as sns
from scipy.stats import norm

# establishing the directory from which to retrieve esi vs. imp csv files
root_dir = "/home/data/madlab/mvrn_ESI_study/clean_pilot_subs/"

# compiling list of esi vs. imp subjects
final_esi_imp_subs = ["101","102","103","105","106","107","109","110","111","112","113",
                      "114","115","117","118","119","120","121","122","123","124","127",
                      "128","129","130","131","132","133","134","135","136","137","138",
                      "139","140","141","142","145","146","147","148","149","151","152",
                      "153","154","158","159","160","162","163","164","165","168","169",
                      "170","173","175","180","181","184","185","186","187","194","197",
                      "200","201","204","210","211","212","213","216","222", "246"]

study_cols = [
    'Subject', 
    'Randomization',
    'study_stim1', 
    'study_stim2',
    'study_resp_rt1',
    'study_resp_rt2'
    ]

test_cols = [
    'Subject', 
    'Randomization',
    'test_run', 
    'test_stim', 
    'test_stimtype', 
    'test_stimsim', 
    'test_resp',
    'test_resp_rt'
    ]

# creating lists for study and test dfs for subsequent csv creation
study = []
test = []

# iterating over every subject
for sub in final_esi_imp_subs:
    for file in glob(
        os.path.join(
            root_dir,
            f"{sub}*.csv"
            )):
        study_df = pd.read_csv(
            file, 
            usecols=study_cols,
            nrows=86
            )
        
        test_df = pd.read_csv(
            file, 
            usecols=test_cols,
            nrows=238
            )
        
    study_df['Randomization'] = study_df['Randomization'].replace([1, 2], ['ESIthenIMP','IMPthenESI'])
    # getting rid of parts of the column string for better coding
    study_df['study_stim1'] = study_df['study_stim1'].map(lambda x: x.lstrip('esi_full_stims/').rstrip('jpg'))
    study_df['study_stim2'] = study_df['study_stim2'].map(lambda x: x.lstrip('esi_full_stims/').rstrip('jpg'))
                                        

    test_df['Randomization'] = test_df['Randomization'].replace([1, 2], ['ESIthenIMP','IMPthenESI'])
    test_df['test_stim'] = test_df['test_stim'].map(lambda x: x.lstrip('esi_full_stims/').rstrip('jpg'))
    
    test_df['test_stimtype'] = test_df['test_stimtype'].replace([1, 2], ['negative','neutral'])
    test_df['test_stimsim'] = test_df['test_stimsim'].replace([1, 2, 4], ['target','lure', 'foil'])
    test_df['test_resp'] = test_df['test_resp'].replace([1, 2], ['old','new'])
    test_df['test_resp'] = test_df['test_resp'].replace('None', np.nan)


    # Getting df outside of the for loop to then convert to csv
    for index, row in study_df.iterrows():
        study.append(row)

    for index, row in test_df.iterrows():
        test.append(row)

study_df = pd.DataFrame(study).to_csv('study_esi_imp.csv', index=False)
test_df = pd.DataFrame(test).to_csv('test_esi_imp.csv', index=False)

# %%
