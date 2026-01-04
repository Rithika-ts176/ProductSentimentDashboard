from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time

class AmazonReviewScraper:
    def __init__(self):
        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        # options.add_argument("--headless")  # optional

        self.driver = webdriver.Edge(options=options)

    def get_reviews(self, url, max_pages=2):
        self.driver.get(url)
        time.sleep(2)

        reviews = []

        for _ in range(max_pages):
            blocks = self.driver.find_elements(By.XPATH, "//div[@data-hook='review']")

            for block in blocks:
                try:
                    rating = block.find_element(
                        By.XPATH, ".//i[@data-hook='review-star-rating']/span"
                    ).text
                except:
                    rating = None

                try:
                    title = block.find_element(
                        By.XPATH, ".//a[@data-hook='review-title']/span"
                    ).text
                except:
                    title = None

                try:
                    text = block.find_element(
                        By.XPATH, ".//span[@data-hook='review-body']/span"
                    ).text
                except:
                    text = None

                reviews.append({
                    "rating": rating,
                    "title": title,
                    "review": text
                })

            try:
                next_btn = self.driver.find_element(By.XPATH, "//li[@class='a-last']/a")
                next_btn.click()
                time.sleep(2)
            except:
                break

        return reviews

    def close(self):
        self.driver.quit()
