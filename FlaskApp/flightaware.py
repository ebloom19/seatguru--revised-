import json
from os import confstr
import re
import random
# from urllib import urlretrieve
from urllib.request import urlopen, URLError, urlretrieve
from pprint import pprint
from bs4 import BeautifulSoup
from bs4.element import Script
from retrying import retry
from datetime import datetime


# https://flightaware.com/live/flight/{flightcode}
FLIGHTAWARE_URL = "https://flightaware.com/live/flight/{}"

""" gets origin and destination airport code for a given flight """
@retry(stop_max_attempt_number=5)
def get_flight_details(flight_code):
  resp = urlopen(FLIGHTAWARE_URL.format(flight_code)).read()
  print(FLIGHTAWARE_URL.format(flight_code))
  soup = BeautifulSoup(resp, features="html.parser")

  # https://www.youtube.com/watch?v=QNLBBGWEQ3Q
  script = soup.find_all('script')[73].text[25:-1]
  flightData = json.loads(script)

  aircraftIncManu = list(flightData["flights"].values())[0]["activityLog"]["flights"][0]["aircraftType"]

  if aircraftIncManu == '':
    aircraftIncManu = str(soup.find_all('meta')[11])[15:-23]
    
  # Removing the manufacturer letter 'A' or 'B'
  if aircraftIncManu.startswith('A') or aircraftIncManu.startswith('B'):
    aircraft = aircraftIncManu[1:]
  else:
    aircraft = aircraftIncManu


  departUnixTime = list(flightData["flights"].values())[0]["activityLog"]["flights"][0]["flightPlan"]["departure"]
  departTime = datetime.utcfromtimestamp(departUnixTime).strftime('%Y-%m-%d %H:%M:%S')

  departureIataCode = list(flightData["flights"].values())[0]["activityLog"]["flights"][0]["origin"]["iata"]
  arrivalIataCode = list(flightData["flights"].values())[0]["activityLog"]["flights"][0]["destination"]["iata"]
  
  print(arrivalIataCode, '=>', departureIataCode)
  print('Aircraft', aircraft)
  
  return (departureIataCode, arrivalIataCode, aircraft)
  
  # def extract_aircraft_code(html_soup):
  #   aircraft_code = html_soup.parent.find_next_sibling('td').find('a')
  #   if (aircraft_code):
  #     aircraft_code = aircraft_code['href'].split('/')[-1]
  #   # we only need the numeric part of the model
  #   # i.e. for H/B744/L we get 744
  #   # CRJ 700 borks - http://flightaware.com/live/flight/BAW4449
  #   numeric_code = re.search('.*?(\d+).*?$', aircraft_code)
  #   if (numeric_code):
  #     return numeric_code.group(1)
