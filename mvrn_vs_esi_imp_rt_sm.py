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
final_esi_imp_subs = [
    "101","102","103","105","106","107","109","110","111","112","113",
    "114","115","117","118","119","120","121","122","123","124","127",
    "128","129","130","131","132","133","134","135","136","137","138",
    "139","140","141","142","145","146","147","148","149","151","152",
    "153","154","158","159","160","162","163","164","165","168","169",
    "170","173","175","180","181","184","185","186","187","194","197",
    "200","201","204","210","211","212","213","216","222","246"
    ]


behav_data = {

    'Subject':[],

    'PostESI_NegLureFA_Count': [],
    'PostESI_NeuLureFA_Count': [],

    'PostESI_NegLureCR_Count': [],
    'PostESI_NeuLureCR_Count': [],
    
    'PostESI_NegTargHit_Count': [],
    'PostESI_NeuTargHit_Count': [],
    
    'PostESI_NegTargMiss_Count': [],
    'PostESI_NeuTargMiss_Count': [],


    'PostIMP_NegLureFA_Count': [],
    'PostIMP_NeuLureFA_Count': [],

    'PostIMP_NegLureCR_Count': [],
    'PostIMP_NeuLureCR_Count': [],

    'PostIMP_NegTargHit_Count': [],
    'PostIMP_NeuTargHit_Count': [],

    'PostIMP_NegTargMiss_Count': [],
    'PostIMP_NeuTargMiss_Count': [],


    'NegFoilFA_Count': [],
    'NegFoilCR_Count': [],

    'NeuFoilFA_Count': [],
    'NeuFoilCR_Count': []

    }

study_cols = [
    'Subject', 
    'Randomization',
    'study_stim1', 
    'study_stim2'
    ]

test_cols = [
    'Subject', 
    'Randomization',
    'test_run', 
    'test_stim', 
    'test_stimtype', 
    'test_stimsim', 
    'test_resp'
    ]


study_run1 = "study_stim1"
study_run2 = "study_stim2"

lurefas = "test_stimsim == 'lure' and test_resp == 'old'"
lurecrs = "test_stimsim == 'lure' and test_resp == 'new'"

targhits = "test_stimsim == 'target' and test_resp == 'old'"
targmiss = "test_stimsim == 'target' and test_resp == 'new'"

foilfas = "test_stimsim == 'foil' and test_resp == 'old'"
foilcrs = "test_stimsim == 'foil' and test_resp == 'new'"

trial_types = [
    lurefas, 
    lurecrs,

    targhits, 
    targmiss,
    
    foilfas, 
    foilcrs
    ]

runs = [
    study_run1,
    study_run2
]
#%%
# function to query for FA, CR, TH, TM for each subject
def query_facr_thtm(df, resp_cat):
    query = df[df["Subject"] == int(f"{sub}")].query(resp_cat).reset_index(drop=True)
    query_stim_list = list(query['test_stim'].str.slice(15, 20))
    return(query_stim_list)

# function to query for foils for each subject
# no need to grab the test_stim column cause it's just foils
def query_foils(df, resp_cat):
    query = df[df["Subject"] == int(f"{sub}")].query(resp_cat).reset_index(drop=True)
    return(query)

# function to match specific test trials to study items in run 1 or 2
def matching(df, run, lista):
    length = len(df[df[run].str[15:20].isin(lista)].reset_index(drop=True))
    return(length)

