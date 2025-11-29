import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter"
});

export const metadata: Metadata = {
  title: "AutoMed AI",
  description: "AI-powered medical image analysis and model training platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} antialiased`}>
        <div className="min-h-screen bg-gradient-to-br from-[hsl(240,10%,8%)] to-[hsl(240,10%,12%)]">
          <header className="border-b border-white/10 backdrop-blur-sm bg-white/5">
            <div className="container mx-auto px-6 py-4">
              <h1 className="text-2xl font-bold gradient-text">
                AutoMed AI
              </h1>
            </div>
          </header>
          <main className="container mx-auto px-6 py-8">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
