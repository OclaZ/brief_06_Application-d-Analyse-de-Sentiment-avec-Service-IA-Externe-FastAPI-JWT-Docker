"use client";

import { useState } from "react";

interface Prediction {
  label: string;
  score: number;
}

interface SentimentResult {
  text: string;
  bestLabel: string;
  bestScore: number;
  raw: Prediction[];
}

export default function SentimentPage() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<SentimentResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyzeSentiment = async () => {
    setLoading(true);
    setResult(null);
    setError(null);

    const token = localStorage.getItem("token");

    if (!token) {
      setError("You are not logged in");
      setLoading(false);
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ text }),
      });

      if (res.status === 401) {
        setError("Not authenticated. Please login.");
        setLoading(false);
        return;
      }

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        setError(err.detail || "Backend error");
        setLoading(false);
        return;
      }

      const data = await res.json();
      // Ensure we have the expected nested array
      const predictions =
        Array.isArray(data.sentiment) && Array.isArray(data.sentiment[0])
          ? data.sentiment[0]
          : [];

      if (predictions.length === 0) {
        setError("No sentiment data returned from backend");
        setLoading(false);
        return;
      }

      // Pick the item with highest score
      const best = predictions.reduce((a: Prediction, b: Prediction) =>
        a.score > b.score ? a : b
      );

      setResult({
        text: data.text,
        bestLabel: best.label,
        bestScore: best.score,
        raw: predictions,
      });
    } catch (err) {
      console.error(err);
      setError("Network or parsing error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "auto", padding: 40 }}>
      <h1>Sentiment Analysis</h1>

      <textarea
        rows={4}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type your text..."
        style={{ width: "100%", padding: 10 }}
      />

      <button
        onClick={analyzeSentiment}
        disabled={loading || !text.trim()}
        style={{
          marginTop: 10,
          padding: "10px 20px",
          backgroundColor: "#0070f3",
          color: "#fff",
          borderRadius: 5,
          cursor: "pointer",
        }}
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {error && (
        <p style={{ color: "red", marginTop: 20 }}>
          <b>Error:</b> {error}
        </p>
      )}

      {result && (
        <div
          style={{
            marginTop: 20,
            padding: 20,
            border: "1px solid #ddd",
            borderRadius: 5,
          }}
        >
          <h3>Result</h3>
          <p>
            <b>Text:</b> {result.text}
          </p>
          <p>
            <b>Predicted Sentiment:</b> {result.bestLabel}
          </p>
          <p>
            <b>Score:</b> {result.bestScore.toFixed(4)}
          </p>

          <div style={{ marginTop: 15 }}>
            <b>All predictions:</b>
            <ul>
              {result.raw.map((item: Prediction, idx: number) => (
                <li key={idx}>
                  {item.label}: {item.score.toFixed(4)}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
