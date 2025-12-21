import pandas as pd

# Load reviews
df = pd.read_csv("sample_reviews.csv")

# Simple word lists
positive_words = [
    "good", "great", "excellent", "amazing", "fantastic",
    "love", "loved", "smooth", "best", "awesome", "perfect"
]

negative_words = [
    "bad", "poor", "worst", "disappointed", "heating",
    "drains", "slow", "issue", "problem", "expensive"
]

def analyze_sentiment(text):
    text = text.lower()
    pos_count = sum(word in text for word in positive_words)
    neg_count = sum(word in text for word in negative_words)

    if pos_count > neg_count:
        return "Positive"
    elif neg_count > pos_count:
        return "Negative"
    else:
        return "Neutral"

# Apply sentiment
df["Sentiment"] = df["Review_Text"].apply(analyze_sentiment)

# Save output
df.to_csv("sample_reviews_sentiment.csv", index=False)

print("✅ Sentiment analysis completed!")
print(df[["Review_Text", "Sentiment"]])
