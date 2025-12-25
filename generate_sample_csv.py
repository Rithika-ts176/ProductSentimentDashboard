import pandas as pd

# Sample data
data = {
    "Platform": ["Amazon", "Amazon", "Amazon", "Flipkart", "Flipkart", "Flipkart"],
    "Product_Name": [
        "Samsung Galaxy S25 Ultra 5G",
        "Samsung Galaxy S25 Ultra 5G",
        "Samsung Galaxy S25 Ultra 5G",
        "Samsung Galaxy S25 Ultra 5G",
        "Samsung Galaxy S25 Ultra 5G",
        "Samsung Galaxy S25 Ultra 5G",
    ],
    "Reviewer_Name": ["Rahul Sharma", "Priya Menon", "Ankit Verma", "Sneha Reddy", "Karan Singh", "Meera Joshi"],
    "Rating": [5, 4, 3, 5, 4, 2],
    "Review_Title": ["Excellent Phone", "Great, but expensive", "Average experience", "Loved it!", "Very good", "Disappointed"],
    "Review_Text": [
        "Amazing performance and battery life. Highly recommended!",
        "Very good phone but a bit pricey.",
        "Camera is good, but heating issues.",
        "Fantastic display and smooth performance.",
        "Great phone but a bit heavy.",
        "Battery drains fast."
    ],
    "Review_Date": ["2025-12-15", "2025-12-14", "2025-12-13", "2025-12-15", "2025-12-14", "2025-12-12"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("sample_reviews.csv", index=False)

print("sample_reviews.csv created successfully!")
