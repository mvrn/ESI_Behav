#%%
'''IMPORTING TOOLS'''
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

#%%
'''ESI VS. IMP ANALYSIS'''
#%%
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
'''PRINTING DATAFRAME (INCL. CREATING CSV)'''
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
'''POST ESI VS. IMP LURE FA, LURE CR COUNTS (VALENCE COLLAPSED)'''
#%%
behav_data_df['PostESI_LureFA_Count'] = behav_data_df['PostESI_NegLureFA_Count'] + behav_data_df['PostESI_NeuLureFA_Count']

behav_data_df['PostIMP_LureFA_Count'] = behav_data_df['PostIMP_NegLureFA_Count'] + behav_data_df['PostIMP_NeuLureFA_Count']


behav_data_df['PostESI_LureCR_Count'] = behav_data_df['PostESI_NegLureCR_Count'] + behav_data_df['PostESI_NeuLureCR_Count']

behav_data_df['PostIMP_LureCR_Count'] = behav_data_df['PostIMP_NegLureCR_Count'] + behav_data_df['PostIMP_NeuLureCR_Count']

#%%
'''POST ESI VS. IMP TARG HIT/MISS COUNT (VALENCE COLLAPSED)'''
#%%
behav_data_df['PostESI_TargHit_Count'] = behav_data_df['PostESI_NegTargHit_Count'] + behav_data_df['PostESI_NeuTargHit_Count']

behav_data_df['PostIMP_TargHit_Count'] = behav_data_df['PostIMP_NegTargHit_Count'] + behav_data_df['PostIMP_NeuTargHit_Count']


behav_data_df['PostESI_TargMiss_Count'] = behav_data_df['PostESI_NegTargMiss_Count'] + behav_data_df['PostESI_NeuTargMiss_Count']

behav_data_df['PostIMP_TargMiss_Count'] = behav_data_df['PostIMP_NegTargMiss_Count'] + behav_data_df['PostIMP_NeuTargMiss_Count']

#%%
'''POST ESI VS. IMP FOILS COUNT (VALENCE COLLAPSED)'''
#%%
behav_data_df['FoilFA_Count'] = behav_data_df['NegFoilFA_Count'] + behav_data_df['NeuFoilFA_Count']

behav_data_df['FoilCR_Count'] = behav_data_df['NegFoilCR_Count'] + behav_data_df['NeuFoilCR_Count']

behav_data_df

#%%
'''OFFICIAL POST ESI VS. IMP 
LURE FAs, LURE CRs, HITS, MISSES,
FOIL FAs, FOIL CRs, LGI, LDI
(VALENCE COLLAPSED)'''
#%%

# LURE FAs AND LURE CRs
behav_data_df['PostESI_LureFA'] = behav_data_df['PostESI_LureFA_Count']/(behav_data_df['PostESI_LureFA_Count'] + behav_data_df['PostESI_LureCR_Count'])

behav_data_df['PostIMP_LureFA'] = behav_data_df['PostIMP_LureFA_Count']/(behav_data_df['PostIMP_LureFA_Count'] + behav_data_df['PostIMP_LureCR_Count'])


behav_data_df['PostESI_LureCR'] = behav_data_df['PostESI_LureCR_Count']/(behav_data_df['PostESI_LureCR_Count'] + behav_data_df['PostESI_LureFA_Count'])

behav_data_df['PostIMP_LureCR'] = behav_data_df['PostIMP_LureCR_Count']/(behav_data_df['PostIMP_LureCR_Count'] + behav_data_df['PostIMP_LureFA_Count'])

# HITS AND MISSES
behav_data_df["PostESI_TargHit"] = behav_data_df["PostESI_TargHit_Count"]/(behav_data_df["PostESI_TargHit_Count"] + behav_data_df["PostESI_TargMiss_Count"])

behav_data_df["PostIMP_TargHit"] = behav_data_df["PostIMP_TargHit_Count"]/(behav_data_df["PostIMP_TargHit_Count"] + behav_data_df["PostIMP_TargMiss_Count"])


behav_data_df["PostESI_TargMiss"] = behav_data_df["PostESI_TargMiss_Count"]/(behav_data_df["PostESI_TargMiss_Count"] + behav_data_df["PostESI_TargHit_Count"])

behav_data_df["PostIMP_TargMiss"] = behav_data_df["PostIMP_TargMiss_Count"]/(behav_data_df["PostIMP_TargMiss_Count"] + behav_data_df["PostIMP_TargHit_Count"])

# FOILS
behav_data_df['FoilFA'] = behav_data_df['FoilFA_Count']/(behav_data_df['FoilFA_Count'] + behav_data_df['FoilCR_Count'])

behav_data_df['FoilCR'] = behav_data_df['FoilCR_Count']/(behav_data_df['FoilCR_Count'] + behav_data_df['FoilFA_Count'])

# LGI
behav_data_df['PostESI_LGI'] = behav_data_df['PostESI_LureFA'] - behav_data_df['FoilFA'] 

behav_data_df['PostIMP_LGI'] = behav_data_df['PostIMP_LureFA'] - behav_data_df['FoilFA'] 

# LDI
behav_data_df['PostESI_LDI'] = behav_data_df['PostESI_LureCR'] - behav_data_df['PostESI_TargMiss'] 

behav_data_df['PostIMP_LDI'] = behav_data_df['PostIMP_LureCR'] - behav_data_df['PostIMP_TargMiss'] 


#%%
'''OFFICIAL POST ESI VS. IMP 
LURE FAs, LURE CRs, HITS, MISSES,
FOIL FAs, FOIL CRs, LGI, LDI
(FOR EACH VALENCE)'''
#%%
# NEGATIVE LURE FA 
behav_data_df['PostESI_NegLureFA'] = behav_data_df['PostESI_NegLureFA_Count']/(behav_data_df['PostESI_NegLureFA_Count'] + behav_data_df['PostESI_NegLureCR_Count'])

behav_data_df['PostIMP_NegLureFA'] = behav_data_df['PostIMP_NegLureFA_Count']/(behav_data_df['PostIMP_NegLureFA_Count'] + behav_data_df['PostIMP_NegLureCR_Count'])

# NEUTRAL LURE FA 
behav_data_df['PostESI_NeuLureFA'] = behav_data_df['PostESI_NeuLureFA_Count']/(behav_data_df['PostESI_NeuLureFA_Count'] + behav_data_df['PostESI_NeuLureCR_Count'])

behav_data_df['PostIMP_NeuLureFA'] = behav_data_df['PostIMP_NeuLureFA_Count']/(behav_data_df['PostIMP_NeuLureFA_Count'] + behav_data_df['PostIMP_NeuLureCR_Count'])

# NEGATIVE LURE CR 
behav_data_df['PostESI_NegLureCR'] = behav_data_df['PostESI_NegLureCR_Count']/(behav_data_df['PostESI_NegLureCR_Count'] + behav_data_df['PostESI_NegLureFA_Count'])

behav_data_df['PostIMP_NegLureCR'] = behav_data_df['PostIMP_NegLureCR_Count']/(behav_data_df['PostIMP_NegLureCR_Count'] + behav_data_df['PostIMP_NegLureFA_Count'])

# NEUTRAL LURE CR 
behav_data_df['PostESI_NeuLureCR'] = behav_data_df['PostESI_NeuLureCR_Count']/(behav_data_df['PostESI_NeuLureCR_Count'] + behav_data_df['PostESI_NeuLureFA_Count'])

behav_data_df['PostIMP_NeuLureCR'] = behav_data_df['PostIMP_NeuLureCR_Count']/(behav_data_df['PostIMP_NeuLureCR_Count'] + behav_data_df['PostIMP_NeuLureFA_Count'])

# TARGET HITS
behav_data_df["PostESI_NegTargHit"] = behav_data_df["PostESI_NegTargHit_Count"]/(behav_data_df["PostESI_NegTargHit_Count"] + behav_data_df["PostESI_NegTargMiss_Count"])

behav_data_df["PostIMP_NegTargHit"] = behav_data_df["PostIMP_NegTargHit_Count"]/(behav_data_df["PostIMP_NegTargHit_Count"] + behav_data_df["PostIMP_NegTargMiss_Count"])

behav_data_df["PostESI_NeuTargHit"] = behav_data_df["PostESI_NeuTargHit_Count"]/(behav_data_df["PostESI_NeuTargHit_Count"] + behav_data_df["PostESI_NeuTargMiss_Count"])

behav_data_df["PostIMP_NeuTargHit"] = behav_data_df["PostIMP_NeuTargHit_Count"]/(behav_data_df["PostIMP_NeuTargHit_Count"] + behav_data_df["PostIMP_NeuTargMiss_Count"])

# TARGET MISSES

behav_data_df["PostESI_NegTargMiss"] = behav_data_df["PostESI_NegTargMiss_Count"]/(behav_data_df["PostESI_NegTargMiss_Count"] + behav_data_df["PostESI_NegTargHit_Count"])

behav_data_df["PostIMP_NegTargMiss"] = behav_data_df["PostIMP_NegTargMiss_Count"]/(behav_data_df["PostIMP_NegTargMiss_Count"] + behav_data_df["PostIMP_NegTargHit_Count"])

behav_data_df["PostESI_NeuTargMiss"] = behav_data_df["PostESI_NeuTargMiss_Count"]/(behav_data_df["PostESI_NeuTargMiss_Count"] + behav_data_df["PostESI_NeuTargHit_Count"])

