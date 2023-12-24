import "~/styles/globals.css";

import { Inter } from "next/font/google";
import { headers } from "next/headers";

import { TRPCReactProvider } from "~/trpc/react";
import { Layout } from "~/app/components/layout";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  
  return (
    <html lang="en">
      <body className={`font-sans ${inter.variable}`}>
        <Layout>
          <TRPCReactProvider headers={headers()}>{children}</TRPCReactProvider>
        </Layout>
      </body>
    </html>
  );
}

export const metadata = {
  title: "Vibranium",
  description: "Security for LLM Apps",
  icons: [{ rel: "icon", url: "/favicon.ico" }],
};