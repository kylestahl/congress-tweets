## Get List of Congress Twitter Handles from Internet
from bs4 import BeautifulSoup
import urllib2
import pickle

# Open HTML in BeautifulSoup
html = urllib2.urlopen('http://triagecancer.org/congressional-twitter-handles').read()
soup = BeautifulSoup(html, 'lxml')
table = soup.findAll('table')

# First Table is senate, second is the house
senate = table[0]
house = table[1]


senators= [] # Initialize list for handles
for row in senate.findAll('tr'): # Loop through table
    cells = row.findAll('td') # Extract Row
    twitter_tag = str(cells[2]) # Get Handle
    handle = '@'+twitter_tag.partition('@')[2].partition('</td>')[0]# Remove <td> tag
    senators.append(handle) # Add to list
    
# Repeat for House
house_reps = []
for row in house.findAll('tr'):
    cells = row.findAll('td')
    twitter_tag = str(cells[2])
    # Remove <td> tag
    handle = '@'+twitter_tag.partition('@')[2].partition('</td>')[0].partition('</a>')[0]
    house_reps.append(handle)


# Combine House and Senate
congress = senators + house_reps
# Remove empty strings just '@'
congress = [handle for handle in congress if handle != '@']


# Pickle List for later use
with open('congress_handles.pkl', 'wb') as f:
    pickle.dump(congress, f)