#%%
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

    test_df['Randomization'] = test_df['Randomization'].replace([1, 2], ['ESIthenIMP','IMPthenESI'])
    test_df['test_stimtype'] = test_df['test_stimtype'].replace([1, 2], ['negative','neutral'])
    test_df['test_stimsim'] = test_df['test_stimsim'].replace([1, 2, 4], ['target','lure', 'foil'])
    test_df['test_resp'] = test_df['test_resp'].replace([1, 2], ['old','new'])
    test_df['test_resp'] = test_df['test_resp'].replace('None', np.nan)

    # # adding list of subjects to the dictionary we created above
    behav_data['Subject'].append(sub)

    negative_list = []
    neutral_list = []

    # searching for negative/neutral stimuli in each row of the test DF
    for index, row in test_df.iterrows():
        # print(row)
        
        if "negative" in row["test_stimtype"]:
            # adding the filtered rows to a list
            negative_list.append(row)
        else:
            neutral_list.append(row)
    
    # getting DF with only negative stimuli shown at test
    neg_stim_pd = pd.DataFrame(negative_list).reset_index(drop=True)

    # getting DF with only neutral stimuli shown at test
    neu_stim_pd = pd.DataFrame(neutral_list).reset_index(drop=True)

    # # testing whether each subject has 117 negative stimuli at test
    # total_neg_stim_persub = len(neg_stim_pd[neg_stim_pd["Subject"]==int(f"{sub}")])
    # if total_neg_stim_persub != 117:
    #     print(f"{sub}" + " test stim count: not all is well :/")
    

    for trials in trial_types:
        # negative querying for each trial type
        if trials == lurefas:
            # negative lurefas
            neg_lurefas_list = query_facr_thtm(neg_stim_pd,trials)
            # neutral lurefas
            neu_lurefa_list = query_facr_thtm(neu_stim_pd,trials)
        elif trials == lurecrs:
            # negative lurecrs
            neg_lurecr_list = query_facr_thtm(neg_stim_pd,trials)
            # neutral lurecrs
            neu_lurecr_list = query_facr_thtm(neu_stim_pd,trials)
        elif trials == targhits:
            # negative ths
            neg_ths_list = query_facr_thtm(neg_stim_pd,trials)
            # neutral ths
            neu_ths_list = query_facr_thtm(neu_stim_pd,trials)
        elif trials == targmiss:
            # negative tms
            neg_tms_list = query_facr_thtm(neg_stim_pd,trials)
            # neutral ths
            neu_tms_list = query_facr_thtm(neu_stim_pd,trials)
        elif trials == foilfas:
            # negative foilfas
            neg_foilfa_list = query_foils(neg_stim_pd,trials)
            # neutral foilfas
            neu_foilfa_list = query_foils(neu_stim_pd,trials)
        elif trials == foilcrs:
            # negative foilcrs
            neg_foilcr_list = query_foils(neg_stim_pd,trials)
            # neutral foilcrs
            neu_foilcr_list = query_foils(neu_stim_pd,trials)

            # matching all the FA/CR Foils
            behav_data['NegFoilFA_Count'].append(len(
                neg_foilfa_list
                ))
            
            behav_data['NegFoilCR_Count'].append(len(
                neg_foilcr_list
                ))
            
            # matching all the FA/CR Foils
            behav_data['NeuFoilFA_Count'].append(len(
                neu_foilfa_list
                ))
            
            behav_data['NeuFoilCR_Count'].append(len(
                neu_foilcr_list
                ))

            if study_df['Randomization'][0] == "ESIthenIMP":
                '''
                Negative
                '''
                # matching all the FAs
                behav_data['PostESI_NegLureFA_Count'].append(
                    matching(
                        study_df,
                        study_run1, 
                        neg_lurefas_list
                        ))
                behav_data['PostIMP_NegLureFA_Count'].append(
                    matching(
                        study_df,
                        study_run2, 
                        neg_lurefas_list
                        ))

                # matching all the CRs
                behav_data['PostESI_NegLureCR_Count'].append(
                    matching(
                        study_df,
                        study_run1, 
                        neg_lurecr_list
                        ))
                
                behav_data['PostIMP_NegLureCR_Count'].append(
                    matching(
                        study_df,
                        study_run2, 
                        neg_lurecr_list
                        )) 
                        
                # matching all the THs
                behav_data['PostESI_NegTargHit_Count'].append(
                    matching(
                        study_df,
                        study_run1, 
                        neg_ths_list
                        ))
                
                behav_data['PostIMP_NegTargHit_Count'].append(
                    matching(
                        study_df,
                        study_run2, 
                        neg_ths_list
                        ))
                
                # matching all the TMs
                behav_data['PostESI_NegTargMiss_Count'].append(
                    matching(
                        study_df,
                        study_run1, 
                        neg_tms_list
                        ))
                
                behav_data['PostIMP_NegTargMiss_Count'].append(
                    matching(
                        study_df,
                        study_run2, 
                        neg_tms_list
                        ))
                            
                '''Neutral'''

                        # matching all the FAs
                behav_data['PostESI_NeuLureFA_Count'].append(
                    matching(
                        study_df,
                        study_run1, 
                        neu_lurefa_list
                        ))

                behav_data['PostIMP_NeuLureFA_Count'].append(
                    matching(
                        study_df,
                        study_run2, 
                        neu_lurefa_list
                        ))

                # matching all the CRs
                behav_data['PostESI_NeuLureCR_Count'].append(
                    matching(
                        study_df,
                        study_run1, 
                        neu_lurecr_list
                        ))
                
                behav_data['PostIMP_NeuLureCR_Count'].append(
                    matching(
                        study_df,
                        study_run2, 
                        neu_lurecr_list
                        )) 
                
                # matching all the THs
                behav_data['PostESI_NeuTargHit_Count'].append(
                    matching(
                        study_df,
                        study_run1, 
                        neu_ths_list
                        ))
                
                behav_data['PostIMP_NeuTargHit_Count'].append(
                    matching(
                        study_df,
                        study_run2, 
                        neu_ths_list
                        ))
                
                # matching all the TMs
                behav_data['PostESI_NeuTargMiss_Count'].append(
                    matching(
                        study_df,
                        study_run1, 
                        neu_tms_list
                        ))
                
                behav_data['PostIMP_NeuTargMiss_Count'].append(
                    matching(
                        study_df,
                        study_run2, 
                        neu_tms_list
                        ))
                
            else:
                '''
                Negative
                '''
                # matching all the FAs
                behav_data['PostESI_NegLureFA_Count'].append(
                    matching(
                        study_df,
                        study_run2, 
                        neg_lurefas_list
                        ))
                behav_data['PostIMP_NegLureFA_Count'].append(
                    matching(
                        study_df,
                        study_run1, 
                        neg_lurefas_list
                        ))

                # matching all the CRs
                behav_data['PostESI_NegLureCR_Count'].append(
                    matching(
                        study_df,
                        study_run2, 
                        neg_lurecr_list
                        ))
                
                behav_data['PostIMP_NegLureCR_Count'].append(
                    matching(
                        study_df,
                        study_run1, 
                        neg_lurecr_list
                        )) 
                        
                # matching all the THs
                behav_data['PostESI_NegTargHit_Count'].append(
                    matching(
                        study_df,
                        study_run2, 
                        neg_ths_list
                        ))
                
                behav_data['PostIMP_NegTargHit_Count'].append(
                    matching(
                        study_df,
                        study_run1, 
                        neg_ths_list
                        ))
                
                # matching all the TMs
                behav_data['PostESI_NegTargMiss_Count'].append(
                    matching(
                        study_df,
                        study_run2, 
                        neg_tms_list
                        ))
                
                behav_data['PostIMP_NegTargMiss_Count'].append(
                    matching(
                        study_df,
                        study_run1, 
                        neg_tms_list
                        ))
            
                '''Neutral'''

                        # matching all the FAs
                behav_data['PostESI_NeuLureFA_Count'].append(
                    matching(
                        study_df,
                        study_run2, 
                        neu_lurefa_list
                        ))

                behav_data['PostIMP_NeuLureFA_Count'].append(
                    matching(
                        study_df,
                        study_run1, 
                        neu_lurefa_list
                        ))

                # matching all the CRs
                behav_data['PostESI_NeuLureCR_Count'].append(
                    matching(
                        study_df,
                        study_run2, 
                        neu_lurecr_list
                        ))
                
                behav_data['PostIMP_NeuLureCR_Count'].append(
                    matching(
                        study_df,
                        study_run1, 
                        neu_lurecr_list
                        )) 
                
                # matching all the THs
                behav_data['PostESI_NeuTargHit_Count'].append(
                    matching(
                        study_df,
                        study_run2, 
                        neu_ths_list
                        ))
                
                behav_data['PostIMP_NeuTargHit_Count'].append(
                    matching(
                        study_df,
                        study_run1, 
                        neu_ths_list
                        ))
                
                # matching all the TMs
                behav_data['PostESI_NeuTargMiss_Count'].append(
                    matching(
                        study_df,
                        study_run2, 
                        neu_tms_list
                        ))
                
                behav_data['PostIMP_NeuTargMiss_Count'].append(
                    matching(
                        study_df,
                        study_run1, 
                        neu_tms_list
                        ))
                