behav_data_df["PostIMP_NeuTargMiss"] = behav_data_df["PostIMP_NeuTargMiss_Count"]/(behav_data_df["PostIMP_NeuTargMiss_Count"] + behav_data_df["PostIMP_NeuTargHit_Count"])

# FOILS
behav_data_df['NegFoilFA'] = behav_data_df['NegFoilFA_Count']/(behav_data_df['NegFoilFA_Count'] + behav_data_df['NegFoilCR_Count'])

behav_data_df['NeuFoilFA'] = behav_data_df['NeuFoilFA_Count']/(behav_data_df['NeuFoilFA_Count'] + behav_data_df['NeuFoilCR_Count'])

# LGI
behav_data_df['PostESI_NegativeLGI'] = behav_data_df['PostESI_NegLureFA'] - behav_data_df['NegFoilFA'] 

behav_data_df['PostIMP_NegativeLGI'] = behav_data_df['PostIMP_NegLureFA'] - behav_data_df['NegFoilFA'] 

behav_data_df['PostESI_NeutralLGI'] = behav_data_df['PostESI_NeuLureFA'] - behav_data_df['NeuFoilFA'] 

behav_data_df['PostIMP_NeutralLGI'] = behav_data_df['PostIMP_NeuLureFA'] - behav_data_df['NeuFoilFA'] 

# LDI
behav_data_df['PostESI_NegativeLDI'] = behav_data_df['PostESI_NegLureCR'] - behav_data_df['PostESI_NegTargMiss'] 

behav_data_df['PostIMP_NegativeLDI'] = behav_data_df['PostIMP_NegLureCR'] - behav_data_df['PostIMP_NegTargMiss'] 

behav_data_df['PostESI_NeutralLDI'] = behav_data_df['PostESI_NeuLureCR'] - behav_data_df['PostESI_NeuTargMiss'] 

behav_data_df['PostIMP_NeutralLDI'] = behav_data_df['PostIMP_NeuLureCR'] - behav_data_df['PostIMP_NeuTargMiss'] 

#%%
'''HRs, FAR, 1/2HRs, 1/2FARs, DPrime
FOR EACH VALENCE <<< NEEDS WORK'''
#%%
# HIT RATES
behav_data_df['PostESI_HRNeg'] = float(len(behav_data_df["PostESI_NegTargHit_Count"]))/(len(behav_data_df["PostESI_NegTargHit_Count"]) + len(behav_data_df["PostESI_NegTargMiss_Count"]))

behav_data_df['PostESI_HRNeu'] = float(len(behav_data_df["PostESI_NeuTargHit_Count"]))/(len(behav_data_df["PostESI_NeuTargHit_Count"]) + len(behav_data_df["PostESI_NeuTargMiss_Count"]))

behav_data_df['PostIMP_HRNeg'] = float(len(behav_data_df["PostIMP_NegTargHit_Count"]))/(len(behav_data_df["PostIMP_NegTargHit_Count"]) + len(behav_data_df["PostIMP_NegTargMiss_Count"]))

behav_data_df['PostIMP_HRNeu'] = float(len(behav_data_df["PostIMP_NeuTargHit_Count"]))/(len(behav_data_df["PostIMP_NeuTargHit_Count"]) + len(behav_data_df["PostIMP_NeuTargMiss_Count"]))

# FA RATE
behav_data_df['PostESI_FARNeg'] = float(len(behav_data_df["NegFoilFA_Count"]) + len(behav_data_df["PostESI_NegLureFA_Count"]))/ (len(behav_data_df["NegFoilFA_Count"]) + len(behav_data_df["NegFoilCR_Count"]) +
                                                                                                    len(behav_data_df["PostESI_NegLureFA_Count"]) + len(behav_data_df["PostESI_NegLureCR_Count"]))

behav_data_df['PostESI_FARNeu'] = float(len(behav_data_df["NeuFoilFA_Count"]) + len(behav_data_df["PostESI_NeuLureFA_Count"]))/ (len(behav_data_df["NeuFoilFA_Count"]) + len(behav_data_df["NeuFoilCR_Count"]) +
                                                                                                    len(behav_data_df["PostESI_NeuLureFA_Count"]) + len(behav_data_df["PostESI_NeuLureCR_Count"]))

behav_data_df['PostIMP_FARNeg'] = float(len(behav_data_df["NegFoilFA_Count"]) + len(behav_data_df["PostIMP_NegLureFA_Count"]))/ (len(behav_data_df["NegFoilFA_Count"]) + len(behav_data_df["NegFoilCR_Count"]) +
                                                                                                    len(behav_data_df["PostIMP_NegLureFA_Count"]) + len(behav_data_df["PostIMP_NegLureCR_Count"]))

behav_data_df['PostIMP_FARNeu'] = float(len(behav_data_df["NeuFoilFA_Count"]) + len(behav_data_df["PostIMP_NeuLureFA_Count"]))/ (len(behav_data_df["NeuFoilFA_Count"]) + len(behav_data_df["NeuFoilCR_Count"]) +
                                                                                                    len(behav_data_df["PostIMP_NeuLureFA_Count"]) + len(behav_data_df["PostIMP_NeuLureCR_Count"]))

# HALF HR
behav_data_df['Half_PostESI_HRNeg'] = 0.5/(len(behav_data_df["PostESI_NegTargHit_Count"])+len(behav_data_df["PostESI_NegTargMiss_Count"]))

behav_data_df['Half_PostESI_HRNeu'] = 0.5/(len(behav_data_df["PostESI_NeuTargHit_Count"])+len(behav_data_df["PostESI_NeuTargMiss_Count"]))

behav_data_df['Half_PostIMP_HRNeg'] = 0.5/(len(behav_data_df["PostIMP_NegTargHit_Count"])+len(behav_data_df["PostIMP_NegTargMiss_Count"]))

behav_data_df['Half_PostIMP_HRNeu'] = 0.5/(len(behav_data_df["PostIMP_NeuTargHit_Count"])+len(behav_data_df["PostIMP_NeuTargMiss_Count"]))

# HALF FAR
behav_data_df['Half_PostESI_FARNeg'] = 0.5/(len(behav_data_df["NegFoilFA_Count"]) + len(behav_data_df["NegFoilCR_Count"]) +
                        len(behav_data_df["PostESI_NegLureFA_Count"]) + len(behav_data_df["PostESI_NegLureCR_Count"]))

behav_data_df['Half_PostIMP_FARNeg'] = 0.5/(len(behav_data_df["NegFoilFA_Count"]) + len(behav_data_df["NegFoilCR_Count"]) +
                        len(behav_data_df["PostIMP_NegLureFA_Count"]) + len(behav_data_df["PostIMP_NegLureCR_Count"]))

behav_data_df['Half_PostESI_FARNeu'] = 0.5/(len(behav_data_df["NeuFoilFA_Count"]) + len(behav_data_df["NeuFoilCR_Count"]) +
                        len(behav_data_df["PostESI_NeuLureFA_Count"]) + len(behav_data_df["PostESI_NeuLureCR_Count"]))

behav_data_df['Half_PostIMP_FARNeu'] = 0.5/(len(behav_data_df["NeuFoilFA_Count"]) + len(behav_data_df["NeuFoilCR_Count"]) +
                        len(behav_data_df["PostIMP_NeuLureFA_Count"]) + len(behav_data_df["PostIMP_NeuLureCR_Count"]))

# HALF POST ESI HR
if behav_data_df['PostESI_HRNeg'] == 1: behav_data_df['PostESI_HRNeg'] = 1 - behav_data_df['Half_PostESI_HRNeg']
if behav_data_df['PostESI_HRNeg'] == 0: behav_data_df['PostESI_HRNeg'] = behav_data_df['Half_PostESI_HRNeg']

if behav_data_df['PostESI_HRNeu'] == 1: behav_data_df['PostESI_HRNeu'] = 1 - behav_data_df['Half_PostESI_HRNeu']
if behav_data_df['PostESI_HRNeu'] == 0: behav_data_df['PostESI_HRNeu'] = behav_data_df['Half_PostESI_HRNeu']

# HALF POST IMP HR
if behav_data_df['PostIMP_HRNeg'] == 1: behav_data_df['PostIMP_HRNeg'] = 1 - behav_data_df['Half_PostIMP_HRNeg']
if behav_data_df['PostIMP_HRNeg'] == 0: behav_data_df['PostIMP_HRNeg'] = behav_data_df['Half_PostIMP_HRNeg']

if behav_data_df['PostIMP_HRNeu'] == 1: behav_data_df['PostIMP_HRNeu'] = 1 - behav_data_df['Half_PostIMP_HRNeu']
if behav_data_df['PostIMP_HRNeu'] == 0: behav_data_df['PostIMP_HRNeu'] = behav_data_df['Half_PostIMP_HRNeu']

# HALF POST ESI FAR
if behav_data_df['PostESI_FARNeg'] == 1: behav_data_df['PostESI_FARNeg'] = 1 - behav_data_df['Half_PostESI_FARNeg']
if behav_data_df['PostESI_FARNeg'] == 0: behav_data_df['PostESI_FARNeg'] = behav_data_df['Half_PostESI_FARNeg']

if behav_data_df['PostESI_FARNeu'] == 1: behav_data_df['PostESI_FARNeu'] = 1 - behav_data_df['Half_PostESI_FARNeu']
if behav_data_df['PostESI_FARNeu'] == 0: behav_data_df['PostESI_FARNeu'] = behav_data_df['Half_PostESI_FARNeu']

