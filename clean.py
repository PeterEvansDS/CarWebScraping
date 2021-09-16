
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm


df= pd.read_csv(r'/Users/peterevans/UniCloud/Scripting/Assignment1/cars1.csv', index_col=0)

#convert numerical columns values to ints or floats, after deleting units where appropriate
df['price'] = df['price'].map(lambda x: pd.to_numeric(x.replace('£','').replace(',','')))
df['mileage'] = df['mileage'].map(lambda x: pd.to_numeric(x.replace(',','')))
df['year'] = df['year'].map(lambda x: pd.to_numeric(x))
df['doors'] = df['doors'].map(lambda x: pd.to_numeric(x))
df['engine size'] = df['engine size'].map(lambda x: pd.to_numeric(x.replace('L', '')), na_action = 'ignore')
df['CO2'] = df['CO2'].map(lambda x: pd.to_numeric(x.replace('g/km', '')), na_action = 'ignore')
df['review count'] = df['review count'].map(lambda x: pd.to_numeric(x))

#rename columns to include units
df.rename(columns={'price':'price (£)', 'mileage':'mileage (miles)',
                 'engine size':'engine size (L)', 'CO2':'CO2 (g/km)'}, inplace = True)

#transform 'make' column
print("UNIQUE VALUES OF MAKE:\n", pd.unique(df.make))
df['make'] = df['make'].map(lambda x: x.title())
print("UNIQUE VALUES OF MAKE AFTER .title()\n", pd.unique(df.make))
df['make'].replace('Mercedes', 'Mercedes-Benz', inplace=True)
df['make'].replace('Bmw', 'BMW', inplace=True)
print("FINAL VALUES OF MAKE:\n", pd.unique(df.make))

#transform 'model' column
df['model'] = df['model'].map(lambda x: x.title())
grouped_cars = df.groupby(['make','model']).size()
df['model'].replace({'A Class':'A-Class', 'C Class':'C-Class', 'E Class':'E-Class',
                   'S Class':'S-Class', 'Hatchback':'Hatch', 'X Trail':"X-Trail",
                   'Zafira Tourer':'Zafira'},
                  inplace = True)

#transform 'variant' column
grouped_variant = df.groupby(['make', 'model', 'variant']).size()
df['variant'] = df['variant'].map(lambda x: x.title().strip())

#check and transform 'fuel'
print('\nBEFORE UNIQUE VALUES OF FUEL: ', df.fuel.unique())
df['fuel'].replace({'Petrol hybrid': 'Hybrid', 'Petrol/plugin elec h':'Hybrid',
                  'Petrol/electric hybr':'Hybrid', 'Petrol / electric hy':'Hybrid',
                  'Hybrid – petrol/elec':'Hybrid'}, inplace = True)
print('AFTER UNIQUE VALUES OF FUEL: ', df.fuel.unique())

#check and transform 'transmission'
print('\nUNIQUE VALUES OF TRANSMISSION: ', df.transmission.unique())
df.transmission.replace({'Semi auto': 'Semiauto', 'Semi automatic': 'Semiauto'}, inplace = True)
print('UNIQUE VALUES OF TRANSMISSION AFTER REPLACE: ', df.transmission.unique())

#check 'bodytype'
print('\nBEFORE UNIQUE VALUES OF BODYTYPE: ', df['body type'].unique())
df['body type'].replace({'Window van':'Van', 'Panel van':'Van',
                       'Combi van':'Van', 'High volume/high roof van':'Van',
                       'Station wagon':'Estate', 'Double cab pick-up':'Pickup',
                       'Camper van':'Motor caravan'},
                       inplace = True)
print('AFTER UNIQUE VALUES OF BODYTYPE: ', df['body type'].unique())