#%%
behav_data_df = pd.DataFrame(behav_data)

behav_data_df.reset_index(drop=True)

# dropping 109 and 129 due to excessive number of FAd Foils
# behav_data_df = behav_data_df.drop([6, 23])

# getting mean for every column except for the subject column
# behav_data_df.loc['Mean'] = behav_data_df.iloc[:,1:].mean()
behav_data_df.to_csv("/home/mrive301/mvrn_esi_analysis/esi_imp.csv")

behav_data_df

#%%

# Collapsing across valence!

behav_data_df['PostESI_LureFA_Count'] = behav_data_df['PostESI_NegLureFA_Count'] + behav_data_df['PostESI_NeuLureFA_Count']

behav_data_df['PostIMP_LureFA_Count'] = behav_data_df['PostIMP_NegLureFA_Count'] + behav_data_df['PostIMP_NeuLureFA_Count']


behav_data_df['PostESI_LureCR_Count'] = behav_data_df['PostESI_NegLureCR_Count'] + behav_data_df['PostESI_NeuLureCR_Count']

behav_data_df['PostIMP_LureCR_Count'] = behav_data_df['PostIMP_NegLureCR_Count'] + behav_data_df['PostIMP_NeuLureCR_Count']



behav_data_df['PostESI_TargHit_Count'] = behav_data_df['PostESI_NegTargHit_Count'] + behav_data_df['PostESI_NeuTargHit_Count']

