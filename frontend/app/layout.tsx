import type { Metadata } from "next";
import { Noto_Sans_JP } from "next/font/google";
import "./globals.css";

const noto = Noto_Sans_JP({
  subsets: ['latin'],
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
  return (
    <html lang="jp">
      <body className={noto.className}>
        {children}
      </body>
    </html>
  );
}
