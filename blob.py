from textblob import TextBlob

# Example usage
text = "i hate mumbai"
blob = TextBlob(text)
sentiment = blob.sentiment.polarity
print(sentiment)
