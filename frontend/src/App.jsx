import { useState } from "react";
import axios from "axios";

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [recommendations, setRecommendations] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchRecommendations = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await axios.post("http://localhost:5000/chat", { prompt });
      setRecommendations(response.data.recommendations);
    } catch (err) {
      setError("Error fetching recommendations.");
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">🏠 Real Estate Chatbot</h1>

      <textarea
        className="border p-4 w-full h-32 rounded"
        placeholder="Describe your ideal home, e.g., 'Find me a 2-bedroom apartment under $3000.'"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />

      <button
        onClick={fetchRecommendations}
        className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Get Recommendations
      </button>

      {loading && <p className="mt-4">Loading...</p>}
      {error && <p className="mt-4 text-red-500">{error}</p>}

      {recommendations && (
        <div className="mt-4 bg-gray-100 p-4 rounded whitespace-pre-line">
          {recommendations}
        </div>
      )}
    </div>
  );
}
