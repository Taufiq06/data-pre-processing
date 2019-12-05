#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os 
import pandas as pd 


# In[2]:


# define directory
path= os.getcwd()
path = "C:/Users/tina.huang/OneDrive - World Resources Institute/Desktop/"
os.chdir(path)
print(path)


# In[3]:


# read in csv file as Dataframe 
energy_df = pd.read_csv('SE4AllData.csv')


# In[4]:


# examine this data frame 
energy_df


# In[5]:


# subset for renewable energy intensity data 
energy_intensity_df = energy_df[energy_df['Indicator Name'].str.contains('Energy intensity level of primary energy')]


# In[6]:


# examine renewable energy intensity data frame
energy_intensity_df


# In[10]:


#convert tables from wide form (each year is a column) to long form (a single column of years and a single column of values)
energy_intensity_long = pd.melt (energy_intensity_df, id_vars= ['Country Name' ,'Country Code'] , 
                                 value_vars = ['1990', '1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016'],
                                 var_name = 'year',
                                 value_name = 'energy_intensity')


# In[11]:


# examine the new data frame 
energy_intensity_long


# In[12]:


# examine each column's data type
energy_intensity_long.dtypes


# In[14]:


#convert year column from object to number
energy_intensity_long.year=energy_intensity_long.year.astype('int64')


# In[15]:


# export df as csv 
energy_intensity_long.to_csv(r'C:/Users/tina.huang/OneDrive - World Resources Institute/Desktop/energy_intensity.csv')

