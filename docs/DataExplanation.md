# Data Explanation

Explanation on how data collection works and why we delete some data.

## Cities Files

We get all files from [Geonames data dump](http://download.geonames.org/export/dump/).
The city files are store in XX.zip where XX is ISO code of the country.
From this file, we keep all point of interests where Feature Class has value P. [Link](http://download.geonames.org/export/dump/featureCodes_en.txt)

We delete the dem column (it's the digital elevation model), the elevation column, the admin1, 2, 3 and 4, we also don't need cc2 because we filter for country code anyway.

Cities with PPLA2 are groups of cities/towns and google maps makes them searchable but they don't put the city name on the map.

## Translation Files

We get the translation files the same way we get the cities files.
After getting both, we query through them and keep only translations of cities we have in the cities files.

## Important Cities

To start with, I decided to rank important cities in 8 levels

1 - Huge cities and Country names > 700.000
2 - Biggest cities > 400.000
3 - Big cities > 200.000
4 - Medium cities > 100.000
5 - Small cities > 10.000
6 - Towns > 2.000
7 - Settlements > 0
8 - Really small settlements or undefined population for that city == 0

If the population is zero we encounter a problem. We are not sure if the population numbers are wrong or if it's just a really small town. 
For the moment, all 0 population are ranked 8th.