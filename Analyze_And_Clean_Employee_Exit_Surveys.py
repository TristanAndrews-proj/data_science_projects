#!/usr/bin/env python
# coding: utf-8

# # Brief Project Summary.
# - In this guided project, we'll work with exit surveys from employees of the Department of Education, Training and Employment (DETE) and the Technical and Further Education (TAFE) institute in Queensland, Australia.
# - In this project, we'll play the role of data analyst and pretend our stakeholders want to know the following:
# 
#     - Are employees who only worked for the institutes for a short period of time resigning due to some kind of dissatisfaction? What about employees who have been there longer?
#     - Are younger employees resigning due to some kind of dissatisfaction? What about older employees?

# In[1]:


import pandas as pd
import numpy as np

#Read the data. 
dete_survey = pd.read_csv('dete-exit-survey-january-2014.csv', encoding='Latin-1')
tafe_survey = pd.read_csv('tafe-employee-exit-survey-access-database-december-2013.csv', encoding='Latin-1')


# In[2]:


# A quick display 150 columns max to prevent truncated display of columns.
pd.options.display.max_columns = 150
dete_survey.head()


# In[3]:


dete_survey.info()


# As you can see, many of these columns contain a lot of `NaN` or `null` values. However, to determine if the employees who worked for a short period of time resigned due to a dissatisfaction, we don't need a lot of these columns.

# In[4]:


tafe_survey.head()


# In[5]:


tafe_survey.info()


# In[6]:


dete_survey.isnull()


# In the `tafe_survey` dataframe, there are a lot of columns that contain many `NaN` values. There are even some that have values that are Not Stated. But like the `dete_survey` dataframe, there are a lot of columns we don't need to use to analyze whether or not short-term employees resigned because of a dissatisfaction. I also found that both dataframes contain many of the same columns. There were many columns in the dataframes that tells us that a certain number of employees resigned because of some sort of dissatisfaction.

# # Simplifying the Dataframes.

# Re-reading the datasets as dataframes but this time we will also be replacing `Nan` Values with `Not Stated`.

# In[7]:


dete_survey = pd.read_csv('dete-exit-survey-january-2014.csv', encoding='Latin-1', na_values= 'Not Stated')

#Dropping the columns we don't need for our analysis.
dete_survey_updated = dete_survey.drop(dete_survey.columns[28:49], axis=1)
tafe_survey_updated = tafe_survey.drop(tafe_survey.columns[17:66], axis=1)


# In[8]:


# Print all the column names we need to make our analysis.
print(dete_survey_updated.columns)
print(tafe_survey_updated.columns)


# Since some `tafe_survey` dataframe had columns contained 'Not Stated' values, we also had to make sure we did the same thing for our `dete_survey` dataframe as well since it's likely that we will have to merge these two dataframes into one. We also made sure to drop the columns in both dataframes that we didn't need in order to narrow our focus down to all the important datapoints we will need to complete our analysis. 

# # Updating and Re-naming columns.

# In[9]:


dete_survey_updated.columns = dete_survey_updated.columns.str.replace('\s+','_').str.replace(' ','').str.lower()
dete_survey_updated.columns


# In[10]:


#First 5 rows of dete_survey_updated. 
dete_survey_updated.head()


# The `tafe_survey_updated` dataframe has a lot of the same columns as the `dete_survey_updated` dataframe except they have different names. There are columns in both dataframes we will need to make our final analysis so to make it easier, we renamed some of the columns in the `tafe_survey_updated` dataframe to the names in their respective identical columns in the `dete_survey_updated` dataframe.

# In[11]:


#Using the column names as column indexes wasn't working so I had to use their numerical indexes.
mapping = {tafe_survey_updated.columns[0]: 'id', tafe_survey_updated.columns[3]: 'cease_date', 
                               tafe_survey_updated.columns[4]: 'separationtype', 
               tafe_survey_updated.columns[17]: 'gender', 
               tafe_survey_updated.columns[18]: 'age',
       tafe_survey_updated.columns[19]: 'employment_status',
      tafe_survey_updated.columns[20]: 'position',
       tafe_survey_updated.columns[21]: 'institute_service',
       tafe_survey_updated.columns[22]: 'role_service'}
tafe_survey_updated = tafe_survey_updated.rename(columns=mapping)
tafe_survey_updated.columns


# In[12]:


#First 5 rows of tafe_survey_updated. 
tafe_survey_updated.head()


# In[13]:


#Reviewing unique values in the 'seperationtype' column in dete_survey_updated.
dete_survey_updated['separationtype'].value_counts()


# In[14]:


