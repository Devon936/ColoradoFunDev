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

print("ARVADA")
db = boto3.resource('dynamodb')
if(len(sys.argv) == 2): # action with given argument
	print("Custom Behavior: Saving to ", sys.argv[1])
	table = db.Table(sys.argv[1])
else: # default action
	print("Default Behavior: Saving to Development Database")
	table = db.Table('ColoradoFunDevTable')
	
def extract(url):
	try:
		req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		print("Extracting...")
		s = urlopen(req).read()
		soup = bs.BeautifulSoup(s,'lxml')
		info = soup.find(class_='mn-section mn-event-detail-listing')
		
		try:
			event = Event()
			myStr = ""
			for i in range(14):
				myStr+= random.choice(string.ascii_letters + string.digits)
			event.id=myStr

			event.title = info.find(class_='mn-event-content').text
			event.link = url
			description = info.find(itemprop='description').text
			event.description = description
			#event.short_description = description[:92]+"..."
			event.date = datetime.strptime(info.find(class_='mn-event-day').text, '%B %d, %Y').strftime('%Y-%m-%d')
			#event.category = event.categoryFinder(description)
			location = info.find(itemprop='name').text
			event.address, event.city, event.lat, event.lng = event.addressFinder(location)
			if(type(event.lat)!=str):
				event.lat = str(event.lat)
				event.lng = str(event.lng)
				print("SUCCESS\n")
				table.put_item(Item=event.toJSON())
			else:
				event.address, event.city, event.lat, event.lng = event.addressFinderBasic(location)
				if(type(event.lat)!=str):
					event.lat = str(event.lat)
					event.lng = str(event.lng)
					print("Success\n")
					table.put_item(Item=event.toJSON())
				else:
					print("address failure\n")
		except:
			print("Event error",url,"\n")
	except:
		print("Page error", url,"\n")
	
def main(url,num):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	s = urlopen(req).read()
	soup = bs.BeautifulSoup(s,'lxml')
	if(num<4):
		main(soup.find(class_='mn-cal-next').a.get('href'),num+1)
	table = soup.find(class_='mn-cal-grid')
	for e in table.find_all('li'):
		extract(e.a.get('href'))
main('http://business.arvadachamber.org/events/calendar',0)
	
