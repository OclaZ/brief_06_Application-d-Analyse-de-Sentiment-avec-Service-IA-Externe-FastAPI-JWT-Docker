    "use client";

import { useRouter } from "next/navigation";

export default function LandingPage() {
  const router = useRouter();

  const goToSentiment = () => {
    router.push("/login");
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
        padding: 20,
        background:
          "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        color: "#fff",
        textAlign: "center",
      }}
    >
      <h1 style={{ fontSize: 48, fontWeight: 700, marginBottom: 20 }}>
        Sentiment Analyzer
      </h1>

      <p style={{ fontSize: 18, maxWidth: 600, marginBottom: 40 }}>
        Analyze customer reviews, social media comments, and e-commerce
        feedback automatically. Powered by AI, with real-time sentiment
        scoring.
      </p>

      <button
        onClick={goToSentiment}
        style={{
          padding: "15px 30px",
          fontSize: 18,
          fontWeight: 600,
          backgroundColor: "#fff",
          color: "#764ba2",
          border: "none",
          borderRadius: 8,
          cursor: "pointer",
          transition: "all 0.2s",
        }}
        onMouseOver={(e) =>
          (e.currentTarget.style.backgroundColor = "#f0f0f0")
        }
        onMouseOut={(e) =>
          (e.currentTarget.style.backgroundColor = "#fff")
        }
      >
        Go to Sentiment Analysis
      </button>

      <footer style={{ marginTop: 60, fontSize: 14, opacity: 0.8 }}>
 OclaZ
      </footer>
    </div>
  );
}
