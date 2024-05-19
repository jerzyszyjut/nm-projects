from enum import Enum
import json
import urllib.parse
import urllib.request
import os
import dotenv
from math import sin, cos, acos, pi

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
PATHS_LOCATION = 'paths/'

class ElevationProfile(Enum):
  CEWICE_LEBA = 'cewice-leba-elevation.csv'
  WIEZYCA = 'wiezyca-elevation.csv'
  SZKLARKA = 'szklarka-elevation.csv'

def get_distance(lat1, lon1, lat2, lon2):
  R = 6371
  lat1 = lat1 * pi / 180
  lon1 = lon1 * pi / 180
  lat2 = lat2 * pi / 180
  lon2 = lon2 * pi / 180
  return acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1)) * R  

def get_elevation_profile_from_google_api(api_key, locations):
  base_url = 'https://maps.googleapis.com/maps/api/elevation/json'
  params = {
    'key': api_key,
    'locations': '|'.join(locations)
  }
  url = base_url + '?' + urllib.parse.urlencode(params)
  response = urllib.request.urlopen(url)
  response_data = json.loads(response.read())
  return response_data

def get_elevation_profile_from_files(profile: ElevationProfile):
  data = []
  with open(f'{PATHS_LOCATION}{profile.value}', 'r') as f:
    f.readline() # Skip the header
    for line in f:
      data.append([float(x) for x in line.split(',')])
  data_points = len(data)
  distance = data[-1][0] - data[0][0]
  step = distance / data_points
  for i in range(data_points):
    data[i][0] = i * step
  return data

def apply_moving_average_to_elevation_profile(data, window_size):
  smoothed_data = []
  for i in range(len(data)):
    distance = data[i][0]
    elevation_sum = 0
    elevation_count = 0
    for j in range(i - window_size, i + window_size + 1):
      if j >= 0 and j < len(data):
        elevation_sum += data[j][1]
        elevation_count += 1
    smoothed_data.append([distance, elevation_sum / elevation_count])
  return smoothed_data

def main():
  filename = 'szklarka'
  locations = open(f"paths/{filename}-coords.csv", 'r').readlines()
  locations = [x.strip()[:-2] for x in locations]
  locations_limit = 500
  results = []
  for locations_chunk in [locations[i:i+locations_limit] for i in range(0, len(locations), locations_limit)]:
    data = get_elevation_profile_from_google_api(os.getenv('GOOGLE_API_KEY'), locations_chunk)
    open(f"paths/{filename}-elevation.json", 'a').write(json.dumps(data, indent=2))
    results += data['results']
    
  with open(f"paths/{filename}-elevation.csv", 'w') as f:
    f.write('distance,elevation\n')
    current_distance = 0
    for idx, result in enumerate(results):
      f.write(f'{current_distance},{result["elevation"]}\n')
      if idx < len(results) - 1:
        current_distance += get_distance(result['location']['lat'], result['location']['lng'], results[idx+1]['location']['lat'], results[idx+1]['location']['lng'])
        
if __name__ == '__main__':
  dotenv.load_dotenv()
  main()
  