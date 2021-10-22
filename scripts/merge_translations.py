#!/usr/bin/env python

# Use pandas for data analysis for faster processing
# ERROR CODE STARTS WITH 02
from posixpath import expanduser
import pandas as pd
import sys
import os
from termcolor import colored
import json

# Name guard, init
if __name__ == "__main__":

  # Called to see pretty colors in terminal
  os.system('color')

  # Files
  NLFile = r'..\data\netherlands\NL_translations.json'
  DEFile = r'..\data\germany\DE_translations.json'
  UKFile = r'..\data\uk\GB_translations.json'
  outputFile = r'..\data\translations\Combined_Translations.json'

  # Open JSON file and load it to validate
  print("Loading translation NL JSON...")
  NLtranslations = []
  with open(NLFile, encoding='utf-8') as file:
    try:
      NLtranslations = json.load(file)
    except Exception as e:
      print(colored(f"ERRROR: Incorrectly formatted JSON (NL), {e} (ECODE: 0201)", "red"))
      sys.exit(1)
  
  # If json is empty give error
  if len(NLtranslations) == 0:
    print(colored(f"ERRROR: Translation JSON is empty (ECODE: 0202)", "red"))
    sys.exit(1)
  
  # Open JSON file and load it to validate
  print("Loading translation DE JSON...")
  DEtranslations = []
  with open(DEFile, encoding='utf-8') as file:
    try:
      DEtranslations = json.load(file)
    except Exception as e:
      print(colored(f"ERRROR: Incorrectly formatted JSON (DE), {e} (ECODE: 0201)", "red"))
      sys.exit(1)
  
  # If json is empty give error
  if len(DEtranslations) == 0:
    print(colored(f"ERRROR: Translation JSON is empty (ECODE: 0202)", "red"))
    sys.exit(1)
  
  # Open JSON file and load it to validate
  print("Loading translation UK JSON...")
  UKtranslations = []
  with open(UKFile, encoding='utf-8') as file:
    try:
      UKtranslations = json.load(file)
    except Exception as e:
      print(colored(f"ERRROR: Incorrectly formatted JSON (UK), {e} (ECODE: 0201)", "red"))
      sys.exit(1)
  
  # If json is empty give error
  if len(DEtranslations) == 0:
    print(colored(f"ERRROR: Translation JSON is empty (ECODE: 0202)", "red"))
    sys.exit(1)
  
  result = []
  result.append([NLtranslations, DEtranslations, UKtranslations])

  # Print translations into the JSON file
  print("Writing JSON file...")
  try:
    with open(outputFile, 'w', encoding='utf-8') as file:
      file.write(json.dumps(result, indent=4))
  except FileNotFoundError:
    print(colored(f"ERROR: File not found, check data subfolders (ECODE: 0203)", "red"))
    sys.exit(1)

  # Exit program correctly
  print(colored("Operation completed, created JSON file.", "green"))
  sys.exit(0)

  