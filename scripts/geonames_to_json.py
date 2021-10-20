#!/usr/bin/env python

# Converts AllCountries.txt file from GeoNames to a CSV than to a JSON.
# AllCoutries sub-files also work the same way.
# Use pandas for data analysis for faster processing
# ERROR CODE STARTS WITH 00
from posixpath import expanduser
import pandas as pd
import sys
import os
from termcolor import colored

# Name guard, init
if __name__ == "__main__":

  # Possible input flags:
  countryFlags = [
    'ALL', 'all', 'All', # All countries
    'NL', 'nl', # Netherlands
    'GE', 'ge', # Germany
    'GB', 'gb', 'uk', 'UK', # United Kindgom 
  ]

  # Called to see pretty colors in terminal
  os.system('color')

  # Get input file or exit with error
  try:
    flag = sys.argv[1]
    if not flag in countryFlags:
      raise ValueError('flag not found')
  except IndexError as error:
    print(colored("ERROR: Country flag needed, please read readme (ECODE: 0001)", "red"))
    sys.exit(1)
  except ValueError as error:
    print(colored("ERROR: Country flag not recognized (ECODE: 0002)", "red"))
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

  # Set input and output files
  inputFile = None
  outputFile = None
  match flag:
    case ('ALL' | 'all' | 'All'):
      inputFile = r'..\data\allCountries\allCountries.txt'
      outputFile = r'..\data\allCountries\allCountries.json'
    case ('NL' | 'nl'):
      inputFile = r'..\data\netherlands\NL.txt'
      outputFile = r'..\data\netherlands\NL.json'
  
  # If input or output is None give error and exit
  if inputFile is None or outputFile is None:
    print(colored("ERROR: Country flag not recognized (ECODE: 0003)", "red"))
    sys.exit(1)
  
  # Convert txt to csv. Remember sep parameter and header none. Pass names to have them named something else than 0...15.
  print("Starting reading and writing process...")
  # Convert each chunk instead of the full file so we don't get memory problems for C
  for index, chunk in enumerate(pd.read_csv(inputFile, sep="\t", header=None, names=jsonKeys, encoding = "ISO-8859-1", chunksize=20000, low_memory=False)):
    print(f"Converting chunk number {index}")
    with open(outputFile, 'a', encoding='utf-8') as file:
      print(f"Writing chunk number {index} to JSON")
      chunk.to_json(file, force_ascii=False, orient="records")

  # Exit program correctly
  print(colored("Operation completed, created JSON file.", "green"))
  sys.exit(0)