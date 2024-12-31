import type { Metadata } from "next";
import { M_PLUS_1 } from "next/font/google";
import "./globals.css";
import Head from 'next/head';

const mplus = M_PLUS_1({
  subsets: ['latin']
});

export const metadata: Metadata = {
  title: "生成詩人A - Boundless Voices",
  description: "「生成詩人A - boundless voices」は、60秒ごとに新たな歌詞が生成され続けるインタラクティブな詩的体験を提供します。時間の流れと共に生まれる言葉のリズムと響きを感じる、終わりなき詩の旅へと誘います。",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  // Todo ogp設定
  return (
    <html lang="jp">
      <Head>
        <title>生成詩人A - Boundless Voices</title>
        <meta property="og:title" content="タイトル" />
        <meta property="og:description" content="description" />
        <meta property="og:image" content="imageURL" />
        <meta property="og:url" content="URL" />
        <meta name="twitter:card" content="twitterimage" />
        <meta name='twitter:title' content="生成詩人A - Boundless Voices" />
        <meta name='twitter:description' content="" />
        <meta name='twitter:image' content="" />
      </Head>
      <body className={mplus.className}>
        {children}
      </body>
    </html>
  );
}
