def analyze_sentiment(text):
    text = text.lower()
    if "good" in text or "excellent" in text or "amazing" in text:
        return "Positive"
    elif "bad" in text or "worst" in text or "poor" in text:
        return "Negative"
    else:
        return "Neutral"
