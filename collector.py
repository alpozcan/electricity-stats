#!/usr/bin/env python3

import requests, json, logging, time, psycopg2, signal, sys
from psycopg2.extras import execute_values

CHUNK_SIZE = 64
INTERVAL = 10 # fetch interval in seconds
LOG_LEVEL = logging.ERROR
URL = 'http://inverter/solar_api/v1/GetPowerFlowRealtimeData.fcgi'

logging.basicConfig(level=LOG_LEVEL)

db_conn = psycopg2.connect("dbname='home' user='postgres'")
db_cursor = db_conn.cursor()

chunk = []

def fetch():
  try:
    resp = requests.get(url=URL).json()
  except:
    logging.error('error fetching data')
    return

  sample = {}
  sample['time'] = int(time.time())
  sample['prod'] = resp['Body']['Data']['Site']['P_PV'] or 0
  sample['load'] = round(resp['Body']['Data']['Site']['P_Load']) * -1
# sample['grid'] = round(resp['Body']['Data']['Site']['P_Grid'])

  logging.debug('sample: %s', sample)

  chunk.append(sample)

def insert(chunk):
  columns = chunk[0].keys()
  values_list = [ tuple([sample[c] for c in columns]) for sample in chunk ]
  execute_values(db_cursor, f'INSERT INTO electricity ({",".join(columns)}) VALUES %s', values_list)
  db_conn.commit()
  logging.info('inserted %d samples', len(chunk))

def exit_handler(signal_received, frame):
  logging.warning('Exiting on signal')
  db_conn.close()
  sys.exit(0)

if __name__ == "__main__":
  signal.signal(signal.SIGINT, exit_handler)

  while True:
    fetch()

    if len(chunk) == CHUNK_SIZE:
      insert(chunk)
      chunk = []

    time.sleep(INTERVAL)
