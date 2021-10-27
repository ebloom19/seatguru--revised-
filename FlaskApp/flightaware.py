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
from attr import attrs

# https://flightaware.com/live/flight/{flightcode}
FLIGHTAWARE_URL = "https://flightaware.com/live/flight/{}"

""" gets origin and destination airport code for a given flight """
@retry(stop_max_attempt_number=5)
def get_flight_details(flight_code):

  def extract_iata_airport_code(html_soup):
    # link_text = html_soup.find(class_='track-panel-airport').a.contents[0]
    # iata_search = re.search('.*?([A-Za-z]{3})$', link_text)
    if (iata_search):
      return iata_search.group(1)

  def extract_aircraft_code(html_soup):
    aircraft_code = html_soup.parent.find_next_sibling('td').find('a')
    if (aircraft_code):
      aircraft_code = aircraft_code['href'].split('/')[-1]
    # we only need the numeric part of the model
    # i.e. for H/B744/L we get 744
    # CRJ 700 borks - http://flightaware.com/live/flight/BAW4449
    numeric_code = re.search('.*?(\d+).*?$', aircraft_code)
    if (numeric_code):
      return numeric_code.group(1)

  # print('FindThis', FLIGHTAWARE_URL.format(flight_code))
  resp = urlopen(FLIGHTAWARE_URL.format(flight_code)).read()
  print(FLIGHTAWARE_URL.format(flight_code))
  soup = BeautifulSoup(resp, features="html.parser")
  # print(soup)

  # https://www.youtube.com/watch?v=QNLBBGWEQ3Q
  script = soup.find_all('script')[73].text[25:-1]
  flightData = json.loads(script)

  aircraft = list(flightData["flights"].values())[0]["activityLog"]["flights"][0]["aircraftType"]

  print('Aircraft ', aircraft)
  

  # aircraft = soup.find("script").attrs["aircraft"]

  # tag = soup('script')
  # print('ThisY', aircraft)
  
  # arrive    = extract_iata_airport_code(soup.find(class_='track-panel-arrival'))
  # aircraft  = extract_aircraft_code(soup.find(text='aircraftType'))



  return (depart, arrive, aircraft)

