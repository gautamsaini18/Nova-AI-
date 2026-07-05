import type { Metadata } from "next";
import { Inter, Outfit } from "next/font/google";
import "./globals.css";
import { Toaster } from "react-hot-toast";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const outfit = Outfit({
  subsets: ["latin"],
  variable: "--font-outfit",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Nova AI — Next-Generation AI Voice Assistant",
  description:
    "Nova AI is your intelligent voice assistant powered by GPT-4. Experience natural conversations, smart home control, and 60+ premium voice options. Comparable to Siri, Alexa, and Google Assistant.",
  keywords: [
    "AI voice assistant",
    "Nova AI",
    "GPT-4",
    "voice recognition",
    "smart home",
    "AI chat",
    "voice commands",
  ],
  authors: [{ name: "Nova AI Team" }],
  openGraph: {
    title: "Nova AI — Next-Generation AI Voice Assistant",
    description: "Your intelligent AI assistant with natural voice, smart automation, and human-like conversations.",
    type: "website",
    siteName: "Nova AI",
  },
  twitter: {
    card: "summary_large_image",
    title: "Nova AI — Next-Generation AI Voice Assistant",
    description: "Your intelligent AI assistant with natural voice, smart automation, and human-like conversations.",
  },
  viewport: "width=device-width, initial-scale=1",
  themeColor: "#6C63FF",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${outfit.variable}`}>
      <body className={`${inter.className} antialiased`}>
        {children}
        <Toaster
          position="top-right"
          toastOptions={{
            style: {
              background: "var(--bg-elevated)",
              color: "var(--text-primary)",
              border: "1px solid rgba(255,255,255,0.08)",
              borderRadius: "12px",
              fontSize: "14px",
              backdropFilter: "blur(20px)",
            },
            success: {
              iconTheme: {
                primary: "#6C63FF",
                secondary: "white",
              },
            },
            error: {
              iconTheme: {
                primary: "#FF6B9D",
                secondary: "white",
              },
            },
          }}
        />
      </body>
    </html>
  );
}
