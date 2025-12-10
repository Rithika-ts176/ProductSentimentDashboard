from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import time

class FlipkartReviewScraper:
    def __init__(self):
        options = Options()
        options.use_chromium = True
        # options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        service = Service(r"E:\edge_driver\msedgedriver.exe")

        self.driver = webdriver.Edge(service=service, options=options)

    def get_reviews(self, url, max_pages=2):
        self.driver.get(url)
        time.sleep(2)

        reviews = []

        for _ in range(max_pages):
            blocks = self.driver.find_elements(By.CSS_SELECTOR, "div.col._2wzgFH")

            for block in blocks:
                try:
                    rating = block.find_element(By.CSS_SELECTOR, "div._3LWZlK").text
                except:
                    rating = None

                try:
                    title = block.find_element(By.CSS_SELECTOR, "p._2-N8zT").text
                except:
                    title = None

                try:
                    text = block.find_element(By.CSS_SELECTOR, "div.t-ZTKy div").text
                except:
                    text = None

                reviews.append({
                    "rating": rating,
                    "title": title,
                    "review": text
                })

            # Next page
            try:
                next_btn = self.driver.find_element(By.CSS_SELECTOR, "a._1LKTO3:last-child")
                next_btn.click()
                time.sleep(2)
            except:
                break

        return reviews

    def close(self):
        self.driver.quit()
