from flask import Flask, jsonify, request
import pandas as pd
from sentiment_analysis import analyze_sentiment
review=input("Enter product review:")
result= analyze_sentiment(review)
print("Sentiment",result)

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Backend API is running"})

@app.route("/reviews", methods=["GET"])
def get_reviews():
    df = pd.read_csv("sample_reviews_sentiment.csv")
    return jsonify(df.to_dict(orient="records"))

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("review")

    result = analyze_sentiment(text)
    return jsonify({
        "review": text,
        "sentiment": result
    })

@app.route("/dashboard-data", methods=["GET"])
def dashboard_data():
    df = pd.read_csv("sample_reviews_sentiment.csv")

    summary = df["sentiment"].value_counts().to_dict()
    return jsonify(summary)

if __name__ == "__main__":
    app.run(debug=False)

from amazon_scraper import AmazonReviewScraper
from flipkart_scraper import FlipkartReviewScraper

# ---------------- AMAZON ----------------
amazon_url = "https://www.amazon.in/product-reviews/B0C7S5H7L3"

amazon = AmazonReviewScraper()
amazon_reviews = amazon.get_reviews(amazon_url, max_pages=2)
amazon.close()

print("\nAMAZON REVIEWS:")
for r in amazon_reviews:
    print(r)

# ---------------- FLIPKART ----------------
flipkart_url = "https://www.flipkart.com/product-reviews/XYZ"

flip = FlipkartReviewScraper()
flipkart_reviews = flip.get_reviews(flipkart_url, max_pages=2)
flip.close()

print("\nFLIPKART REVIEWS:")
for r in flipkart_reviews:
    print(r)