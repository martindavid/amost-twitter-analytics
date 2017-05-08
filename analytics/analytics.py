from __future__ import print_function
import os
import json
import couchdb
import settings
from lib.genderComputer.genderComputer import GenderComputer

server = couchdb.Server(url=settings.COUCHDB_SERVER)
db = server[settings.COUCHDB_DB]

result = []
count = 0
for row in db.view('_design/filters/_view/fast_food'):
    coordinates = row.value["coordinates"]
    if count > 10:
        break
    if (coordinates[0] >= 139.654083252 and coordinates[0] <= 149.0885925293) and (coordinates[1] >= -38.548165423 and coordinates[1] <= -34.1436348203):
        print(row.value)
        count = count + 1