behav_data_df['PostIMP_TargHit_Count'] = behav_data_df['PostIMP_NegTargHit_Count'] + behav_data_df['PostIMP_NeuTargHit_Count']


behav_data_df['PostESI_TargMiss_Count'] = behav_data_df['PostESI_NegTargMiss_Count'] + behav_data_df['PostESI_NeuTargMiss_Count']

behav_data_df['PostIMP_TargMiss_Count'] = behav_data_df['PostIMP_NegTargMiss_Count'] + behav_data_df['PostIMP_NeuTargMiss_Count']


behav_data_df['FoilFA_Count'] = behav_data_df['NegFoilFA_Count'] + behav_data_df['NeuFoilFA_Count']

behav_data_df['FoilCR_Count'] = behav_data_df['NegFoilCR_Count'] + behav_data_df['NeuFoilCR_Count']

behav_data_df


#%%

'''
Adding RT (by Vane)
'''

rt_dset= ['Subject', 'LureFARslowme', 'LureFARfastme']

rt_dataset = pd.read_csv('/home/data/madlab/mvrn_ESI_study/esi_scored_details/lureFA_rt_df.csv', usecols=rt_dset)

# final_esi_imp_subs = [int(i) for i in final_esi_imp_subs]

esi_details_df = rt_dataset.query("Subject in @final_esi_imp_subs")

esi_details_df.reset_index(drop=True, inplace=True)

# Getting new list of subjects based on the esi_details_df
esi_details_ppt_list = esi_details_df['Subject'].tolist()

# Reducing the behav_data_df and then concatenate them to run analyses
behav_data_df = behav_data_df.query("Subject in @esi_details_ppt_list")

behav_data_df.reset_index(drop=True, inplace=True)

# Concatenate both dataframes
behav_data_df = pd.concat([behav_data_df, esi_details_df], axis=1)

# drop duplicate Subject columns
behav_data_df = behav_data_df.loc[:,~behav_data_df.columns.duplicated()].copy()

#%%

'''
Adding IN/OUT ZONE 80th (by Vane)
'''

in_out_80= ['Subject', 'LDItestper80zoneout', 'LDItestper80zonein']

in_out_80_dataset = pd.read_csv('/home/data/madlab/mvrn_ESI_study/esi_scored_details/inout_vs_mvrn.csv', usecols=in_out_80)

# final_esi_imp_subs = [int(i) for i in final_esi_imp_subs]

in_out_80_df = in_out_80_dataset.query("Subject in @final_esi_imp_subs")

in_out_80_df.reset_index(drop=True, inplace=True)

# Getting new list of subjects based on the esi_details_df
in_out_80_ppt_list = in_out_80_df['Subject'].tolist()

# Reducing the behav_data_df and then concatenate them to run analyses
behav_data_df = behav_data_df.query("Subject in @in_out_80_ppt_list")

behav_data_df.reset_index(drop=True, inplace=True)

# Concatenate both dataframes
behav_data_df = pd.concat([behav_data_df, in_out_80_df], axis=1)

# drop duplicate Subject columns
behav_data_df = behav_data_df.loc[:,~behav_data_df.columns.duplicated()].copy()


#%%
'''
Sequence memory ESI recalled details 
on LGI differences across valence

Due to issues with audio recordings
and the randomization of ESI vs. IMP 
subjects, sample size for this analysis
would be 65.
'''

cols = [
    'Subject',
    'Seq_Memo'
]
esi_details_dataset = pd.read_csv('/home/data/madlab/mvrn_ESI_study/esi_scored_details/esi_details_scored_3.csv', usecols=cols)

# the file includes all participants, I am isolating those that were
# used for the ESI vs. IMP condition only 
# NOTE: the number of participants (i.e., rows) between the  
#       behav_data_df and the esi_details_df is different because of the
#       poor audio quality of some participants' recordings leading to
#       further reduction of the pool...to 66.
final_esi_imp_subs = [int(i) for i in final_esi_imp_subs]

esi_details_df = esi_details_dataset.query("Subject in @final_esi_imp_subs")

esi_details_df.reset_index(drop=True, inplace=True)

# Getting new list of subjects based on the esi_details_df
esi_details_ppt_list = esi_details_df['Subject'].tolist()

behav_data_df['Subject'] = pd.to_numeric(behav_data_df['Subject'])

# # converting each subject in the list into a string
# esi_details_ppt_list = [str(element) for element in esi_details_ppt_list]

