import "@/styles/globals.css";
import type { AppProps } from "next/app";
import { Analytics } from "@vercel/analytics/react";
import { Provider as RWBProvider } from "react-wrap-balancer";
import cx from "classnames";
import localFont from "@next/font/local";
import { Inter } from "@next/font/google";

const sfPro = localFont({
  src: "../styles/SF-Pro-Display-Medium.otf",
  variable: "--font-sf",
});

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export default function MyApp({
  Component,
  pageProps: { ...pageProps },
}: AppProps) {
  return (
    <div className="h-full w-full">
      <RWBProvider>
        <main className={cx(sfPro.variable, inter.variable, "h-full w-full")}>
          <Component {...pageProps} />
        </main>
      </RWBProvider>
      <Analytics />
    </div>
  );
}
