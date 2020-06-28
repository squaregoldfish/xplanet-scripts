#!/usr/bin/python3
import sys
import urllib.request
import json

# Get latest earthquake data from USGS and generate an Xplnet marker file
#
# Usage: earthquakes.py output_file min_strength
#
# output_file  is the name of the marker file to generate
# min_strength will filter the earthquakes so that quakes with a magnitude
#              less than this value will not be included

# The URL for the USGS JSON - all quakes for the last 7 days
URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"

# The main functio
def main(output_file, min_strength):

  # Download the JSON from USGS
  with urllib.request.urlopen(URL) as url:
    data_string = url.read().decode()

  # For debugging - download the USGS json into a file
  #with open("quake.json", "r") as f:
  #  data_string = f.read()

  # Parse the JSON
  data = json.loads(data_string)

  # Open the output file
  with open(output_file, 'w') as f:

    # Loop through each quake
    for quake in data["features"]:

      # Check the magnitude
      mag = quake["properties"]["mag"]
      if mag >= min_strength:

        # Extract details and write line to the output file
        lon = quake["geometry"]["coordinates"][0]
        lat = quake["geometry"]["coordinates"][1]
        alert = quake["properties"]["alert"]
        if alert not in ["green", "yellow", "orange", "red"]:
          alert = "green"

        f.write('{:1.3f} {:1.3f} "{:3.1f}" color={} align=Above\n'.format(lat, lon, mag, alert))


if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], float(sys.argv[2]))
    else:
        exit('USAGE: earthquakes.py output_file min_strength')
