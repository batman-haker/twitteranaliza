import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Twitter/X Analyzer",
  description: "Analyze Twitter/X accounts and extract article links",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.Node;
}>) {
  return (
    <html lang="en">
      <body className="bg-gray-50">{children}</body>
    </html>
  );
}
