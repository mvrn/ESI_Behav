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

# establishing the directory from which to retrieve esi vs. math csv files
root_dir = "/home/data/madlab/mvrn_ESI_study/clean_pilot_subs/"


# compiling list of esi vs. math subjects
final_esi_math_subs = sorted([
    "125","143","150","155","156","157","161","166","167","171","172",
    "174","176","177","178","179","182","183","188","189","190",
    "191","192","193","195","196","198","199","202","203","205",
    "206","207","208","209","214","215","217","218","219","220","221",
    "223","224","225","226","227","228","229","230","231","232","233",
    "234","235","236","237","238","239","240","241","242","243","244",
    "245","247","248","249","250"
])

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


    'Postmath_NegLureFA_Count': [],
    'Postmath_NeuLureFA_Count': [],

    'Postmath_NegLureCR_Count': [],
    'Postmath_NeuLureCR_Count': [],

    'Postmath_NegTargHit_Count': [],
    'Postmath_NeuTargHit_Count': [],

    'Postmath_NegTargMiss_Count': [],
    'Postmath_NeuTargMiss_Count': [],


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

# iterating over every subject
for sub in final_esi_math_subs:
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
        
    study_df['Randomization'] = study_df['Randomization'].replace([1, 2], ['ESIthenmath','maththenESI'])

    test_df['Randomization'] = test_df['Randomization'].replace([1, 2], ['ESIthenmath','maththenESI'])
    test_df['test_stimtype'] = test_df['test_stimtype'].replace([1, 2], ['negative','neutral'])
    test_df['test_stimsim'] = test_df['test_stimsim'].replace([1, 2, 4], ['target','lure', 'foil'])
    test_df['test_resp'] = test_df['test_resp'].replace([1, 2], ['old','new'])
    test_df['test_resp'] = test_df['test_resp'].replace('None', np.nan)

    dfs = [study_df, test_df]

    # adding list of subjects to the dictionary we created above
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

    # testing whether each subject has 117 negative stimuli at test
    total_neg_stim_persub = len(neg_stim_pd[neg_stim_pd["Subject"]==int(f"{sub}")])
    if total_neg_stim_persub != 117:
        print(f"{sub}" + " test stim count: not all is well :/")
    
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

            if study_df['Randomization'][0] == "ESIthenmath":
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
                behav_data['Postmath_NegLureFA_Count'].append(
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
                
                behav_data['Postmath_NegLureCR_Count'].append(
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
                
                behav_data['Postmath_NegTargHit_Count'].append(
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
                
                behav_data['Postmath_NegTargMiss_Count'].append(
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

                behav_data['Postmath_NeuLureFA_Count'].append(
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
                
                behav_data['Postmath_NeuLureCR_Count'].append(
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
                
                behav_data['Postmath_NeuTargHit_Count'].append(
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
                
                behav_data['Postmath_NeuTargMiss_Count'].append(
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
                behav_data['Postmath_NegLureFA_Count'].append(
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
                
                behav_data['Postmath_NegLureCR_Count'].append(
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
                
                behav_data['Postmath_NegTargHit_Count'].append(
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
                
                behav_data['Postmath_NegTargMiss_Count'].append(
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

                behav_data['Postmath_NeuLureFA_Count'].append(
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
                
                behav_data['Postmath_NeuLureCR_Count'].append(
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
                
                behav_data['Postmath_NeuTargHit_Count'].append(
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
                
                behav_data['Postmath_NeuTargMiss_Count'].append(
                    matching(
                        study_df,
                        study_run1, 
                        neu_tms_list
                        ))

#%%
behav_data_df = pd.DataFrame(behav_data)

behav_data_df.reset_index(drop=True)

# getting mean for every column except for the subject column
# behav_data_df.loc['Mean'] = behav_data_df.iloc[:,1:].mean()

behav_data_df.to_csv("/home/mrive301/mvrn_esi_analysis/esi_math.csv")

behav_data_df


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
esi_details_df = pd.DataFrame(esi_details_dataset)

esi_details_df.sort_values(by=['Subject'])

#%%


# the file includes all participants, I am isolating those that were
# used for the ESI vs. IMP condition only 
# NOTE: the number of participants (i.e., rows) between the  
#       behav_data_df and the esi_details_df is different because of the
#       poor audio quality of some participants' recordings leading to
#       further reduction of the pool...to 66.
esi_details_df = esi_details_df.query("Subject in @final_esi_math_subs")
# dropping 109 and 129 to align with behav_data_df
# esi_details_df = esi_details_df.drop([2, 18])
esi_details_df.reset_index(drop=True, inplace=True)


#%%

# Getting new list of subjects based on the esi_details_df
esi_details_ppt_list = esi_details_df['Subject'].tolist()
# converting each subject in the list into a string
esi_details_ppt_list = [str(element) for element in esi_details_ppt_list]

#%%
# Reducing the behav_data_df and then concatenate them to run analyses
# NOTE: the final subject list is 64 and not 66 (based on the esi_details_list)
#       because if you look above I eliminated subjects 109 and 126
behav_data_df = behav_data_df.query("Subject in @esi_details_ppt_list")
behav_data_df.reset_index(drop=True, inplace=True)

# # Concatenate both dataframes
# behav_data_df = pd.concat([behav_data_df, esi_details_df], axis=1)

# # drop duplicate Subject columns
# behav_data_df = behav_data_df.loc[:,~behav_data_df.columns.duplicated()].copy()

#%%
import pandas as pd
import seaborn as sns

'''Collapsing Across Valence'''

behav_data_df['PostESI_LureFA_Count'] = behav_data_df['PostESI_NegLureFA_Count'] + behav_data_df['PostESI_NeuLureFA_Count']

behav_data_df['Postmath_LureFA_Count'] = behav_data_df['Postmath_NegLureFA_Count'] + behav_data_df['Postmath_NeuLureFA_Count']


behav_data_df['PostESI_LureCR_Count'] = behav_data_df['PostESI_NegLureCR_Count'] + behav_data_df['PostESI_NeuLureCR_Count']

behav_data_df['Postmath_LureCR_Count'] = behav_data_df['Postmath_NegLureCR_Count'] + behav_data_df['Postmath_NeuLureCR_Count']



behav_data_df['PostESI_TargHit_Count'] = behav_data_df['PostESI_NegTargHit_Count'] + behav_data_df['PostESI_NeuTargHit_Count']

behav_data_df['Postmath_TargHit_Count'] = behav_data_df['Postmath_NegTargHit_Count'] + behav_data_df['Postmath_NeuTargHit_Count']


behav_data_df['PostESI_TargMiss_Count'] = behav_data_df['PostESI_NegTargMiss_Count'] + behav_data_df['PostESI_NeuTargMiss_Count']

behav_data_df['Postmath_TargMiss_Count'] = behav_data_df['Postmath_NegTargMiss_Count'] + behav_data_df['Postmath_NeuTargMiss_Count']


behav_data_df['FoilFA_Count'] = behav_data_df['NegFoilFA_Count'] + behav_data_df['NeuFoilFA_Count']

behav_data_df['FoilCR_Count'] = behav_data_df['NegFoilCR_Count'] + behav_data_df['NeuFoilCR_Count']

#%%

'''Calculating FAs, Foil FAs, LGI, HR, FAR, dPrimes'''

# Negative Lure FAs per Condition
behav_data_df['PostESI_LureFA'] = behav_data_df['PostESI_LureFA_Count']/(behav_data_df['PostESI_LureFA_Count'] + behav_data_df['PostESI_LureCR_Count'])

behav_data_df['Postmath_LureFA'] = behav_data_df['Postmath_LureFA_Count']/(behav_data_df['Postmath_LureFA_Count'] + behav_data_df['Postmath_LureCR_Count'])

behav_data_df['FoilFA'] = behav_data_df['FoilFA_Count']/(behav_data_df['FoilFA_Count'] + behav_data_df['FoilCR_Count'])


# Negative LGIs per Condition
behav_data_df['PostESI_LGI'] = behav_data_df['PostESI_LureFA'] - behav_data_df['FoilFA'] 

behav_data_df['Postmath_LGI'] = behav_data_df['Postmath_LureFA'] - behav_data_df['FoilFA'] 



behav_data_df["PostESI_TargHit"] = behav_data_df["PostESI_TargHit_Count"]/(behav_data_df["PostESI_TargHit_Count"] + behav_data_df["PostESI_TargMiss_Count"])

behav_data_df["Postmath_TargHit"] = behav_data_df["Postmath_TargHit_Count"]/(behav_data_df["Postmath_TargHit_Count"] + behav_data_df["Postmath_TargMiss_Count"])


behav_data_df["PostESI_TargMiss"] = behav_data_df["PostESI_TargMiss_Count"]/(behav_data_df["PostESI_TargMiss_Count"] + behav_data_df["PostESI_TargHit_Count"])

behav_data_df["Postmath_TargMiss"] = behav_data_df["Postmath_TargMiss_Count"]/(behav_data_df["Postmath_TargMiss_Count"] + behav_data_df["Postmath_TargHit_Count"])

# Negative CRs, TM, LDI per Condition
behav_data_df['PostESI_LureCR'] = behav_data_df['PostESI_LureCR_Count']/(behav_data_df['PostESI_LureCR_Count'] + behav_data_df['PostESI_LureFA_Count'])

behav_data_df['Postmath_LureCR'] = behav_data_df['Postmath_LureCR_Count']/(behav_data_df['Postmath_LureCR_Count'] + behav_data_df['Postmath_LureFA_Count'])

behav_data_df['FoilCR'] = behav_data_df['FoilCR_Count']/(behav_data_df['FoilCR_Count'] + behav_data_df['FoilFA_Count'])

# Negative LDI per Condition
behav_data_df['PostESI_LDI'] = behav_data_df['PostESI_LureCR'] - behav_data_df['PostESI_TargMiss'] 

behav_data_df['Postmath_LDI'] = behav_data_df['Postmath_LureCR'] - behav_data_df['Postmath_TargMiss'] 




# Negative Lure FAs per Condition
behav_data_df['PostESI_NegLureFA'] = behav_data_df['PostESI_NegLureFA_Count']/(behav_data_df['PostESI_NegLureFA_Count'] + behav_data_df['PostESI_NegLureCR_Count'])

behav_data_df['Postmath_NegLureFA'] = behav_data_df['Postmath_NegLureFA_Count']/(behav_data_df['Postmath_NegLureFA_Count'] + behav_data_df['Postmath_NegLureCR_Count'])

# Negative Foils 
behav_data_df['NegFoilFA'] = behav_data_df['NegFoilFA_Count']/(behav_data_df['NegFoilFA_Count'] + behav_data_df['NegFoilCR_Count'])


# Neutral Lure FAs per Condition
behav_data_df['PostESI_NeuLureFA'] = behav_data_df['PostESI_NeuLureFA_Count']/(behav_data_df['PostESI_NeuLureFA_Count'] + behav_data_df['PostESI_NeuLureCR_Count'])

behav_data_df['Postmath_NeuLureFA'] = behav_data_df['Postmath_NeuLureFA_Count']/(behav_data_df['Postmath_NeuLureFA_Count'] + behav_data_df['Postmath_NeuLureCR_Count'])

# Neutral Foils 
behav_data_df['NeuFoilFA'] = behav_data_df['NeuFoilFA_Count']/(behav_data_df['NeuFoilFA_Count'] + behav_data_df['NeuFoilCR_Count'])


# Negative LGIs per Condition
behav_data_df['PostESI_NegativeLGI'] = behav_data_df['PostESI_NegLureFA'] - behav_data_df['NegFoilFA'] 

behav_data_df['Postmath_NegativeLGI'] = behav_data_df['Postmath_NegLureFA'] - behav_data_df['NegFoilFA'] 


# Neutral LGIs per Condition
behav_data_df['PostESI_NeutralLGI'] = behav_data_df['PostESI_NeuLureFA'] - behav_data_df['NeuFoilFA'] 

behav_data_df['Postmath_NeutralLGI'] = behav_data_df['Postmath_NeuLureFA'] - behav_data_df['NeuFoilFA'] 


# Post ESI Negative Hit Rate, FA Rate, dPrime
behav_data_df['PostESI_HRNeg'] = behav_data_df["PostESI_NegTargHit_Count"]/(behav_data_df["PostESI_NegTargHit_Count"] + behav_data_df["PostESI_NegTargMiss_Count"])

behav_data_df['PostESI_FARNeg'] = behav_data_df["NegFoilFA_Count"] + behav_data_df["PostESI_NegLureFA_Count"] / (behav_data_df["NegFoilFA_Count"] + behav_data_df["NegFoilCR_Count"] +
                                                                                                    behav_data_df["PostESI_NegLureFA_Count"] + behav_data_df["PostESI_NegLureCR_Count"])

behav_data_df['PostESI_dPrimeNeg'] = norm.ppf(behav_data_df['PostESI_HRNeg']) - norm.ppf(behav_data_df['PostESI_FARNeg'])


# Post ESI Neutral Hit Rate, FA Rate, dPrime
behav_data_df['PostESI_HRNeu'] = behav_data_df["PostESI_NeuTargHit_Count"]/(behav_data_df["PostESI_NeuTargHit_Count"] + behav_data_df["PostESI_NeuTargMiss_Count"])

behav_data_df['PostESI_FARNeu'] = behav_data_df["NeuFoilFA_Count"] + behav_data_df["PostESI_NeuLureFA_Count"] / (behav_data_df["NeuFoilFA_Count"] + behav_data_df["NeuFoilCR_Count"] +
                                                                                                    behav_data_df["PostESI_NeuLureFA_Count"] + behav_data_df["PostESI_NeuLureCR_Count"])

behav_data_df['PostESI_dPrimeNeu'] = norm.ppf(behav_data_df['PostESI_HRNeu']) - norm.ppf(behav_data_df['PostESI_HRNeu'])


# Post math Negative Hit Rate, FA Rate, dPrime
behav_data_df['Postmath_HRNeg'] = behav_data_df["Postmath_NegTargHit_Count"]/(behav_data_df["Postmath_NegTargHit_Count"] + behav_data_df["Postmath_NegTargMiss_Count"])

behav_data_df['Postmath_FARNeg'] = behav_data_df["NegFoilFA_Count"] + behav_data_df["Postmath_NegLureFA_Count"] / (behav_data_df["NegFoilFA_Count"] + behav_data_df["NegFoilCR_Count"] +
                                                                                                    behav_data_df["Postmath_NegLureFA_Count"] + behav_data_df["Postmath_NegLureCR_Count"])

behav_data_df['Postmath_dPrimeNeg'] = norm.ppf(behav_data_df['Postmath_HRNeg']) - norm.ppf(behav_data_df['Postmath_FARNeg'])

# Post math Neutral Hit Rate, FA Rate, dPrime
behav_data_df['Postmath_HRNeu'] = behav_data_df["PostESI_NeuTargHit_Count"]/(behav_data_df["PostESI_NeuTargHit_Count"] + behav_data_df["PostESI_NeuTargMiss_Count"])

behav_data_df['Postmath_FARNeu'] = behav_data_df["NeuFoilFA_Count"] + behav_data_df["PostESI_NeuLureFA_Count"] / (behav_data_df["NeuFoilFA_Count"] + behav_data_df["NeuFoilCR_Count"] +
                                                                                                    behav_data_df["PostESI_NeuLureFA_Count"] + behav_data_df["PostESI_NeuLureCR_Count"])

behav_data_df['Postmath_dPrimeNeu'] = norm.ppf(behav_data_df['Postmath_HRNeu']) - norm.ppf(behav_data_df['Postmath_FARNeu'])

# TH per Condition
behav_data_df["PostESI_NegTargHit"] = behav_data_df["PostESI_NegTargHit_Count"]/(behav_data_df["PostESI_NegTargHit_Count"] + behav_data_df["PostESI_NegTargMiss_Count"])
behav_data_df["Postmath_NegTargHit"] = behav_data_df["Postmath_NegTargHit_Count"]/(behav_data_df["Postmath_NegTargHit_Count"] + behav_data_df["Postmath_NegTargMiss_Count"])

behav_data_df["PostESI_NeuTargHit"] = behav_data_df["PostESI_NeuTargHit_Count"]/(behav_data_df["PostESI_NeuTargHit_Count"] + behav_data_df["PostESI_NeuTargMiss_Count"])
behav_data_df["Postmath_NeuTargHit"] = behav_data_df["Postmath_NeuTargHit_Count"]/(behav_data_df["Postmath_NeuTargHit_Count"] + behav_data_df["Postmath_NeuTargMiss_Count"])


# Negative CRs, TM, LDI per Condition
behav_data_df['PostESI_NegLureCR'] = behav_data_df['PostESI_NegLureCR_Count']/(behav_data_df['PostESI_NegLureCR_Count'] + behav_data_df['PostESI_NegLureFA_Count'])

behav_data_df['Postmath_NegLureCR'] = behav_data_df['Postmath_NegLureCR_Count']/(behav_data_df['Postmath_NegLureCR_Count'] + behav_data_df['Postmath_NegLureFA_Count'])

behav_data_df["PostESI_NegTargMiss"] = behav_data_df["PostESI_NegTargMiss_Count"]/(behav_data_df["PostESI_NegTargMiss_Count"] + behav_data_df["PostESI_NegTargHit_Count"])

behav_data_df["Postmath_NegTargMiss"] = behav_data_df["Postmath_NegTargMiss_Count"]/(behav_data_df["Postmath_NegTargMiss_Count"] + behav_data_df["Postmath_NegTargHit_Count"])


# Negative LDI per Condition
behav_data_df['PostESI_NegativeLDI'] = behav_data_df['PostESI_NegLureCR'] - behav_data_df['PostESI_NegTargMiss'] 

behav_data_df['Postmath_NegativeLDI'] = behav_data_df['Postmath_NegLureCR'] - behav_data_df['Postmath_NegTargMiss'] 


# Neutral CRs, TM, LDI per Condition
behav_data_df['PostESI_NeuLureCR'] = behav_data_df['PostESI_NeuLureCR_Count']/(behav_data_df['PostESI_NeuLureCR_Count'] + behav_data_df['PostESI_NeuLureFA_Count'])

behav_data_df['Postmath_NeuLureCR'] = behav_data_df['Postmath_NeuLureCR_Count']/(behav_data_df['Postmath_NeuLureCR_Count'] + behav_data_df['Postmath_NeuLureFA_Count'])

behav_data_df["PostESI_NeuTargMiss"] = behav_data_df["PostESI_NeuTargMiss_Count"]/(behav_data_df["PostESI_NeuTargMiss_Count"] + behav_data_df["PostESI_NeuTargHit_Count"])

behav_data_df["Postmath_NeuTargMiss"] = behav_data_df["Postmath_NeuTargMiss_Count"]/(behav_data_df["Postmath_NeuTargMiss_Count"] + behav_data_df["Postmath_NeuTargHit_Count"])


# Neutral LDI per Condition
behav_data_df['PostESI_NeutralLDI'] = behav_data_df['PostESI_NeuLureCR'] - behav_data_df['PostESI_NeuTargMiss'] 

behav_data_df['Postmath_NeutralLDI'] = behav_data_df['Postmath_NeuLureCR'] - behav_data_df['Postmath_NeuTargMiss'] 

# Windsorizing LGIs and LDIs

from scipy.stats.mstats import winsorize

behav_data_df['PostESI_LGI'] = winsorize(behav_data_df['PostESI_LGI'], limits=[0.05, 0.05])
behav_data_df['PostESI_LGI'] = winsorize(behav_data_df['PostESI_LGI'], limits=[0.05, 0.05])

behav_data_df['Postmath_LGI'] = winsorize(behav_data_df['Postmath_LGI'], limits=[0.05, 0.05])
behav_data_df['Postmath_LGI'] = winsorize(behav_data_df['Postmath_LGI'], limits=[0.05, 0.05])

behav_data_df['PostESI_LDI'] = winsorize(behav_data_df['PostESI_LDI'], limits=[0.05, 0.05])
behav_data_df['PostESI_LDI'] = winsorize(behav_data_df['PostESI_LDI'], limits=[0.05, 0.05])

behav_data_df['Postmath_LDI'] = winsorize(behav_data_df['Postmath_LDI'], limits=[0.05, 0.05])
behav_data_df['Postmath_LDI'] = winsorize(behav_data_df['Postmath_LDI'], limits=[0.05, 0.05])



behav_data_df['PostESI_NegativeLGI'] = winsorize(behav_data_df['PostESI_NegativeLGI'], limits=[0.05, 0.05])
behav_data_df['PostESI_NeutralLGI'] = winsorize(behav_data_df['PostESI_NeutralLGI'], limits=[0.05, 0.05])

behav_data_df['Postmath_NegativeLGI'] = winsorize(behav_data_df['Postmath_NegativeLGI'], limits=[0.05, 0.05])
behav_data_df['Postmath_NeutralLGI'] = winsorize(behav_data_df['Postmath_NeutralLGI'], limits=[0.05, 0.05])

behav_data_df['PostESI_NegativeLDI'] = winsorize(behav_data_df['PostESI_NegativeLDI'], limits=[0.05, 0.05])
behav_data_df['PostESI_NeutralLDI'] = winsorize(behav_data_df['PostESI_NeutralLDI'], limits=[0.05, 0.05])

behav_data_df['Postmath_NegativeLDI'] = winsorize(behav_data_df['Postmath_NegativeLDI'], limits=[0.05, 0.05])
behav_data_df['Postmath_NeutralLDI'] = winsorize(behav_data_df['Postmath_NeutralLDI'], limits=[0.05, 0.05])

behav_data_df

#%%
# Concatenate both dataframes
behav_data_df = pd.concat([behav_data_df, esi_details_df], axis=1)

# drop duplicate Subject columns
behav_data_df = behav_data_df.loc[:,~behav_data_df.columns.duplicated()].copy()

behav_data_df


#%%
'''
Is sequence memory recall modulating
memory discrimination following ESI?

Sequence memory should improve 
memory discrimination by decreasing
negative relative to neutral LGI and
increasing LDI
'''
esi_seq_melt = pd.melt(behav_data_df, id_vars=['Subject', 'Seq_Memo'], value_vars=[
    "PostESI_NegativeLGI",
    "PostESI_NeutralLGI",

    "PostESI_NegativeLDI",
    "PostESI_NeutralLDI"
    ])
esi_seq_melt.columns = ['Subject', 'Seq_Memo', 'Response', 'Value']

valence = []
for i, row in esi_seq_melt.iterrows():
    if 'Negative' in row['Response']:
        valence.append('Neg')
    if 'Neutral' in row['Response']:
        valence.append('Neu')
esi_seq_melt['Valence'] = valence

condition = []
for i, row in esi_seq_melt.iterrows():
    if 'LGI' in row['Response']:
        condition.append('LGI')
    if 'LDI' in row['Response']:
        condition.append('LDI')
esi_seq_melt['Condition'] = condition

esi_seq_melt = esi_seq_melt[[
    "Subject", "Seq_Memo", "Response", "Valence", "Condition", "Value"]]
esi_seq_melt.dropna(inplace = True)

esi_seq_melt

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.glm(
    "Value ~ Valence*Condition*Seq_Memo",
    esi_seq_melt, groups=esi_seq_melt["Subject"])
mdf = md.fit()
print(mdf.summary())


import seaborn as sns
#row = one graph on top of the other
#col = one graph next to the other

#truncate = to prevent thew graph to end abruptly on the last data point 
    #and thus let it continue

palette = ['mediumorchid',  
                    'darkturquoise']

sns.lmplot(data=esi_seq_melt, x='Seq_Memo', y='Value', hue='Valence', col='Condition', palette = palette, truncate=False)
#%%
'''
Is sequence memory recall modulating 
the degree of LGI after ESI?
'''
esi_seq_melt = pd.melt(behav_data_df, id_vars=['Subject', 'Seq_Memo'], value_vars=[
    "PostESI_NegativeLGI",
    "PostESI_NeutralLGI"
    ])
esi_seq_melt.columns = ['Subject', 'Seq_Memo', 'Response', 'Value']

valence = []
for i, row in esi_seq_melt.iterrows():
    if 'Negative' in row['Response']:
        valence.append('Neg')
    if 'Neutral' in row['Response']:
        valence.append('Neu')
esi_seq_melt['Valence'] = valence

esi_seq_melt = esi_seq_melt[[
    "Subject", "Seq_Memo", "Response", "Valence", "Value"]]
esi_seq_melt.dropna(inplace = True)

esi_seq_melt

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.glm(
    "Value ~ Valence*Seq_Memo",
    esi_seq_melt, groups=esi_seq_melt["Subject"])
mdf = md.fit()
print(mdf.summary())


import seaborn as sns
#row = one graph on top of the other
#col = one graph next to the other

#truncate = to prevent thew graph to end abruptly on the last data point 
    #and thus let it continue

palette = ['mediumorchid',  
                    'darkturquoise']

sns.lmplot(data=esi_seq_melt, x='Seq_Memo', y='Value', hue='Valence', palette = palette, truncate=False)

#%%
'''
Is sequence memory recall modulating 
the degree of LDI after ESI?
'''
esi_seq_melt = pd.melt(behav_data_df, id_vars=['Subject', 'Seq_Memo'], value_vars=[
    "PostESI_NegativeLDI",
    "PostESI_NeutralLDI"
    ])
esi_seq_melt.columns = ['Subject', 'Seq_Memo', 'Response', 'Value']

valence = []
for i, row in esi_seq_melt.iterrows():
    if 'Negative' in row['Response']:
        valence.append('Neg')
    if 'Neutral' in row['Response']:
        valence.append('Neu')
esi_seq_melt['Valence'] = valence

esi_seq_melt = esi_seq_melt[[
    "Subject", "Seq_Memo", "Response", "Valence", "Value"]]
esi_seq_melt.dropna(inplace = True)

esi_seq_melt

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.glm(
    "Value ~ Valence*Seq_Memo",
    esi_seq_melt, groups=esi_seq_melt["Subject"])
mdf = md.fit()
print(mdf.summary())


import seaborn as sns
#row = one graph on top of the other
#col = one graph next to the other

#truncate = to prevent thew graph to end abruptly on the last data point 
    #and thus let it continue

palette = ['mediumorchid',  
                    'darkturquoise']

sns.lmplot(data=esi_seq_melt, x='Seq_Memo', y='Value', hue='Valence', palette = palette, truncate=False)


#%%

"""
ESI vs IMP LDI
"""
'''
Shapiro for Post ESI Negative vs. Neutral
'''
from scipy import stats
test_postesi_ldi = behav_data_df["PostESI_LDI"]
test_postmath_ldi = behav_data_df["Postmath_LDI"]

print(test_postesi_ldi.mean())
print(test_postmath_ldi.mean())

print('Shapiro for Post ESI LDI:', stats.shapiro(test_postesi_ldi))
print('Shapiro for Post IMP LDI:', stats.shapiro(test_postmath_ldi))


'''
Plotting Post ESI vs. Post IMP LDI
'''
from scipy import stats
import seaborn as sns

test_data = behav_data_df.dropna(how='any', subset=['PostESI_LDI', 'Postmath_LDI'])
print(stats.wilcoxon(test_data['PostESI_LDI'], test_data['Postmath_LDI']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostESI_LDI": "mediumvioletred", "Postmath_LDI": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostESI_LDI', 'Postmath_LDI']]) 
sns.boxplot(data=test_data[['PostESI_LDI', 'Postmath_LDI']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Lure Discrimination Index (LDI)'), fontsize=17)
axes.tick_params(axis='y', labelsize=13, width=2) 

axes.set_xlabel(('Condition'), fontsize=17)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Post-ESI LDI'
labels[1] = 'Post-MATH LDI'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)

plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_ESIvMATH_LDI.png', bbox_inches='tight',dpi=1200)

#%%



#%%

'''LURE GENERALIZATION INDEX ANALYSES'''

'''
Melting data to compare Post ESI vs. Post math LGIs
'''
esi_melt = pd.melt(behav_data_df, id_vars=['Subject'], value_vars=[
    'PostESI_NegativeLGI',
    'PostESI_NeutralLGI',

    'Postmath_NegativeLGI',
    'Postmath_NeutralLGI'
    ])

esi_melt.columns = ['Subject', 'Response', 'Value']

valence = []
for i, row in esi_melt.iterrows():
    if 'Negative' in row['Response']:
        valence.append('Neg')
    if 'Neutral' in row['Response']:
        valence.append('Neu')
esi_melt['Valence'] = valence

condition = []
for j, row in esi_melt.iterrows():
    if 'PostESI' in row['Response']:
        condition.append('PostESI')
    if 'Postmath' in row['Response']:
        condition.append('Postmath')
esi_melt['Condition'] = condition

esi_melt = esi_melt[[
    "Subject", "Response", "Valence", "Condition", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt

'''
(PostESI vs. Postmath) x Valence (Neg vs. Neu) 
'''

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.mixedlm(
    "Value ~ Condition*Valence",
    esi_melt, groups=esi_melt["Subject"])
mdf = md.fit()
print(mdf.summary())

import matplotlib.pyplot as plt

'''
Shapiro for Post ESI Negative vs. Neutral
'''
from scipy import stats
test_postesi_neg_lgi = behav_data_df["PostESI_NegativeLGI"]
test_postesi_neu_lgi = behav_data_df["PostESI_NeutralLGI"]

print(test_postesi_neg_lgi.mean())
print(test_postesi_neu_lgi.mean())

print('Shapiro for Post ESI Negative LGI:', stats.shapiro(test_postesi_neg_lgi))
print('Shapiro for Post ESI Neutral LGI:', stats.shapiro(test_postesi_neu_lgi))


'''
Plotting Post ESI Neg vs. Neu LGI
'''
from scipy import stats
import seaborn as sns

# not using ttest_rel because....violation in the distribution
test_data = behav_data_df.dropna(how='any', subset=['PostESI_NegativeLGI', 'PostESI_NeutralLGI'])
print(stats.ttest_rel(test_data['PostESI_NegativeLGI'], test_data['PostESI_NeutralLGI']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostESI_NegativeLGI": "mediumvioletred", "PostESI_NeutralLGI": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostESI_NegativeLGI', 'PostESI_NeutralLGI']]) 
sns.boxplot(data=test_data[['PostESI_NegativeLGI', 'PostESI_NeutralLGI']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post ESI Lure Generalization Index (LGI)'), fontsize=15)
axes.tick_params(axis='y', labelsize=13, width=2) 

axes.set_xlabel(('Valence'), fontsize=15)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Negative'
labels[1] = 'Neutral'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)

plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_ESI_LGI(MATH).png', bbox_inches='tight',dpi=1200)
'''
Shapiro for Post math Negative vs. Neutral
'''
from scipy import stats
test_postmath_neg_lgi = behav_data_df["Postmath_NegativeLGI"]
test_postmath_neu_lgi = behav_data_df["Postmath_NeutralLGI"]

print(test_postmath_neg_lgi.mean())
print(test_postmath_neu_lgi.mean())

print('Shapiro for Post math Negative LGI:', stats.shapiro(test_postmath_neg_lgi))
print('Shapiro for Post math Neutral LGI:', stats.shapiro(test_postmath_neu_lgi))

'''
Plotting Post math Neg vs. Neu LGI
'''
from scipy import stats
import seaborn as sns

test_data = behav_data_df.dropna(how='any', subset=['Postmath_NegativeLGI', 'Postmath_NeutralLGI'])
print(stats.ttest_rel(test_data['Postmath_NegativeLGI'], test_data['Postmath_NeutralLGI']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"Postmath_NegativeLGI": "mediumvioletred", "Postmath_NeutralLGI": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['Postmath_NegativeLGI', 'Postmath_NeutralLGI']]) 
sns.boxplot(data=test_data[['Postmath_NegativeLGI', 'Postmath_NeutralLGI']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post Math Lure Generalization Index (LGI)'), fontsize=15)
axes.tick_params(axis='y', labelsize=13, width=2) 

axes.set_xlabel(('Valence'), fontsize=15)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Negative'
labels[1] = 'Neutral'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)

plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_MATH_LGI(MATH).png', bbox_inches='tight',dpi=1200)


# %%

'''LURE DISCRIMINATION INDEX ANALYSES'''

'''
Melting data to compare Post ESI vs. Post math LDIs
'''
esi_melt = pd.melt(behav_data_df, id_vars=['Subject'], value_vars=[
    'PostESI_NegativeLDI',
    'PostESI_NeutralLDI',

    'Postmath_NegativeLDI',
    'Postmath_NeutralLDI'
    ])

esi_melt.columns = ['Subject', 'Response', 'Value']

valence = []
for i, row in esi_melt.iterrows():
    if 'Negative' in row['Response']:
        valence.append('Neg')
    if 'Neutral' in row['Response']:
        valence.append('Neu')
esi_melt['Valence'] = valence

condition = []
for j, row in esi_melt.iterrows():
    if 'PostESI' in row['Response']:
        condition.append('PostESI')
    if 'Postmath' in row['Response']:
        condition.append('Postmath')
esi_melt['Condition'] = condition

esi_melt = esi_melt[[
    "Subject", "Response", "Valence", "Condition", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt

'''
(PostESI vs. Postmath) x Valence (Neg vs. Neu) 
'''

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.mixedlm(
    "Value ~ Condition*Valence",
    esi_melt, groups=esi_melt["Subject"])
mdf = md.fit()
print(mdf.summary())

import matplotlib.pyplot as plt

'''
Shapiro for Post ESI Negative vs. Neutral
'''
from scipy import stats
test_postesi_neg_ldi = behav_data_df["PostESI_NegativeLDI"]
test_postesi_neu_ldi = behav_data_df["PostESI_NeutralLDI"]

print(test_postesi_neg_ldi.mean())
print(test_postesi_neu_ldi.mean())

print('Shapiro for Post ESI Negative LDI:', stats.shapiro(test_postesi_neg_ldi))
print('Shapiro for Post ESI Neutral LDI:', stats.shapiro(test_postesi_neu_ldi))


'''
Plotting Post ESI Neg vs. Neu LDI
'''
from scipy import stats
import seaborn as sns

# not using ttest_rel because....violation in the distribution
test_data = behav_data_df.dropna(how='any', subset=['PostESI_NegativeLDI', 'PostESI_NeutralLDI'])
print(stats.ttest_rel(test_data['PostESI_NegativeLDI'], test_data['PostESI_NeutralLDI']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostESI_NegativeLDI": "mediumvioletred", "PostESI_NeutralLDI": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostESI_NegativeLDI', 'PostESI_NeutralLDI']]) 
sns.boxplot(data=test_data[['PostESI_NegativeLDI', 'PostESI_NeutralLDI']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post ESI Lure Discrimination Index (LDI)'), fontsize=15)
axes.tick_params(axis='y', labelsize=13, width=2) 

axes.set_xlabel(('Valence'), fontsize=15)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Negative'
labels[1] = 'Neutral'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)

plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_ESI_LDI(MATH).png', bbox_inches='tight',dpi=1200)
'''
Shapiro for Post math Negative vs. Neutral
'''
from scipy import stats
test_postmath_neg_ldi = behav_data_df["Postmath_NegativeLDI"]
test_postmath_neu_ldi = behav_data_df["Postmath_NeutralLDI"]

print(test_postmath_neg_ldi.mean())
print(test_postmath_neu_ldi.mean())

print('Shapiro for Post math Negative LDI:', stats.shapiro(test_postmath_neg_ldi))
print('Shapiro for Post math Neutral LDI:', stats.shapiro(test_postmath_neu_ldi))

'''
Plotting Post math Neg vs. Neu LDI
'''
from scipy import stats
import seaborn as sns

test_data = behav_data_df.dropna(how='any', subset=['Postmath_NegativeLDI', 'Postmath_NeutralLDI'])
print(stats.ttest_rel(test_data['Postmath_NegativeLDI'], test_data['Postmath_NeutralLDI']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"Postmath_NegativeLDI": "mediumvioletred", "Postmath_NeutralLDI": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['Postmath_NegativeLDI', 'Postmath_NeutralLDI']]) 
sns.boxplot(data=test_data[['Postmath_NegativeLDI', 'Postmath_NeutralLDI']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post Math Lure Discrimination Index (LDI)'), fontsize=15)
axes.tick_params(axis='y', labelsize=13, width=2) 

axes.set_xlabel(('Valence'), fontsize=15)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Negative'
labels[1] = 'Neutral'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)

plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_MATH_LDI(MATH).png', bbox_inches='tight',dpi=1200)

# %%
'''POST ESI VS. math HIT RATE ANALYSES'''

# behav_data_df = behav_data_df.drop(labels = ["Mean"], axis=0)

'''
Melting data to compare Post ESI vs. Post math LGIs
'''
esi_melt = pd.melt(behav_data_df, id_vars=['Subject'], value_vars=[
    'PostESI_HRNeg',
    'PostESI_HRNeu',

    'Postmath_HRNeg',
    'Postmath_HRNeu'

    ])

esi_melt.columns = ['Subject', 'Response', 'Value']

valence = []
for i, row in esi_melt.iterrows():
    if 'Neg' in row['Response']:
        valence.append('Neg')
    if 'Neu' in row['Response']:
        valence.append('Neu')
esi_melt['Valence'] = valence

condition = []
for j, row in esi_melt.iterrows():
    if 'PostESI' in row['Response']:
        condition.append('PostESI')
    if 'Postmath' in row['Response']:
        condition.append('Postmath')
esi_melt['Condition'] = condition


esi_melt = esi_melt[[
    "Subject", "Response", "Valence", "Condition", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt

'''
(PostESI vs. Postmath) x Valence (Neg vs. Neu) 
'''

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.mixedlm(
    "Value ~ Condition*Valence",
    esi_melt, groups=esi_melt["Subject"])
mdf = md.fit()
print(mdf.summary())
#%%
import matplotlib.pyplot as plt

'''
Shapiro for Post ESI Negative vs. Neutral
'''
from scipy import stats
test_postesi_neg_hr = behav_data_df["PostESI_HRNeg"]
test_postesi_neu_hr = behav_data_df["PostESI_HRNeu"]

print(test_postesi_neg_hr.mean())
print(test_postesi_neu_hr.mean())

print('Shapiro for Post ESI Negative HR:', stats.shapiro(test_postesi_neg_hr))
print('Shapiro for Post ESI Neutral HR:', stats.shapiro(test_postesi_neu_hr))


'''
Plotting Post ESI Neg vs. Neu LGI
'''
from scipy import stats
import seaborn as sns

# not using ttest_rel because....violation in the distribution
test_data = behav_data_df.dropna(how='any', subset=['PostESI_HRNeg', 'PostESI_HRNeu'])
print(stats.ttest_rel(test_data['PostESI_HRNeg'], test_data['PostESI_HRNeu']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostESI_HRNeg": "mediumvioletred", "PostESI_HRNeu": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostESI_HRNeg', 'PostESI_HRNeu']]) 
sns.boxplot(data=test_data[['PostESI_HRNeg', 'PostESI_HRNeu']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post ESI Lure Hit Rate'), fontsize=15)
axes.tick_params(axis='y', labelsize=13, width=2) 

axes.set_xlabel(('Valence'), fontsize=15)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Negative'
labels[1] = 'Neutral'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)

# plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_ESI_LGI.png', bbox_inches='tight',dpi=1200)

#%%
import matplotlib.pyplot as plt

'''
Shapiro for Post ESI Negative vs. Neutral
'''
from scipy import stats
test_postmath_neg_hr = behav_data_df["Postmath_HRNeg"]
test_postmath_neu_hr = behav_data_df["Postmath_HRNeu"]

print(test_postmath_neg_hr.mean())
print(test_postmath_neu_hr.mean())

print('Shapiro for Post math Negative HR:', stats.shapiro(test_postmath_neg_hr))
print('Shapiro for Post math Neutral HR:', stats.shapiro(test_postmath_neu_hr))


'''
Plotting Post ESI Neg vs. Neu math
'''
from scipy import stats
import seaborn as sns

# not using ttest_rel because....violation in the distribution
test_data = behav_data_df.dropna(how='any', subset=['Postmath_HRNeg', 'Postmath_HRNeu'])
print(stats.ttest_rel(test_data['Postmath_HRNeg'], test_data['Postmath_HRNeu']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"Postmath_HRNeg": "mediumvioletred", "Postmath_HRNeu": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['Postmath_HRNeg', 'Postmath_HRNeu']]) 
sns.boxplot(data=test_data[['Postmath_HRNeg', 'Postmath_HRNeu']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post math Lure Hit Rate'), fontsize=15)
axes.tick_params(axis='y', labelsize=13, width=2) 

axes.set_xlabel(('Valence'), fontsize=15)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Negative'
labels[1] = 'Neutral'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)

# plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_ESI_LGI.png', bbox_inches='tight',dpi=1200)

# %%

'''POST ESI VS. math FA RATE ANALYSES'''

# behav_data_df = behav_data_df.drop(labels = ["Mean"], axis=0)

'''
Melting data to compare Post ESI vs. Post math FAR
'''
esi_melt = pd.melt(behav_data_df, id_vars=['Subject'], value_vars=[
    'PostESI_FARNeg',
    'PostESI_FARNeu',

    'Postmath_FARNeg',
    'Postmath_FARNeu'

    ])

esi_melt.columns = ['Subject', 'Response', 'Value']

valence = []
for i, row in esi_melt.iterrows():
    if 'Neg' in row['Response']:
        valence.append('Neg')
    if 'Neu' in row['Response']:
        valence.append('Neu')
esi_melt['Valence'] = valence

condition = []
for j, row in esi_melt.iterrows():
    if 'PostESI' in row['Response']:
        condition.append('PostESI')
    if 'Postmath' in row['Response']:
        condition.append('Postmath')
esi_melt['Condition'] = condition


esi_melt = esi_melt[[
    "Subject", "Response", "Valence", "Condition", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt

'''
(PostESI vs. Postmath) x Valence (Neg vs. Neu) 
'''

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.mixedlm(
    "Value ~ Condition*Valence",
    esi_melt, groups=esi_melt["Subject"])
mdf = md.fit()
print(mdf.summary())
#%%
import matplotlib.pyplot as plt

'''
Shapiro for Post ESI Negative vs. Neutral
'''
from scipy import stats
test_postesi_neg_far = behav_data_df["PostESI_FARNeg"]
test_postesi_neu_far = behav_data_df["PostESI_FARNeu"]

print(test_postesi_neg_far.mean())
print(test_postesi_neu_far.mean())

print('Shapiro for Post ESI Negative FAR:', stats.shapiro(test_postesi_neg_far))
print('Shapiro for Post ESI Neutral FAR:', stats.shapiro(test_postesi_neu_far))


'''
Plotting Post ESI Neg vs. Neu LGI
'''
from scipy import stats
import seaborn as sns

# not using ttest_rel because....violation in the distribution
test_data = behav_data_df.dropna(how='any', subset=['PostESI_FARNeg', 'PostESI_FARNeu'])
print(stats.ttest_rel(test_data['PostESI_FARNeg'], test_data['PostESI_FARNeu']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostESI_FARNeg": "mediumvioletred", "PostESI_FARNeu": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostESI_FARNeg', 'PostESI_FARNeu']]) 
sns.boxplot(data=test_data[['PostESI_FARNeg', 'PostESI_FARNeu']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post ESI Lure FA Rate'), fontsize=15)
axes.tick_params(axis='y', labelsize=13, width=2) 

axes.set_xlabel(('Valence'), fontsize=15)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Negative'
labels[1] = 'Neutral'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)

# plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_ESI_LGI.png', bbox_inches='tight',dpi=1200)

#%%
import matplotlib.pyplot as plt

'''
Shapiro for Post ESI Negative vs. Neutral
'''
from scipy import stats
test_postmath_neg_far = behav_data_df["Postmath_FARNeg"]
test_postmath_neu_far = behav_data_df["Postmath_FARNeu"]

print(test_postmath_neg_far.mean())
print(test_postmath_neu_far.mean())

print('Shapiro for Post math Negative FAR:', stats.shapiro(test_postmath_neg_far))
print('Shapiro for Post math Neutral FAR:', stats.shapiro(test_postmath_neu_far))


'''
Plotting Post ESI Neg vs. Neu FAR
'''
from scipy import stats
import seaborn as sns

# not using ttest_rel because....violation in the distribution
test_data = behav_data_df.dropna(how='any', subset=['Postmath_FARNeg', 'Postmath_FARNeu'])
print(stats.ttest_rel(test_data['Postmath_FARNeg'], test_data['Postmath_FARNeu']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"Postmath_FARNeg": "mediumvioletred", "Postmath_FARNeu": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['Postmath_FARNeg', 'Postmath_FARNeu']]) 
sns.boxplot(data=test_data[['Postmath_FARNeg', 'Postmath_FARNeu']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post math Lure FA Rate'), fontsize=15)
axes.tick_params(axis='y', labelsize=13, width=2) 

axes.set_xlabel(('Valence'), fontsize=15)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Negative'
labels[1] = 'Neutral'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)
# %%


'''POST ESI VS. math FA ANALYSES'''

# behav_data_df = behav_data_df.drop(labels = ["Mean"], axis=0)

'''
Melting data to compare Post ESI vs. Post math FAR
'''
esi_melt = pd.melt(behav_data_df, id_vars=['Subject'], value_vars=[
    'PostESI_NegLureFA',
    'PostESI_NeuLureFA',

    'Postmath_NegLureFA',
    'Postmath_NeuLureFA'

    ])

esi_melt.columns = ['Subject', 'Response', 'Value']

valence = []
for i, row in esi_melt.iterrows():
    if 'Neg' in row['Response']:
        valence.append('Neg')
    if 'Neu' in row['Response']:
        valence.append('Neu')
esi_melt['Valence'] = valence

condition = []
for j, row in esi_melt.iterrows():
    if 'PostESI' in row['Response']:
        condition.append('PostESI')
    if 'Postmath' in row['Response']:
        condition.append('Postmath')
esi_melt['Condition'] = condition


esi_melt = esi_melt[[
    "Subject", "Response", "Valence", "Condition", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt

'''
(PostESI vs. Postmath) x Valence (Neg vs. Neu) 
'''

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.mixedlm(
    "Value ~ Condition*Valence",
    esi_melt, groups=esi_melt["Subject"])
mdf = md.fit()
print(mdf.summary())
#%%
import matplotlib.pyplot as plt

'''
Shapiro for Post ESI Negative vs. Neutral
'''
from scipy import stats
test_postesi_neg_fa = behav_data_df["PostESI_NegLureFA"]
test_postesi_neu_fa = behav_data_df["PostESI_NeuLureFA"]

print(test_postesi_neg_fa.mean())
print(test_postesi_neu_fa.mean())

print('Shapiro for Post ESI Negative FA:', stats.shapiro(test_postesi_neg_fa))
print('Shapiro for Post ESI Neutral FA:', stats.shapiro(test_postesi_neu_fa))


'''
Plotting Post ESI Neg vs. Neu LGI
'''
from scipy import stats
import seaborn as sns

# not using ttest_rel because....violation in the distribution
test_data = behav_data_df.dropna(how='any', subset=['PostESI_NegLureFA', 'PostESI_NeuLureFA'])
print(stats.ttest_rel(test_data['PostESI_NegLureFA'], test_data['PostESI_NeuLureFA']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostESI_NegLureFA": "mediumvioletred", "PostESI_NeuLureFA": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostESI_NegLureFA', 'PostESI_NeuLureFA']]) 
sns.boxplot(data=test_data[['PostESI_NegLureFA', 'PostESI_NeuLureFA']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post ESI Lure FA'), fontsize=15)
axes.tick_params(axis='y', labelsize=13, width=2) 

axes.set_xlabel(('Valence'), fontsize=15)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Negative'
labels[1] = 'Neutral'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)

# plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_ESI_LGI.png', bbox_inches='tight',dpi=1200)

#%%

import matplotlib.pyplot as plt

'''
Shapiro for Post math Negative vs. Neutral
'''
from scipy import stats
test_postmath_neg_fa = behav_data_df["Postmath_NegLureFA"]
test_postmath_neu_fa = behav_data_df["Postmath_NeuLureFA"]

print(test_postesi_neg_fa.mean())
print(test_postesi_neu_fa.mean())

print('Shapiro for Post math Negative FA:', stats.shapiro(test_postmath_neg_fa))
print('Shapiro for Post math Neutral FA:', stats.shapiro(test_postmath_neu_fa))


'''
Plotting Post math Neg vs. Neu LGI
'''
from scipy import stats
import seaborn as sns

# not using ttest_rel because....violation in the distribution
test_data = behav_data_df.dropna(how='any', subset=['Postmath_NegLureFA', 'Postmath_NeuLureFA'])
print(stats.ttest_rel(test_data['Postmath_NegLureFA'], test_data['Postmath_NeuLureFA']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"Postmath_NegLureFA": "mediumvioletred", "Postmath_NeuLureFA": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['Postmath_NegLureFA', 'Postmath_NeuLureFA']]) 
sns.boxplot(data=test_data[['Postmath_NegLureFA', 'Postmath_NeuLureFA']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post math Lure FA'), fontsize=15)
axes.tick_params(axis='y', labelsize=13, width=2) 

axes.set_xlabel(('Valence'), fontsize=15)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Negative'
labels[1] = 'Neutral'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)


#%%
'''POST ESI VS. math dPrime ANALYSES'''

# behav_data_df = behav_data_df.drop(labels = ["Mean"], axis=0)

'''
Melting data to compare Post ESI vs. Post math dPrime
'''
esi_melt = pd.melt(behav_data_df, id_vars=['Subject'], value_vars=[
    'PostESI_dPrimeNeg',
    'PostESI_dPrimeNeu',

    'Postmath_dPrimeNeg',
    'Postmath_dPrimeNeu'

    ])

esi_melt.columns = ['Subject', 'Response', 'Value']

valence = []
for i, row in esi_melt.iterrows():
    if 'Neg' in row['Response']:
        valence.append('Neg')
    if 'Neu' in row['Response']:
        valence.append('Neu')
esi_melt['Valence'] = valence

condition = []
for j, row in esi_melt.iterrows():
    if 'PostESI' in row['Response']:
        condition.append('PostESI')
    if 'Postmath' in row['Response']:
        condition.append('Postmath')
esi_melt['Condition'] = condition


esi_melt = esi_melt[[
    "Subject", "Response", "Valence", "Condition", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt

'''
(PostESI vs. Postmath) x Valence (Neg vs. Neu) 
'''

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.mixedlm(
    "Value ~ Condition*Valence",
    esi_melt, groups=esi_melt["Subject"])
mdf = md.fit()
print(mdf.summary())
#%%
import matplotlib.pyplot as plt

'''
Shapiro for Post ESI Negative vs. Neutral
'''
from scipy import stats
test_postesi_neg_fa = behav_data_df["PostESI_NegLureFA"]
test_postesi_neu_fa = behav_data_df["PostESI_NeuLureFA"]

print(test_postesi_neg_fa.mean())
print(test_postesi_neu_fa.mean())

print('Shapiro for Post ESI Negative FA:', stats.shapiro(test_postesi_neg_fa))
print('Shapiro for Post ESI Neutral FA:', stats.shapiro(test_postesi_neu_fa))


'''
Plotting Post ESI Neg vs. Neu LGI
'''
from scipy import stats
import seaborn as sns

# not using ttest_rel because....violation in the distribution
test_data = behav_data_df.dropna(how='any', subset=['PostESI_NegLureFA', 'PostESI_NeuLureFA'])
print(stats.ttest_rel(test_data['PostESI_NegLureFA'], test_data['PostESI_NeuLureFA']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostESI_NegLureFA": "mediumvioletred", "PostESI_NeuLureFA": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostESI_NegLureFA', 'PostESI_NeuLureFA']]) 
sns.boxplot(data=test_data[['PostESI_NegLureFA', 'PostESI_NeuLureFA']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post ESI Lure FA'), fontsize=15)
axes.tick_params(axis='y', labelsize=13, width=2) 

axes.set_xlabel(('Valence'), fontsize=15)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Negative'
labels[1] = 'Neutral'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)

# plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_ESI_LGI.png', bbox_inches='tight',dpi=1200)

#%%

import matplotlib.pyplot as plt

'''
Shapiro for Post math Negative vs. Neutral
'''
from scipy import stats
test_postmath_neg_fa = behav_data_df["Postmath_NegLureFA"]
test_postmath_neu_fa = behav_data_df["Postmath_NeuLureFA"]

print(test_postesi_neg_fa.mean())
print(test_postesi_neu_fa.mean())

print('Shapiro for Post math Negative FA:', stats.shapiro(test_postmath_neg_fa))
print('Shapiro for Post math Neutral FA:', stats.shapiro(test_postmath_neu_fa))


'''
Plotting Post math Neg vs. Neu LGI
'''
from scipy import stats
import seaborn as sns

# not using ttest_rel because....violation in the distribution
test_data = behav_data_df.dropna(how='any', subset=['Postmath_NegLureFA', 'Postmath_NeuLureFA'])
print(stats.ttest_rel(test_data['Postmath_NegLureFA'], test_data['Postmath_NeuLureFA']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"Postmath_NegLureFA": "mediumvioletred", "Postmath_NeuLureFA": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['Postmath_NegLureFA', 'Postmath_NeuLureFA']]) 
sns.boxplot(data=test_data[['Postmath_NegLureFA', 'Postmath_NeuLureFA']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post math Lure FA'), fontsize=15)
axes.tick_params(axis='y', labelsize=13, width=2) 

axes.set_xlabel(('Valence'), fontsize=15)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Negative'
labels[1] = 'Neutral'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)








#%%

    for trials in trial_types:
        # negative querying for each trial type
        if trials == lurefas:
            # PostESI_NegLureFA
            neg_lurefas_list = query_facr_thtm(neg_stim_pd,trials)

            for curr_category in categories:
                if curr_category == PostESI_NegLureFA:
                    if study_df['Randomization'][0] == "ESIthenmath":
                        for run in runs:
                            if run == study_run1:
                                curr_category.append(matching(study_df,run,neg_lurefas_list))

                    else:
                        for run in runs:
                            if run == study_run2:
                                curr_category.append(matching(study_df,run,neg_lurefas_list))
        
            # PostESI_NeuLureFA
            neu_lurefas_list = query_facr_thtm(neu_stim_pd,trials)

            for curr_category in categories:
                if curr_category == PostESI_NeuLureFA:
                    if study_df['Randomization'][0] == "ESIthenmath":
                        for run in runs:
                            if run == study_run1:
                                curr_category.append(matching(study_df,run,neu_lurefas_list))
                    else:
                        for run in runs:
                            if run == study_run2:
                                curr_category.append(matching(study_df,run,neu_lurefas_list))

            # Postmath_NegLureFA
            for curr_category in categories:
                if curr_category == Postmath_NegLureFA:
                    if study_df['Randomization'][0] == "ESIthenmath":
                        for run in runs:
                            if run == study_run2:
                                curr_category.append(matching(study_df,run,neg_lurefas_list))

                    else:
                        for run in runs:
                            if run == study_run1:
                                curr_category.append(matching(study_df,run,neg_lurefas_list))
            
            # Postmath_NeuLureFA
            for curr_category in categories:
                if curr_category == PostESI_NeuLureFA:
                    if study_df['Randomization'][0] == "ESIthenmath":
                        for run in runs:
                            if run == study_run2:
                                curr_category.append(matching(study_df,run,neu_lurefas_list))
                    else:
                        for run in runs:
                            if run == study_run1:
                                curr_category.append(matching(study_df,run,neu_lurefas_list))