#check and transform 'colour'
print('\nBEFORE UNIQUE VALUES OF COLOUR: ', df.colour.unique())
colour_changes = {'Montalcino red pearl':'Red', 'Sport red':'Red', 'Crossover black':'Black',
                'Avantgarde bordeaux':'Dark Red', 'Ambient white':'White', 'Pasodoble red':'Red',
                'Tech house grey':'Grey', 'Bossanova white':'White', 'Epic blue':'Blue',
                'Glam coral':'Red', 'Smooth mint':'Light Blue', 'Electronica blue':'Blue',
                'Electroclash grey':"Grey", 'Volare blue':'Blue', 'Exotica red':'Red',
                'Pearl black':'Black', 'Gun metallic':'Grey', 'Ebisu black':'Black',
                'Blade silver':'Silver', 'Storm white':'White', 'Ink blue':'Blue',
                'Spring cloud':'Silver', 'Nightshade':'Black', 'Arctic white':'White',
                'Vivid blue':'Blue', 'Magnetic red':'Red', 'Titanium olive':'Green',
                'Solid white':'White', 'Power blue':'Blue', 'Enigma black':'black',
                'Pearl - pearl white':'White', 'Special - vertigo blue':'Blue',
                'Pearlescent - pearlescent white':'White', 'Metallic - perla nera black':'Black',
                'Metallic - cumulus grey':'Grey', 'Special metallic - cumulus grey':'Grey',
                'Grey colour':'Grey', 'Metallic - platinum grey':'Grey',
                'Special metallic - platinum grey':'Grey', 'Special - arctic steel':'Silver',
                'Blue colour':'Blue', 'Special solid - lipizzan white':'White',
                'Metallic - green fizz':'Green', 'Metallic - raven black':'Black', 'Standard':'Other',
                'Silver colour':'Silver', 'Platinum silver':'Silver',
                'Metallic - nimbus grey':'Grey', 'Metallic - obsidian black':'Black', 'N/a':'Other'}
df.colour.replace(colour_changes, inplace = True)
df.colour = df.colour.map(lambda x: x.title().strip())
print('AFTER UNIQUE VALUES OF COLOUR: ', df.colour.unique())

#check and transform distance
df['distance'] = df['distance'].map(lambda x: pd.to_numeric(x.split()[0]))
print('\nUNIQUE VALUES OF DISTANCE: ', df.distance.unique())

#% 1c) Calculate the total car sales based on the “registration year” feature

no_sales = df.groupby('year').size()
plot1 = plt.figure(1)
sns.set_theme()
ax = sns.lineplot(data = no_sales)
ax.set(xlabel='Registration Year', ylabel='Number of sales', title = 'Number of Sales')
plt.show()

sales_total = df.groupby('year').sum()['price (£)']
plot2 = plt.figure(2)
ax = sns.lineplot(data=sales_total)
ax.set(xlabel='Registration Year', ylabel = 'Sales total (£)', title = 'Total Sales (£)')
plt.show()

#% 1d) Compare car sales on their transmission features

sales_transmission = df.groupby(['year', 'transmission'], as_index=False).size()
plot1 = plt.figure(1)
ax = sns.lineplot(data = sales_transmission, x = 'year', y='size', hue = 'transmission',
                style = 'transmission', markers = True)
ax.set(xlabel='Registration Year', ylabel='Number of sales', title = 'Number of Sales')
plt.show()

sales_transmission_total = df.groupby(['transmission'], as_index=False).size()
plot2 = plt.figure(2)
ax = sns.barplot(data = sales_transmission_total, x='transmission', y='size',
               order =['Manual', 'Automatic', 'Semiauto'])
ax.set(xlabel='Transmission', ylabel='Number of sales', title = 'Sales by Transmission')
plt.show()

#% 1e) What are the most popular car sales based on the “Body Type”?

body_type_sales = df.groupby(['body type'], as_index=False).size()
plot1 = plt.figure(1)
ax = sns.barplot(data = body_type_sales, x='body type', y='size',
               order = body_type_sales.sort_values('size')['body type'])
ax.set(xlabel='Body Type', ylabel='Number of sales', title = 'Number of Sales')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
plt.show()

#% 1f) List top 10 cars having highest numbers of reviews.

review_list = df.groupby(['make', 'model'], as_index=False).mean()\
  .sort_values(by=['review count'], ascending = False)[['make', 'model','review count']]

print('\n10 Cars with highest review count: \n', review_list.head(10))
