import urllib.request
import bs4 as bs
import string
import random
import boto3
import time
import sys
from datetime import datetime, timedelta, date
from urllib.request import Request, urlopen
from selenium import webdriver
from EventClass import Event
from time import sleep

print("ACTIVE")

db = boto3.resource('dynamodb')
if(len(sys.argv) == 2): # action with given argument
	print("Custom Behavior: Saving to ", sys.argv[1])
	table = db.Table(sys.argv[1])
else: # default action
	print("Default Behavior: Saving to Development Database")
	table = db.Table('ColoradoFunDevTable')

def extract(url):
	base = "https://www.active.com"
	sleep(0.2)
	try:
		if(url[:3]=="http"):
			req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		else:
			req = Request(base+url, headers={'User-Agent': 'Mozilla/5.0'})
		s = urlopen(req).read()
		soup = bs.BeautifulSoup(s,'lxml')
		info = soup.find(id='body-container')
		#print("\n-----> Extracting: ",base+url)
		try:
			event = Event()
			myStr = ""
			for i in range(14):
				myStr+= random.choice(string.ascii_letters + string.digits)
			event.id=myStr

			event.title = info.h1.text
			event.link = base+url
			print("Title: ",event.title)
			description = info.find(class_='asset-summary span8').text
			event.description = description
			date = info.h5.text
			event.date = event.dateFinder(date)
			location = info.find(class_='ed-address-text').text
			event.address, event.city, event.lat, event.lng = event.addressFinder(location)
			if(type(event.lat)!=str):
				event.lat = str(event.lat)
				event.lng = str(event.lng)
				print("SUCCESS")
				table.put_item(Item=event.toJSON())
			else:
				event.address, event.city, event.lat, event.lng = event.addressFinderBasic(location)
				if(type(event.lat)!=str):
					event.lat = str(event.lat)
					event.lng = str(event.lng)
					print("Success")
					table.put_item(Item=event.toJSON())
				else:
					print("address failure")
		except:
			print("Error")
	except:
		print("Page error", base+url)

def main(url):
	base = "https://www.active.com"
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	s = urlopen(req).read()
	soup = bs.BeautifulSoup(s,'lxml')
	try:
		nextPage = soup.find(class_ = 'next-page btn-small-yellow').get('href')
		main(base+nextPage)
	except:
		 pass
	for item in soup.findAll('article', {'class' : 'activity-feed ie-activity-list activity with-anchor'} ):
		extract(item.find(class_ = 'ie-article-link').get('href'))

now = date.today()
then = now + timedelta(days=2)
url = 'https://www.active.com/search?&location=CO%2C+United+States&dateFrom='+str(now.month)+'%2F'+str(now.day)+'%2F'+str(now.year)+'&dateTo='+str(then.month)+'%2F'+str(then.day)+'%2F'+str(then.year)
main('https://www.active.com/running')
main('https://www.active.com/cycling')
main('https://www.active.com/swimming')
main(url)
