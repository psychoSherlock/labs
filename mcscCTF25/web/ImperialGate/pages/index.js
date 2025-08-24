import Link from "next/link";
import Head from "next/head";
import { useEffect, useState } from "react";
import styles from "../styles/Home.module.css";

export default function Home() {
  const [torchFlicker, setTorchFlicker] = useState(false);

  useEffect(() => {
    // Create torch flickering effect
    const flickerInterval = setInterval(() => {
      setTorchFlicker((prev) => !prev);
    }, 700);

    return () => clearInterval(flickerInterval);
  }, []);

  return (
    <div className={styles.imperialGate}>
      <Head>
        <title>The Imperial Gate</title>
        {/* Font preload to avoid FOUC */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700;900&family=Cormorant+Garamond:wght@400;600&display=swap"
          rel="stylesheet"
          media="print"
          onLoad="this.media='all'"
        />
      </Head>

      <div className={styles.dust}></div>

      <div
        className={`${styles.torch} ${styles.torchLeft} ${
          torchFlicker ? styles.flicker : ""
        }`}
      >
        <div className={styles.torchFlame}></div>
        <div className={styles.torchHolder}></div>
        <div className={styles.torchBase}></div>
      </div>

      <div
        className={`${styles.torch} ${styles.torchRight} ${
          !torchFlicker ? styles.flicker : ""
        }`}
      >
        <div className={styles.torchFlame}></div>
        <div className={styles.torchHolder}></div>
        <div className={styles.torchBase}></div>
      </div>

      <div className={`${styles.bgOrnament} ${styles.ornamentTop}`}>✦ ❧ ✦</div>
      <div className={`${styles.bgOrnament} ${styles.ornamentBottom}`}>
        ✦ ☙ ✦
      </div>

      <div className={styles.gateContainer}>
        <h1 className={styles.imperialTitle}>The Imperial Gate</h1>
        <h2 className={styles.imperialSubtitle}>
          Guardian of Sacred Knowledge
        </h2>

        <div className={styles.imperialCrest}>
          <svg width="120" height="120" viewBox="0 0 120 120">
            <defs>
              <radialGradient id="crestGlow" cx="50%" cy="50%" r="60%">
                <stop offset="0%" stopColor="#b8860b" stopOpacity="0.8" />
                <stop offset="100%" stopColor="#8b0000" stopOpacity="0" />
              </radialGradient>
              <linearGradient id="crestGold" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stopColor="#b8860b" />
                <stop offset="100%" stopColor="#fffbe6" />
              </linearGradient>
            </defs>
            <circle cx="60" cy="60" r="48" fill="url(#crestGlow)" />
            <circle
              cx="60"
              cy="60"
              r="36"
              fill="#0a0a0a"
              stroke="url(#crestGold)"
              strokeWidth="6"
            />
            {/* Imperial sigil: stylized crown+eye */}
            <path
              d="M40 70 Q60 40 80 70"
              stroke="#b8860b"
              strokeWidth="4"
              fill="none"
            />
            <ellipse
              cx="60"
              cy="65"
              rx="8"
              ry="5"
              fill="#8b0000"
              stroke="#b8860b"
              strokeWidth="2"
            />
            <circle cx="60" cy="65" r="2.5" fill="#fffbe6" />
            <path
              d="M50 55 L60 45 L70 55"
              stroke="#b8860b"
              strokeWidth="3"
              fill="none"
            />
          </svg>
          <div className={styles.crestRays} />
        </div>

        <div className={styles.imperialWarning}>
          Beyond this threshold lies the Emperor's Will. Those without the Seal
          shall turn back—or be lost forever.
        </div>

        <Link href="/will" className={styles.gateButton}>
          Enter the Sacred Chamber
        </Link>
      </div>
    </div>
  );
}
