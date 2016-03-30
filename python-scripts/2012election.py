import pandas
import numpy as np
from lxml import etree
from colors import *

stylefill = "fill:#d0d0d0"

# Get data #
data = pandas.read_csv('US_elect_county.csv')
countyIDs = np.array(data['FIPS'],dtype=int)
demVotesRatio = np.array(data['Obama vote'],dtype=float)
repVotesRatio = np.array(data['Romney vote'],dtype=float)
# Process data #
totalCountyVotes = demVotesRatio+repVotesRatio
demVotesRatio /= totalCountyVotes
repVotesRatio /= totalCountyVotes
# Zip into dictionary #
countydictionary = dict(zip(countyIDs,zip(demVotesRatio,repVotesRatio)))

# Read from map #
f = open('USA_Counties_with_FIPS_and_names.svg')
s = f.read()
f.close()
doc = etree.fromstring(s)
# Loop through counties #
for item in doc:
    if item.tag == "{http://www.w3.org/2000/svg}path":
        try:
            myid = int(item.attrib['id'])
            countyvotes = countydictionary[myid]
            # Get fill color #
            if countyvotes[0] >= 0.5:
                color = colormeblue( (countyvotes[0]-0.5)/0.5 )
            else:
                color = colormered( (countyvotes[1]-0.5)/0.5 )
            stylestring = item.attrib['style'].replace(stylefill,'fill:'+color)
            item.attrib['style'] = stylestring
        except KeyError, e:
            print 'No data for this county.',myid
        except ValueError, e:
            print 'ValueError on county.',myid
# Create new map with appropriate color gradient #
news = etree.tostring(doc)
o = open('electionmap.svg','w')
o.write(news)
o.close()
