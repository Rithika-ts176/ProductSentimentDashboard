import pandas as pd
import matplotlib.pyplot as plt

# Load sentiment CSV (from Part 3)
df = pd.read_csv("sample_reviews_sentiment.csv")

# Count sentiment values
sentiment_counts = df["Sentiment"].value_counts()

print("\nSentiment Summary:")
print(sentiment_counts)

# -------- Bar Chart --------
plt.figure()
sentiment_counts.plot(kind="bar")
plt.title("Product Sentiment Analysis")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")
plt.tight_layout()
plt.savefig("sentiment_bar_chart.png")
plt.show()

# -------- Pie Chart --------
plt.figure()
sentiment_counts.plot(kind="pie", autopct="%1.1f%%")
plt.title("Sentiment Distribution")
plt.ylabel("")
plt.tight_layout()
plt.savefig("sentiment_pie_chart.png")
plt.show()

print("✅ Sentiment visualization completed!")
