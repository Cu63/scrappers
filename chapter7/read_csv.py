from urllib.request import urlopen
from io import StringIO
import csv

data = urlopen('http://pythonscraping.com/files/'
               'MontyPythonAlbums.csv').read().decode('ascii', 'ignore')

dataFile = StringIO(data)
csvReader = csv.reader(dataFile)
dataFile = StringIO(data)
dictReader = csv.DictReader(dataFile)

for row in csvReader:
    print(row)

for row in dictReader:
    print(row)
