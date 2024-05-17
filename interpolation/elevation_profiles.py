from enum import Enum
import json
import urllib.parse
import urllib.request

PATHS_LOCATION = 'paths/'

class ElevationProfile(Enum):
  MOUNT_EVEREST = "MountEverest.csv"
  CHELM = "chelm.txt"
  GRAND_CANYON = "WielkiKanionKolorado.csv"
  

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
  if profile in [ElevationProfile.MOUNT_EVEREST, ElevationProfile.GRAND_CANYON]:
    with open(f'{PATHS_LOCATION}{profile.value}', 'r') as f:
      f.readline() # Skip the header
      for line in f:
        data.append([float(x) for x in line.split(',')])
  elif profile in [ElevationProfile.CHELM]:
    with open(f'{PATHS_LOCATION}{profile.value}', 'r') as f:
      for line in f:
        data.append([float(x) for x in line.split()])
  return data
