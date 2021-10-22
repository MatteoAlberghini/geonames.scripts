#!/usr/bin/env python

# Use pandas for data analysis for faster processing
# ERROR CODE STARTS WITH 01
from posixpath import expanduser
import pandas as pd
import sys
import os
from termcolor import colored
import json

# Name guard, init
if __name__ == "__main__":

  # Possible input flags:
  countryFlags = [
    'NL', 'nl', # Netherlands
    'DE', 'de',  # Germany
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
    print(colored("ERROR: Country flag needed, please read readme (ECODE: 0101)", "red"))
    sys.exit(1)
  except ValueError as error:
    print(colored("ERROR: Country flag not recognized (ECODE: 0102)", "red"))
    sys.exit(1)
  
  # Array containing the names that will be in the JSON file
  jsonKeys = [
    'alternateNameId',
    'geonameid',
    'isolanguage',
    'alternateName',
    'isPreferredName',
    'isShortName',
    'isColloquial',
    'isHistoric',
    'from',
    'to'
  ]

  # Set input and output files
  inputFile = None
  outputFile = None
  match flag:
    case ('NL' | 'nl'):
      inputFile = r'..\data\netherlands\NL_translations.txt'
      outputFile = r'..\data\netherlands\NL_translations.json'
    case ('DE' | 'de'):
      inputFile = r'..\data\germany\DE_translations.txt'
      outputFile = r'..\data\germany\DE_translations.json'
    case ('GB' | 'gb' | 'uk' | 'UK'):
      inputFile = r'..\data\uk\GB_translations.txt'
      outputFile = r'..\data\uk\GB_translations.json'
  
  # If input or output is None give error and exit
  if inputFile is None or outputFile is None:
    print(colored("ERROR: Country flag not recognized (ECODE: 0103)", "red"))
    sys.exit(1)
  
  # Convert txt to csv. Remember sep parameter and header none. Pass names to have them named something else than 0...15.
  print("Reading TXT and making CSV...")
  data = pd.read_csv(inputFile, sep="\t", header=None, names=jsonKeys, encoding = "ISO-8859-1", low_memory=False)

  # Convert CSV to JSON
  print("Converting CSV to JSON...")
  try:
    with open(outputFile, 'w', encoding='utf-8') as file:
      data.to_json(file, force_ascii=False, orient="records", indent=4)
  except FileNotFoundError:
    print(colored(f"ERROR: File not found for country {flag}, check data subfolders (ECODE: 0004)", "red"))
    sys.exit(1)
  
  print("Testing JSON...")
  # Open JSON file and load it to validate
  startingTranslations = []
  with open(outputFile, encoding='utf-8') as file:
    try:
      startingTranslations = json.load(file)
    except Exception as e:
      print(colored(f"ERRROR: Incorrectly formatted JSON, {e} (ECODE: 0105)", "red"))
      sys.exit(1)
  
  # If json is empty give error
  if len(startingTranslations) == 0:
    print(colored(f"ERRROR: JSON is empty (ECODE: 0106)", "red"))
    sys.exit(1)
  
  # Delete all non important translations, or null ones
  print("Deleting useless infos...")
  translations = []
  for t in startingTranslations:
    if t["isolanguage"] == 'nl' or t["isolanguage"] == 'de' or t["isolanguage"] == 'en':
      translations.append(t)
  
  # If there is no translations exit
  if len(translations) == 0:
    print(colored(f"ERRROR: No useful translation found (ECODE: 0107)", "red"))
    sys.exit(1)
  
  # Print translations into the JSON file
  try:
    with open(outputFile, 'w', encoding='utf-8') as file:
      file.write(json.dumps(translations, indent=4))
  except FileNotFoundError:
    print(colored(f"ERROR: File not found for country {flag}, check data subfolders (ECODE: 0004)", "red"))
    sys.exit(1)

  # Exit program correctly
  print(colored("Operation completed, created JSON file.", "green"))
  sys.exit(0)