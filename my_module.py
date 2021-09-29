#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import iqr


# In[2]:


# method to establish a dataframe survey
def dataframe_survey(dataframes):
    data_survey=pd.DataFrame(columns=['dataframe','(rows, column)','Total number of nans','percentage of nans','number of duplicated rows','percentage of duplicated rows'])
    for df_name, df_var in dataframes.items():
        shape='({},{})'.format(str(df_var.shape[0]),str(df_var.shape[1]))   
        nans=df_var.isna().sum().sum()
        per_nans='{} %'.format(  round(  ((df_var.isna().sum().sum()/df_var.size).astype(float))*100 ,2) )
        dup_rows=df_var.duplicated().sum()
        per_dup_rows='{} %'.format((df_var.duplicated().sum())/(df_var.shape[0]))
        new_row={'dataframe':df_name,
                 '(rows, column)':shape,
                 'Total number of nans': nans,
                 'percentage of nans': per_nans,
                 'number of duplicated rows':dup_rows,
                 'percentage of duplicated rows':per_dup_rows}
        data_survey=data_survey.append(new_row, ignore_index=True)
    return data_survey


# In[3]:


# method to make a survey of dataframe columns
def variable_survey (dataframe):
    df=pd.DataFrame(columns = ['variable name', 'variable type', 'nbr of distinct values','percentage of NaNs'])
    for column in (dataframe.columns):
        var_type = dataframe[column].dtypes
        distinct_values = dataframe[column].nunique()
        percentage_nans = '{} %'.format(round((dataframe[column].isna().sum()/len(dataframe))*100,2))
        new_row={'variable name':column,
                 'variable type':var_type,
                 'nbr of distinct values':distinct_values,
                 'percentage of NaNs':percentage_nans}
        df=df.append(new_row, ignore_index=True)
    return df


# In[4]:


#define a novel dataframe to stock variables nans percentage 
def nans_df (dataframe):
    df=pd.DataFrame(columns = ['variable name', 'percentage of NaNs'])
    for column in (dataframe.columns):
        percentage_nans = round((dataframe[column].isna().sum()/len(dataframe))*100,2)
        new_row={'variable name':column,
                 'percentage of NaNs':percentage_nans}
        df=df.append(new_row, ignore_index=True)
    df.sort_values(by='percentage of NaNs',inplace=True)
    df.plot(kind='bar',x='variable name', stacked=False,rot=45,figsize=(20,6))
    


# In[ ]:


#definir une fonction qu permet de détecter les outliers et de les supprimer

def find_outliers(df, column):
    #get initial rows
    #find Q1, Q3, and interquartile range for each column
    q1 = df[column].quantile(q=.25)
    q3 = df[column].quantile(q=.75)
    iqr = q3-q1
    #only keep rows in dataframe that have values within 1.5*IQR of Q1 and Q3
    value1=q1-1.5*iqr
    value2=q3+1.5*iqr
    df = df[~((df[column] < value1) | (df[column] > value2))]
    return df

