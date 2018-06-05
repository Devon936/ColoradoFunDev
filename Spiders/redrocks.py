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
	sleep(0.2)
	try:
		if(url[:3]=="http"):
			req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		else:
			req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		s = urlopen(req).read()
		soup = bs.BeautifulSoup(s,'lxml')
		info = soup.find(class_='full m-event-detail clearfix')
		#print("\n-----> Extracting: ",base+url)
		try:
			event = Event()
			myStr = ""
			for i in range(14):
				myStr+= random.choice(string.ascii_letters + string.digits)
			event.id=myStr

			event.title = info.h1.text
			event.link = url
			description = info.find(class_='m-event-detail-description').text
			event.description = description
			date = info.find(class_="m-date__singleDate").text
			event.date = event.dateFinder(date)
			#location = "18300 W Alameda Pkwy, Morrison, CO 80465"
			event.lng = "-105.2048546"
			event.lat = "39.6664666"
			event.city = "Morrison"
			event.address = "8300 W Alameda Pkwy"
			print("\n\n Item: ",event.title)
			table.put_item(Item=event.toJSON())
		except:
			print("Info error", url)
	except:
		print("Page error", url)

def main(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	s = urlopen(req).read()
	soup = bs.BeautifulSoup(s,'lxml')
	for item in soup.find(class_='list'):
		i = item.find('a')
		if(i!= -1):
			extract(i.get('href'))
url = 'http://www.redrocksonline.com/concerts-events'
main(url)