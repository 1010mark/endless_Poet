"use client";
import { useEffect, useRef, useState } from "react";
import styles from "./page.module.css";
import io from 'socket.io-client';
interface Subtitle {
  time: number;
  text: string;
}

export default function Home() {
  let cautionRef = useRef<HTMLDivElement>(null);
  let playerRef = useRef<HTMLDivElement>(null);
  let lastWaterRef = useRef<HTMLDivElement>(null);
  let logoRef = useRef<HTMLIFrameElement>(null);
  let logoContainerRef = useRef<HTMLDivElement>(null);
  const [audioBuffers, setAudioBuffers] = useState<(AudioBuffer)[]>([]);
  const [scripts, setScripts] = useState<Subtitle[][]>([]);
  const audioContextRef = useRef<AudioContext | null>(null);
  const nextStartTimeRef = useRef(0);
  const [isPlaying, setIsPlaying] = useState(false);
  // const [isCaracterFadingOut, setIsCaracterFadingOut] = useState(false);
  // const [charactors, setCharactors] = useState<string[]>([]);
  // const [gridRows, setGridRows] = useState<number>(5);
  // const [gridColumns, setGridColumns] = useState<number>(5);
  const [showLogo, setShowLogo] = useState<boolean>(false);
  const [isMobile, setIsMobile] = useState<boolean>(false);
  const scriptsRef = useRef(scripts);
 // const timeoutsRef = useRef<NodeJS.Timeout[]>([]);
  const [lyrics, setLyrics] = useState<string[]>([]);
  const [isScriptOver, setIsScriptOver] = useState<boolean>(false);
  const [currentTime, setCurrentTime] = useState<number>(0);
  const scriptIndex = useRef<number>(0);

  // モバイル処理
  useEffect(() => {
    setIsMobile(window.innerWidth <= 768);
  }, []);

  // useEffect(() => {
  //   // コンポーネントのアンマウント時にすべてのタイムアウトをクリア
  //   return () => {
  //     timeoutsRef.current.forEach((timeoutId) => clearTimeout(timeoutId));
  //     timeoutsRef.current = [];
  //   };
  // }, []);

  useEffect(() => {
    scriptsRef.current = scripts;
  }, [scripts]);

  // ロゴ表示処理
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

  // socket.io
  useEffect(() => {
    const socket = io(process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:5001", {
      transports: ['websocket'],
      withCredentials: true
    });
    const bufferLimit = process.env.NEXT_PUBLIC_BUFFER_LIMIT ? parseInt(process.env.NEXT_PUBLIC_BUFFER_LIMIT) : 10;

    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
    }
    setInterval(() => {
      socket.emit('request_audio');
      console.log("Sent request_audio");
    }, 35000);
    socket.emit('request_audio');

    socket.on('script_data', (data) => {
      if (scripts.length <= bufferLimit) setScripts((prev) => [...prev, data]);
    });

    socket.on('audio', async (data: ArrayBuffer) => {
      try {
        const arrayBuffer = data;
  
        // const blob = new Blob([arrayBuffer], { type: 'audio/mp3' });
        const audioBuffer = await audioContextRef.current?.decodeAudioData(arrayBuffer);
        if (audioBuffer && audioBuffers.length <= bufferLimit) {
          setAudioBuffers((prev) => [...prev, audioBuffer]);
          console.log("Audio buffer stored successfully.");
        } else {
          throw new Error("Audio decoding failed.");
        }
      } catch (err) {
        console.error("Error processing audio data:", err);
      }
    });
    
  }, []);

  // 再生処理
  useEffect(() => {
    const audioContext = audioContextRef.current;
    if (audioBuffers.length > 0 && audioContext && isPlaying) {
      const buffer = audioBuffers[0];

      const source = audioContext.createBufferSource();
      source.buffer = buffer;
      source.connect(audioContext.destination);

      const now = audioContext.currentTime;
      const startTime = Math.max(now, nextStartTimeRef.current);
      source.start(startTime);
      console.log("Next Audio started at", startTime);

      nextStartTimeRef.current = startTime + buffer.duration;
      source.onended = () => {
        setAudioBuffers((prev) => prev.slice(1));
        setScripts((prev) => prev.slice(1));
        setIsScriptOver(false);
        scriptIndex.current++;
      };
    }
  }, [audioBuffers, isPlaying]);

  function handleStart() {
    if (isPlaying) return;
    cautionRef.current?.classList.remove(styles["cautionOn"]);
    cautionRef.current?.classList.add(styles["cautionOff"]);
    playerRef.current?.classList.add(styles["playerOn"]);
    setTimeout(() => {
      setIsPlaying(true);
    }, 1000);
  }

  useEffect(() => {
    const updateTime = () => {
      setCurrentTime(audioContextRef.current?.currentTime ?? 0);
      if (isPlaying) {
        requestAnimationFrame(updateTime);
      }
    };
    requestAnimationFrame(updateTime);
  }, [isPlaying]);

  useEffect(() => {
    if (!isPlaying) return;

    const intervalId = setInterval(() => {
      let script = scripts[0];
      if (!script) return;
      const nextLyrics = script[0]?.text;
      const nextTime = script[0]?.time;
      console.log("Now time:", audioContextRef.current?.currentTime, "Next Lyr:", nextLyrics ,lyrics, script);
      const now = audioContextRef.current ? audioContextRef.current.currentTime - scriptIndex.current * 64 : 0;
      if (now > nextTime && script.length > 0 && !isScriptOver) {
        setLyrics((prev) => [...prev, nextLyrics]);
        script = script.slice(1);
        setScripts((prev) => [script, ...prev.slice(1)]);
      }
      if (script.length === 0) {
        setScripts((prev) => prev.slice(1));
        setIsScriptOver(true);
      }
    }, 100);

    return () => clearInterval(intervalId);
  }, [isPlaying, scripts]);

  useEffect(() => {
    const script = document.createElement("script");
    script.src = "https://platform.twitter.com/widgets.js";
    script.async = true;
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
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
          <h1>一過性の言葉。</h1>
          <p>本Webアプリケーションでは{isMobile && <br />}音声を再生します。<br />
            そのすべてがリアルタイムに{isMobile && <br />}生成された言葉で{isMobile && "あり"}、<br />
            空想上のお話です。<br />
            真に受けてはなりません。必ず。<br />
            <br />
            <small>語り部: VOICEVOX ナースロボ_タイプT<br />
              <span style={{ color: "darkslategrey" }}>本Webアプリケーションは謎解きではありません。ご注意ください。</span>
            </small>
          </p>
          <div className={styles.startButton} onClick={handleStart}>Start ▶</div>
        </div>
      </div>
      <div ref={playerRef} className={styles["player"]}>
        <header className={styles["player-header"]}>
          <span className={styles["player-header-left"]}>{currentTime.toFixed(2)} s</span>
          <span className={styles["player-header-right"]}>
            <a href={`https://twitter.com/share?text=${encodeURI(`私は${currentTime.toFixed(1)}秒間、その声に耳を傾けました。`)}${process.env.NEXT_PUBLIC_BASE_URL ? `&url=${process.env.NEXT_PUBLIC_BASE_URL}` : ""}`} className="twitter-share-button" data-show-count="false">
              Post
            </a>
          </span>
        </header>

        <p className={styles["lyrics"]}>
          {(() => {
            let elements = [];
            for (let i = 0; i < lyrics.length-1; i++) {
              elements.push(<span key={i} className={styles["lyrics-content"]}>{lyrics[i]}</span>);
            }
            if(lyrics.length > 0) {
              elements.push(<span key={lyrics.length-1} className={styles["lyrics-content-last"]}>{lyrics[lyrics.length-1]}</span>);
            }
            return elements;
          })()}
        </p>
      </div>
    </main>
  );
}
