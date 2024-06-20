#!/usr/bin/env python
# coding: utf-8

# ### Data Cleaning  ###

# The Data Cleaning step is necessary because it allows to: 
# get meaningful results by filling up the cells with NaN values
# dropping the rows/columns which doesn't bring any value to the overall analysis

# Thus, in order to proceed with data cleaning, it is usefull to know which are the missing values and how many they are.

ffp.shape


ffp_missing_values = ffp.isna().sum()
ffp_missing_values


# There are missing values in this dataframe because countries which were formed lately, such as South Sudan and Russian Federation, were kept, even though they do not have all full data going back to 1961.


# I am filling the missing values with 0, since it could be misleading replacing the NaN values 
# with any other central tendancy measures (mean, median)
ffp = ffp.fillna(0.0)

# Now, I will remove from the ffp dataframe the columns that aren't useful to my analysis.

# Before deleting the column, verify if the unit of measurement is unique
ffp['Unit'].unique()


columns_to_delete = ["Area Code", "Item Code", "Element Code","Unit"]
ffp = ffp.drop(columns=columns_to_delete)
ffp = ffp.sort_values(by = "Area Abbreviation")
ffp.head()

# At this point, I can proceed with cleaning the fpi dataframe.
fpi.shape


fpi_missing_values =fpi.isna().sum()
fpi_missing_values


# It can be observed that emissions not expressed in kilograms have more missing values.

# Replace the NaN with 0
fpi = fpi.fillna(0.0)


