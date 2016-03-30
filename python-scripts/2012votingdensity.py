import pandas
import numpy as np
from lxml import etree
from colors import *

stylefill = "fill:#d0d0d0"

# Get data #
data = pandas.read_csv('US_elect_county.csv')
countyIDs = np.array(data['FIPS'],dtype=int)
totalVoteRatios = np.array(data['Obama vote'],dtype=float)+np.array(data['Romney vote'],dtype=float)
maxVotes = max(totalVoteRatios)
totalVoteRatios /= maxVotes
countydictionary = dict(zip(countyIDs,totalVoteRatios))

f = open('USA_Counties_with_FIPS_and_names.svg')
s = f.read()
f.close()
doc = etree.fromstring(s)
for item in doc:
    if item.tag == "{http://www.w3.org/2000/svg}path":
        try:
            myid = int(item.attrib['id'])
            countyvotes = countydictionary[myid]
            if countyvotes < 0.0001:
                color = colormegreen( 0 )
            else:
                color = colormegreen( (np.log10(countyvotes)-np.log10(0.0001))/4. )
            stylestring = item.attrib['style'].replace(stylefill,'fill:'+color)
            item.attrib['style'] = stylestring
        except KeyError, e:
            print 'No data for this county.',myid
        except ValueError, e:
            print 'ValueError on county.',myid
news = etree.tostring(doc)
o = open('votingdensitymap.svg','w')
o.write(news)
o.close()
