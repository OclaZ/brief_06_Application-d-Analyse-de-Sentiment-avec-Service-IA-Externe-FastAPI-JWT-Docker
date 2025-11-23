import "./globals.css";
import { ReactNode } from "react";

export const metadata = {
  title: "Sentiment Analyzer",
  description: "Next.js frontend for sentiment API",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: "sans-serif" }}>
        {children}
      </body>
    </html>
  );
}