# Reducing the behav_data_df and then concatenate them to run analyses
behav_data_df = behav_data_df.query("Subject in @esi_details_ppt_list")

behav_data_df.reset_index(drop=True, inplace=True)

# # Concatenate both dataframes
# behav_data_df = pd.concat([behav_data_df, esi_details_df], axis=1)

# # drop duplicate Subject columns
# behav_data_df = behav_data_df.loc[:,~behav_data_df.columns.duplicated()].copy()
# behav_data_df

#%%
import pandas as pd
import seaborn as sns

'''Calculating FAs, Foil FAs, LGI, HR, FAR, dPrimes'''

# Negative Lure FAs per Condition
behav_data_df['PostESI_LureFA'] = behav_data_df['PostESI_LureFA_Count']/(behav_data_df['PostESI_LureFA_Count'] + behav_data_df['PostESI_LureCR_Count'])

behav_data_df['PostIMP_LureFA'] = behav_data_df['PostIMP_LureFA_Count']/(behav_data_df['PostIMP_LureFA_Count'] + behav_data_df['PostIMP_LureCR_Count'])

behav_data_df['FoilFA'] = behav_data_df['FoilFA_Count']/(behav_data_df['FoilFA_Count'] + behav_data_df['FoilCR_Count'])


# Negative LGIs per Condition
behav_data_df['PostESI_LGI'] = behav_data_df['PostESI_LureFA'] - behav_data_df['FoilFA'] 

behav_data_df['PostIMP_LGI'] = behav_data_df['PostIMP_LureFA'] - behav_data_df['FoilFA'] 



behav_data_df["PostESI_TargHit"] = behav_data_df["PostESI_TargHit_Count"]/(behav_data_df["PostESI_TargHit_Count"] + behav_data_df["PostESI_TargMiss_Count"])

behav_data_df["PostIMP_TargHit"] = behav_data_df["PostIMP_TargHit_Count"]/(behav_data_df["PostIMP_TargHit_Count"] + behav_data_df["PostIMP_TargMiss_Count"])


behav_data_df["PostESI_TargMiss"] = behav_data_df["PostESI_TargMiss_Count"]/(behav_data_df["PostESI_TargMiss_Count"] + behav_data_df["PostESI_TargHit_Count"])

behav_data_df["PostIMP_TargMiss"] = behav_data_df["PostIMP_TargMiss_Count"]/(behav_data_df["PostIMP_TargMiss_Count"] + behav_data_df["PostIMP_TargHit_Count"])

# Negative CRs, TM, LDI per Condition
behav_data_df['PostESI_LureCR'] = behav_data_df['PostESI_LureCR_Count']/(behav_data_df['PostESI_LureCR_Count'] + behav_data_df['PostESI_LureFA_Count'])

behav_data_df['PostIMP_LureCR'] = behav_data_df['PostIMP_LureCR_Count']/(behav_data_df['PostIMP_LureCR_Count'] + behav_data_df['PostIMP_LureFA_Count'])

behav_data_df['FoilCR'] = behav_data_df['FoilCR_Count']/(behav_data_df['FoilCR_Count'] + behav_data_df['FoilFA_Count'])

# Negative LDI per Condition
behav_data_df['PostESI_LDI'] = behav_data_df['PostESI_LureCR'] - behav_data_df['PostESI_TargMiss'] 

behav_data_df['PostIMP_LDI'] = behav_data_df['PostIMP_LureCR'] - behav_data_df['PostIMP_TargMiss'] 



# Negative Lure FAs per Condition
behav_data_df['PostESI_NegLureFA'] = behav_data_df['PostESI_NegLureFA_Count']/(behav_data_df['PostESI_NegLureFA_Count'] + behav_data_df['PostESI_NegLureCR_Count'])

behav_data_df['PostIMP_NegLureFA'] = behav_data_df['PostIMP_NegLureFA_Count']/(behav_data_df['PostIMP_NegLureFA_Count'] + behav_data_df['PostIMP_NegLureCR_Count'])

# Negative Foils 
behav_data_df['NegFoilFA'] = behav_data_df['NegFoilFA_Count']/(behav_data_df['NegFoilFA_Count'] + behav_data_df['NegFoilCR_Count'])


# Neutral Lure FAs per Condition
behav_data_df['PostESI_NeuLureFA'] = behav_data_df['PostESI_NeuLureFA_Count']/(behav_data_df['PostESI_NeuLureFA_Count'] + behav_data_df['PostESI_NeuLureCR_Count'])

behav_data_df['PostIMP_NeuLureFA'] = behav_data_df['PostIMP_NeuLureFA_Count']/(behav_data_df['PostIMP_NeuLureFA_Count'] + behav_data_df['PostIMP_NeuLureCR_Count'])

