
#importing the needed repositories for webscraping and writing to .csv files
from bs4 import BeautifulSoup
import requests
import csv

#initializing empty lists. The lists will eventually be filled through scraping and then read into the .csv file
prices = []
addresses = []
details1 = []
links= []

#the purpose of this function as a whole is to go through the desired elements within each web page and put the desired elements into their appropriate list to be written to csv file later.
def getListings(page):

    URL= 'https://www.dhomes4u.com/cgi-bin/real?myid=83735465&pge=ia_search&curpage='
    req = requests.get(URL + str(page))


    soup= BeautifulSoup(req.text, 'lxml')
    listings = soup.find_all('div', class_='viewgrid_cell')
    for listing in listings:
        prices.append(listing.find('div', class_='viewgrid_price').text)
        addresses.append(listing.find('div', class_='viewgrid_addr').text)
        details1.append(listing.find('div', class_='viewgrid_info').text)
        links.append(listing.div.a['href'])

#Using this range as there are 224 total pages worth of listings on the site we are scraping.    
for x in range(1,225):
    getListings(x)

#opening the csv file and getting it ready to be written to
with open('UT_Listings.csv','w', newline='') as f:
    contents = csv.writer(f)

#before i start writing the scraped info to the file, I need to  create titles for each row which is what the line below is accomplishing
    contents.writerow(['Price', 'Address', 'Details', 'Link'])

#this for loop is used to write the populated lists to the csv file
    for i in range(len(prices)):
        contents.writerow([prices[i], addresses[i], details1[i], links[i]])


    