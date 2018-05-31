import csv
import pyap
import re
import geocoder
import datetime
import json

class Event:
	def __init__(self):
		self.id = ""
		self.title = ""
		self.link = ""
		self.description = ""
		self.date = ""
		self.category = []
		self.address = ""
		self.city = ""
		self.lat = ""
		self.lng = ""
		self.image = ""

	def toJSON(self):
		jd = {}
		jd['id']=self.id
		jd['title'] = self.title
		jd['link'] = self.link
		jd['description'] = self.description
		jd['date'] = self.date
		jd['category'] = self.category
		jd['address'] = self.address
		jd['city'] = self.city
		jd['lat'] = self.lat
		jd['lng'] = self.lng
		jd['image'] = self.image
		return jd
		
	def addressFinder(self,string):
		try:
			found_address = str(pyap.parse(string, country='US')[0])
			g = geocoder.google(found_address)
			address = g.housenumber +" "+ g.street
			return address, g.city, g.state, g.postal, g.lat, g.lng
		except:
			return "","","","","",""

	def addressFinderBasic(self,string):
		try:
			g = geocoder.google(string)
			address = g.housenumber +" "+ g.street
			return address, g.city, g.state, g.postal, g.lat, g.lng
		except:
			return "","","","","",""

	def categoryFinder(self,information):
		categoryList = [' running', ' bicycle',' music ','riveer rafting',' zip line',' horseback', ' free']
		ans = ""
		for word in categoryList:
			if(word in information):
				ans = ans + word
		return ans
		
	def dateFinder(self, string):
		regex = r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?) {1,2}(?:\d{1,2}), (?:2\d{3})"
		ans = re.findall(regex,string);
		return(datetime.datetime.strptime(ans[0], '%B %d, %Y').strftime('%Y-%m-%d'));