# HALF POST IMP FAR
if behav_data_df['PostIMP_FARNeg'] == 1: behav_data_df['PostIMP_FARNeg'] = 1 - behav_data_df['Half_PostIMP_FARNeg']
if behav_data_df['PostIMP_FARNeg'] == 0: behav_data_df['PostIMP_FARNeg'] = behav_data_df['Half_PostIMP_FARNeg']

if behav_data_df['PostIMP_FARNeu'] == 1: behav_data_df['PostIMP_FARNeu'] = 1 - behav_data_df['Half_PostIMP_FARNeu']
if behav_data_df['PostIMP_FARNeu'] == 0: behav_data_df['PostIMP_FARNeu'] = behav_data_df['Half_PostIMP_FARNeu']


# dPRIME

behav_data_df['PostESI_dPrimeNeg'] = (norm.ppf(behav_data_df['PostESI_HRNeg']) - norm.ppf(behav_data_df['PostESI_FARNeg']))

behav_data_df['PostESI_dPrimeNeu'] = (norm.ppf(behav_data_df['PostESI_HRNeu']) - norm.ppf(behav_data_df['PostESI_FARNeu']))

behav_data_df['PostIMP_dPrimeNeg'] = (norm.ppf(behav_data_df['PostIMP_HRNeg']) - norm.ppf(behav_data_df['PostIMP_FARNeg']))

behav_data_df['PostIMP_dPrimeNeu'] = (norm.ppf(behav_data_df['PostIMP_HRNeu']) - norm.ppf(behav_data_df['PostIMP_FARNeu']))

behav_data_df


#%%
'''WINSORIZING LGIs, LDIs (WITH AND WITHOUT VALENCE)'''
#%%
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
'''ADDING SEQUENCE MEMORY 
**NOTE: MAKE SURE TO CHANGE 
INDICES FOR SROPPING SUBS IF
ADDING SEQ MEMO'''
#%%
# Due to issues with audio recordings
# and the randomization of ESI vs. IMP 
# subjects, sample size for this analysis
# would be 66.

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

# Concatenate both dataframes
behav_data_df = pd.concat([behav_data_df, esi_details_df], axis=1)

# drop duplicate Subject columns
behav_data_df = behav_data_df.loc[:,~behav_data_df.columns.duplicated()].copy()
behav_data_df

#%%
'''RECOGNITION MEMORY
PERFORMANCE'''
#%%
behav_data_df["Neg_Recog_Mem"] = behav_data_df["PostESI_NegTargHit"] - behav_data_df['NegFoilFA']
behav_data_df["Neu_Recog_Mem"] = behav_data_df["PostESI_NeuTargHit"] - behav_data_df['NeuFoilFA']

#%%
'''DROPPING SUBJECTS DUE TO 
POOR PERFORMANCE'''
#%%
# Dropping subjects 165 and 246 due to poor memory recognition (less than 0.5)
# NOTE: you need to change indices to 52 and 75 if not including seq memo
# NOTE: if including seq memo then indices change to 42 and 65
behav_data_df = behav_data_df.drop([52, 75])

behav_data_df.reset_index(drop=True, inplace=True)

behav_data_df


#%%

"""""""""""""""""""""""""""""""""
MELTING NEG VS. NEU THs 
FOR POST ESI VS. POST IMP
COMPARISON 
(NOT INCLUDING SEQ. MEMO.)
"""""""""""""""""""""""""""""""""
#%%
esi_melt = pd.melt(behav_data_df, id_vars=['Subject'], value_vars=[
    'PostESI_NegTargHit',
    'PostESI_NeuTargHit',

    'PostIMP_NegTargHit',
    'PostIMP_NeuTargHit'
    ])

esi_melt.columns = ['Subject', 'Response', 'Value']

valence = []
for j, row in esi_melt.iterrows():
    if 'Neg' in row['Response']:
        valence.append('Neg')
    if 'Neu' in row['Response']:
        valence.append('Neu')
esi_melt['Valence'] = valence

randomization = []
for j, row in esi_melt.iterrows():
    if 'ESI' in row['Response']:
        randomization.append('ESI')
    if 'IMP' in row['Response']:
        randomization.append('IMP')
esi_melt['Randomization'] = randomization


