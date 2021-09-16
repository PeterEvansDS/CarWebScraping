#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 13:56:31 2021

@author: peterevans
"""

import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from tqdm import tqdm

def try_find(s, var):
    
    if var == 'reviews':
        try:
            x = s.find(itemprop = 'reviewCount').attrs['content']
            return x
        except:
            return np.nan
    elif var == 'delivery':
        try:
            x = s.find('div', class_ = "delivery")
            x.find('strong', class_ = 'strong-inline').text
            return True
        except:
            return False
    elif var == 'variant':
        try:
            x = s.find('span', class_='variant new-transport--regular').text
            return x
        except:
            return np.nan
    else:
        print('ERROR: Variable not accounted for.')


def get_query_data(url):
    """find the individual links of each sale,
    and the distances to each sale, as these are not available on the individual pages"""
    querypage = requests.get(url)
    soup = bs4.BeautifulSoup(querypage.text, 'html.parser')
    sales = soup.find_all('div', {'class':'vl-item clearfix'})
    # titles = [s.find('h3').text.replace('\n', ' ').strip() for s in sales]
    links = [s.find('a')['href'] for s in sales]
    distances = [s.find('div', class_='vl-location').find('strong').text for s in sales]
    return links, distances

def get_data(links):

    """access each listing's individual page and extract its data"""

    pages = [requests.get(r'https://www.theaa.com/{}'.format(l)) for l in links]
    soups = [bs4.BeautifulSoup(p.text, 'html.parser') for p in pages]
    titles = [s.title.text for s in soups]
    makes = [s.find('span', class_='make').text for s in soups]
    models = [s.find('span', class_='model').text for s in soups]
    variants = [try_find(s, 'variant') for s in soups]
    prices = [s.find('strong', class_='total-price').text for s in soups]
    specs = [s.find_all('span', class_='vd-spec-value') for s in soups]
    spec_no = [len(s) for s in specs]
    mileages = [s[0].text for s in specs]
    years = [s[1].text for s in specs]
    fuels = [s[2].text for s in specs]
    transmissions = [s[3].text for s in specs]
    bodies = [s[4].text for s in specs]
    colours = [s[5].text for s in specs]
    doors = [s[6].text for s in specs]
    #later specs only applicable to non-electric cars
    enginesizes = [s[7].text if len(s) == 9 else np.nan for s in specs]
    co2 = [s[8].text if len(s) == 9 else np.nan for s in specs]
    no_reviews = [try_find(s, 'reviews') for s in soups]
    delivery = [try_find(s, 'delivery') for s in soups]

    data = pd.DataFrame({'title':titles, 'make':makes, 'model':models, 'variant':variants,
                         'price':prices, 'no specs':spec_no, 'mileage':mileages,
                         'year':years, 'fuel':fuels, 'transmission':transmissions,
                         'body type':bodies, 'colour':colours, 'doors':doors,
                         'engine size':enginesizes, 'CO2':co2, 'review count':no_reviews,
                         'delivery':delivery})
    return data

if __name__ == "__main__":

    urls =[r'https://www.theaa.com/used-cars/displaycars?fullpostcode=MK181EG&sortby=\
           closest&page={}&pricefrom=0&priceto=1000000'.format(i) for i in range(1,51)]
    
    links, distances = get_query_data(urls[0])
    df = get_data(links)
    df.insert(len(df.columns)-1, 'distance', distances)
    for i in tqdm(range(1,50)):
        links, distances = get_query_data(urls[i])
        df_temp = get_data(links)
        df_temp.insert(len(df.columns)-1, 'distance', distances)
        df = pd.concat([df, df_temp], ignore_index=True)
    
    
    df.to_csv('./cars.csv')
