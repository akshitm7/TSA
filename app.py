import tweepy
from textblob import TextBlob
import pandas as pd
import re
import matplotlib.pyplot as plt
client = tweepy.Client(
    bearer_token='',
    consumer_key='',
    consumer_secret='',
    access_token='',
    access_token_secret='',
    wait_on_rate_limit=True
)
def clean_tweet(tweet):
    tweet = re.sub(r'http\S+|www.\S+', '', tweet) 
    tweet = re.sub(r'@\w+|#', '', tweet)           
    tweet = re.sub(r'[^A-Za-z0-9 ]+', '', tweet)   
    tweet = tweet.lower()                       
    return tweet
def get_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity == 0:
        return "Neutral"
    else:
        return "Negative"
def fetch_and_analyze(keyword, count=50):
    response = client.search_recent_tweets(
        query=keyword,
        max_results=min(count, 100),  # max 100 per request
        tweet_fields=['text', 'created_at', 'author_id'],
    )
    tweets = response.data if response.data else []
    tweet_list = []
    for tweet in tweets:
        cleaned = clean_tweet(tweet.text)
        sentiment = get_sentiment(cleaned)
        tweet_list.append([tweet.text, cleaned, sentiment])
    df = pd.DataFrame(tweet_list, columns=["Original Tweet", "Cleaned Tweet", "Sentiment"])
    return df
if __name__ == "__main__":
    keyword = input("Enter a keyword to search tweets for sentiment analysis: ")
    df = fetch_and_analyze(keyword, count=50)
    print(df)
    sentiment_counts = df['Sentiment'].value_counts()
    sentiment_counts.plot(kind='bar', color=['green', 'blue', 'red'])
    plt.title(f"Sentiment Analysis for '{keyword}'")
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Tweets")
    plt.show()
