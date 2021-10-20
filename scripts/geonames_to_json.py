#!/usr/bin/env python

# Converts AllCountries.txt file from GeoNames to a CSV than to a JSON.
# AllCoutries sub-files also work the same way.
# Use pandas for data analysis for faster processing
import pandas as pd
from os import sep
import sys

# Name guard, init
if __name__ == "__main__":

  # Get input file or exit with error
  try:
    inputFile = sys.argv[1]
  except:
    print("ERROR: Input file needed")
    sys.exit(1)
  
  # Get output file or exit with error
  try:
    outputFile = sys.argv[2]
  except:
    print("ERROR: Output file needed")
    sys.exit(1)
  
  # Array containing the names that will be in the JSON file
  jsonKeys = [
    'geonameID', 
    'name', 
    'ASCIIName', 
    'alternateNames', 
    'latitude', 
    'longitude', 
    'featureClass', 
    'featureCode', 
    'countryCode', 
    'cc2', 
    'admin1Code', 
    'admin2Code', 
    'admin3Code', 
    'admin4Code', 
    'population', 
    'elevation', 
    'dem', 
    'timezone', 
    'modificationDate'
  ]

  # Convert txt to csv. Remember sep parameter and header none. Pass names to have them named something else than 0...15.
  data = pd.read_csv(inputFile, sep="\t", header=None, names=jsonKeys)

  # Convert to JSON and saves to new file path
  data.to_json(outputFile, orient="records")

  # Exit program correctly
  sys.exit(0)