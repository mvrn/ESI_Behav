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

# the first chunk of subs were randomized to the ESI vs. IMP condition. 
# the second half were randomized to the ESI vs. MATH condition

final_esi_seqmemo_subs = [
    "101","102","103","105","106","107","109","110","111","112","113",
    "114","115","117","118","119","120","121","122","123","124","127",
    "128","129","130","131","132","133","134","135","136","137","138",
    "139","140","141","142","145","146","147","148","149","151","152",
    "153","154","158","159","160","162","163","164","165","168","169",
    "170","173","175","180","181","184","185","186","187","194","197",
    "200","201","204","210","211","212","213","216","222","246",
    
    "125","143","150","155","156","157","161","166","167","171","172",
    "174","176","177","178","179","182","183","188","189","190",
    "191","192","193","195","196","198","199","202","203","205",
    "206","207","208","209","214","215","217","218","219","220","221",
    "223","224","225","226","227","228","229","230","231","232","233",
    "234","235","236","237","238","239","240","241","242","243","244",
    "245","247","248","249","250"
    ]

#list all csv files only
csv_files = glob('*.{}'.format('csv'))
csv_files
# print(csv_files)

esi_seqmemo_df = pd.DataFrame()
#append all files together
for file in csv_files:
            df_temp = pd.read_csv(file)
            esi_seqmemo_df = esi_seqmemo_df.append(df_temp)

esi_seqmemo_df.reset_index(drop=True, inplace=True)

esi_seqmemo_df = esi_seqmemo_df.loc[:, ~esi_seqmemo_df.columns.str.contains('^Unnamed')]

esi_seqmemo_df = esi_seqmemo_df[esi_seqmemo_df.columns.drop(list(esi_seqmemo_df.filter(regex='Postmath')))]

esi_seqmemo_df = esi_seqmemo_df[esi_seqmemo_df.columns.drop(list(esi_seqmemo_df.filter(regex='PostIMP')))]

esi_seqmemo_df

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

# the file includes all participants, I am isolating those that were
# used for the ESI vs. IMP condition only 
# NOTE: the number of participants (i.e., rows) between the  
#       behav_data_df and the esi_details_df is different because of the
#       poor audio quality of some participants' recordings leading to
#       further reduction of the pool...to 66.
esi_details_df = esi_details_df.query("Subject in @final_esi_seqmemo_subs")
esi_details_df.reset_index(drop=True, inplace=True)

# Getting new list of subjects based on the esi_details_df
esi_details_ppt_list = esi_details_df['Subject'].tolist()
# converting each subject in the list into a string
esi_details_ppt_list = [str(element) for element in esi_details_ppt_list]

# Reducing the behav_data_df and then concatenate them to run analyses
# NOTE: the final subject list is 64 and not 66 (based on the esi_details_list)
#       because if you look above I eliminated subjects 109 and 126
esi_seqmemo_df = esi_seqmemo_df.query("Subject in @esi_details_ppt_list")
esi_seqmemo_df.reset_index(drop=True, inplace=True)


esi_seqmemo_df

#%%

# Concatenate both dataframes
esi_seqmemo_df = pd.concat([esi_seqmemo_df, esi_details_df], axis=1)

# drop duplicate Subject columns
esi_seqmemo_df = esi_seqmemo_df.loc[:,~esi_seqmemo_df.columns.duplicated()].copy()

esi_seqmemo_df
#%%
import pandas as pd
import seaborn as sns

'''Calculating FAs, Foil FAs, LGI, HR, FAR, dPrimes'''

# Negative Lure FAs per Condition
esi_seqmemo_df['PostESI_NegLureFA'] = esi_seqmemo_df['PostESI_NegLureFA_Count']/(esi_seqmemo_df['PostESI_NegLureFA_Count'] + esi_seqmemo_df['PostESI_NegLureCR_Count'])

# Negative Foils 
esi_seqmemo_df['NegFoilFA'] = esi_seqmemo_df['NegFoilFA_Count']/(esi_seqmemo_df['NegFoilFA_Count'] + esi_seqmemo_df['NegFoilCR_Count'])


# Neutral Lure FAs per Condition
esi_seqmemo_df['PostESI_NeuLureFA'] = esi_seqmemo_df['PostESI_NeuLureFA_Count']/(esi_seqmemo_df['PostESI_NeuLureFA_Count'] + esi_seqmemo_df['PostESI_NeuLureCR_Count'])
# Neutral Foils 
esi_seqmemo_df['NeuFoilFA'] = esi_seqmemo_df['NeuFoilFA_Count']/(esi_seqmemo_df['NeuFoilFA_Count'] + esi_seqmemo_df['NeuFoilCR_Count'])


