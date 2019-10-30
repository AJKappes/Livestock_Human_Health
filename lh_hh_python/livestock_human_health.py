### Human-Livestock Health Analysis ###

import numpy as np
import pandas as pd
import scipy.stats as stats
import glob as glob
import matplotlib.pyplot as plt

def get_files(subdir):
    return glob.glob('/home/alex/research/africa' + subdir + '*.csv')


data_list = np.array(get_files('/Nutrient_Demand/'))
species_list = ['bovine', 'goat', 'sheep']
data_read = []

for s in species_list:
    for i in range(len(data_list)):
        if s in data_list[i]:
            print(i, data_list[i])
            data_read.append(data_list[i])

df_bovine = pd.read_csv(data_read[0])
df_goat = pd.read_csv(data_read[1])
df_sheep = pd.read_csv(data_read[2])

villages = df_bovine['VillageID_x'].unique().tolist()
for v in villages:
    if v in df_goat['VillageID_x'].unique():
        print(v, 'is in goat df - lengths are:', len(villages), len(df_goat['VillageID_x'].unique()))
    else:
        print('village', v, 'is not in goat df')
    if v in df_sheep['VillageID_x'].unique().tolist():
        print(v, 'is in sheep df - lengths are:', len(villages), len(df_sheep['VillageID_x'].unique()))
    else:
        print('village', v, 'is not in sheep df')
print()

d_bov_villages = {}
d_goat_villages = {}
d_sheep_villages = {}
d_v_list = [d_bov_villages, d_goat_villages, d_sheep_villages]
d_list = [df_bovine, df_goat, df_sheep]

for d in d_v_list:
    for v in villages:
        d[v] = pd.DataFrame()

for dv, dl, s in zip(d_v_list, d_list, species_list):
    for key in dv:
        print(s + ':', 'village', key, 'data subset complete')
        dv[key] = dl[dl['VillageID_x'] == key]
    print()

# village vaccination rates
vacc_rates = pd.DataFrame({'village': villages})
vacc_cols = ['bov_vacc_rate', 'goat_vacc_rate', 'sheep_vac_rate']
health_cols = ['bov_hh', 'goat_hh', 'sheep_hh']

for c, dv in zip(vacc_cols, d_v_list):
    for key in villages:
        vacc_rates.loc[vacc_rates['village'] == key, c] = sum(dv[key]['AnimalVaccinated'] == 1) / len(dv[key])

for c, dv in zip(health_cols, d_v_list):
    for key in villages:
        vacc_rates.loc[vacc_rates['village'] == key, c] = sum(dv[key]['VisitedClinic'] == 1) / len(dv[key])

# vacc_rates.to_csv('/home/alex/research/africa/Livestock_Human_Health/data/vacc_rates.csv')