#Reviewing unique values in the 'seperationtype' column in tafe_survey_updated.
tafe_survey_updated['separationtype'].value_counts()


# # Filtering data based on Resignation.
# The `dete_survey_updated` dataframe has 3 types of Resignations whereas `tafe_survey_updated` dataframe has only 1. Since we have to merge both frames together, we have to ensure that all the identical columns from both frames have the same exact name and values. 

# In[15]:


#Replacing all 3 types of Resignations into 1. 
dete_survey_updated['separationtype'] = dete_survey_updated['separationtype'].str.split('-').str[0]
dete_survey_updated['separationtype'].value_counts()


# As you can see from the information above, we were able to combine all of 3 different types of Resignations in `dete_survey_updated` into one Resignation type. 

# In[16]:


#Filtering both dataframes to rows whose 'separationtype' column is 'Resignation' only.
dete_resignations = dete_survey_updated[dete_survey_updated['separationtype']=='Resignation']
tafe_resignations = tafe_survey_updated[tafe_survey_updated['separationtype']=='Resignation']


# # Filtering dates and creating Visualizations.
# Here we'll focus on verifying that the years in the `cease_date` and `dete_start_date` columns make sense based on these criterias: 
# - Since the cease_date is the last year of the person's employment and the dete_start_date is the person's first year of employment, it wouldn't make sense to have years after the current date.
# - Given that most people in this field start working in their 20s, it's also unlikely that the dete_start_date was before the year 1940.

# In[17]:


#Reviewing unique values in the 'cease_date' column in dete_resignations.
dete_resignations['cease_date'].value_counts()


# In[18]:


#Reviewing unique values in the 'dete_start_date' column in dete_resignations.
dete_resignations['dete_start_date'].value_counts()


# In[19]:


#Using string methods to extact the years in the 'cease_date' and 'dete_start_date' columns.

dete_resignations = dete_resignations.copy() #Using .copy() method to get around 'SettingWithCopy' warning.

dete_resignations['cease_date'] = dete_resignations['cease_date'].str.split('/').str[-1]

#Displaying years as a float data type.
dete_resignations['cease_date'] = dete_resignations['cease_date'].astype('float')


# In[20]:


dete_resignations['cease_date'].value_counts().sort_values(ascending=False)


# In[21]:


dete_resignations['dete_start_date'].value_counts().sort_values(ascending=False)


# In[22]:


#Reviewing unique values in the 'cease_date' column in tafe_resignations.
tafe_resignations['cease_date'].value_counts().sort_index()


# In[23]:


#Creating visualizations for our data to find out what may have went wrong.
import matplotlib.pyplot as plt
dete_resignations['cease_date'].hist(bins=25, range = (2005,2015))


# In[24]:


dete_resignations['dete_start_date'].hist(bins=25, range = (1960,2015))


# In[25]:


tafe_resignations['cease_date'].hist(bins=25, range = (2008, 2014))


# From the visualizations created above, I found that the dates don't completely align. The only years that align in the `cease_date` column for both dataframes are: 2010, 2012, and 2013. Additionally, the visual for the `cease_date` column in the `tafe_resignations` dataframe shows a higher count in 2010 than the `cease_date` column in the `dete_resignations` column for that same year. This still isn't a major issue though. We should still be able to work with this.

# # Creating a new column in `dete_resginations`.

# Recall that our end goal is to answer the following question:
# 
# - Are employees who have only worked for the institutes for a short period of time resigning due to some kind of dissatisfaction? What about employees who have been at the job longer?
# 
# In the Human Resources field, the length of time an employee spent in a workplace is referred to as their years of service.
# 
# You may have noticed that the `tafe_resignations` dataframe already contains a `service` column, which we renamed to `institute_service`. In order to analyze both surveys together, we'll have to create a corresponding `institute_service` column in dete_resignations.

# In[26]:


#Creating a new column called 'institute_service' which contains the number of years each employee was employed for.
dete_resignations['institute_service'] = dete_resignations['cease_date'] - dete_resignations['dete_start_date']


# In[27]:


#A quick review of our results.
dete_resignations['institute_service'].head()


