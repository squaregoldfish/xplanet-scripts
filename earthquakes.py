#!/usr/bin/python3
import sys
import urllib.request
import json

URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"

def main(output_file, min_strength):
  with urllib.request.urlopen(URL) as url:
    data_string = url.read().decode()

  # For debugging
  #with open("quake.json", "r") as f:
  #  data_string = f.read()

  # The USGS JSON comes with single quotes which is invalid
  data = json.loads(data_string)
  with open(output_file, 'w') as f:

    for quake in data["features"]:
      mag = quake["properties"]["mag"]

      if mag >= min_strength:
        lon = quake["geometry"]["coordinates"][0]
        lat = quake["geometry"]["coordinates"][1]
        alert = quake["properties"]["alert"]
        if alert not in ["green", "yellow", "orange", "red"]:
          alert = "green"

        f.write('{0} {1} "{2}" color={3} align=Above\n'.format(lat, lon, mag, alert))


if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], float(sys.argv[2]))
    else:
        exit('USAGE: earthquakes.py output_file min_strength')
