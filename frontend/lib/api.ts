export const API_URL = "http://localhost:8000";

// ---------- Types ----------
export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface PredictResponse {
  score: number;
  sentiment: "positive" | "negative" | "neutral";
}

// ---------- API Calls ----------
export async function apiLogin(username: string, password: string): Promise<LoginResponse> {
  const res = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!res.ok) {
    throw new Error("Invalid credentials");
  }

  return res.json() as Promise<LoginResponse>;
}

export async function apiPredict(text: string, token: string): Promise<PredictResponse> {
  const res = await fetch(`${API_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ text }),
  });

  if (!res.ok) {
    throw new Error("Prediction failed");
  }

  return res.json() as Promise<PredictResponse>;
}
