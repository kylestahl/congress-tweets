import tweepy
import datetime
import os
from bs4 import BeautifulSoup
import urllib2

## Access Twitter API
consumer_key = 'Y7IZ3jKPtwklV71Z7w6YiRnEO'
consumer_secret = '4HaNXfnpAyQHxvG8qYRHIW8WA8PIO9J9rXeQmp5VW3Q6WeCAs6'
access_token = '343387964-GAZq8gdwZ5FC7CXRv02WAfv8Fk1h8EIO7LVFPNjS'
access_token_secret = 'eRdg81dkV7on4vJdix0nzGERJLtKS1hT0p4oVye1mQQBf'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

## Get List of Congress Twitter Handles from Internet
from bs4 import BeautifulSoup
import urllib2

html = urllib2.urlopen('http://triagecancer.org/congressional-twitter-handles').read()
soup = BeautifulSoup(html, 'lxml')
table = soup.findAll('table')
senate = table[0]
house = table[1]

senators= []
for row in senate.findAll('tr'):
    cells = row.findAll('td')
    twitter_tag = str(cells[2])
    # Remove <td> tag
    handle = '@'+twitter_tag.partition('@')[2].partition('</td>')[0]
    senators.append(handle)
    

house_reps = []
for row in house.findAll('tr'):
    cells = row.findAll('td')
    twitter_tag = str(cells[2])
    # Remove <td> tag
    handle = '@'+twitter_tag.partition('@')[2].partition('</td>')[0].partition('</a>')[0]
    house_reps.append(handle)


congress = senators + house_reps
congress = [handle for handle in congress if handle != '@']



def grab_tweets(handle):
    """
    Thank you https://gist.github.com/yanofsky/5436496 for this function (slightly modified)
    This function will use the twitter api connection to pull the tweets for any twitter 
    handle. 
    
    Input: A string <str> with a valid twitter handle beginning with the @ symbol
           Example: '@kstahl13'
    
    Output: A list of the text of tweets from the specified twitter account going back to
            Jan 1st 2018, and rounded up to the next 200th tweet
    
    """
    #initialize a list to hold all the tweepy Tweets
    alltweets = []	
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(handle, count=200,tweet_mode='extended')
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        # all subsiquent requests use the max_id param to prevent duplicates
        # Stop at 2018
        if alltweets[-1].created_at > datetime.datetime(2018,1,1):
            new_tweets = api.user_timeline(handle,count=200,max_id=oldest,tweet_mode='extended')
        else:
            new_tweets = []
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
    
    # Extract Text from Tweepy object, remove links at end
    tweet_text = [t.full_text for t in alltweets]
    
    return tweet_text



def clean_tweets(tweets):
    """
    Clean up the tweet list given by grab_tweets().
    - Encode as string instead of unicode
    - Remove hashtags
    - Remove hypertext links
    - Remove mentions with '@' symbols
    - Remove numbers
    - Remove RT for Retweets
    - Tweets must be more than two characters
    Returns the same tweet list with the above adjustments
    """
    # Encode as string
    as_string = [t.encode('ascii','ignore') for t in tweets]
    
    # Remove hashtag, mentions, links
    # Thank to this guy https://stackoverflow.com/questions/8376691/
    # how-to-remove-hashtag-user-link-of-a-tweet-using-regular-expression
    no_bs_stuff = [' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)",
                                " ",t).split()) for t in as_string]
    
    # Remove RT
    no_rt = [t[3:] if t[:3]=='RT ' else t for t in no_bs_stuff]
    
    # Remove numbers periods commas
    clean_list = [t.translate(None, '0123456789,.') for t in no_bs_stuff]
    
    # Remove tweets less than 2 characters
    actual_tweets = [t for t in clean_list if len(t) > 2 ]
    
    return actual_tweets











os.chdir("C:/Users/kyles/Desktop/tweets")
for person in senators:
    write_tweets(person)







def write_tweets(handle):
    
    # Grab Tweets
    tweet_list = grab_tweets(handle)
    
    # Create Folder for tweets
    if not os.path.exists(handle):
        os.makedirs(handle)
    
    # Write tweets to files
    i=1
    for tweet in tweet_list:
        with open(handle+'/tweet'+str(i)+'.txt', 'w') as output:
            output.write(tweet.encode("ascii", "ignore"))
        i+=1

