import requests, json

URL = 'http://inverter/solar_api/v1/GetPowerFlowRealtimeData.fcgi'

resp = requests.get(url=URL).json()

data = {}
data['time'] = resp['Head']['Timestamp']
data['prod'] = resp['Body']['Data']['Site']['P_PV'] or 0
data['load'] = round(resp['Body']['Data']['Site']['P_Load']) * -1
# data['grid'] = round(resp['Body']['Data']['Site']['P_Grid'])

print(data)
