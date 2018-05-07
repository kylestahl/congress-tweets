"""
Here we can in the tweets that were pickled and run LDA with Scikit Learn
We use NLTK to either stem or lemmatize the words in the tweets

I am still trying to figure out which is best and what the best
parameters for min_df and max_df are.
"""



import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation



def stem(s):
    """
    Given a list of strings (tweets)
    
    Returns a new list of strings with every word
    of every string ran through a SnowballStemmer
    """
    from nltk.stem import SnowballStemmer
    stemmer = SnowballStemmer('english')
    return [" ".join(listed_tweet) for listed_tweet in \
            [[stemmer.stem(word) for word in tweet.split(' ') if len(stemmer.stem(word)) > 4] \
                for tweet in s]]


def lemma(s):
    """
    Given a list of strings (tweets)
    
    Returns a new list of strings with every word
    of every string ran through a Lemmatizer   
    """
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    return [" ".join(listed_tweet) for listed_tweet in \
                [[lemmatizer.lemmatize(word) for word in tweet.split(' ') if len(lemmatizer.lemmatize(word)) > 3] \
                for tweet in s]]



# Vectorize the Words into Term-Document Matrix
vect = CountVectorizer(min_df = .001, max_df = .025)
tdm = pd.DataFrame(vect.fit_transform(lemma(tweet_list)).toarray(), \
                    columns=vect.get_feature_names())

# Perform LDA 
lda = LatentDirichletAllocation(n_components=5)
lda.fit(tdm)


# Look at top words in each Topic
ttm = pd.DataFrame(lda.components_,columns=vect.get_feature_names()).transpose()
for c in ttm.columns.values:
    print ttm.sort_values(c,ascending=False).head(20).index


topics = pd.DataFrame(lda.transform(tdm))