# Negative LGIs per Condition
esi_seqmemo_df['PostESI_NegativeLGI'] = esi_seqmemo_df['PostESI_NegLureFA'] - esi_seqmemo_df['NegFoilFA'] 

# Neutral LGIs per Condition
esi_seqmemo_df['PostESI_NeutralLGI'] = esi_seqmemo_df['PostESI_NeuLureFA'] - esi_seqmemo_df['NeuFoilFA'] 

# TH per Condition
esi_seqmemo_df["PostESI_NegTargHit"] = esi_seqmemo_df["PostESI_NegTargHit_Count"]/(esi_seqmemo_df["PostESI_NegTargHit_Count"] + esi_seqmemo_df["PostESI_NegTargMiss_Count"])

esi_seqmemo_df["PostESI_NeuTargHit"] = esi_seqmemo_df["PostESI_NeuTargHit_Count"]/(esi_seqmemo_df["PostESI_NeuTargHit_Count"] + esi_seqmemo_df["PostESI_NeuTargMiss_Count"])


# Negative CRs, TM, LDI per Condition
esi_seqmemo_df['PostESI_NegLureCR'] = esi_seqmemo_df['PostESI_NegLureCR_Count']/(esi_seqmemo_df['PostESI_NegLureCR_Count'] + esi_seqmemo_df['PostESI_NegLureFA_Count'])
esi_seqmemo_df["PostESI_NegTargMiss"] = esi_seqmemo_df["PostESI_NegTargMiss_Count"]/(esi_seqmemo_df["PostESI_NegTargMiss_Count"] + esi_seqmemo_df["PostESI_NegTargHit_Count"])


# Negative LDI per Condition
esi_seqmemo_df['PostESI_NegativeLDI'] = esi_seqmemo_df['PostESI_NegLureCR'] - esi_seqmemo_df['PostESI_NegTargMiss'] 

# Neutral CRs, TM, LDI per Condition
esi_seqmemo_df['PostESI_NeuLureCR'] = esi_seqmemo_df['PostESI_NeuLureCR_Count']/(esi_seqmemo_df['PostESI_NeuLureCR_Count'] + esi_seqmemo_df['PostESI_NeuLureFA_Count'])

esi_seqmemo_df["PostESI_NeuTargMiss"] = esi_seqmemo_df["PostESI_NeuTargMiss_Count"]/(esi_seqmemo_df["PostESI_NeuTargMiss_Count"] + esi_seqmemo_df["PostESI_NeuTargHit_Count"])

# Neutral LDI per Condition
esi_seqmemo_df['PostESI_NeutralLDI'] = esi_seqmemo_df['PostESI_NeuLureCR'] - esi_seqmemo_df['PostESI_NeuTargMiss'] 

# Windsorizing LGIs and LDIs

from scipy.stats.mstats import winsorize

esi_seqmemo_df['PostESI_NegativeLGI'] = winsorize(esi_seqmemo_df['PostESI_NegativeLGI'], limits=[0.05, 0.05])
esi_seqmemo_df['PostESI_NeutralLGI'] = winsorize(esi_seqmemo_df['PostESI_NeutralLGI'], limits=[0.05, 0.05])

esi_seqmemo_df['PostESI_NegativeLDI'] = winsorize(esi_seqmemo_df['PostESI_NegativeLDI'], limits=[0.05, 0.05])
esi_seqmemo_df['PostESI_NeutralLDI'] = winsorize(esi_seqmemo_df['PostESI_NeutralLDI'], limits=[0.05, 0.05])

esi_seqmemo_df

# %%

esi_seq_melt = pd.melt(esi_seqmemo_df, id_vars=['Subject', 'Seq_Memo'], value_vars=[
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

plt.savefig('/home/mrive301/mvrn_esi_analysis/Post_ESI_SeqMemo_LGI_AllSubs.png', bbox_inches='tight',dpi=1200)


#%%
'''
Is sequence memory recall modulating 
the degree of LGI after ESI?
'''
esi_seq_melt = pd.melt(esi_seqmemo_df, id_vars=['Subject', 'Seq_Memo'], value_vars=[
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
esi_seq_melt = pd.melt(esi_seqmemo_df, id_vars=['Subject', 'Seq_Memo'], value_vars=[
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

# %%
