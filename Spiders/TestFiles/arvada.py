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

print("ARVADA")
db = boto3.resource('dynamodb')
table = db.Table('ColoradoFunEvents')
	
def extract(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	print("Extracting: "+url)
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
		event.date = datetime.datetime.strptime(info.find(class_='mn-event-day').text, '%B %d, %Y').strftime('%Y-%m-%d')
		#event.category = event.categoryFinder(description)
		location = info.find(itemprop='name').text
		event.address,event.city, event.state, event.zip, event.lat, event.lng = event.addressFinder(location)
		table.put_item(Item=event.toJSON())
	except:
		print("ERROR: "+str(event.toJSON()))
	
	
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
	
