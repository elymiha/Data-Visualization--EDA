#!/usr/bin/env python
# coding: utf-8

# ### DATA SELECTION ###

# Now, I am going to upload both datasets and take a look at their content.

# WORLD FOOD/FEED PRODUCTION dataset will be uploaded into the "ffp" dataframe (ffp stands fo "food feed production")
# ENVIRONMENT IMPACT OF FOOD PRODUCTION dataset will be uploaded into the "fpi" dataframe (fpi stands fo "food production impact")

# Let's first give a look at WORLD FOOD/FEED PRODUCTION dataset.

ffp = pd.read_csv("FAO.csv", encoding='latin1')
ffp.head()


# The above dataset's attributes are:

# - Country name abbreviation 
# - Country code 
# - County name 
# - Item code 
# - Item (type of product) 
# - Element code 
# - Element (Food or Feed) 
# - Latitude (the north–south position of a point on the Earth's surface) 
# - Longitude (the east-west position of a point on the Earth's surface) 
# - Production per year (food items produced in 1000 tonnes).

# The dataset provided by FAO defines each food item in two ways:

# Food: refers to the total amount of the food item available as human food during the reference period.
# Feed: refers to the quantity of the food item available for feeding to the livestock and poultry during the reference period.

# Now, let's load and give a look at the ENVIRONMENT IMPACT OF FOOD PRODUCTION dataset.
fpi = pd.read_csv("Food_Production.csv")
fpi.head()

type_products = fpi['Food product'].unique()
len(type_products)


# The Food Production dataset has only quantitative variables, except the first column "Food product", which has unique (different type of food) qualitative variables. At this point it makes sense to reindex the fpi dataframe by defining the "Food product" column as the index column.

fpi = pd.read_csv("Food_Production.csv", index_col = 'Food product')
fpi.head()


# The first 7 columns concurr at defining the values inside the column "Total_Emissions", whereas other columns express food type production impact in terms of eutrophying emission/ freshwater withdrawals/greenhouse gas emission/ land use change/scarsity-weighted water use.