# Neutral Foils 
behav_data_df['NeuFoilFA'] = behav_data_df['NeuFoilFA_Count']/(behav_data_df['NeuFoilFA_Count'] + behav_data_df['NeuFoilCR_Count'])


# Negative LGIs per Condition
behav_data_df['PostESI_NegativeLGI'] = behav_data_df['PostESI_NegLureFA'] - behav_data_df['NegFoilFA'] 

behav_data_df['PostIMP_NegativeLGI'] = behav_data_df['PostIMP_NegLureFA'] - behav_data_df['NegFoilFA'] 


# Neutral LGIs per Condition
behav_data_df['PostESI_NeutralLGI'] = behav_data_df['PostESI_NeuLureFA'] - behav_data_df['NeuFoilFA'] 

behav_data_df['PostIMP_NeutralLGI'] = behav_data_df['PostIMP_NeuLureFA'] - behav_data_df['NeuFoilFA'] 


# Post ESI Negative Hit Rate, FA Rate, dPrime
# behav_data_df['PostESI_HRNeg'] = behav_data_df["PostESI_NegTargHit_Count"]/(behav_data_df["PostESI_NegTargHit_Count"] + behav_data_df["PostESI_NegTargMiss_Count"])

# behav_data_df['PostESI_FARNeg'] = behav_data_df["NegFoilFA_Count"] + behav_data_df["PostESI_NegLureFA_Count"] / (behav_data_df["NegFoilFA_Count"] + behav_data_df["NegFoilCR_Count"] +
#                                                                                                     behav_data_df["PostESI_NegLureFA_Count"] + behav_data_df["PostESI_NegLureCR_Count"])

# behav_data_df['PostESI_dPrimeNeg'] = norm.ppf(behav_data_df['PostESI_HRNeg']) - norm.ppf(behav_data_df['PostESI_FARNeg'])


# # Post ESI Neutral Hit Rate, FA Rate, dPrime
# behav_data_df['PostESI_HRNeu'] = behav_data_df["PostESI_NeuTargHit_Count"]/(behav_data_df["PostESI_NeuTargHit_Count"] + behav_data_df["PostESI_NeuTargMiss_Count"])

# behav_data_df['PostESI_FARNeu'] = behav_data_df["NeuFoilFA_Count"] + behav_data_df["PostESI_NeuLureFA_Count"] / (behav_data_df["NeuFoilFA_Count"] + behav_data_df["NeuFoilCR_Count"] +
#                                                                                                     behav_data_df["PostESI_NeuLureFA_Count"] + behav_data_df["PostESI_NeuLureCR_Count"])

# behav_data_df['PostESI_dPrimeNeu'] = norm.ppf(behav_data_df['PostESI_HRNeu']) - norm.ppf(behav_data_df['PostESI_HRNeu'])


# # Post IMP Negative Hit Rate, FA Rate, dPrime
# behav_data_df['PostIMP_HRNeg'] = behav_data_df["PostIMP_NegTargHit_Count"]/(behav_data_df["PostIMP_NegTargHit_Count"] + behav_data_df["PostIMP_NegTargMiss_Count"])

# behav_data_df['PostIMP_FARNeg'] = behav_data_df["NegFoilFA_Count"] + behav_data_df["PostIMP_NegLureFA_Count"] / (behav_data_df["NegFoilFA_Count"] + behav_data_df["NegFoilCR_Count"] +
#                                                                                                     behav_data_df["PostIMP_NegLureFA_Count"] + behav_data_df["PostIMP_NegLureCR_Count"])

# behav_data_df['PostIMP_dPrimeNeg'] = norm.ppf(behav_data_df['PostIMP_HRNeg']) - norm.ppf(behav_data_df['PostIMP_FARNeg'])

# # Post IMP Neutral Hit Rate, FA Rate, dPrime
# behav_data_df['PostIMP_HRNeu'] = behav_data_df["PostESI_NeuTargHit_Count"]/(behav_data_df["PostESI_NeuTargHit_Count"] + behav_data_df["PostESI_NeuTargMiss_Count"])

# behav_data_df['PostIMP_FARNeu'] = behav_data_df["NeuFoilFA_Count"] + behav_data_df["PostESI_NeuLureFA_Count"] / (behav_data_df["NeuFoilFA_Count"] + behav_data_df["NeuFoilCR_Count"] +
#                                                                                                     behav_data_df["PostESI_NeuLureFA_Count"] + behav_data_df["PostESI_NeuLureCR_Count"])

# behav_data_df['PostIMP_dPrimeNeu'] = norm.ppf(behav_data_df['PostIMP_HRNeu']) - norm.ppf(behav_data_df['PostIMP_FARNeu'])

