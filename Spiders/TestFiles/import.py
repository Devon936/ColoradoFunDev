import boto3
import string
import random
from EventClass import Event
import random
from elizabeth import Text, Address
import datetime

if(len(sys.argv) == 2): # action with given argument
	print("Custom Behavior: Saving to ", sys.argv[1])
	db = boto3.resource('dynamodb')
	table = db.Table(sys.argv[1])
else: # default action
	print("Default Behavior: Saving to Development Databasee")
	db = boto3.resource('dynamodb')
	table = db.Table('ColoradoFunDevTable')
	
text = Text('en')
address = Address('en')

now = datetime.datetime.now()
def random_date(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

for i in range(50):
	event=Event()
	myID = ""
	for i in range(14):
		myID+= random.choice(string.ascii_letters + string.digits)
	images = ["one.jpg", "two.jpg", "three.jpg", "four.jpg"]
	event.id=myID
	event.title = text.sentence()
	event.link = "https://google.com"
	event.description = text.quote()
	event.date= str(random_date(now,now+datetime.timedelta(600)))
	event.category = text.words(quantity=4)
	event.address = address.address()
	event.city = address.city()
	event.lat = str(round(random.uniform(37,40.8),7))
	event.lng = str(round(random.uniform(-108.9,-102.2),7))
	event.image = random.choice(images)

	ans = event.toJSON()
	#print(ans)
	table.put_item(Item=ans)