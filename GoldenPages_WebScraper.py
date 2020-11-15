# Author: Shalom Osiadi #
# Resource: https://www.youtube.com/watch?v=PhJFg1THF9E #

"""

Things to note:
    1. If using this script on a different computer make sure to change the User-Agent (currently in headers variable
    2. This script will only work on the Goldenpages.ie

"""

import requests
from lxml import html
import unicodecsv as csv
import argparse
from bs4 import BeautifulSoup
import pandas as pd
import time
import re


main_list = [] #declaring a blank list variable to put our data in at the end

url = "https://www.goldenpages.ie/q/business/advanced/where/Dublin/what/Restaurants/"
#The URL we want to search
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
#BeautifulSoup requires your PC user agent to work properly
r = requests.get(url, headers=headers)
#The above will be specified to the server when we make the request
soup = BeautifulSoup(r.content, 'html.parser')

#Now we need to find the specific data we need from the webpage
#Everytime our script sees a class that matches the below it will pull it as a result
results = soup.find_all('div', class_ = 'listing_container')
for item in results:
    name = item.find('a', class_ = 'listing_title_link').text.strip().replace('\n', '') #should replace numbers with nothing
    biz = re.sub(r'[0-9.]+', '', name) #this will remove any numbers or special characters from the 'name' variable
    address = item.find('div', class_ = 'listing_address').text
    number = item.find('div', class_ = 'listing_number').text.strip().replace('\n','') #replace blank lines with nothing
    ul = item.find('ul', {'class': 'list_inline pull_left'})
    website = ul.find('a', {'href': True})['href']
    #The above ul & website variables are just pulling the href tag to display the websites of our items
    #if no website exists it gives the href of 'Directions' instead

def extract(url):
    url = "https://www.goldenpages.ie/q/business/advanced/where/Dublin/what/Restaurants/"
    #The URL we want to search
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    #BeautifulSoup requires your PC user agent to work properly
    r = requests.get(url, headers=headers)
    #The above will be specified to the server when we make the request
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup.find_all('div', class_ = 'listing_container')

def transform(results):
    for item in results:
        try:
            name = item.find('a', class_ = 'listing_title_link').text.strip().replace('%d','') #should replace numbers with nothing
        except:
            name = '' #if pulling the name variable results in an error ignore it and give me blank
        address = item.find('div', class_ = 'listing_address').text
        try:
            number = item.find('div', class_ = 'listing_number').text.strip().replace('\n','') #replace blank lines with nothing
        except:
            number = ''
        ul = item.find('ul', {'class': 'list_inline pull_left'})
        try:
            website = ul.find('a', {'href': True})['href']
        except:
            website = ''
        #The above ul & website variables are just pulling the href tag to display the websites of our items
        #if no website exists it gives the href of 'Directions' instead
        business = {'name': name, 'address': address, 'number': number, 'website': website}
        #{} signifies a python dictionary
        main_list.append(business)
        #putting 'business' dictionary inside our list created above
    return

for x in range(1,11):
    print(f'getting page {x}')
    result = extract(f'https://www.goldenpages.ie/q/business/advanced/where/Dublin/what/Restaurants/{x}')
    transform(result)
    time.sleep(3)
#whenever we run this script the above will loop through all the page numbers of our desired URL starting at page 1 up to page 10
#The f at the start tells python that we want it to search through all variations of x
#time.sleep() makes sure our script isn't overloading the golden pages server with requests to avoid us getting blocked

transform(result)
print(len(main_list))

def load():
    df = pd.DataFrame(main_list)
    df.to_csv('RestaurantsInDublin.csv')

load()
print("Saved To CSV")