# # Updating values in all Dissatisfaction columns and creating a new column.
# Below are the columns we'll use to categorize employees as "dissatisfied" from each dataframe.
# - For `tafe_resignations`:
#   - Contributing Factors. Dissatisfaction
#   - Contributing Factors. Job Dissatisfaction
# 
# - For `dete_resignations`:
#    - job_dissatisfaction
#    - dissatisfaction_with_the_department
#    - physical_work_environment
#    - lack_of_recognition
#    - lack_of_job_security
#    - work_location
#    - employment_conditions
#    - work_life_balance
#    - workload
# 
# If the employee indicated that there were dissatisfying factors that caused him/her to resign, we would mark their response down in a newly created column called `dissatisfaction`. In that column, the employee's response would be listed as either `True`, `False`, or `NaN`. `True`: indicating that the employee resigned because of a dissatisfaction. `False`: indicating that the employee did not resign because of an dissatisfactions. `Nan`: indicating that the employee resigned but did not indicated whether or not it was because of any dissatisfactions.
#  

# In[28]:


#Reviewing all the unique values in both the Dissatisfaction columns of tafe_resignations.
tafe_resignations['Contributing Factors. Dissatisfaction'].value_counts()


# In[29]:


tafe_resignations['Contributing Factors. Job Dissatisfaction'].value_counts()


# In[30]:


#Creating a function that updates the values in the 'dissatisfaction' columns to True, False, or Nan.
def update_vals(row_value):
    if row_value == '-':
        return False
    elif pd.isnull(row_value):
        return np.nan
    else:
        return True
tafe_resignations['dissatisfied'] = tafe_resignations[['Contributing Factors. Dissatisfaction',
                                                       'Contributing Factors. Job Dissatisfaction'
                                                      ]].applymap(update_vals).any(axis=1, skipna=False)
tafe_resignations_up = tafe_resignations.copy()
dete_resignations['dissatisfied'] = dete_resignations[['job_dissatisfaction','dissatisfaction_with_the_department',
                                                       'physical_work_environment','lack_of_recognition',
                                                       'lack_of_job_security','work_location','employment_conditions',
                                                       'work_life_balance','workload']].any(axis=1, skipna=False)
dete_resignations_up = dete_resignations.copy()


# In[31]:


tafe_resignations_up['dissatisfied'].value_counts(dropna=False)


# In[32]:


dete_resignations_up['dissatisfied'].value_counts(dropna=False)


# # Creating a new column and dropping columns we don't need.
# Below, we created a new column called `institute` identifying which dataframe each row came from before combining both dataframes together. We then combined our dataframes and then dropped all the columns that we won't need for our analysis.

# In[33]:


#Creating a new column in each dataframe and filling it values identifying which dataframe the row came from.
dete_resignations_up['institute'] = 'DETE'
tafe_resignations_up['institute'] = 'TAFE'

#Combining both dataframes. 
combined = pd.concat([dete_resignations_up, tafe_resignations_up], ignore_index=True)


# In[34]:


#Checking for the sum of non-null values to identify which columns should be dropped.
combined.notnull().sum().sort_values()


# In[35]:


#Dropping columns with less than 500 non-null values.
combined_updated = combined.dropna(thresh = 500, axis = 1)

#Checking to make sure the right columns got dropped.
combined_updated.notnull().sum().sort_values()


# # Cleaning up our `institute_service` column.
# 
# Before we can perform any kind of analysis, we have to clean up the `institute_service` column. It's a bit tricky cleaning up this column as its values come in the following forms: 
#     - NaN                 88
#     - Less than 1 year    73
#     - 1-2                 64
#     - 3-4                 63
#     - 5-6                 33
#     - 11-20               26
#     - 5.0                 23
#     - 1.0                 22
#     - 7-10                21
#     - 0.0                 20
#     ...
# 
# So we have to seperate values into several different categories before we make an analysis. The categories is as follows:
# - New: Less than 3 years at a company
# - Experienced: 3-6 years at a company
# - Established: 7-10 years at a company
# - Veteran: 11 or more years at a company

# In[36]:


#Checking for unique values in 'institute_service' column
combined_updated['institute_service'].value_counts(dropna=False)


# In[37]:


#Change the value type for this column to type 'str'.
combined_updated = combined_updated.copy()

#Extract only the numbers in the string values in the 'institute_service' column.
combined_updated['institute_service_updated'] = combined_updated['institute_service'].astype('str').str.extract(r'(\d+)')
combined_updated['institute_service_updated'] = combined_updated['institute_service_updated'].astype('float')


# In[38]:


#Check values to make sure they are floats.
combined_updated['institute_service_updated'].value_counts().sort_index()


# In[39]:


#Creating a function that maps each value to the career stage definition listed in the markup above.
def mapvalue(val):
    if pd.isnull(val):
        return np.nan
    elif 3 <= val <= 6:
        return 'Experienced'
    elif 7 <= val <= 10:
        return 'Established'
    elif val >= 11:
        return 'Veteran'
    else:
        return 'New'
    
