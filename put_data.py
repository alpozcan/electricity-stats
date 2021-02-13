#!/usr/bin/env python3

import requests, json, time, psycopg2
from psycopg2.extensions import AsIs

URL = 'http://inverter/solar_api/v1/GetPowerFlowRealtimeData.fcgi'

resp = requests.get(url=URL).json()

data = {}
data['time'] = int(time.time())
data['prod'] = resp['Body']['Data']['Site']['P_PV'] or 0
data['load'] = round(resp['Body']['Data']['Site']['P_Load']) * -1
# data['grid'] = round(resp['Body']['Data']['Site']['P_Grid'])

insert_statement = 'insert into electricity (%s) values %s'
columns = data.keys()
values = [data[c] for c in columns]

db_conn = psycopg2.connect("dbname='home' user='postgres'")
db_cursor = db_conn.cursor()
sql = db_cursor.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values)))
db_cursor.execute(sql)
db_conn.commit()
db_conn.close()
