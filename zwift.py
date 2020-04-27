import requests
import json
from datetime import datetime

from urllib.parse import urlencode
from urllib.request import Request, urlopen
dataURL = 'https://www.zwiftpower.com/cache3/lists/0_zwift_event_list_3.json?_'
file = requests.get(dataURL)

decoded = file.content.decode("utf-8")
dict = json.loads(decoded)

with open('preferences.txt') as f:
    read_data = f.read()
    preferences = read_data.split(',')
    preferences.remove('')

races_names = []
race_records = []

for record in dict['data']:
    if record['f_r'] in preferences and record['f_km'] in preferences:
        races_names.append(record['t'])
        race_records.append(record)

races = " - " + "\n - ".join(races_names)

url = 'https://www.pushsafer.com/api' # Set destination URL here
post_fields = {                       # Set POST fields here
	"t" : "Races found",
	"m" : races,
	"s" : 33,
	"v" : None,
	"i" : 173,
	"c" : "",
	"d" : 24066,
	"u" : "http://jakub9367.dubaicollegedev.me/zwift/results.html",
	"ut" : "See results",
	"k" : "your_private_key_here"
	}

request = Request(url, urlencode(post_fields).encode())
json = urlopen(request).read().decode()
print(json)

for race in race_records:
    race['f_w'] = race['f_w'][6:]
    if race['f_r'] == 'ROUTE_FLAT':
        race['f_r'] = 'Flat'
    elif race['f_r'] == 'ROUTE_HILLY':
        race['f_r'] = 'Hilly'
    if race['layout'] == '':
        race['layout'] = "n/a"

    race['tm'] = datetime.utcfromtimestamp(race['tm']).strftime('%Y-%m-%d %H:%M%S')

f = open('/home/jakub9367/public_html/zwift/results.html','wb')

message = """<html>
<head>
    <title>Found races</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
<body>
  <table class="table">
      <thead class="thead-light">
          <tr>
              <th>Race title</th>
              <th>Race location</th>
              <th>Date and time</th>
              <th>Length in meters</th>
              <th>Number of laps</th>
              <th>Categories</th>
              <th>Incline description</th>
              <th>Incline value</th>
              <th>Go to race site</th>
          </tr>
      </thead>
      <tbody id="result_rows">"""

for race in race_records:
    message += "<tr><td>"+str(race['t'])+"</td><td>"+str(race['f_w'])+"</td><td>"+str(race['tm'])+"</td><td>"+str(race['km'])+"</td><td>"+str(race['laps'])+"</td><td>"+str(race['cats'])+"</td><td>"+str(race['f_r'])+"</td><td>"+str(race['layout'])+"</td><td><a href='https://www.zwiftpower.com/events.php?zid="+str(race['DT_RowId'])+"''><button class='btn btn-primary'>Register</button></a><a></a></td></tr>"

message += "</table></body></html>"
message = str(message).encode('utf-8')

f.write(message)
f.close()
