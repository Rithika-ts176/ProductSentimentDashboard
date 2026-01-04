from flask import Flask, render_template, request
from amazon_scraper import AmazonReviewScraper
from flipkart_scraper import FlipkartReviewScraper
import csv
from flask import Response


app = Flask(__name__)

def analyze_sentiment(text):
    text = text.lower()
    if any(w in text for w in ["good", "great", "excellent", "amazing"]):
        return "Positive"
    elif any(w in text for w in ["bad", "poor", "worst", "heating"]):
        return "Negative"
    else:
        return "Neutral"

MOCK_REVIEWS = [
    {"review": "Amazing performance and battery life"},
    {"review": "Camera is good but heating issue"},
    {"review": "Worth the price"},
]

@app.route("/", methods=["GET", "POST"])
def index():
    reviews = []
    platform = ""
    mode = ""

    if request.method == "POST":
        platform = request.form["platform"]
        mode = request.form["mode"]

        if mode == "mock":
            reviews = MOCK_REVIEWS
        else:
            url = request.form["url"]
            scraper = AmazonReviewScraper() if platform == "amazon" else FlipkartReviewScraper()
            reviews = scraper.get_reviews(url)
            scraper.close()

        for r in reviews:
            r["sentiment"] = analyze_sentiment(r["review"])

    return render_template("index.html", reviews=reviews, platform=platform, mode=mode)

if __name__ == "__main__":
    app.run(debug=False)
