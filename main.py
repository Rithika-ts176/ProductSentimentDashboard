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

