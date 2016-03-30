import pandas
import numpy as np
from lxml import etree
from colors import *

stylefill = "fill:#d0d0d0"

# Get data from .csv file. #
data = pandas.read_csv('US_elect_county.csv')
# Extract the useful columns from DataFrame into NumPy arrays and calulate ratios. #
countyIDs = np.array(data['FIPS'],dtype=int)
totalVoteRatios = np.array(data['Obama vote'],dtype=float)+np.array(data['Romney vote'],dtype=float)
maxVotes = max(totalVoteRatios)
totalVoteRatios /= maxVotes
# Zip into dictionary #
countydictionary = dict(zip(countyIDs,totalVoteRatios))

# Read from the blank map. #
f = open('USA_Counties_with_FIPS_and_names.svg')
s = f.read()
f.close()
doc = etree.fromstring(s)
# Loop through each county #
for item in doc:
    if item.tag == "{http://www.w3.org/2000/svg}path":
        try:
            # Get the county data #
            myid = int(item.attrib['id'])
            countyvotes = countydictionary[myid]
            # Get the new fill color #
            if countyvotes < 0.0001:
                color = colormegreen( 0 )
            else:
                color = colormegreen( (np.log10(countyvotes)-np.log10(0.0001))/4. )
            # Replace the .svg fill attribute #
            stylestring = item.attrib['style'].replace(stylefill,'fill:'+color)
            item.attrib['style'] = stylestring
        except KeyError, e:
            print 'No data for this county.',myid
        except ValueError, e:
            print 'ValueError on county.',myid
# Create the new .svg file with the updated fills #
news = etree.tostring(doc)
o = open('votingdensitymap.svg','w')
o.write(news)
o.close()