#Applying function to the 'institute_service' column.
combined_updated['service_cat'] = combined_updated['institute_service_updated'].apply(mapvalue)


# In[40]:


#Check for unique values in the column 'service_cat'.
combined_updated['service_cat'].value_counts()


# # Initializing our Analysis.

# In[41]:


#Confirming the number of True and False values in the 'dissatisfied' column.
combined_updated['dissatisfied'].value_counts(dropna=False)


# In[42]:


#Filling in the missing values with the True or False values that occurs more frequently, which is False.
combined_updated['dissatisfied'] = combined_updated['dissatisfied'].fillna(False)


# In[62]:


#Re-confirming the number of True and False values in the 'dissatisfied' column.
combined_updated['dissatisfied'].value_counts()


# In[63]:


diss_pct


# In[49]:


diss_pct = combined_updated.pivot_table(index='service_cat', values='dissatisfied')
get_ipython().run_line_magic('matplotlib', 'inline')
diss_pct.plot(kind='bar', rot=45)


# We've found that over 50% of Established employees of 7-10 years of service resigned because of a dissatisfaction alongside about 50% of Veteran employees with 11 years or more of service, about 35% of Experienced employees with 3-6 years of service, and a little under 30% of New employees with service of less than 3 years.

# # Cleaning the `Age` Column.

# In[50]:


combined_updated['age'].value_counts(dropna=False)


# Here we have to decide what to do with our data in the `age` column.
# - Do we drop all rows containing `NaN` values? Yes.
# - Do we fill the `NaN` values with an age? No.
# - How do we categorize the data? There is one way that comes to mind. First, there are some unique values that appear to be unique but are actually the same as some other unique values in the column. We need to use string methods to combine those values into one type of unique value, and then categorize them accordingly before we make our analyses.

# In[53]:


combined_updated = combined_updated.copy()
combined_updated['age'] = combined_updated['age'].astype('str').str.extract(r'(\d+)')
combined_updated['age'] = combined_updated['age'].astype('float')


# In[57]:


combined_updated['age'].value_counts().sort_index()


# We seperated values in the`age` column into several different categories before making an analysis and a visual. We've decided to seperate them into the following categories: 
# - Young Adults: Employees between the ages of 20 and 30 years old.
# - Middle Age: Employees between the ages of 31 and 50 years old.
# - Older Adults: Employees between the ages of 51 and 60 years old.
# - Elderly: Employees 61 years and older.

# In[60]:


#Function that categorizes the age column.
def map_age(age):
    if pd.isnull(age):
        return np.nan
    elif 20 <= age <= 30:
        return 'Young Adults'
    elif 31 <= age <= 50:
        return 'Middle Age'
    elif 51 <= age <= 60:
        return 'Older Adults'
    else:
        return 'Elderly'

combined_updated['age_cat'] = combined_updated['age'].apply(map_age)


# In[70]:


age_diss_pct = combined_updated.pivot_table(index='age_cat', values='dissatisfied')*100
age_diss_pct


# In[69]:


#Visual representation of the different age groups that were dissatisfied.
age_diss_pct = combined_updated.pivot_table(index='age_cat', values='dissatisfied')*100
get_ipython().run_line_magic('matplotlib', 'inline')
age_diss_pct.plot(kind='bar', rot=45)


# According to the visual above, over 50% of elderly employees ages 61 years or older were dissatisfied. Additionally, over 40% of older adults between the ages of 51-60 years old were dissatisfied, under 40% of Middle-Age adults between the ages of 31 and 50, and about 35% of Young Adults between the ages of 21 and 30 years old. 

# # Checking to see which Survey had more resignations due to Dissatisfactions
# Since we've already created a column in each survey dataframe that identifies which of the resigning employees belong to which survey before combining both dataframes into 1, we can use that column to identify which survey contains to most resigations that were the result of some dissatisfaction.

# In[66]:


#Displaying unique values in the 'institute' column in combined_updated.
combined_updated['institute'].value_counts(dropna=False)


# In[71]:


#Creating a pivot table to see which survey has the most resignations resulting from some dissatisfaction.
survey_diss_pct = combined_updated.pivot_table(index='institute', values='dissatisfied')*100

#Displaying pivot table
survey_diss_pct


# Approximately 47.9% of all resignations for dissatisfactions belonged to the `DETE` survey dataframe, approximately 26.8% to the `TAFE` survey dataframe, and the rest were resignations for other reason other than for dissatisfactions. We can clearly see that `DETE` has the most resignations for dissatisfactions out of the 2 surveys since it has the higher percentage of resignations.

# In[ ]:




