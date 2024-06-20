#!/usr/bin/env python
# coding: utf-8

# ### Data Trasformation  ###

# I will perform some data trasformation based on the observations made in the previous chapter.

# #### Trasformation 1 (based on observation 1) ###

# Let's investigate better how many and which are the negative values present in the columns "Y2012" and "Y2013"

(ffp.loc[:,"Y2012":"Y2013"] < 0.0).sum()


ffp[ffp["Y2012"] < 0.0]


# Since it makes no sense to have a negative value for production, I will replace it with the mean of Oats food production in Japan across all years.


mean_10082 = ffp.loc[10082, "Y1961":"Y2011"].mean()
ffp.at[10082, "Y2012"] = mean_10082
ffp.at[10082, "Y2013"] = mean_10082
ffp.loc[10082, "Y2012":"Y2013"]


# #### Trasformation 2 (based on observation 2) ###

# Let's investigate better which areas are defined by each abbreviation

abb = ffp['Area Abbreviation']
country = ffp['Area']

area_correspondence = (abb.unique()==country.unique())
print("There is an one-to-one correspondence between 'Area Abbreviation' and 'Area' columns: ", str(area_correspondence))


# After running the above code, I can assert that there is not an one-to-one correspondence between 'Area Abbreviation' and 'Area' columns. Thus, let's go deeper into this analysis and find out the extent of the misalignment.

# Create tuples in order investigate which abbreviations do not match with the area name
area_tuples=list(zip(abb,country))
c=Counter(area_tuples)
list(c)


# The above list proofs that we can not rely on 'Area Abbreviation' column's values since the mapping between areas name and their abbreviations is erroneous in these cases:

# Bahamas has been assigned with the 'AZE' abbreviation (it should be given only to Azerbaijan)
# The former Yugoslav Republic of Macedonia has been assigned with the 'THA' abbreviation (it should be given only to Thailand)
# As for the abbreviation 'CHN', we can spot that it gets assigned to four different areas (Hong Kong, Macao, Mainland, Taiwan)

# #### Trasformation 3 (based on observation 3) ###

# Now I am going to delete from fpi dataframe the emissions NOT expressed in kilograms since the total number of null values for these emissions are higher than for those expressed in kilograms.

# Let's first verify if there is a convertion rate between different units of measurement (kcal/kg/100gr protein) for each type of product. In order to find it out I will divide the kcal values by kg values of two different emission types and will check if they match.

unit_convertion = pd.DataFrame(fpi['Eutrophying emissions per 1000kcal (gPO₄eq per 1000kcal)']/fpi['Eutrophying emissions per kilogram (gPO₄eq per kilogram)'], index = fpi.index, columns =['EE:kcal/kg'])
unit_convertion['LU:kcal/kg'] = fpi['Land use per 1000kcal (m² per 1000kcal)']/fpi['Land use per kilogram (m² per kilogram)']

# If there are any NaN values, the 'equals' method will say that  Nan = NaN is false
# Thus, I should transform the unit_conversion dataframe values into boolean type in order to get a correct answer
boolean_uc = unit_convertion.notna()
boolean_uc['EE:kcal/kg'].equals(boolean_uc['LU:kcal/kg'])


# Since I have assessed that there is a conversion rate between different units of measurement for each type of product. I will apply it in order to recostruct the missing values for Greenhouse Gas emission expressed in kilograms. Thus, if (kcal/kg = conv_rate) -> (kg =kcal/conv_rate)

unit_convertion['GGE:kg'] = fpi['Greenhouse gas emissions per 1000kcal (kgCO₂eq per 1000kcal)']/unit_convertion['EE:kcal/kg']
unit_convertion = unit_convertion['GGE:kg'].fillna(0.0)

#unit_convertion

fpi.insert(15, 'GreenhouseGasEmissions_kg', pd.Series(unit_convertion))


columns_to_delete = ['Eutrophying emissions per 1000kcal (gPO₄eq per 1000kcal)',
                    'Eutrophying emissions per 100g protein (gPO₄eq per 100 grams protein)',
                    'Freshwater withdrawals per 1000kcal (liters per 1000kcal)',
                    'Freshwater withdrawals per 100g protein (liters per 100g protein)',
                    'Greenhouse gas emissions per 1000kcal (kgCO₂eq per 1000kcal)',
                    'Greenhouse gas emissions per 100g protein (kgCO₂eq per 100g protein)',
                    'Land use per 1000kcal (m² per 1000kcal)',
                    'Land use per 100g protein (m² per 100g protein)',
                    'Scarcity-weighted water use per 100g protein (liters per 100g protein)',
                    'Scarcity-weighted water use per 1000kcal (liters per 1000 kilocalories)']

fpi = fpi.drop(columns=columns_to_delete)


# At this point, I can change the name of some column headers inside the fpi dataframe so that to remove the spaces in between the words and make them shorter and easier to call

# Replace the columns headers having spaces in between the words
fpi.rename(columns = {'Land use change': 'LandUseChange', 
                     'Animal feed': 'AnimalFeed',
                     'Total_emissions': 'TotalEmissions'}, 
            inplace = True)

# Replace the columns headers with a very long name with a shorter name
fpi.rename(columns = {'Eutrophying emissions per kilogram (gPO₄eq per kilogram)': 'EutrophyingEmissions_kg',
                     'Freshwater withdrawals per kilogram (liters per kilogram)': 'FreshwaterWithdrawals_kg',
                     'Land use per kilogram (m² per kilogram)': 'LandUse_kg',
                     'Scarcity-weighted water use per kilogram (liters per kilogram)': 'ScarcityWeightedWaterUse_kg'},
           
          inplace = True)

fpi.head(10)

fpi.shape


# #### Trasformation 4: check if possible to match the food type among the two datasets ###

# Let's verify now if we can merge the two datasets. The only value that they have in common is the food products list.

shape_data = ffp.groupby(by='Element')
shape_data = shape_data.get_group('Food')
food_list = shape_data['Item'].unique()
print("Food products presents in the ffp dataset:", len(food_list))
print("Food products presents in the fpi dataset:", len(fpi.index))


# The total amount of food products items listed in the two datasets is too different. The ffp dataset holds almost three times more food products than the fpi dataset. Unfortunately, there isn't any intelligent and fast way of grouping and matching the above food lists except than by doing it manually.

# #### Trasformation 5: prepare data hold in the ffp dataset for visualization ###

# I am going to group the data inside the ffp dataframe by "Element" values, in order to extract the mean production estimates for food and feed production across all countries for each year.

element_mean_ffp = ffp.groupby(["Element"]).mean()
element_mean_ffp.head()


# I am going to group the data inside the ffp dataframe by "Area" values, extract from the latest aggregated estimations such as sum/max/mean and save this information into a new dataframe called "totals_ffp".

# Group the information inside ffp by "Area" and compute the cumulative sum for each area for each year
area_sum_ffp = ffp.groupby(["Area"]).sum()

# Populate the new dataframe "totals_ffp" with the columns: latitude, longitude, TotalProduction (sum upon all years)
totals_ffp = pd.DataFrame(data=[area_sum_ffp['latitude'], area_sum_ffp['longitude'],
                                area_sum_ffp.loc[:,"Y1961":"Y2013"].sum(axis=1)])
totals_ffp = totals_ffp.T
totals_ffp.rename(columns = {'Unnamed 0': 'TotalProduction_Y1961:Y2013'}, inplace = True)

# Calculating Percentage
totals_ffp['TotalProduction_%'] = (totals_ffp['TotalProduction_Y1961:Y2013'] / totals_ffp['TotalProduction_Y1961:Y2013'].sum()) * 100

# Round to two numbers after .
totals_ffp = totals_ffp.round(decimals=2)

# Display the "totals_ffp" dataframe
totals_ffp.sort_values(by = 'TotalProduction_Y1961:Y2013', ascending = False)


# I am going to apply multiple grouping on the ffp dataframe, in order to extract for each country the proportion among total production of food and feed upon all years.

# Group the information inside ffp by ["Area", "Element"] and compute the cumulative mean for each area and type of product, for each year
grouped_mean_ffp = ffp.groupby(["Area","Element"]).mean()

# Create the series with the total "Mean" (mean upon all years)
mean_ffp = grouped_mean_ffp.loc[:,"Y1961":"Y2013"]
general_mean_ffp = pd.Series(data=mean_ffp.mean(axis=1), index = grouped_mean_ffp.index, name="mean")
general_mean_ffp.head()

