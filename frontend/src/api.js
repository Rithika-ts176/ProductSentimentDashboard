import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000";

// -------------------- REVIEWS --------------------
// Fetch all reviews
export const fetchAllReviews = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/reviews`);
    return response.data;
  } catch (error) {
    console.error("Error fetching reviews:", error);
    return [];
  }
};

// -------------------- SCRAPE REVIEW ----------------
export const scrapeReviewFromLink = async (url) => {
  try {
    const response = await axios.post(`${BASE_URL}/scrape`, { url });
    return response.data;
  } catch (error) {
    console.error("Error scraping reviews:", error);
    return null;
  }
};

// -------------------- CHART URLS ----------------
export const getBarChartUrl = () => `${BASE_URL}/chart/bar?ts=${Date.now()}`;
export const getPieChartUrl = () => `${BASE_URL}/chart/pie?ts=${Date.now()}`;
