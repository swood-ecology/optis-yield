# Import packages
import pandas as pd
import numpy as np

# Read data
optis = pd.read_csv("../raw-data/OpTIS/predictors_2020_04_01_shp.csv", low_memory=False)

# Set row id
optis = optis.set_index('row_id')

# Focus on pre-2012 data
optis_pre2012 = optis.query('Year < 2012')

a = optis_pre2012.groupby(['State_Name','County_Name'])['Corn_RedTill_High_Pct'].mean().reset_index().rename(columns={'Corn_RedTill_High_Pct': 'meanRT'})

# Get lowest and highest 5 within each state
low = a.sort_values('meanRT', ascending=True).groupby(['State_Name']).head(5).reset_index()
high = a.sort_values('meanRT', ascending=False).groupby(['State_Name']).head(5).reset_index()

# Select out Minnesota and Kansas
states = ['Kansas', 'Minnesota']
selectCounties = low[low.State_Name.isin(states)].append(high[high.State_Name.isin(states)],ignore_index=True)

# Merge with existing data to be able to get FIPS codes
merged = selectCounties.merge(optis[['State_Name','County_Name','County_FIPS']], 
                              on=['State_Name','County_Name'], 
                              how='left').drop_duplicates()
                              
# Export file to run in GEE
merged.to_csv('../processed-data/counties-for-gee.csv', index=False)