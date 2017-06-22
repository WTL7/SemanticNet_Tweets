#!/usr/bin/python
import tweepy
import csv #Import csv
from time import gmtime, strftime
import pandas as pd
import nltk

current_time=strftime("%Y-%m-%d", gmtime())

#Variables that contains the user credentials to access Twitter API 

consumer_key=" "
consumer_secret=" "
access_key=" "
access_secret=" "


auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)
csvFile = open('Result_%s.csv'%current_time, 'wb')    # output file
#Use csv Writer
csvWriter = csv.writer(csvFile)
csvWriter.writerow(['User','Screen_Name','Date','Tweet','Retweet','Favorite']) #entity


for status in tweepy.Cursor(api.search, 
    q="#foodwaste -RT -planet",   #https://dev.twitter.com/rest/public/search (Check query operators)
    #geocode="39.6395,-98.1298,1500mi",  # roughly geo boundaries
    since="2015-08-07",       # query from   # users can put any date within past 7 days from now
    until= current_time,       # query to
    lang="en").items():
    #if status.geo is not None:
    #    #Write a row to the csv file
    csvWriter.writerow([status.user.id, status.user.screen_name, status.created_at, status.text.encode('utf-8'), status.retweet_count, status.favorite_count])
    print status.created_at, status.text
print "Tweets Downloaded Complete"
csvFile.close()

state_df=pd.read_csv('Result_%s.csv'%current_time) 
tweet_lines=state_df['Tweet'].tolist()

for line in tweet_lines:
    line=unicode(line, errors='ignore')

    
corn_word= [cw.lower() for line in tweet_lines for cw in nltk.tokenize.word_tokenize(unicode(line, errors='ignore'))]  #words from all tweets in tweet_corn_df
stop_words = nltk.corpus.stopwords.words('english') + ['#',',','.','?','@',':',
                                                      'http','https',';','!','...',"''","``","'s",')','(','&','-','amp','RT','rt',"'re","'m","n't",'+']   # costumize stop word list
corn_word= [w for w in corn_word if w not in stop_words]
fdist= nltk.FreqDist(corn_word)   #word freq statistic 
word_keys=fdist.keys()
word_value=fdist.values()

csvFile2 = open('Freq_Statistics.csv', 'wb')
#Use csv Writer
csvWriter2 = csv.writer(csvFile2)
csvWriter2.writerow(['Word','Frequency']) #entity
for i in range(len(word_keys)):
    #if word_value[i] >= 2:    # only show words frequency >=2 (exclude the words only appear once)
    csvWriter2.writerow([word_keys[i],word_value[i]])