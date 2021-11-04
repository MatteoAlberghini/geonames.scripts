#!/usr/bin/env python

# Use pandas for data analysis for faster processing
# The script works in different parts
# ERROR CODE STARTS WITH 01
import pandas as pd
import sys
import os
from requests.api import request
from requests.exceptions import RequestException
from termcolor import colored
import json
import requests, zipfile, io
from geojson import Point, Feature, FeatureCollection, dump
import sqlalchemy
import sqlite3

### ANCHOR VARIABLES ###
# Cities
citiesZipURLs = [
  # Nederlands
  { 
    "name": "Netherlands",
    "url": "http://download.geonames.org/export/dump/NL.zip",
    "path": r"../data/startingFiles/cities/netherlands",
    "shortcode": "NL",
  },
  # Germany
  {
    "name": "Germany",
    "url": "http://download.geonames.org/export/dump/DE.zip",
    "path": r"../data/startingFiles/cities/germany",
    "shortcode": "DE",
  },
  # UK
  {
    "name": "United Kingdom",
    "url": "http://download.geonames.org/export/dump/GB.zip",
    "path": r"../data/startingFiles/cities/unitedKingdom",
    "shortcode": "GB",
  },
]
# Translations
translationsZipURLs = [
  # Nederlands
  { 
    "name": "Netherlands",
    "url": "http://download.geonames.org/export/dump/alternatenames/NL.zip",
    "path": r"../data/startingFiles/translations/netherlands",
    "shortcode": "NL",
  },
  # Germany
  {
    "name": "Germany",
    "url": "http://download.geonames.org/export/dump/alternatenames/DE.zip",
    "path": r"../data/startingFiles/translations/germany",
    "shortcode": "DE",
  },
  # UK
  {
    "name": "United Kingdom",
    "url": "http://download.geonames.org/export/dump/alternatenames/GB.zip",
    "path": r"../data/startingFiles/translations/unitedKingdom",
    "shortcode": "GB",
  },
]
# Array containing the names that will be in the cities JSON file
citiesJsonKeys = [
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
# Array containing the names that will be in the JSON file
translationsJsonKeys = [
  'alternateNameID',
  'geonameID',
  'isoLanguage',
  'alternateName',
  'isPreferredName',
  'isShortName',
  'isColloquial',
  'isHistoric',
  'from',
  'to'
]
# Output path folder
outputPath = r"../data/endingFiles"

### ANCHOR NAME GUARD -- INIT ###
if __name__ == "__main__":

  # Called to see pretty colors in terminal
  os.system('color')

  # Download and unzip all files into startingFiles directory (CITIES)
  # If you don't have the folders setup it will create them
  # Start with the city zips
  print(colored(f"Starting request for cities zip files!", "blue"))
  for index, city in enumerate(citiesZipURLs):
    # Request
    print(f"Making request for {city['name']}...")
    try:
      r = requests.get(city["url"])
    except RequestException as e:
      print(colored(f"ERROR: Connection error in cities at index {index}: {e} (ECODE: 0101)", "red"))
      sys.exit(1)
    
    # Create zip file
    print(f"Making zip file for {city['name']}...")
    try: 
      z = zipfile.ZipFile(io.BytesIO(r.content))
    except Exception as e:
      print(colored(f"ERROR: Zipfile creation error in cities at index {index}: {e} (ECODE: 0102)", "red"))
      sys.exit(1)

    # Extract file
    print(f"Extracting zip file for {city['name']}...")
    try: 
      z.extractall(city["path"])
    except Exception as e:
      print(colored(f"ERROR: Zipfile extraction error in cities at index {index}: {e} (ECODE: 0103)", "red"))
      sys.exit(1)
  # Removes annoying readme.txt files inside subfolders
  for index, city in enumerate(citiesZipURLs):
    # Deletion
    print(f"Deleting readme.txt file for {city['name']}...")
    try:
      os.remove(city["path"] + "/readme.txt")
    except Exception as e:
      print(colored(f"ERROR: Error deleting readme file for city at {index}: {e} (ECODE: 0104)", "red"))
      sys.exit(1)
  

  # Download and unzip all files into startingFiles directory (TRANSLATIONS)
  # If you don't have the folders setup it will create them
  # Download translation zips and unzips them
  print(colored(f"Starting request for translation zip files!", "blue"))
  for index, translation in enumerate(translationsZipURLs):
    # Request
    print(f"Making request for {translation['name']}...")
    try:
      r = requests.get(translation["url"])
    except RequestException as e:
      print(colored(f"ERROR: Connection error in translations at index {index}: {e} (ECODE: 0105)", "red"))
      sys.exit(1)
    
    # Create zip file
    print(f"Making zip file for {translation['name']}...")
    try: 
      z = zipfile.ZipFile(io.BytesIO(r.content))
    except Exception as e:
      print(colored(f"ERROR: Zipfile creation error in translations at index {index}: {e} (ECODE: 0106)", "red"))
      sys.exit(1)

    # Extract file
    print(f"Extracting zip file for {translation['name']}...")
    try: 
      z.extractall(translation["path"])
    except Exception as e:
      print(colored(f"ERROR: Zipfile extraction error in translations at index {index}: {e} (ECODE: 0107)", "red"))
      sys.exit(1)
  # Removes annoying readme.txt files inside subfolders
  for index, translation in enumerate(translationsZipURLs):
    # Deletion
    print(f"Deleting readme.txt file for {translation['name']}...")
    try:
      os.remove(translation["path"] + "/readme.txt")
    except Exception as e:
      print(colored(f"ERROR: Error deleting readme file for translation at {index}: {e} (ECODE: 0108)", "red"))
      sys.exit(1)


  # Get all the txt files downloaded and convert them to JSON files (CITIES)
  # Save them at the same location with the shortcode name (used later, also useful for testing if needed)
  print(colored(f"Starting conversion from TXT to JSON for cities!", "blue"))
  for index, city in enumerate(citiesZipURLs):
    # Declare input output files 
    print(f"Reading TXT file and converting to CSV for country {city['name']}...")
    inputFile = city["path"] + '/' + city["shortcode"] + '.txt'
    outputFile = city["path"] + '/' + city["shortcode"] + '.json'

    # Pandas convert TXT file to CSV
    try: 
      data = pd.read_csv(inputFile, sep="\t", header=None, names=citiesJsonKeys, encoding = "ISO-8859-1", low_memory=False)
    except Exception as e:
      print(colored(f"ERROR: Converting TXT file to CSV in cities at {index}: {e} (ECODE: 0109)", "red"))
      sys.exit(1)
    
    # Convert CSV to JSON
    print(f"Converting CSV to JSON for country {city['name']}...")
    try:
      with open(outputFile, 'w', encoding='utf-8') as file:
        data.to_json(file, force_ascii=False, orient="records", indent=4)
    except Exception as e:
      print(colored(f"ERROR: Converting CSV file to JSON for cities at {index} (ECODE: 0110)", "red"))
      sys.exit(1)
    
    # Open JSON file and load it to validate
    print(f"Testing if JSON file is correctly created and formatted for country {city['name']}...")
    startingCities = []
    with open(outputFile, encoding='utf-8') as file:
      try:
        startingCities = json.load(file)
      except Exception as e:
        print(colored(f"ERRROR: Incorrectly formatted JSON for country {city['name']}, {e} (ECODE: 0111)", "red"))
        sys.exit(1)
    
    # If json is empty give error
    if len(startingCities) == 0:
      print(colored(f"ERROR: JSON is empty for country {city['name']} (ECODE: 0124)", "red"))
      sys.exit(1)
    
    # Delete all non important translations, or null ones
    print(f"Deleting useless infos from country {city['name']}...")
    endCities = []
    for c in startingCities:
      if c["featureClass"] == 'p' or c["featureClass"] == 'P':
        endCities.append(c)
    
    # If there is no translations exit
    if len(endCities) == 0:
      print(colored(f"ERROR: No useful translation found for cities file {city['name']} (ECODE: 0125)", "red"))
      sys.exit(1)
    
    # Print translations into the JSON file
    print(f"Writing fixed translations to JSON file to country {city['name']}...")
    try:
      with open(outputFile, 'w', encoding='utf-8') as file:
        file.write(json.dumps(endCities, indent=4))
    except Exception as e:
      print(colored(f"ERROR: Writing file to JSON for country {city['name']} (ECODE: 0126)", "red"))
      sys.exit(1)


  # Get all the txt files downloaded and convert them to JSON files (TRANSLATIONS)
  # Save them at the same location with the shortcode name (used later, also useful for testing if needed)
  print(colored(f"Starting conversion from TXT to JSON for translations!", "blue"))
  for index, translation in enumerate(translationsZipURLs):
    # Declare input output files 
    print(f"Reading TXT file and converting to CSV for translation {translation['name']}...")
    inputFile = translation["path"] + '/' + translation["shortcode"] + '.txt'
    outputFile = translation["path"] + '/' + translation["shortcode"] + '.json'

    # Pandas convert TXT file to CSV
    try: 
      data = pd.read_csv(inputFile, sep="\t", header=None, names=translationsJsonKeys, encoding = "ISO-8859-1", low_memory=False)
    except Exception as e:
      print(colored(f"ERROR: Converting TXT file to CSV in translation at {index}: {e} (ECODE: 0112)", "red"))
      sys.exit(1)
    
    # Convert CSV to JSON
    print(f"Converting CSV to JSON for translation {translation['name']}...")
    try:
      with open(outputFile, 'w', encoding='utf-8') as file:
        data.to_json(file, force_ascii=False, orient="records", indent=4)
    except Exception as e:
      print(colored(f"ERROR: Converting CSV file to JSON for translation at {index} (ECODE: 0113)", "red"))
      sys.exit(1)
    
    # Open JSON file and load it to validate
    print(f"Testing if JSON file is correctly created and formatted for translation {translation['name']}...")
    startingTranslations = []
    with open(outputFile, encoding='utf-8') as file:
      try:
        startingTranslations = json.load(file)
      except Exception as e:
        print(colored(f"ERROR: Incorrectly formatted JSON for translation {translation['name']}, {e} (ECODE: 0114)", "red"))
        sys.exit(1)
    
    # If json is empty give error
    if len(startingTranslations) == 0:
      print(colored(f"ERROR: JSON is empty for translation {translation['name']} (ECODE: 0115)", "red"))
      sys.exit(1)
    
    # Delete all non important translations, or null ones
    print(f"Deleting useless infos from translation {translation['name']}...")
    translations = []
    for t in startingTranslations:
      if t["isoLanguage"] == 'nl' or t["isoLanguage"] == 'de' or t["isoLanguage"] == 'en':
        translations.append(t)
    
    # If there is no translations exit
    if len(translations) == 0:
      print(colored(f"ERROR: No useful translation found for translation {translation['name']} (ECODE: 0116)", "red"))
      sys.exit(1)
    
    # Print translations into the JSON file
    print(f"Writing fixed translations to JSON file to translation {translation['name']}...")
    try:
      with open(outputFile, 'w', encoding='utf-8') as file:
        file.write(json.dumps(translations, indent=4))
    except Exception as e:
      print(colored(f"ERROR: Writing file to JSON for translation {translation['name']} (ECODE: 0117)", "red"))
      sys.exit(1)


  # Merge translation file into city file for the same country
  print(colored(f"Starting merge of cities into translations!", "blue"))
  for index, city in enumerate(citiesZipURLs):
    # Declare input output files 
    translation = translationsZipURLs[index]
    cityInputFile = city["path"] + '/' + city["shortcode"] + '.json'
    translationInputFIle = translation["path"] + "/" + translation["shortcode"] + '.json'
    outputFile = outputPath + '/' + city["shortcode"] + '.json'

    # Open city JSON file
    print(f"Loading JSON from {city['name']} (country) JSON file...")
    cities = []
    with open(cityInputFile, encoding='utf-8') as file:
      try:
        cities = json.load(file)
      except Exception as e:
        print(colored(f"ERROR: Incorrectly formatted JSON for {city['name']} JSON, {e} (ECODE: 0118)", "red"))
        sys.exit(1)
    
    # Open translation JSON file
    print(f"Loading JSON from {translation['name']} (translation) JSON file...")
    translations = []
    with open(translationInputFIle, encoding='utf-8') as file:
      try:
        translations = json.load(file)
      except Exception as e:
        print(colored(f"ERROR: Incorrectly formatted JSON for {translation['name']} JSON, {e} (ECODE: 0119)", "red"))
        sys.exit(1)
    
    # Merge the two lists (Can we make this process faster?)
    print(f"Merging files for {translation['name']} (HEAVY OPERATION)...")
    merged = []
    for c in cities:
      cityID = c["geonameID"]
      endingJSON = {
        "genonameID": cityID,
        "name": c["name"],
        "ASCIIName": c["ASCIIName"],
        "latitude": c["latitude"],
        "longitude": c["longitude"],
        "featureCode": c["featureCode"],
        "countryCode": c["countryCode"],
        "population": c["population"],
        "nameNL": None,
        "nameDE": None,
        "nameEN": None,
      }
      for t in translations:
        translationID = t["geonameID"]
        if translationID == cityID:
          iso = str(t["isoLanguage"]).upper()
          endingJSON[f"name{iso}"] = t["alternateName"]
      
      merged.append(endingJSON)
    
    # Print translations into the JSON file
    print(f"Writing merged JSON file for country {city['name']}...")
    # We make directory if not present, we don't have to do it for others because we use libraries like Zip and Pandas
    os.makedirs(os.path.dirname(outputFile), exist_ok=True)
    try:
      with open(outputFile, 'w', encoding='utf-8') as file:
        file.write(json.dumps(merged, indent=4))
    except Exception as e:
      print(colored(f"ERROR: Writing file to JSON for merged country {city['name']} (ECODE: 0120)", "red"))
      sys.exit(1)


  # Rank city based on population numbers
  for index, city in enumerate(citiesZipURLs):
    file = outputPath + '/' + city["shortcode"] + '.json'
    
    # Open city JSON file
    print(f"Loading JSON from {city['name']} merged JSON file...")
    cities = []
    with open(file, encoding='utf-8') as f:
      try:
        cities = json.load(f)
      except Exception as e:
        print(colored(f"ERROR: Incorrectly formatted JSON for {city['name']} JSON, {e} (ECODE: 0124)", "red"))
        sys.exit(1)
    
    # Rank based on population number
    for c in cities:
      population = c["population"]
      if population == 0:
        c["ranking"] = 9
      if population > 0:
        c["ranking"] = 8
      if population > 2000:
        c["ranking"] = 7
      if population > 10000:
        c["ranking"] = 6
      if population > 35000:
        c["ranking"] = 5
      if population > 100000:
        c["ranking"] = 4
      if population > 200000:
        c["ranking"] = 3
      if population > 400000:
        c["ranking"] = 2
      if population > 700000:
        c["ranking"] = 1

    # Writes the new JSON file
    try:
      with open(file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(cities, indent=4, ensure_ascii=False))
    except Exception as e:
      print(colored(f"ERROR: Writing file to JSON for merged country {city['name']} (ECODE: 0125)", "red"))
      sys.exit(1)

  # Create GEOJSON file from JSON files just created
  print(colored(f"Creating GEOJSON files from the merged files!", "blue"))
  for index, city in enumerate(citiesZipURLs):
    inputFile = outputPath + '/' + city["shortcode"] + '.json'
    outputFile = outputPath + '/' + city["shortcode"] + '.geojson'
  
    # Open city JSON file
    print(f"Loading JSON from {city['name']} merged JSON file...")
    cities = []
    with open(inputFile, encoding='utf-8') as file:
      try:
        cities = json.load(file)
      except Exception as e:
        print(colored(f"ERROR: Incorrectly formatted JSON for {city['name']} JSON, {e} (ECODE: 0121)", "red"))
        sys.exit(1)
    
    # Create GEOJSON object
    print(f"Creating GEOJSON object from {city['name']} JSON...")
    features = []
    for c in cities: 
      point = Point((c["longitude"], c["latitude"]))
      features.append(Feature(geometry=point, properties=c))
    
    featuresCollection = FeatureCollection(features)
    
    # Writing GEOJSON to file
    print(f"Writing GEOJSON file for {city['name']}...")
    try:
      with open(outputFile, 'w', encoding='utf-8') as file:
        dump(featuresCollection, file, indent=4, ensure_ascii=False)
    except Exception as e:
      print(colored(f"ERROR: Writing file to GEOJSON for country {city['name']} (ECODE: 0122)", "red"))
      sys.exit(1)


  # Create merged JSON file from single merged JSON
  combinedCities = []
  combinedCitiesFile = outputPath + '/merged.json'
  for index, city in enumerate(citiesZipURLs):
    file = outputPath + '/' + city["shortcode"] + '.json'

    # Open city JSON file
    print(f"Loading JSON from {city['name']} merged JSON file...")
    cities = []
    with open(inputFile, encoding='utf-8') as file:
      try:
        cities = json.load(file)
      except Exception as e:
        print(colored(f"ERROR: Incorrectly formatted JSON for {city['name']} JSON, {e} (ECODE: 0127)", "red"))
        sys.exit(1)
    
    combinedCities.append(cities)

  # Writes the new combined JSON file (out of the for loop)
  try:
    with open(combinedCitiesFile, 'w', encoding='utf-8') as f:
      f.write(json.dumps(combinedCities, indent=4, ensure_ascii=False))
  except Exception as e:
    print(colored(f"ERROR: Writing file to JSON for merged country {city['name']} (ECODE: 0126)", "red"))
    sys.exit(1)

  # Create SQL files
  print(colored(f"Creating SQL files from the merged files!", "blue"))
  for index, city in enumerate(citiesZipURLs):
    inputFile = outputPath + '/' + city["shortcode"] + '.json'
    outputFile = 'sqlite:///' + city["shortcode"] + '.db' # Did not find a way to save it to output folder
  
    # Open city JSON file
    print(f"Loading JSON from {city['name']} merged JSON file...")
    cities = None
    with open(inputFile, encoding='utf-8') as file:
      try:
        cities = pd.read_json(inputFile, orient="records")
      except Exception as e:
        print(colored(f"ERROR: Incorrectly formatted JSON for {city['name']} JSON, {e} (ECODE: 0123)", "red"))
        sys.exit(1)

    # Connect to DB
    print(f"Creating SQL database for {city['name']}...")
    engine = sqlalchemy.create_engine(outputFile)
    cities.to_sql("Cities", engine, if_exists="replace")


  # Make combined SQL file
  print(colored(f"Creating SQL database from combined cities file!", "blue"))
  # finalDatabaseOutput = 'sqlite:///combinedCities.db' # Did not find a way to save it to output folder

  # Merge GB into NL
  print("Merging GB into NL...")
  con3 = sqlite3.connect('NL.db')
  con3.execute("ATTACH 'GB.db' as dba")
  con3.execute("BEGIN")
  for row in con3.execute("SELECT * FROM dba.sqlite_master WHERE type='table'"):
      combine = "INSERT INTO "+ row[1] + " SELECT * FROM dba." + row[1]
      con3.execute(combine)
  con3.commit()
  con3.execute("detach database dba")

  # Merge DE into NL
  print("Merging DE into NL...")
  con3 = sqlite3.connect('NL.db')
  con3.execute("ATTACH 'DE.db' as dba")
  con3.execute("BEGIN")
  for row in con3.execute("SELECT * FROM dba.sqlite_master WHERE type='table'"):
      combine = "INSERT INTO "+ row[1] + " SELECT * FROM dba." + row[1]
      con3.execute(combine)
  con3.commit()
  con3.execute("detach database dba")
  con3.close()

  # Change NL name and delete useless DBs
  print("Deleting temporary files...")
  os.remove('GB.db')
  os.remove('DE.db')
  try:
    os.remove('../data/endingFiles/AllCities.db')
  except:
    pass
  os.rename('NL.db', '../data/endingFiles/AllCities.db')
  
  # Exit program correctly
  print(colored("Operation completed without errors!", "green"))
  sys.exit(0)