esi_melt = esi_melt[[
    "Subject", "Response", "Valence", "Randomization", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt
#%%
"""""""""""""""""""""""""""""""""
GLM ON NEG VS. NEU THs RESULTS
FOR POST ESI VS. POST IMP
COMPARISON -- INCL FIG
(NOT INCLUDING SEQ. MEMO.)
"""""""""""""""""""""""""""""""""
#%%
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.glm(
    "Value ~ Valence*Randomization",
    esi_melt, groups=esi_melt["Subject"])
mdf = md.fit()
print(mdf.summary())

import statsmodels.api as sm
from scipy import stats

my_pal = {
    'PostESI_NegTargHit': "mediumvioletred", 
    'PostESI_NeuTargHit': "darkgoldenrod", 

    'PostIMP_NegTargHit': "mediumvioletred",
    'PostIMP_NeuTargHit': "darkgoldenrod"
    }
axes = sns.swarmplot(
    size=5, 
    palette=my_pal, 
    linewidth=1.7, 
    data=behav_data_df[[
    'PostESI_NegTargHit',
    'PostESI_NeuTargHit',

    'PostIMP_NegTargHit',
    'PostIMP_NeuTargHit'
        ]])
sns.boxplot(
    data=behav_data_df[[
    'PostESI_NegTargHit',
    'PostESI_NeuTargHit',

    'PostIMP_NegTargHit',
    'PostIMP_NeuTargHit'
        ]], 
        palette=my_pal, 
        linewidth = 2, 
        width = 0.8, 
        ax=axes
        )

axes.set_ylabel(('Target Hits'), 
                fontsize=15)

axes.tick_params(
    axis='y', 
    labelsize=13, 
    width=2
    ) 

axes.tick_params(
    axis='x', 
    labelsize=15, 
    width=2
    ) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Post-ESI \n Negative'
labels[1] = 'Post-ESI \n Neutral'
labels[2] = 'Post-IMP \n Negative'
labels[3] = 'Post-IMP \n Neutral'

axes.set_xticklabels(labels)

for location in [
    'left', 
    'bottom'
    ]:
    axes.spines[location].set_linewidth(2)

for location in [
    'right', 
    'top', 
    ]:
    axes.spines[location].set_linewidth(0)


#%%
"""
ESI vs IMP CR
"""
'''
Shapiro for Post ESI Negative vs. Neutral
'''
from scipy import stats
postesi_neglurecr = behav_data_df["PostESI_NegLureCR_Count"]
postesi_neulurecr = behav_data_df["PostESI_NeuLureCR_Count"]

print(postesi_neglurecr.mean())
print(postesi_neulurecr.mean())

print('Shapiro for Post ESI NEG CR:', stats.shapiro(postesi_neglurecr))
print('Shapiro for Post ESI NEU CR:', stats.shapiro(postesi_neulurecr))


'''
Plotting Post ESI vs. Post IMP CR
'''
from scipy import stats
import seaborn as sns

test_data = behav_data_df.dropna(how='any', subset=['PostESI_NegLureCR_Count', 'PostESI_NeuLureCR_Count'])
print(stats.ttest_rel(test_data['PostESI_NegLureCR_Count'], test_data['PostESI_NeuLureCR_Count']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostESI_NegLureCR_Count": "mediumvioletred", "PostESI_NeuLureCR_Count": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostESI_NegLureCR_Count', 'PostESI_NeuLureCR_Count']]) 
sns.boxplot(data=test_data[['PostESI_NegLureCR_Count', 'PostESI_NeuLureCR_Count']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Correct Rejections'), fontsize=17)
axes.tick_params(axis='y', labelsize=13, width=2)  

axes.set_xlabel(('Condition'), fontsize=17)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Neg CR'
labels[1] = 'Neu CR'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)


#%%
    """
ESI vs IMP CR
"""
'''
Shapiro for Post IMP Negative vs. Neutral
'''
from scipy import stats
test_postesi_ldi = behav_data_df["PostIMP_NegLureCR_Count"]
test_postimp_ldi = behav_data_df["PostIMP_NeuLureCR_Count"]

print(test_postesi_ldi.mean())
print(test_postimp_ldi.mean())

print('Shapiro for Post IMP CR:', stats.shapiro(test_postesi_ldi))
print('Shapiro for Post IMP CR:', stats.shapiro(test_postimp_ldi))


'''
Plotting Post IMP CR
'''
from scipy import stats
import seaborn as sns

test_data = behav_data_df.dropna(how='any', subset=['PostIMP_NegLureCR_Count', 'PostIMP_NeuLureCR_Count'])
print(stats.ttest_rel(test_data['PostIMP_NegLureCR_Count'], test_data['PostIMP_NeuLureCR_Count']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostIMP_NegLureCR_Count": "mediumvioletred", "PostIMP_NeuLureCR_Count": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostIMP_NegLureCR_Count', 'PostIMP_NeuLureCR_Count']]) 
sns.boxplot(data=test_data[['PostIMP_NegLureCR_Count', 'PostIMP_NeuLureCR_Count']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Correct Rejections'), fontsize=17)
axes.tick_params(axis='y', labelsize=13, width=2)  

axes.set_xlabel(('Condition'), fontsize=17)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Neg CR'
labels[1] = 'Neu CR'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']: axes.spines[location].set_linewidth(2)

#%%

"""""""""""""""""""""""""""""""""
Neg vs Neu CR RESULTS 
(NOT INCLUDING SEQ. MEMO.)
"""""""""""""""""""""""""""""""""

esi_melt = pd.melt(behav_data_df, id_vars=['Subject', 'Seq_Memo'], value_vars=[
    'PostESI_NegLureCR_Count',
    'PostESI_NeuLureCR_Count',

    'PostIMP_NegLureCR_Count',
    'PostIMP_NeuLureCR_Count'
    ])

esi_melt.columns = ['Subject', 'Seq_Memo', 'Response', 'Value']

valence = []
for j, row in esi_melt.iterrows():
    if 'Neg' in row['Response']:
        valence.append('Neg')
    if 'Neu' in row['Response']:
        valence.append('Neu')
esi_melt['Valence'] = valence

randomization = []
for j, row in esi_melt.iterrows():
    if 'ESI' in row['Response']:
        randomization.append('ESI')
    if 'IMP' in row['Response']:
        randomization.append('IMP')
esi_melt['Randomization'] = randomization


esi_melt = esi_melt[[
    "Subject", "Response", "Valence", "Randomization", "Value", "Seq_Memo"]]
esi_melt.dropna(inplace = True)

esi_melt

#%%

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.glm(
    "Value ~ Valence*Randomization*Seq_Memo",
    esi_melt, groups=esi_melt["Subject"])
mdf = md.fit()
print(mdf.summary())

# Adding sequence memory!
import seaborn as sns
#row = one graph on top of the other
#col = one graph next to the other

#truncate = to prevent thew graph to end abruptly on the last data point 
    #and thus let it continue

palette = ['mediumvioletred',  
                    'darkgoldenrod']

sns.lmplot(data=esi_melt, x='Seq_Memo', y='Value', hue='Valence', col='Randomization', palette = palette, truncate=False)


#%%

import statsmodels.api as sm
from scipy import stats

my_pal = {
    'PostESI_NegLureCR_Count': "mediumvioletred", 
    'PostESI_NeuLureCR_Count': "darkgoldenrod", 

    'PostIMP_NegLureCR_Count': "mediumvioletred",
    'PostIMP_NeuLureCR_Count': "darkgoldenrod"
    }
axes = sns.swarmplot(
    size=5, 
    palette=my_pal, 
    linewidth=1.7, 
    data=behav_data_df[[
    'PostESI_NegLureCR_Count',
    'PostESI_NeuLureCR_Count',

    'PostIMP_NegLureCR_Count',
    'PostIMP_NeuLureCR_Count'
        ]])
sns.boxplot(
    data=behav_data_df[[
    'PostESI_NegLureCR_Count',
    'PostESI_NeuLureCR_Count',

    'PostIMP_NegLureCR_Count',
    'PostIMP_NeuLureCR_Count'
        ]], 
        palette=my_pal, 
        linewidth = 2, 
        width = 0.8, 
        ax=axes
        )

axes.set_ylabel(('Correct Rejections'), 
                fontsize=15)

axes.tick_params(
    axis='y', 
    labelsize=13, 
    width=2
    ) 

axes.tick_params(
    axis='x', 
    labelsize=15, 
    width=2
    ) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Post-ESI \n Negative'
labels[1] = 'Post-ESI \n Neutral'
labels[2] = 'Post-IMP \n Negative'
labels[3] = 'Post-IMP \n Neutral'

axes.set_xticklabels(labels)

for location in [
    'left', 
    'bottom'
    ]:
    axes.spines[location].set_linewidth(2)

for location in [
    'right', 
    'top', 
    ]:
    axes.spines[location].set_linewidth(0)

#%%
    
"""
ESI vs IMP FA
"""
'''
Shapiro for Post ESI Negative vs. Neutral
'''
from scipy import stats
test_postesi_ldi = behav_data_df["PostESI_NegLureFA_Count"]
test_postimp_ldi = behav_data_df["PostESI_NeuLureFA_Count"]

print(test_postesi_ldi.mean())
print(test_postimp_ldi.mean())

print('Shapiro for Post ESI Neg FA:', stats.shapiro(test_postesi_ldi))
print('Shapiro for Post ESI Neu FA:', stats.shapiro(test_postimp_ldi))


'''
Plotting Post ESI vs. Post IMP FA
'''
from scipy import stats
import seaborn as sns

test_data = behav_data_df.dropna(how='any', subset=['PostESI_NegLureFA_Count', 'PostESI_NeuLureFA_Count'])
print(stats.ttest_rel(test_data['PostESI_NegLureFA_Count'], test_data['PostESI_NeuLureFA_Count']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostESI_NegLureFA_Count": "mediumvioletred", "PostESI_NeuLureFA_Count": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostESI_NegLureFA_Count', 'PostESI_NeuLureFA_Count']]) 
sns.boxplot(data=test_data[['PostESI_NegLureFA_Count', 'PostESI_NeuLureFA_Count']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('False Alarms'), fontsize=17)
axes.tick_params(axis='y', labelsize=13, width=2)  

axes.set_xlabel(('Condition'), fontsize=17)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Neg FA'
labels[1] = 'Neu FA'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)

plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_ESI_FA.png', bbox_inches='tight',dpi=1200)


#%%
"""
ESI vs IMP FA
"""
'''
Shapiro for Post IMP Negative vs. Neutral
'''
from scipy import stats
test_postesi_ldi = behav_data_df["PostIMP_NegLureFA_Count"]
test_postimp_ldi = behav_data_df["PostIMP_NeuLureFA_Count"]

print(test_postesi_ldi.mean())
print(test_postimp_ldi.mean())

print('Shapiro for Post IMP Neg FA:', stats.shapiro(test_postesi_ldi))
print('Shapiro for Post IMP Neu FA:', stats.shapiro(test_postimp_ldi))


'''
Plotting Post IMP FA
'''
from scipy import stats
import seaborn as sns

test_data = behav_data_df.dropna(how='any', subset=['PostIMP_NegLureFA_Count', 'PostIMP_NeuLureFA_Count'])
print(stats.ttest_rel(test_data['PostIMP_NegLureFA_Count'], test_data['PostIMP_NeuLureFA_Count']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostIMP_NegLureFA_Count": "mediumvioletred", "PostIMP_NeuLureFA_Count": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostIMP_NegLureFA_Count', 'PostIMP_NeuLureFA_Count']]) 
sns.boxplot(data=test_data[['PostIMP_NegLureFA_Count', 'PostIMP_NeuLureFA_Count']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('False Alarms'), fontsize=17)
axes.tick_params(axis='y', labelsize=13, width=2)  

axes.set_xlabel(('Condition'), fontsize=17)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Neg FA'
labels[1] = 'Neu FA'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']: axes.spines[location].set_linewidth(2)

plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_IMP_FA.png', bbox_inches='tight',dpi=1200)


#%%

"""""""""""""""""""""""""""""""""
Neg vs Neu FA RESULTS 
(NOT INCLUDING SEQ. MEMO.)
"""""""""""""""""""""""""""""""""

esi_melt = pd.melt(behav_data_df, id_vars=['Subject', 'Seq_Memo'], value_vars=[
    'PostESI_NegLureFA',
    'PostESI_NeuLureFA',

    'PostIMP_NegLureFA',
    'PostIMP_NeuLureFA'
    ])

esi_melt.columns = ['Subject', 'Seq_Memo', 'Response', 'Value']

valence = []
for j, row in esi_melt.iterrows():
    if 'Neg' in row['Response']:
        valence.append('Neg')
    if 'Neu' in row['Response']:
        valence.append('Neu')
esi_melt['Valence'] = valence

randomization = []
for j, row in esi_melt.iterrows():
    if 'ESI' in row['Response']:
        randomization.append('ESI')
    if 'IMP' in row['Response']:
        randomization.append('IMP')
esi_melt['Randomization'] = randomization


esi_melt = esi_melt[[
    "Subject", "Seq_Memo", "Response", "Valence", "Randomization", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.glm(
    "Value ~ Valence*Randomization",
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

sns.lmplot(data=esi_melt, x='Seq_Memo', y='Value', hue='Valence', col='Randomization', palette = palette, truncate=False)

#%%

import statsmodels.api as sm
from scipy import stats

my_pal = {
    'PostESI_NegLureFA': "mediumvioletred", 
    'PostESI_NeuLureFA': "darkgoldenrod", 

    'PostIMP_NegLureFA': "mediumvioletred",
    'PostIMP_NeuLureFA': "darkgoldenrod"
    }
axes = sns.swarmplot(
    size=5, 
    palette=my_pal, 
    linewidth=1.7, 
    data=behav_data_df[[
    'PostESI_NegLureFA',
    'PostESI_NeuLureFA',

    'PostIMP_NegLureFA',
    'PostIMP_NeuLureFA'
        ]])
sns.boxplot(
    data=behav_data_df[[
    'PostESI_NegLureFA',
    'PostESI_NeuLureFA',

    'PostIMP_NegLureFA',
    'PostIMP_NeuLureFA'
        ]], 
        palette=my_pal, 
        linewidth = 2, 
        width = 0.8, 
        ax=axes
        )

axes.set_ylabel(('False Alarms'), 
                fontsize=15)

axes.tick_params(
    axis='y', 
    labelsize=13, 
    width=2
    ) 

axes.tick_params(
    axis='x', 
    labelsize=15, 
    width=2
    ) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Post-ESI \n Negative'
labels[1] = 'Post-ESI \n Neutral'
labels[2] = 'Post-IMP \n Negative'
labels[3] = 'Post-IMP \n Neutral'

axes.set_xticklabels(labels)

for location in [
    'left', 
    'bottom'
    ]:
    axes.spines[location].set_linewidth(2)

for location in [
    'right', 
    'top', 
    ]:
    axes.spines[location].set_linewidth(0)

#%%

"""""""""""""""""""""""""""""""""
Neg vs Neu TH RESULTS 
(NOT INCLUDING SEQ. MEMO.)
"""""""""""""""""""""""""""""""""

esi_melt = pd.melt(behav_data_df, id_vars=['Subject'], value_vars=[
    'PostESI_NegTargHit',
    'PostESI_NeuTargHit',

    'PostIMP_NegTargHit',
    'PostIMP_NeuTargHit'
    ])

esi_melt.columns = ['Subject', 'Response', 'Value']

valence = []
for j, row in esi_melt.iterrows():
    if 'Neg' in row['Response']:
        valence.append('Neg')
    if 'Neu' in row['Response']:
        valence.append('Neu')
esi_melt['Valence'] = valence

randomization = []
for j, row in esi_melt.iterrows():
    if 'ESI' in row['Response']:
        randomization.append('ESI')
    if 'IMP' in row['Response']:
        randomization.append('IMP')
esi_melt['Randomization'] = randomization


esi_melt = esi_melt[[
    "Subject", "Response", "Valence", "Randomization", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.glm(
    "Value ~ Valence*Randomization",
    esi_melt, groups=esi_melt["Subject"])
mdf = md.fit()
print(mdf.summary())

#%%

import statsmodels.api as sm
from scipy import stats

my_pal = {
    'PostESI_NegTargHit': "mediumvioletred", 
    'PostESI_NeuTargHit': "darkgoldenrod", 

    'PostIMP_NegTargHit': "mediumvioletred",
    'PostIMP_NeuTargHit': "darkgoldenrod"
    }
axes = sns.swarmplot(
    size=5, 
    palette=my_pal, 
    linewidth=1.7, 
    data=behav_data_df[[
    'PostESI_NegTargHit',
    'PostESI_NeuTargHit',

    'PostIMP_NegTargHit',
    'PostIMP_NeuTargHit'
        ]])
sns.boxplot(
    data=behav_data_df[[
    'PostESI_NegTargHit',
    'PostESI_NeuTargHit',

    'PostIMP_NegTargHit',
    'PostIMP_NeuTargHit'
        ]], 
        palette=my_pal, 
        linewidth = 2, 
        width = 0.8, 
        ax=axes
        )

axes.set_ylabel(('Target Hits'), 
                fontsize=15)

axes.tick_params(
    axis='y', 
    labelsize=13, 
    width=2
    ) 

axes.tick_params(
    axis='x', 
    labelsize=15, 
    width=2
    ) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Post-ESI \n Negative'
labels[1] = 'Post-ESI \n Neutral'
labels[2] = 'Post-IMP \n Negative'
labels[3] = 'Post-IMP \n Neutral'

axes.set_xticklabels(labels)

for location in [
    'left', 
    'bottom'
    ]:
    axes.spines[location].set_linewidth(2)

for location in [
    'right', 
    'top', 
    ]:
    axes.spines[location].set_linewidth(0)


#%%


"""""""""""""""""""""""""""""""""
Neg vs Neu TM RESULTS 
(NOT INCLUDING SEQ. MEMO.)
"""""""""""""""""""""""""""""""""

esi_melt = pd.melt(behav_data_df, id_vars=['Subject'], value_vars=[
    'PostESI_NegTargMiss',
    'PostESI_NeuTargMiss',

    'PostIMP_NegTargMiss',
    'PostIMP_NeuTargMiss'
    ])

esi_melt.columns = ['Subject', 'Response', 'Value']

valence = []
for j, row in esi_melt.iterrows():
    if 'Neg' in row['Response']:
        valence.append('Neg')
    if 'Neu' in row['Response']:
        valence.append('Neu')
esi_melt['Valence'] = valence

randomization = []
for j, row in esi_melt.iterrows():
    if 'ESI' in row['Response']:
        randomization.append('ESI')
    if 'IMP' in row['Response']:
        randomization.append('IMP')
esi_melt['Randomization'] = randomization


esi_melt = esi_melt[[
    "Subject", "Response", "Valence", "Randomization", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.glm(
    "Value ~ Valence*Randomization",
    esi_melt, groups=esi_melt["Subject"])
mdf = md.fit()
print(mdf.summary())

#%%

import statsmodels.api as sm
from scipy import stats

my_pal = {
    'PostESI_NegTargMiss': "mediumvioletred", 
    'PostESI_NeuTargMiss': "darkgoldenrod", 

    'PostIMP_NegTargMiss': "mediumvioletred",
    'PostIMP_NeuTargMiss': "darkgoldenrod"
    }
axes = sns.swarmplot(
    size=5, 
    palette=my_pal, 
    linewidth=1.7, 
    data=behav_data_df[[
    'PostESI_NegTargMiss',
    'PostESI_NeuTargMiss',

    'PostIMP_NegTargMiss',
    'PostIMP_NeuTargMiss'
        ]])
sns.boxplot(
    data=behav_data_df[[
    'PostESI_NegTargMiss',
    'PostESI_NeuTargMiss',

    'PostIMP_NegTargMiss',
    'PostIMP_NeuTargMiss'
        ]], 
        palette=my_pal, 
        linewidth = 2, 
        width = 0.8, 
        ax=axes
        )

axes.set_ylabel(('Target Miss'), 
                fontsize=15)

axes.tick_params(
    axis='y', 
    labelsize=13, 
    width=2
    ) 

axes.tick_params(
    axis='x', 
    labelsize=15, 
    width=2
    ) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Post-ESI \n Negative'
labels[1] = 'Post-ESI \n Neutral'
labels[2] = 'Post-IMP \n Negative'
labels[3] = 'Post-IMP \n Neutral'

axes.set_xticklabels(labels)

for location in [
    'left', 
    'bottom'
    ]:
    axes.spines[location].set_linewidth(2)

for location in [
    'right', 
    'top', 
    ]:
    axes.spines[location].set_linewidth(0)



#%%
"""
ESI vs IMP LDI
"""
'''
Shapiro for Post ESI Negative vs. Neutral
'''
from scipy import stats
test_postesi_ldi = behav_data_df["PostESI_LDI"]
test_postimp_ldi = behav_data_df["PostIMP_LDI"]

print(test_postesi_ldi.mean())
print(test_postimp_ldi.mean())

print('Shapiro for Post ESI LDI:', stats.shapiro(test_postesi_ldi))
print('Shapiro for Post IMP LDI:', stats.shapiro(test_postimp_ldi))


'''
Plotting Post ESI vs. Post IMP LDI
'''
from scipy import stats
import seaborn as sns

test_data = behav_data_df.dropna(how='any', subset=['PostESI_LDI', 'PostIMP_LDI'])
print(stats.wilcoxon(test_data['PostESI_LDI'], test_data['PostIMP_LDI']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostESI_LDI": "mediumvioletred", "PostIMP_LDI": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostESI_LDI', 'PostIMP_LDI']]) 
sns.boxplot(data=test_data[['PostESI_LDI', 'PostIMP_LDI']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Lure Discrimination Index (LDI)'), fontsize=17)
axes.tick_params(axis='y', labelsize=13, width=2) 

axes.set_xlabel(('Condition'), fontsize=17)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Post-ESI LDI'
labels[1] = 'Post-IMP LDI'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)

plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_ESIvIMP_LDI.png', bbox_inches='tight',dpi=1200)

#%%

"""""""""""""""""""""""""""""""""
Neg vs Neu LDI RESULTS 
(NOT INCLUDING SEQ. MEMO.)
"""""""""""""""""""""""""""""""""

esi_melt = pd.melt(behav_data_df, id_vars=['Subject'], value_vars=[
    'PostESI_NegativeLDI',
    'PostESI_NeutralLDI',

    'PostIMP_NegativeLDI',
    'PostIMP_NeutralLDI'
    ])

esi_melt.columns = ['Subject', 'Response', 'Value']

valence = []
for j, row in esi_melt.iterrows():
    if 'Neg' in row['Response']:
        valence.append('Neg')
    if 'Neu' in row['Response']:
        valence.append('Neu')
esi_melt['Valence'] = valence

randomization = []
for j, row in esi_melt.iterrows():
    if 'ESI' in row['Response']:
        randomization.append('ESI')
    if 'IMP' in row['Response']:
        randomization.append('IMP')
esi_melt['Randomization'] = randomization


esi_melt = esi_melt[[
    "Subject", "Response", "Valence", "Randomization", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.glm(
    "Value ~ Valence*Randomization",
    esi_melt, groups=esi_melt["Subject"])
mdf = md.fit()
print(mdf.summary())


import statsmodels.api as sm
from scipy import stats

my_pal = {
    'PostESI_NegativeLDI': "mediumvioletred", 
    'PostESI_NeutralLDI': "darkgoldenrod", 

    'PostIMP_NegativeLDI': "mediumvioletred",
    'PostIMP_NeutralLDI': "darkgoldenrod"
    }
axes = sns.swarmplot(
    size=7, 
    palette=my_pal, 
    linewidth=1.7, 
    data=behav_data_df[[
    'PostESI_NegativeLDI',
    'PostESI_NeutralLDI',

    'PostIMP_NegativeLDI',
    'PostIMP_NeutralLDI'
        ]])
sns.boxplot(
    data=behav_data_df[[
    'PostESI_NegativeLDI',
    'PostESI_NeutralLDI',

    'PostIMP_NegativeLDI',
    'PostIMP_NeutralLDI'
        ]], 
        palette=my_pal, 
        linewidth = 2, 
        width = 0.8, 
        ax=axes
        )

axes.set_ylabel(('Lure Discrimination Index (LDI)'), 
                fontsize=15)

axes.tick_params(
    axis='y', 
    labelsize=13, 
    width=2
    ) 

axes.tick_params(
    axis='x', 
    labelsize=15, 
    width=2
    ) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Post-ESI \n Negative'
labels[1] = 'Post-ESI \n Neutral'
labels[2] = 'Post-IMP \n Negative'
labels[3] = 'Post-IMP \n Neutral'

axes.set_xticklabels(labels)

for location in [
    'left', 
    'bottom'
    ]:
    axes.spines[location].set_linewidth(2)

for location in [
    'right', 
    'top', 
    ]:
    axes.spines[location].set_linewidth(0)

plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_ESIvIMP_NegvNeu_LDI.png', bbox_inches='tight',dpi=1200)

#%%
"""ESI Neg vs Neu
"""
'''
Shapiro for Post ESI Negative vs. Neutral
'''
from scipy import stats
test_postesi_neg_ldi = behav_data_df["PostESI_NegativeLDI"]
test_postesi_neu_ldi = behav_data_df["PostESI_NeutralLDI"]

print(test_postesi_neg_ldi.mean())
print(test_postesi_neu_ldi.mean())

print('Shapiro for Post ESI LDI:', stats.shapiro(test_postesi_neg_ldi))
print('Shapiro for Post IMP LDI:', stats.shapiro(test_postesi_neu_ldi))


'''
Plotting Post ESI vs. Post IMP LDI based on Valence
'''
from scipy import stats
import seaborn as sns

test_data = behav_data_df.dropna(how='any', subset=['PostESI_NegativeLDI', 'PostESI_NeutralLDI'])
print(stats.wilcoxon(test_data['PostESI_NegativeLDI'], test_data['PostESI_NeutralLDI']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostESI_NegativeLDI": "mediumvioletred", "PostESI_NeutralLDI": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostESI_NegativeLDI', 'PostESI_NeutralLDI']]) 
sns.boxplot(data=test_data[['PostESI_NegativeLDI', 'PostESI_NeutralLDI']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Lure Discrimination Index (LDI)'), fontsize=17)
axes.tick_params(axis='y', labelsize=13, width=2) 

# axes.set_xlabel(('Condition'), fontsize=17)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Post-ESI Negative'
labels[1] = 'Post-ESI Neutral'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)

plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_ESI_NegvNeu_LDI.png', bbox_inches='tight',dpi=1200)

#%%
"""IMP Neg vs. Neu"""
'''
Shapiro for Post ESI Negative vs. Neutral
'''
from scipy import stats
test_postesi_neg_ldi = behav_data_df["PostIMP_NegativeLDI"]
test_postesi_neu_ldi = behav_data_df["PostIMP_NeutralLDI"]

print(test_postesi_neg_ldi.mean())
print(test_postesi_neu_ldi.mean())

print('Shapiro for Post ESI LDI:', stats.shapiro(test_postesi_neg_ldi))
print('Shapiro for Post IMP LDI:', stats.shapiro(test_postesi_neu_ldi))


'''
Plotting Post ESI vs. Post IMP LDI based on Valence
'''
from scipy import stats
import seaborn as sns

test_data = behav_data_df.dropna(how='any', subset=['PostIMP_NegativeLDI', 'PostIMP_NeutralLDI'])
print(stats.wilcoxon(test_data['PostIMP_NegativeLDI'], test_data['PostIMP_NeutralLDI']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostIMP_NegativeLDI": "mediumvioletred", "PostIMP_NeutralLDI": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostIMP_NegativeLDI', 'PostIMP_NeutralLDI']]) 
sns.boxplot(data=test_data[['PostIMP_NegativeLDI', 'PostIMP_NeutralLDI']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Lure Discrimination Index (LDI)'), fontsize=17)
axes.tick_params(axis='y', labelsize=13, width=2) 

# axes.set_xlabel(('Condition'), fontsize=17)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Post-IMP Negative'
labels[1] = 'Post-IMP Neutral'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)

plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_IMP_NegvNeu_LDI.png', bbox_inches='tight',dpi=1200)

#%%

'''
Sequence memory should improve 
memory discrimination by decreasing
negative relative to neutral LGI and
increasing LDI
'''
esi_seq_melt = pd.melt(behav_data_df, id_vars=['Subject', 'Seq_Memo'], value_vars=[
    "PostESI_LGI",
    "PostIMP_LGI"
    ])
esi_seq_melt.columns = ['Subject', 'Seq_Memo', 'Response', 'Value']

condition = []
for j, row in esi_seq_melt.iterrows():
    if 'PostESI' in row['Response']:
        condition.append('PostESI')
    if 'PostIMP' in row['Response']:
        condition.append('PostIMP')
esi_seq_melt['Condition'] = condition

esi_seq_melt = esi_seq_melt[[
    "Subject", "Seq_Memo", "Response", "Condition", "Value"]]
esi_seq_melt.dropna(inplace = True)

esi_seq_melt

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.glm(
    "Value ~ Condition*Seq_Memo",
    esi_seq_melt, groups=esi_seq_melt["Subject"])
mdf = md.fit()
print(mdf.summary())


import seaborn as sns
#row = one graph on top of the other
#col = one graph next to the other

#truncate = to prevent thew graph to end abruptly on the last data point 
    #and thus let it continue


sns.lmplot(
    data=esi_seq_melt, 
    x='Seq_Memo', 
    y='Value', 
    hue='Condition',
    palette=['mediumvioletred',  
                    'darkgoldenrod'],
    truncate=False
    )

plt.ylabel('Lure Generalization Index (LGI)', fontsize=13)
plt.xlabel('Sequence Memory', fontsize=13)


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
    "PostESI_NegativeLDI",
    "PostESI_NeutralLDI",
    "PostIMP_NegativeLDI",
    "PostIMP_NeutralLDI"

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
    if 'ESI' in row['Response']:
        condition.append('ESI')
    if 'IMP' in row['Response']:
        condition.append('IMP')
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

palette = ['mediumvioletred',  
                    'darkgoldenrod']

sns.lmplot(data=esi_seq_melt, x='Seq_Memo', y='Value', hue='Valence', col='Condition', palette = palette, truncate=False)

plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_ESI_SeqMemo_LGI_IMPSubs.png', bbox_inches='tight',dpi=1200)

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

"""""""""""""""""""""""""""""""""""""""
LDI RESULTS (COLLAPSED ACROSS VALENCE)

"""""""""""""""""""""""""""""""""""""""

esi_melt = pd.melt(behav_data_df, id_vars=['Subject'], value_vars=[
    'PostESI_LDI',
    'PostESI_LGI'
    ])

esi_melt.columns = ['Subject', 'Response', 'Value']

condition = []
for j, row in esi_melt.iterrows():
    if 'LDI' in row['Response']:
        condition.append('LDI')
    if 'LGI' in row['Response']:
        condition.append('LGI')
esi_melt['Condition'] = condition

esi_melt = esi_melt[[
    "Subject", "Response", "Condition", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.glm(
    "Value ~ Condition",
    esi_melt, groups=esi_melt["Subject"])
mdf = md.fit()
print(mdf.summary())

import matplotlib.pyplot as plt

'''
Shapiro for Post ESI Negative vs. Neutral
'''
from scipy import stats
test_postesi_ldi = behav_data_df["PostESI_LDI"]
test_postesi_lgi = behav_data_df["PostESI_LGI"]

print(test_postesi_ldi.mean())
print(test_postesi_lgi.mean())

print('Shapiro for Post ESI LDI:', stats.shapiro(test_postesi_ldi))
print('Shapiro for Post ESI LGI:', stats.shapiro(test_postesi_lgi))


'''
Plotting Post ESI vs. Post IMP LDI
'''
from scipy import stats
import seaborn as sns

test_data = behav_data_df.dropna(how='any', subset=['PostESI_LDI', 'PostESI_LGI'])
print(stats.ttest_rel(test_data['PostESI_LDI'], test_data['PostESI_LGI']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostESI_LDI": "mediumvioletred", "PostESI_LGI": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostESI_LDI', 'PostESI_LGI']]) 
sns.boxplot(data=test_data[['PostESI_LDI', 'PostESI_LGI']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post-ESI vs. -IMP Lure Generalization Index (LDI)'), fontsize=15)
axes.tick_params(axis='y', labelsize=13, width=2) 

axes.set_xlabel(('Condition'), fontsize=15)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'PostESI_LDI'
labels[1] = 'PostESI_LGI'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)


#%%
    

"""""""""""""""""""""""""""""""""""""""
LDI RESULTS (COLLAPSED ACROSS VALENCE)

"""""""""""""""""""""""""""""""""""""""

esi_melt = pd.melt(behav_data_df, id_vars=['Subject'], value_vars=[
    'PostIMP_LDI',
    'PostIMP_LGI'
    ])

esi_melt.columns = ['Subject', 'Response', 'Value']

condition = []
for j, row in esi_melt.iterrows():
    if 'LDI' in row['Response']:
        condition.append('LDI')
    if 'LGI' in row['Response']:
        condition.append('LGI')
esi_melt['Condition'] = condition

esi_melt = esi_melt[[
    "Subject", "Response", "Condition", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.glm(
    "Value ~ Condition",
    esi_melt, groups=esi_melt["Subject"])
mdf = md.fit()
print(mdf.summary())

import matplotlib.pyplot as plt

'''
Shapiro for Post ESI Negative vs. Neutral
'''
from scipy import stats
test_postimp_ldi = behav_data_df["PostIMP_LDI"]
test_postimp_lgi = behav_data_df["PostIMP_LGI"]

print(test_postimp_ldi.mean())
print(test_postimp_lgi.mean())

print('Shapiro for Post IMP LDI:', stats.shapiro(test_postimp_ldi))
print('Shapiro for Post IMP LGI:', stats.shapiro(test_postimp_lgi))


'''
Plotting Post ESI vs. Post IMP LDI
'''
from scipy import stats
import seaborn as sns

# not using ttest_rel because....violation in the distribution
test_data = behav_data_df.dropna(how='any', subset=['PostIMP_LDI', 'PostIMP_LGI'])
print(stats.ttest_rel(test_data['PostIMP_LDI'], test_data['PostIMP_LGI']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostIMP_LDI": "mediumvioletred", "PostIMP_LGI": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostIMP_LDI', 'PostIMP_LGI']]) 
sns.boxplot(data=test_data[['PostIMP_LDI', 'PostIMP_LGI']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('PostIMP LGI vs. LDI'), fontsize=15)
axes.tick_params(axis='y', labelsize=13, width=2) 

axes.set_xlabel(('Condition'), fontsize=15)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'PostIMP_LDI'
labels[1] = 'PostIMP_LGI'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)


#%%

"""""""""""""""""""""""""""""""""""""""
LGI RESULTS (COLLAPSED ACROSS VALENCE)

"""""""""""""""""""""""""""""""""""""""

esi_melt = pd.melt(behav_data_df, id_vars=['Subject'], value_vars=[
    'PostESI_LGI',
    'PostIMP_LGI'
    ])

esi_melt.columns = ['Subject', 'Response', 'Value']

condition = []
for j, row in esi_melt.iterrows():
    if 'PostESI' in row['Response']:
        condition.append('PostESI')
    if 'PostIMP' in row['Response']:
        condition.append('PostIMP')
esi_melt['Condition'] = condition

esi_melt = esi_melt[[
    "Subject", "Response", "Condition", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.glm(
    "Value ~ Condition",
    esi_melt, groups=esi_melt["Subject"])
mdf = md.fit()
print(mdf.summary())

#%%
import matplotlib.pyplot as plt

'''
Shapiro for Post ESI vs. IMP
'''
from scipy import stats
test_postesi_lgi = behav_data_df["PostESI_LGI"]
test_postimp_lgi = behav_data_df["PostIMP_LGI"]

print(test_postesi_lgi.mean())
print(test_postimp_lgi.mean())

print('Shapiro for Post ESI LGI:', stats.shapiro(test_postesi_lgi))
print('Shapiro for Post IMP LGI:', stats.shapiro(test_postimp_lgi))


'''
Plotting Post ESI vs. Post IMP LDI
'''
from scipy import stats
import seaborn as sns

# not using ttest_rel because....violation in the distribution
test_data = behav_data_df.dropna(how='any', subset=['PostESI_LGI', 'PostIMP_LGI'])
print(stats.ttest_rel(test_data['PostESI_LGI'], test_data['PostIMP_LGI']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostESI_LGI": "mediumvioletred", "PostIMP_LGI": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostESI_LGI', 'PostIMP_LGI']]) 
sns.boxplot(data=test_data[['PostESI_LGI', 'PostIMP_LGI']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post-ESI vs. -IMP Lure Generalization Index (LGI)'), fontsize=15)
axes.tick_params(axis='y', labelsize=13, width=2) 

axes.set_xlabel(('Condition'), fontsize=15)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'PostESI'
labels[1] = 'PostIMP'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)


#%%





'''LURE GENERALIZATION INDEX ANALYSES'''

'''
Melting data to compare Post ESI vs. Post IMP LGIs
'''
esi_melt = pd.melt(behav_data_df, id_vars=['Subject'], value_vars=[
    'PostESI_NegativeLGI',
    'PostESI_NeutralLGI',

    'PostIMP_NegativeLGI',
    'PostIMP_NeutralLGI'
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
    if 'PostIMP' in row['Response']:
        condition.append('PostIMP')
esi_melt['Condition'] = condition

esi_melt = esi_melt[[
    "Subject", "Response", "Valence", "Condition", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt

'''
(PostESI vs. PostIMP) x Valence (Neg vs. Neu) 
'''

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Note: groups must be your repeated measure aka subjects

md = smf.glm(
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

plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_ESI_LGI.png', bbox_inches='tight',dpi=1200)\

'''
Shapiro for Post IMP Negative vs. Neutral
'''
from scipy import stats
test_postimp_neg_lgi = behav_data_df["PostIMP_NegativeLGI"]
test_postimp_neu_lgi = behav_data_df["PostIMP_NeutralLGI"]

print(test_postimp_neg_lgi.mean())
print(test_postimp_neu_lgi.mean())

print('Shapiro for Post IMP Negative LGI:', stats.shapiro(test_postimp_neg_lgi))
print('Shapiro for Post IMP Neutral LGI:', stats.shapiro(test_postimp_neu_lgi))

'''
Plotting Post IMP Neg vs. Neu LGI
'''
from scipy import stats
import seaborn as sns

test_data = behav_data_df.dropna(how='any', subset=['PostIMP_NegativeLGI', 'PostIMP_NeutralLGI'])
print(stats.ttest_rel(test_data['PostIMP_NegativeLGI'], test_data['PostIMP_NeutralLGI']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostIMP_NegativeLGI": "mediumvioletred", "PostIMP_NeutralLGI": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostIMP_NegativeLGI', 'PostIMP_NeutralLGI']]) 
sns.boxplot(data=test_data[['PostIMP_NegativeLGI', 'PostIMP_NeutralLGI']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post IMP Lure Generalization Index (LGI)'), fontsize=15)
axes.tick_params(axis='y', labelsize=13, width=2) 

axes.set_xlabel(('Valence'), fontsize=15)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Negative'
labels[1] = 'Neutral'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)

plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_IMP_LGI.png', bbox_inches='tight',dpi=1200)



# %%

'''LURE DISCRIMINATION INDEX ANALYSES'''

'''
Melting data to compare Post ESI vs. Post IMP LDIs
'''
esi_melt = pd.melt(behav_data_df, id_vars=['Subject'], value_vars=[
    'PostESI_NegativeLDI',
    'PostESI_NeutralLDI',

    'PostIMP_NegativeLDI',
    'PostIMP_NeutralLDI'
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
    if 'PostIMP' in row['Response']:
        condition.append('PostIMP')
esi_melt['Condition'] = condition

esi_melt = esi_melt[[
    "Subject", "Response", "Valence", "Condition", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt

'''
(PostESI vs. PostIMP) x Valence (Neg vs. Neu) 
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

plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_ESI_LDI.png', bbox_inches='tight',dpi=1200)
'''
Shapiro for Post IMP Negative vs. Neutral
'''
from scipy import stats
test_postimp_neg_ldi = behav_data_df["PostIMP_NegativeLDI"]
test_postimp_neu_ldi = behav_data_df["PostIMP_NeutralLDI"]

print(test_postimp_neg_ldi.mean())
print(test_postimp_neu_ldi.mean())

print('Shapiro for Post IMP Negative LDI:', stats.shapiro(test_postimp_neg_ldi))
print('Shapiro for Post IMP Neutral LDI:', stats.shapiro(test_postimp_neu_ldi))

'''
Plotting Post IMP Neg vs. Neu LDI
'''
from scipy import stats
import seaborn as sns

test_data = behav_data_df.dropna(how='any', subset=['PostIMP_NegativeLDI', 'PostIMP_NeutralLDI'])
print(stats.ttest_rel(test_data['PostIMP_NegativeLDI'], test_data['PostIMP_NeutralLDI']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostIMP_NegativeLDI": "mediumvioletred", "PostIMP_NeutralLDI": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostIMP_NegativeLDI', 'PostIMP_NeutralLDI']]) 
sns.boxplot(data=test_data[['PostIMP_NegativeLDI', 'PostIMP_NeutralLDI']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post IMP Lure Discrimination Index (LDI)'), fontsize=15)
axes.tick_params(axis='y', labelsize=13, width=2) 

axes.set_xlabel(('Valence'), fontsize=15)
axes.tick_params(axis='x', labelsize=15, width=2) 

labels = [item.get_text() for item in axes.get_xticklabels()]
labels[0] = 'Negative'
labels[1] = 'Neutral'

axes.set_xticklabels(labels)

for location in ['left', 'right', 'top', 'bottom']:
    axes.spines[location].set_linewidth(2)

plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_IMP_LDI.png', bbox_inches='tight',dpi=1200)

# %%
'''POST ESI VS. IMP HIT RATE ANALYSES'''

# behav_data_df = behav_data_df.drop(labels = ["Mean"], axis=0)

'''
Melting data to compare Post ESI vs. Post IMP LGIs
'''
esi_melt = pd.melt(behav_data_df, id_vars=['Subject'], value_vars=[
    'PostESI_HRNeg',
    'PostESI_HRNeu',

    'PostIMP_HRNeg',
    'PostIMP_HRNeu'

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
    if 'PostIMP' in row['Response']:
        condition.append('PostIMP')
esi_melt['Condition'] = condition


esi_melt = esi_melt[[
    "Subject", "Response", "Valence", "Condition", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt

'''
(PostESI vs. PostIMP) x Valence (Neg vs. Neu) 
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
test_postimp_neg_hr = behav_data_df["PostIMP_HRNeg"]
test_postimp_neu_hr = behav_data_df["PostIMP_HRNeu"]

print(test_postimp_neg_hr.mean())
print(test_postimp_neu_hr.mean())

print('Shapiro for Post IMP Negative HR:', stats.shapiro(test_postimp_neg_hr))
print('Shapiro for Post IMP Neutral HR:', stats.shapiro(test_postimp_neu_hr))


'''
Plotting Post ESI Neg vs. Neu IMP
'''
from scipy import stats
import seaborn as sns

# not using ttest_rel because....violation in the distribution
test_data = behav_data_df.dropna(how='any', subset=['PostIMP_HRNeg', 'PostIMP_HRNeu'])
print(stats.ttest_rel(test_data['PostIMP_HRNeg'], test_data['PostIMP_HRNeu']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostIMP_HRNeg": "mediumvioletred", "PostIMP_HRNeu": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostIMP_HRNeg', 'PostIMP_HRNeu']]) 
sns.boxplot(data=test_data[['PostIMP_HRNeg', 'PostIMP_HRNeu']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post IMP Lure Hit Rate'), fontsize=15)
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

'''POST ESI VS. IMP FA RATE ANALYSES'''

# behav_data_df = behav_data_df.drop(labels = ["Mean"], axis=0)

'''
Melting data to compare Post ESI vs. Post IMP FAR
'''
esi_melt = pd.melt(behav_data_df, id_vars=['Subject'], value_vars=[
    'PostESI_FARNeg',
    'PostESI_FARNeu',

    'PostIMP_FARNeg',
    'PostIMP_FARNeu'

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
    if 'PostIMP' in row['Response']:
        condition.append('PostIMP')
esi_melt['Condition'] = condition


esi_melt = esi_melt[[
    "Subject", "Response", "Valence", "Condition", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt

'''
(PostESI vs. PostIMP) x Valence (Neg vs. Neu) 
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
test_postimp_neg_far = behav_data_df["PostIMP_FARNeg"]
test_postimp_neu_far = behav_data_df["PostIMP_FARNeu"]

print(test_postimp_neg_far.mean())
print(test_postimp_neu_far.mean())

print('Shapiro for Post IMP Negative FAR:', stats.shapiro(test_postimp_neg_far))
print('Shapiro for Post IMP Neutral FAR:', stats.shapiro(test_postimp_neu_far))


'''
Plotting Post ESI Neg vs. Neu FAR
'''
from scipy import stats
import seaborn as sns

# not using ttest_rel because....violation in the distribution
test_data = behav_data_df.dropna(how='any', subset=['PostIMP_FARNeg', 'PostIMP_FARNeu'])
print(stats.ttest_rel(test_data['PostIMP_FARNeg'], test_data['PostIMP_FARNeu']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostIMP_FARNeg": "mediumvioletred", "PostIMP_FARNeu": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostIMP_FARNeg', 'PostIMP_FARNeu']]) 
sns.boxplot(data=test_data[['PostIMP_FARNeg', 'PostIMP_FARNeu']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post IMP Lure FA Rate'), fontsize=15)
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


'''POST ESI VS. IMP FA ANALYSES'''

# behav_data_df = behav_data_df.drop(labels = ["Mean"], axis=0)

'''
Melting data to compare Post ESI vs. Post IMP FAR
'''
esi_melt = pd.melt(behav_data_df, id_vars=['Subject'], value_vars=[
    'PostESI_NegLureFA',
    'PostESI_NeuLureFA',

    'PostIMP_NegLureFA',
    'PostIMP_NeuLureFA'

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
    if 'PostIMP' in row['Response']:
        condition.append('PostIMP')
esi_melt['Condition'] = condition


esi_melt = esi_melt[[
    "Subject", "Response", "Valence", "Condition", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt

'''
(PostESI vs. PostIMP) x Valence (Neg vs. Neu) 
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
Shapiro for Post IMP Negative vs. Neutral
'''
from scipy import stats
test_postimp_neg_fa = behav_data_df["PostIMP_NegLureFA"]
test_postimp_neu_fa = behav_data_df["PostIMP_NeuLureFA"]

print(test_postesi_neg_fa.mean())
print(test_postesi_neu_fa.mean())

print('Shapiro for Post IMP Negative FA:', stats.shapiro(test_postimp_neg_fa))
print('Shapiro for Post IMP Neutral FA:', stats.shapiro(test_postimp_neu_fa))


'''
Plotting Post IMP Neg vs. Neu LGI
'''
from scipy import stats
import seaborn as sns

# not using ttest_rel because....violation in the distribution
test_data = behav_data_df.dropna(how='any', subset=['PostIMP_NegLureFA', 'PostIMP_NeuLureFA'])
print(stats.ttest_rel(test_data['PostIMP_NegLureFA'], test_data['PostIMP_NeuLureFA']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostIMP_NegLureFA": "mediumvioletred", "PostIMP_NeuLureFA": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostIMP_NegLureFA', 'PostIMP_NeuLureFA']]) 
sns.boxplot(data=test_data[['PostIMP_NegLureFA', 'PostIMP_NeuLureFA']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post IMP Lure FA'), fontsize=15)
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
'''POST ESI VS. IMP dPrime ANALYSES'''

# behav_data_df = behav_data_df.drop(labels = ["Mean"], axis=0)

'''
Melting data to compare Post ESI vs. Post IMP dPrime
'''
esi_melt = pd.melt(behav_data_df, id_vars=['Subject'], value_vars=[
    'PostESI_dPrimeNeg',
    'PostESI_dPrimeNeu',

    'PostIMP_dPrimeNeg',
    'PostIMP_dPrimeNeu'

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
    if 'PostIMP' in row['Response']:
        condition.append('PostIMP')
esi_melt['Condition'] = condition


esi_melt = esi_melt[[
    "Subject", "Response", "Valence", "Condition", "Value"]]
esi_melt.dropna(inplace = True)

esi_melt

'''
(PostESI vs. PostIMP) x Valence (Neg vs. Neu) 
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
Shapiro for Post IMP Negative vs. Neutral
'''
from scipy import stats
test_postimp_neg_fa = behav_data_df["PostIMP_NegLureFA"]
test_postimp_neu_fa = behav_data_df["PostIMP_NeuLureFA"]

print(test_postesi_neg_fa.mean())
print(test_postesi_neu_fa.mean())

print('Shapiro for Post IMP Negative FA:', stats.shapiro(test_postimp_neg_fa))
print('Shapiro for Post IMP Neutral FA:', stats.shapiro(test_postimp_neu_fa))


'''
Plotting Post IMP Neg vs. Neu LGI
'''
from scipy import stats
import seaborn as sns

# not using ttest_rel because....violation in the distribution
test_data = behav_data_df.dropna(how='any', subset=['PostIMP_NegLureFA', 'PostIMP_NeuLureFA'])
print(stats.ttest_rel(test_data['PostIMP_NegLureFA'], test_data['PostIMP_NeuLureFA']))

f, axes = plt.subplots(figsize=(6,6))
sns.despine(left=False)

my_pal = {"PostIMP_NegLureFA": "mediumvioletred", "PostIMP_NeuLureFA": "darkgoldenrod"}
axes = sns.swarmplot(size=7, palette=my_pal, linewidth=1.7, data=test_data[['PostIMP_NegLureFA', 'PostIMP_NeuLureFA']]) 
sns.boxplot(data=test_data[['PostIMP_NegLureFA', 'PostIMP_NeuLureFA']], palette=my_pal, linewidth = 2, width = 0.8, ax=axes)

axes.set_ylabel(('Post IMP Lure FA'), fontsize=15)
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
                    if study_df['Randomization'][0] == "ESIthenIMP":
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
                    if study_df['Randomization'][0] == "ESIthenIMP":
                        for run in runs:
                            if run == study_run1:
                                curr_category.append(matching(study_df,run,neu_lurefas_list))
                    else:
                        for run in runs:
                            if run == study_run2:
                                curr_category.append(matching(study_df,run,neu_lurefas_list))

            # PostIMP_NegLureFA
            for curr_category in categories:
                if curr_category == PostIMP_NegLureFA:
                    if study_df['Randomization'][0] == "ESIthenIMP":
                        for run in runs:
                            if run == study_run2:
                                curr_category.append(matching(study_df,run,neg_lurefas_list))

                    else:
                        for run in runs:
                            if run == study_run1:
                                curr_category.append(matching(study_df,run,neg_lurefas_list))
            
            # PostIMP_NeuLureFA
            for curr_category in categories:
                if curr_category == PostESI_NeuLureFA:
                    if study_df['Randomization'][0] == "ESIthenIMP":
                        for run in runs:
                            if run == study_run2:
                                curr_category.append(matching(study_df,run,neu_lurefas_list))
                    else:
                        for run in runs:
                            if run == study_run1:
                                curr_category.append(matching(study_df,run,neu_lurefas_list))