# TH per Condition
behav_data_df["PostESI_NegTargHit"] = behav_data_df["PostESI_NegTargHit_Count"]/(behav_data_df["PostESI_NegTargHit_Count"] + behav_data_df["PostESI_NegTargMiss_Count"])
behav_data_df["PostIMP_NegTargHit"] = behav_data_df["PostIMP_NegTargHit_Count"]/(behav_data_df["PostIMP_NegTargHit_Count"] + behav_data_df["PostIMP_NegTargMiss_Count"])

behav_data_df["PostESI_NeuTargHit"] = behav_data_df["PostESI_NeuTargHit_Count"]/(behav_data_df["PostESI_NeuTargHit_Count"] + behav_data_df["PostESI_NeuTargMiss_Count"])
behav_data_df["PostIMP_NeuTargHit"] = behav_data_df["PostIMP_NeuTargHit_Count"]/(behav_data_df["PostIMP_NeuTargHit_Count"] + behav_data_df["PostIMP_NeuTargMiss_Count"])


# Negative CRs, TM, LDI per Condition
behav_data_df['PostESI_NegLureCR'] = behav_data_df['PostESI_NegLureCR_Count']/(behav_data_df['PostESI_NegLureCR_Count'] + behav_data_df['PostESI_NegLureFA_Count'])

behav_data_df['PostIMP_NegLureCR'] = behav_data_df['PostIMP_NegLureCR_Count']/(behav_data_df['PostIMP_NegLureCR_Count'] + behav_data_df['PostIMP_NegLureFA_Count'])

behav_data_df["PostESI_NegTargMiss"] = behav_data_df["PostESI_NegTargMiss_Count"]/(behav_data_df["PostESI_NegTargMiss_Count"] + behav_data_df["PostESI_NegTargHit_Count"])

behav_data_df["PostIMP_NegTargMiss"] = behav_data_df["PostIMP_NegTargMiss_Count"]/(behav_data_df["PostIMP_NegTargMiss_Count"] + behav_data_df["PostIMP_NegTargHit_Count"])


# Negative LDI per Condition
behav_data_df['PostESI_NegativeLDI'] = behav_data_df['PostESI_NegLureCR'] - behav_data_df['PostESI_NegTargMiss'] 

behav_data_df['PostIMP_NegativeLDI'] = behav_data_df['PostIMP_NegLureCR'] - behav_data_df['PostIMP_NegTargMiss'] 


# Neutral CRs, TM, LDI per Condition
behav_data_df['PostESI_NeuLureCR'] = behav_data_df['PostESI_NeuLureCR_Count']/(behav_data_df['PostESI_NeuLureCR_Count'] + behav_data_df['PostESI_NeuLureFA_Count'])

behav_data_df['PostIMP_NeuLureCR'] = behav_data_df['PostIMP_NeuLureCR_Count']/(behav_data_df['PostIMP_NeuLureCR_Count'] + behav_data_df['PostIMP_NeuLureFA_Count'])

behav_data_df["PostESI_NeuTargMiss"] = behav_data_df["PostESI_NeuTargMiss_Count"]/(behav_data_df["PostESI_NeuTargMiss_Count"] + behav_data_df["PostESI_NeuTargHit_Count"])

behav_data_df["PostIMP_NeuTargMiss"] = behav_data_df["PostIMP_NeuTargMiss_Count"]/(behav_data_df["PostIMP_NeuTargMiss_Count"] + behav_data_df["PostIMP_NeuTargHit_Count"])


# Neutral LDI per Condition
behav_data_df['PostESI_NeutralLDI'] = behav_data_df['PostESI_NeuLureCR'] - behav_data_df['PostESI_NeuTargMiss'] 

behav_data_df['PostIMP_NeutralLDI'] = behav_data_df['PostIMP_NeuLureCR'] - behav_data_df['PostIMP_NeuTargMiss'] 

# Windsorizing LGIs and LDIs

from scipy.stats.mstats import winsorize

behav_data_df['PostESI_LGI'] = winsorize(behav_data_df['PostESI_LGI'], limits=[0.05, 0.05])
behav_data_df['PostESI_LGI'] = winsorize(behav_data_df['PostESI_LGI'], limits=[0.05, 0.05])

behav_data_df['PostIMP_LGI'] = winsorize(behav_data_df['PostIMP_LGI'], limits=[0.05, 0.05])
behav_data_df['PostIMP_LGI'] = winsorize(behav_data_df['PostIMP_LGI'], limits=[0.05, 0.05])

