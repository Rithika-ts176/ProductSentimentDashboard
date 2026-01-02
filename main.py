from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from pymongo import MongoClient
import os

from sentiment_analysis import analyze_sentiment
from data_visualization import generate_charts

# ---------------- APP SETUP ----------------
app = Flask(__name__)
CORS(app)

# ---------------- MONGO DB CONNECTION ----------------
MONGO_URI = "mongodb+srv://keerthanaans2007_db_user:team3mp1@cluster0.eyamryn.mongodb.net/reviewdb?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["reviewdb"]
reviews_collection = db["reviews"]

# ---------------- ENSURE CHART FOLDER ----------------
CHART_FOLDER = "static/charts"
os.makedirs(CHART_FOLDER, exist_ok=True)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "<h2>Backend is running!</h2><p>Use /scrape, /reviews, /chart/bar, /chart/pie</p>"

# ---------------- SCRAPE REVIEWS ----------------
@app.route("/scrape", methods=["POST"])
def scrape():
    try:
        data = request.get_json()
        url = data.get("url", "").strip()

        if not url:
            return jsonify({"error": "URL required"}), 400

        # -------- Platform check --------
        if "amazon" in url.lower():
            from amazon_scraper import AmazonReviewScraper
            scraper = AmazonReviewScraper()
            reviews = scraper.get_reviews(url, max_pages=2)

        elif "flipkart" in url.lower():
            from flipkart_scraper import FlipkartReviewScraper
            scraper = FlipkartReviewScraper()
            reviews = scraper.get_reviews(url, max_pages=2)

        else:
            return jsonify({"error": "Only Amazon or Flipkart URLs allowed"}), 400

        if not reviews:
            return jsonify({"error": "No reviews scraped"}), 200

        saved_reviews = []

        for r in reviews:
            review_text = r.get("review_text", "").strip()
            if not review_text:
                continue

            sentiment = analyze_sentiment(review_text)

            review_doc = {
                "platform": r.get("platform", "Unknown"),
                "reviewtitle": r.get("reviewtitle", "No title"),
                "review_text": review_text,
                "sentiment": sentiment
            }

            reviews_collection.update_one(
                {
                    "platform": review_doc["platform"],
                    "reviewtitle": review_doc["reviewtitle"],
                    "review_text": review_doc["review_text"]
                },
                {"$set": review_doc},
                upsert=True
            )

            saved_reviews.append(review_doc)

        print(f"SCRAPED & SAVED: {len(saved_reviews)} reviews")

        return jsonify({
            "message": "Scraped successfully",
            "count": len(saved_reviews),
            "reviews": saved_reviews
        })

    except Exception as e:
        print("SCRAPER ERROR:", e)
        return jsonify({"error": str(e)}), 500

# ---------------- GET ALL REVIEWS ----------------
@app.route("/reviews", methods=["GET"])
def get_reviews():
    try:
        data = list(reviews_collection.find({}, {"_id": 0}))
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- CHART ENDPOINTS ----------------
@app.route("/chart/bar", methods=["GET"])
def chart_bar():
    try:
        if reviews_collection.count_documents({}) == 0:
            return jsonify({"error": "No reviews available"}), 204

        bar_path, _ = generate_charts(reviews_collection)
        return send_file(bar_path, mimetype="image/png")

    except Exception as e:
        print("BAR CHART ERROR:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/chart/pie", methods=["GET"])
def chart_pie():
    try:
        if reviews_collection.count_documents({}) == 0:
            return jsonify({"error": "No reviews available"}), 204

        _, pie_path = generate_charts(reviews_collection)
        return send_file(pie_path, mimetype="image/png")

    except Exception as e:
        print("PIE CHART ERROR:", e)
        return jsonify({"error": str(e)}), 500

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
