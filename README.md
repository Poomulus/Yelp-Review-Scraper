# Yelp Review Scraper [2019]

_Scrape Yelp Reviews from any page into a .csv file without needing to use API access_

![results](https://i.imgur.com/3d8mlwe.jpg)
____

### How to use it?

Firstly, make sure you have selenium >= 3.141.0 and Chrome or Firefox installed.

Use `reviews.py` to collect the data. 
```
usage: reviews.py [-link]
Data Collection
arguments:

  -link LINK [LINK ...]
                        Link to Yelp Page you want to scrape reviews from
```
Example: ```python reviews.py -link "https://www.yelp.com/biz/mcdonalds-austin-78"```
____
The output is `reviews.csv` inside the script folder.