behav_data_df['PostESI_LDI'] = winsorize(behav_data_df['PostESI_LDI'], limits=[0.05, 0.05])
behav_data_df['PostESI_LDI'] = winsorize(behav_data_df['PostESI_LDI'], limits=[0.05, 0.05])

behav_data_df['PostIMP_LDI'] = winsorize(behav_data_df['PostIMP_LDI'], limits=[0.05, 0.05])
behav_data_df['PostIMP_LDI'] = winsorize(behav_data_df['PostIMP_LDI'], limits=[0.05, 0.05])




behav_data_df['PostESI_NegativeLGI'] = winsorize(behav_data_df['PostESI_NegativeLGI'], limits=[0.05, 0.05])
behav_data_df['PostESI_NeutralLGI'] = winsorize(behav_data_df['PostESI_NeutralLGI'], limits=[0.05, 0.05])

behav_data_df['PostIMP_NegativeLGI'] = winsorize(behav_data_df['PostIMP_NegativeLGI'], limits=[0.05, 0.05])
behav_data_df['PostIMP_NeutralLGI'] = winsorize(behav_data_df['PostIMP_NeutralLGI'], limits=[0.05, 0.05])

behav_data_df['PostESI_NegativeLDI'] = winsorize(behav_data_df['PostESI_NegativeLDI'], limits=[0.05, 0.05])
behav_data_df['PostESI_NeutralLDI'] = winsorize(behav_data_df['PostESI_NeutralLDI'], limits=[0.05, 0.05])

behav_data_df['PostIMP_NegativeLDI'] = winsorize(behav_data_df['PostIMP_NegativeLDI'], limits=[0.05, 0.05])
behav_data_df['PostIMP_NeutralLDI'] = winsorize(behav_data_df['PostIMP_NeutralLDI'], limits=[0.05, 0.05])

#%%
# Concatenate both dataframes
behav_data_df = pd.concat([behav_data_df, esi_details_df], axis=1)

# drop duplicate Subject columns
behav_data_df = behav_data_df.loc[:,~behav_data_df.columns.duplicated()].copy()
behav_data_df

#%%

"""""""""""""""""""""""""""""""""
In-Out zone differences
as a function of 
sequence memory
"""""""""""""""""""""""""""""""""

esi_melt = pd.melt(
    behav_data_df, 
    id_vars=[
        'Subject', 
        'Seq_Memo'
        ], 
    value_vars=[
        'LDItestper80zoneout', 
        'LDItestper80zonein'
        ])

esi_melt.columns = [
    'Subject', 
    'Seq_Memo', 
    'Response', 
    'Value'
    ]

zone = []
for j, row in esi_melt.iterrows():
    if 'out' in row['Response']:
        zone.append('Out')
    if 'in' in row['Response']:
        zone.append('In')
esi_melt['In_Out_80Zone'] = zone


esi_melt = esi_melt[[
    "Subject",
    "Seq_Memo", 
    "Response", 
    "In_Out_80Zone", 
    "Value"
    ]]
esi_melt.dropna(inplace = True)

esi_melt
#%%

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.glm(
    "Value ~ Seq_Memo*In_Out_80Zone",
    esi_melt, groups=esi_melt["Subject"])
mdf = md.fit()
print(mdf.summary())

#%%

# Adding sequence memory!
import seaborn as sns
#row = one graph on top of the other
#col = one graph next to the other

#truncate = to prevent thew graph to end abruptly on the last data point 
    #and thus let it continue

palette = {'Out': 'mediumvioletred',
           'In':'darkgoldenrod'}

{'Dead': 'navy', 'Survived': 'turquoise'}

glm_plot = sns.lmplot(data=esi_melt, 
           x='Seq_Memo', 
           y='Value', 
           hue='In_Out_80Zone', 
           palette = palette, 
           truncate=False,
           legend = False
           )

plt.ylabel('Lure Discrimination index (LDI)', fontsize = 15)
plt.xlabel('Sequence Memory', fontsize = 15)
plt.legend(title='80th_Zone', loc='upper left', labels=['In Zone', 'Out Zone'])
plt.show(glm_plot)

#%%

md = smf.glm(
    "Value ~ Randomization*LureFARfastme",
    esi_melt, groups=esi_melt["Subject"])
mdf = md.fit()
print(mdf.summary())

#%%

# Adding sequence memory!
import seaborn as sns
#row = one graph on top of the other
#col = one graph next to the other

#truncate = to prevent thew graph to end abruptly on the last data point 
    #and thus let it continue

palette = ['mediumvioletred',  
                    'darkgoldenrod']

sns.lmplot(data=esi_melt, x='LureFARfastme', y='Value', col='Randomization', palette = palette, truncate=False)


# %%
