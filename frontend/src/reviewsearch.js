import React, { useState } from "react";

function ReviewSearch() {
  const [product, setProduct] = useState("");
  const [reviews, setReviews] = useState([]);

  const handleSearch = async () => {
    if (!product.trim()) return alert("Enter a product name!");

    try {
      // Call backend reviews endpoint
      const response = await fetch(`http://127.0.0.1:5000/reviews`);
      let data = await response.json();

      // Filter reviews by product title / keyword
      data = data.filter((r) =>
        r.reviewtitle?.toLowerCase().includes(product.toLowerCase()) ||
        r.review_text?.toLowerCase().includes(product.toLowerCase())
      );

      setReviews(data);
    } catch (error) {
      console.error("Error fetching reviews:", error);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h2>Product Review Search</h2>
      <input
        type="text"
        placeholder="Enter product name"
        value={product}
        onChange={(e) => setProduct(e.target.value)}
        style={{ padding: "8px", width: "250px" }}
      />
      <button
        onClick={handleSearch}
        style={{ padding: "8px 16px", marginLeft: "10px" }}
      >
        Search
      </button>

      {reviews.length > 0 && (
        <div style={{ marginTop: "20px" }}>
          <h3>Reviews & Sentiment:</h3>
          <ul>
            {reviews.map((r, index) => (
              <li key={index}>
                <strong>{r.platform || "Unknown"}:</strong>{" "}
                {r.reviewtitle ? `${r.reviewtitle} - ` : ""}
                {r.review_text || ""} — <em>{r.sentiment}</em>
              </li>
            ))}
          </ul>
        </div>
      )}

      {reviews.length === 0 && product.trim() && (
        <p style={{ marginTop: "20px" }}>No reviews found for "{product}".</p>
      )}
    </div>
  );
}

export default ReviewSearch;
