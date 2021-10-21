#!/usr/bin/env python

# Check if json is correctly formatted
import sys
import json
import os
from termcolor import colored

# Name guard, init
if __name__ == "__main__":

  # Possible input flags:
  countryFlags = [
    'ALL', 'all', 'All', # All countries
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
    print(colored("ERROR: Country flag needed, please read readme (ECODE: 0001)", "red"))
    sys.exit(1)
  except ValueError as error:
    print(colored("ERROR: Country flag not recognized (ECODE: 0002)", "red"))
    sys.exit(1)

  # Set input file
  inputFile = None
  match flag:
    case ('ALL' | 'all' | 'All'):
      inputFile = r'..\data\allCountries\allCountries.json'
    case ('NL' | 'nl'):
      inputFile = r'..\data\netherlands\NL.json'
    case ('DE' | 'de'):
      inputFile = r'..\data\germany\DE.json'
    case ('GB' | 'gb' | 'uk' | 'UK'):
      inputFile = r'..\data\uk\GB.json'

  # If input is None give error and exit
  if inputFile is None:
    print(colored("ERROR: Country flag not recognized (ECODE: 0003)", "red"))
    sys.exit(1)
  
  print("Validating JSON file...")
  # Open JSON file and load it to validate
  with open(inputFile, encoding='utf-8') as file:
    try:
      json.load(file)
    except Exception as e:
      print(colored(f"Incorrectly formatted JSON, {e}", "yellow"))
      sys.exit(1)
    else:
      print(colored("Correctly formatted JSON", "green"))
      sys.exit(0)

