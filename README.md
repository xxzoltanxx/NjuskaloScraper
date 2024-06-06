# njuskalo-scraper

</p>
<h3 align="center">An open-source Python program to scrape Njuskalo Playwright and BeautifulSoup.
<h3 align="center">

```diff
You use the software provided at your own risk. I cannot be held responsible for any potential consequences, including any potential damages.
```
### Overview
This open-source program uses Python to scrape data from Njuskalo.hr. The program uses Playwright to navigate Njuskalo and BeautifulSoup to parse the HTML and extract relevant data. It then saves the data in json format inside the directory of your choosing.

### Data format
```
  {
    "name": "ADVERT NAME",
    "location": "LOCATION DATA, KILOMETERS, YEAR OF CAR" ,
    "time": "DATE POSTED",
    "price": "PRICE"
  },
```
  
### Language: 
- [Python](https://www.python.org/)

### Requirements:
- Python 3.x
- Playwright
- Streamlit
- BeautifulSoup 
  
### Modules:
- Playwright for web crawling
- BeautifulSoup for HTML parsing
- JSON for data formatting