# CarWebScraping
Building a used car dataset by scraping the most recently listed vehicles on theaa.com, utilising BeautifulSoup and Requests Python libraries.

Objectives when writing the script were:

- Collect 1000 items returned by search query of the website and save them into csv files, with data including:
Sale’s title, Distance, Price in GBP, Registration Year etc.
- Calculate the total car sales based by Registration Year
- Compare car sales on their transmission features
- Determine the most popular car sales based on Body Type
- List top 10 cars with highest numbers of reviews.

A breakdown of the process is written up in [the project report](/report.pdf).

**NOTE**: clean_and_visualize.py is specific to the dataset originally scraped, cars1.csv. As the page is constantly updating, any newly scraped data will require adjustments to this script.

![alt text](https://github.com/PeterEvansDS/CarWebScraping/blob/main/images/theaa.png?raw=true)
