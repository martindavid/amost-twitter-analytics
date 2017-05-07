import couchdb
from datetime import datetime
import pytz 

# analyze according to daytime (morning, afternnon, night)
try:
    couch = couchdb.Server()
    db_con = couch['sa-time-con']
    db_time = couch['sa-location']
except:
    db_con = couch.create('sa-time-con')

for row in db_time.view('_design/foo/_view/daytime'):
    sum_morning = 0
    sum_afternoon = 0
    sum_night = 0
    time = row.key
    hour = (datetime.strptime(time,'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)).hour
    if 6 <= hour <= 12: 
        sum_morning += row.value
    elif 13 <= hour <= 18:
        sum_afternoon += row.value
    elif 0 <= hour <= 5 or 19 <= hour <= 23:
        sum_night += row.value 