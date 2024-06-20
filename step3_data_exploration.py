#!/usr/bin/env python
# coding: utf-8

# ### Data Exploration ###

# The data exploration step is very important since it allows to grasp the means and value of data content. In fact, this part of data analysis requires to carefully observe the data in order to spot any pitfalls or non-sense content and process the data accordingly.

# From the print of ffp.head () I have already got several useful data insights, such as the number and name of the dataset variables and their content. However, in order to get more precise metadata, I will use the ffp.type function, which will show me the type of each column.

ffp.dtypes.head(10)


# I see that in the ffp dataframe most of the variables are quantitative. Thus, I will run the .describe () method over the years columns in order to get some statistical insights over the numerical data.

columns_to_drop = list(ffp.columns)[0:6]
ffp_qtv = ffp.drop(columns_to_drop, axis=1)
ffp_qtv = ffp_qtv.describe(include="all")
ffp_qtv


# #### OBSERVATION 1 ###

# Most years have missing values. In fact only the last 2 years are fully documented.
# Both mean and std increse over the years, which means that food/feed production has constatly increased over the years but in uneven manner since the difference between areas' year production gets bigger as well.
# The last two years hold negative values (must investigate deeper since it makes no sense)
# As for the qualitative variables(Area Abbreviation, Area, Item, Element), I must adopt another method. The most suitable method is the value_counts(), which counts the occurrences of a certain value in the variable.


ffp_qlt = pd.DataFrame(ffp[['Area Abbreviation', 'Area', 'Item', 'Element']])
df1 = ffp_qlt["Area Abbreviation"].value_counts().sort_values(ascending=False)
df1.head(10)


df2=ffp_qlt["Area"].value_counts().sort_values(ascending=False)
df2.head(10)


# #### OBSERVATION 2 ###

# On global scale, the top three countries with the most diversified food/feed proposal are CHN, THA, AZE (must investigate better which areas are defined by each abbreviation)
# On regional scale (similar area extention), the top areas with the most diversified food/feed proposal are Spain, Italy, Germany.
# Regarding the fpi dataframe, I will run the describe() method over the columns following "Total Emission" column in order to get some statistical insights over the listed emissions' numerical data.


fpi_other_em = fpi.loc[:, 'Eutrophying emissions per 1000kcal (gPO₄eq per 1000kcal)' : 'Scarcity-weighted water use per 1000kcal (liters per 1000 kilocalories)']
fpi_other_em.describe(include="all")


# #### OBSERVATION 3 ###

# To each type of emission is dedicated more than one column since it is expressed in different units of measurement.
# The greenhouse gas emission doesn't have the column with values expressed in kilograms.
