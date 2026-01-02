import { useState, useEffect } from "react";
import "./App.css";
import {
  fetchAllReviews,
  scrapeReviewFromLink,
  getBarChartUrl,
  getPieChartUrl,
} from "./api.js";

function App() {
  const [reviews, setReviews] = useState([]);
  const [productLink, setProductLink] = useState("");
  const [chartTimestamp, setChartTimestamp] = useState(Date.now());

  // Fetch all reviews
  const fetchReviews = async () => {
    const data = await fetchAllReviews();
    setReviews(data);
  };

  // Scrape reviews from product link
  const scrapeReviews = async () => {
    if (!productLink.trim()) {
      alert("Please enter a product link");
      return;
    }

    const result = await scrapeReviewFromLink(productLink);
    if (!result) {
      alert("Error scraping reviews. Check backend connection.");
      return;
    }

    alert(result.message || "Scraping completed");
    fetchReviews();                // update reviews in frontend
    setChartTimestamp(Date.now()); // force chart refresh
    setProductLink("");            // clear input field
  };

  useEffect(() => {
    fetchReviews();
  }, []);

  return (
    <div className="page">
      <div className="card">
        <h1>Product Sentiment Analyzer</h1>
        <p className="subtitle">Scrape customer reviews and see sentiment charts</p>

        {/* Product Link Input */}
        <input
          type="text"
          placeholder="Enter Amazon or Flipkart product link"
          value={productLink}
          onChange={(e) => setProductLink(e.target.value)}
        />
        <button onClick={scrapeReviews}>Scrape Reviews & Update</button>

        {/* Review List */}
        {reviews.length > 0 && (
          <div className="review-list">
            <h2>All Reviews</h2>
            <ul>
              {reviews.map((r, i) => (
                <li key={i}>
                  <strong>{r.platform || "Unknown"}:</strong>{" "}
                  {r.reviewtitle ? `${r.reviewtitle} - ` : ""}
                  {r.review_text || ""} — <em>{r.sentiment}</em>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Charts */}
        <div style={{ marginTop: "40px", textAlign: "center" }}>
          <h2>Sentiment Bar Chart</h2>
          <img
            src={getBarChartUrl(chartTimestamp)}
            alt="Bar Chart"
          />

          <h2 style={{ marginTop: "30px" }}>Sentiment Pie Chart</h2>
          <img
            src={getPieChartUrl(chartTimestamp)}
            alt="Pie Chart"
          />
        </div>
      </div>
    </div>
  );
}

export default App;
