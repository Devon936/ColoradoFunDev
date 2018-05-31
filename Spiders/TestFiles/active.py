import urllib.request
import bs4 as bs
import string
import random
import boto3
import time
from datetime import datetime, timedelta, date
from urllib.request import Request, urlopen
from selenium import webdriver
from EventClass import Event

print("ACTIVE")
db = boto3.resource('dynamodb')
table = db.Table('ColoradoFunEvents')

def extract(url):
	base = "https://www.active.com"
	print("Extracting: "+base+url)
	req = Request(base+url, headers={'User-Agent': 'Mozilla/5.0'})
	s = urlopen(req).read()
	soup = bs.BeautifulSoup(s,'lxml')
	info = soup.find(id='body-container')
	
	try:
		event = Event()
		myStr = ""
		for i in range(14):
			myStr+= random.choice(string.ascii_letters + string.digits)
		event.id=myStr
		event.title = info.h1.text
		event.link = base+url
		description = info.find(class_='asset-summary span8').text
		event.description = description
		date = info.h5.text
		event.date = event.dateFinder(date)
		location = info.find(class_='ed-address-text').text
		event.address,event.city, event.state, event.zip, event.lat, event.lng = event.addressFinderBasic(location)
		table.put_item(Item=event.toJSON())
	except:
		print("ERROR: "+str(event.toJSON()))

def main(url):
	base = "https://www.active.com"
	print(url)
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	s = urlopen(req).read()
	soup = bs.BeautifulSoup(s,'lxml')
	
	try:
		nextPage = soup.find(class_ = 'next-page btn-small-yellow').get('href')
		main(base+nextPage)
	except:
		 pass
	for item in soup.findAll('article', {'class' : 'activity-feed ie-activity-list search-item activity with-anchor'} ):
		extract(item.find(class_ = 'ie-article-link').get('href'))

now = date.today()
then = now + timedelta(days=7)
url = 'https://www.active.com/search?&category=running&location=CO%2C+United+States&dateFrom='+str(now.month)+'%2F'+str(now.day)+'%2F'+str(now.year)+'&dateTo='+str(then.month)+'%2F'+str(then.day)+'%2F'+str(then.year)
#url = 'https://www.active.com/running?clckmp=activecom_global_headernav_runningsports_running'
main(url)
