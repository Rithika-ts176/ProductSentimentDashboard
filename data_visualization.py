import matplotlib
matplotlib.use('Agg')  # headless backend for server
import matplotlib.pyplot as plt
import pandas as pd
import os

# Folder to save charts
CHART_FOLDER = "static/charts"
if not os.path.exists(CHART_FOLDER):
    os.makedirs(CHART_FOLDER)


def generate_charts(reviews_collection):
    """
    Generates bar and pie charts for sentiment visualization.
    Expects MongoDB collection where each document has:
        - sentiment: 'positive', 'neutral', 'negative'
    Returns paths of saved charts.
    """

    # --- Fetch data from MongoDB ---
    data = list(reviews_collection.find({}, {"_id": 0, "sentiment": 1}))

    # --- Default counts in case DB is empty ---
    counts = {"positive": 0, "neutral": 0, "negative": 0}

    if data:
        df = pd.DataFrame(data)
        # Safety check: only count valid sentiments
        for label in ["positive", "neutral", "negative"]:
            counts[label] = df['sentiment'].value_counts().get(label, 0)

    # --- Bar Chart ---
    bar_path = os.path.join(CHART_FOLDER, "sentiment_bar_chart.png")
    plt.figure(figsize=(6, 4))
    plt.bar(
        ["Positive", "Neutral", "Negative"],
        [counts["positive"], counts["neutral"], counts["negative"]],
        color=["green", "gray", "red"]
    )
    plt.title("Sentiment Bar Chart")
    plt.xlabel("Sentiment Type")
    plt.ylabel("Number of Reviews")
    plt.tight_layout()
    plt.savefig(bar_path)
    plt.close()

    # --- Pie Chart ---
    pie_path = os.path.join(CHART_FOLDER, "sentiment_pie_chart.png")
    plt.figure(figsize=(6, 6))
    plt.pie(
        [counts["positive"], counts["neutral"], counts["negative"]],
        labels=["Positive", "Neutral", "Negative"],
        autopct='%1.1f%%',
        colors=["green", "gray", "red"]
    )
    plt.title("Sentiment Pie Chart")
    plt.tight_layout()
    plt.savefig(pie_path)
    plt.close()

    return bar_path, pie_path
