# GEONAMES SCRIPT

Geonames.scripts is a list of python scripts to handle geonames database dumps and make them usable and readable.

## Installation

You'll need pandas to use most scripts.

```bash
pip install pandas
```

## Usage

```python
cd /scripts/

# geonames_to_json accepts 2 paramaters: input txt file and output json file (created if not existent)
python geonames_to_json NL.txt test.json
```

## Folders Description

The data folder contains backups of all the data used by me. They're just examples. To be sure to have the latest data you should be taking them from the [Geonames website](https://download.geonames.org/export/dump/)

The scripts folder contains all the scripts. Can be used with data from the data folder or with any data. See Usage for the paramaters.

## License
[MIT](https://choosealicense.com/licenses/mit/)