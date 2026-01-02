from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import time

from sentiment_analysis import analyze_sentiment


class AmazonReviewScraper:
    def __init__(self):
        options = Options()
        options.use_chromium = True
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        service = Service(r"E:\edge_driver\msedgedriver.exe")
        self.driver = webdriver.Edge(service=service, options=options)

    def get_reviews(self, url, max_pages=2):
        self.driver.get(url)
        time.sleep(4)

        all_reviews = []

        for _ in range(max_pages):
            blocks = self.driver.find_elements(
                By.XPATH, "//div[@data-hook='review']"
            )

            if not blocks:
                break

            for block in blocks:
                try:
                    rating = block.find_element(
                        By.XPATH, ".//i[@data-hook='review-star-rating']//span"
                    ).text
                except:
                    rating = None

                try:
                    title = block.find_element(
                        By.XPATH, ".//a[@data-hook='review-title']//span"
                    ).text
                except:
                    title = None

                try:
                    text = block.find_element(
                        By.XPATH, ".//span[@data-hook='review-body']"
                    ).text
                except:
                    text = ""

                if not text.strip():
                    continue

                sentiment = analyze_sentiment(text)

                all_reviews.append({
                    "platform": "Amazon",
                    "rating": rating,
                    "reviewtitle": title,
                    "review_text": text,
                    "sentiment": sentiment
                })

            # ---------- Pagination ----------
            try:
                next_btn = self.driver.find_element(
                    By.XPATH, "//li[@class='a-last']/a"
                )
                next_btn.click()
                time.sleep(4)
            except:
                break

        return all_reviews

    def close(self):
        self.driver.quit()
