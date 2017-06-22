
import csv
import pandas as pd
import nltk

Codebook_df = pd.read_csv('Codebook.csv')        
#Source_words = Codebook_df['Source'].tolist()  
#Target_words = Codebook_df['Target'].tolist()
   
Tweet_df = pd.read_csv('Result_2015-08-08.csv')
Tweets = Tweet_df['Tweet'].tolist()


stop_words = nltk.corpus.stopwords.words('english') + ['#',',','.','?','@',':',
                                                      'http','https',';','!','...',"''","``","'s",')','(','&','-','amp','RT','rt',"'re","'m","n't",'+']   # costumize stop word list
word_distance = 2

#for tweet in Tweets:    # for every tweet
    
All_tweets = ' * * * * * * * '.join(Tweets)    # join all tweets as one document ( different tweets are seperated by 7*)
        
WordsInTweet_RemoveStopWords = []
WordsInTweet_RemoveStopWords_Stemming = []
WordsInTweet_RemoveStopWords_Stemming_Target = []

WordsInTweet = [context_words.lower() for context_words in nltk.tokenize.word_tokenize(unicode( All_tweets , errors='ignore'))]  # tokenization  #words from a tweet

for word in WordsInTweet:      
    if word not in stop_words:
        WordsInTweet_RemoveStopWords.append(word)     # remove stop words in tweets

for word in WordsInTweet_RemoveStopWords:
    WordsInTweet_RemoveStopWords_Stemming.append(nltk.stem.snowball.SnowballStemmer('english').stem(word))  # word stemming

for word in WordsInTweet_RemoveStopWords_Stemming:
    #if word in Codebook_df['Source'].tolist():   # check if the word in the codebook
    for index, row in Codebook_df.iterrows():   # iterate dataframe
        if word in row['Source']:
            WordsInTweet_RemoveStopWords_Stemming_Target.append(row['Target'])   # replace source word by target word
            break    # this "break" is important. Stop duplicate counting. It avoids the effects from several words with the same root appearing in the codebook (ex: world and worlds, harvesting, harvested and harvest)  
    else:
        WordsInTweet_RemoveStopWords_Stemming_Target.append(word)      # kepp the word unchaged if the word is not in the codebook
             
                
# semantic network generation                      
word_links= {}  # create dictionary for storing results   
check_word=[]    
for word_1 in Codebook_df['Target'].tolist(): 
    check_word.append(word_1)
    for word_2 in Codebook_df['Target'].tolist():
        if word_2 not in check_word:
            count=0    #reset word count
            for k in [i for i, j in enumerate(WordsInTweet_RemoveStopWords_Stemming_Target) if j == word_1]:   #iteratble index operation. Count and locate the index code of word1 in a word list
                if word_2 in WordsInTweet_RemoveStopWords_Stemming_Target[k-word_distance:k] + WordsInTweet_RemoveStopWords_Stemming_Target[k+1:k+1+word_distance]:    #search forward and backward words within the distance
                    count +=1   
            if count <> 0:                  
                word_links[frozenset([word_1,word_2])]=count  
                    
# data output
with open('Edge_List_Word_Radius_%s.csv'%word_distance, 'wb') as myfile:
    wr1 = csv.writer(myfile, quoting=csv.QUOTE_ALL)  #writing file (import csv)            
    wr1.writerow(['source','target','weight'])
    for k1,k2 in word_links:
        wr1.writerow([k1,k2,word_links[frozenset({k1, k2})]])
           
     
