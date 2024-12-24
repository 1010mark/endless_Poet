"use client";
import { useEffect, useRef, useState } from "react";
import styles from "./page.module.css";

export default function Home() {
  let cautionRef = useRef<HTMLDivElement>(null);
  let lastWaterRef = useRef<HTMLDivElement>(null);
  let logoRef = useRef<HTMLIFrameElement>(null);
  let logoContainerRef = useRef<HTMLDivElement>(null);
  let [showLogo, setShowLogo] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    setIsMobile(window.innerWidth <= 768);
  }, []);

  useEffect(() => {
    const lastWaterElement = lastWaterRef.current;
    const changeIntoCaution = () => {
      cautionRef.current?.classList.add(styles["cautionOn"]);
      logoContainerRef.current?.classList.add(styles["logoContainerOff"]);
    }

    if (lastWaterElement) {
      const handleAnimationEnd = () => {
        setShowLogo(true);
        logoRef.current?.contentWindow?.postMessage("startAnimation", "*");
        setTimeout(changeIntoCaution, 5000);
      };
      lastWaterElement.addEventListener('animationend', handleAnimationEnd);
      return () => lastWaterElement.removeEventListener('animationend', handleAnimationEnd); // クリーンアップ関数
    }
  }, []);

  return (
    <main className={styles.main}>
      <div style={{ display: showLogo ? 'block' : 'none' }} className={styles.logoContainer} ref={logoContainerRef}>
        <iframe src={isMobile ? "./html/logo-phone.html" : "./html/logo-PC.html"} className={styles.logo} ref={logoRef} />
      </div>
      <div className={styles["title-bg"]} style={{ display: !showLogo ? 'block' : 'none' }}></div>
      <div className={`${styles["title-water"]} ${styles["title-water1"]}`}></div>
      <div className={`${styles["title-water"]} ${styles["title-water2"]}`}></div>
      <div className={`${styles["title-water"]} ${styles["title-water3"]}`} ref={lastWaterRef}></div>
      <div ref={cautionRef} className={styles.caution}>
        <div className={styles.cautionInner}>
          <h1>再考は二度とない。</h1>
          <p>本Webアプリケーションでは音声を再生します。<br />
          そのすべてがリアルタイムに自動生成された言葉で、<br />
          空想上のお話です。<br />
          真に受けてはなりません。必ず。<br />
          <br />
          <small>語り部: VOICEVOX ナースロボ_タイプT<br />
          <span style={{color: "darkslategrey"}}>本Webアプリケーションは謎解きではありません。ご注意ください。</span>

          </small>
          </p>
          <div className={styles.startButton}>Start ▶</div>
        </div>
      </div>
    </main>
  );
}
