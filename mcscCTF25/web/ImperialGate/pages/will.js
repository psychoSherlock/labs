import Head from "next/head";
import Link from "next/link";
import { useEffect, useState } from "react";

export default function Profile() {
  const [torchFlicker, setTorchFlicker] = useState(false);
  const [revealWill, setRevealWill] = useState(false);
  const [flag, setFlag] = useState("");

  useEffect(() => {
    const flickerInterval = setInterval(() => {
      setTorchFlicker((prev) => !prev);
    }, 700);

    const revealTimer = setTimeout(() => {
      setRevealWill(true);

      fetch("/api/f8a29b7d34e6c1d5", {
        method: "GET",
        headers: {
          "x-f8a29b7d": "f8a29b7d34e6c1d5",
        },

        credentials: "same-origin",
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to retrieve the sacred message");
          }
          return response.json();
        })
        .then((data) => {
          if (data.flag) {
            setFlag(data.flag);
          }
        })
        .catch((error) => {
          console.error("Error fetching the Emperor's will:", error);
          setFlag("The Emperor's sacred message is unavailable.");
        });
    }, 1500);

    return () => {
      clearInterval(flickerInterval);
      clearTimeout(revealTimer);
    };
  }, []);

  return (
    <div className="emperors-will">
      <Head>
        <title>The Will</title>
        <style>{`
          @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700;900&family=Cormorant+Garamond:wght@400;600&family=MedievalSharp&display=swap');
          
          :root {
            --ancient-gold: #d4af37;
            --imperial-gold: #ffdc73;
            --dark-stone: #1a1a1a;
            --worn-parchment: #f2e8c9;
            --scroll-color: #e7d7b1;
            --royal-purple: #541388;
          }
          
          body {
            margin: 0;
            padding: 0;
            background-color: var(--dark-stone);
            color: var(--worn-parchment);
            font-family: 'Cormorant Garamond', serif;
            overflow-x: hidden;
          }
          
          .emperors-will {
            min-height: 100vh;
            background-image: 
              linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.75)),
              url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23d4af37' fill-opacity='0.2' fill-rule='evenodd'%3E%3Ccircle cx='3' cy='3' r='3'/%3E%3Ccircle cx='13' cy='13' r='3'/%3E%3C/g%3E%3C/svg%3E");
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
          }
          
          .will-container {
            text-align: center;
            max-width: 900px;
            padding: 3rem;
            position: relative;
            z-index: 10;
            animation: fade-in 2s ease-out forwards;
          }
          
          @keyframes fade-in {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
          }
          
          .will-title {
            font-family: 'Cinzel Decorative', cursive;
            color: var(--ancient-gold);
            font-size: 3.5rem;
            margin-bottom: 1.5rem;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            text-shadow: 0 0 10px rgba(212, 175, 55, 0.5), 0 0 20px rgba(212, 175, 55, 0.3);
          }
          
          .will-subtitle {
            font-family: 'Cinzel Decorative', cursive;
            color: var(--imperial-gold);
            font-size: 1.8rem;
            margin-bottom: 3rem;
            font-weight: 400;
            text-shadow: 0 0 5px rgba(212, 175, 55, 0.3);
          }
          
          .sacred-scroll {
            background-color: var(--scroll-color);
            max-width: fit-content;
            margin: 0 auto 3rem;
            padding: 3rem 2.5rem;
            border-radius: 5px;
            position: relative;
            color: #433520;
            font-family: 'MedievalSharp', cursive;
            font-size: 1.8rem;
            box-shadow: 0 10px 25px rgba(0,0,0,0.7);
            transform-style: preserve-3d;
            transform: perspective(1000px) rotateX(5deg);
            line-height: 1.7;
          }
          
          .sacred-scroll::before,
          .sacred-scroll::after {
            content: '';
            position: absolute;
            height: 100%;
            width: 30px;
            top: 0;
            background: linear-gradient(to right, #c4b282, #e7d7b1);
            box-shadow: 0 5px 15px rgba(0,0,0,0.4);
            z-index: -1;
          }
          
          .sacred-scroll::before {
            left: -15px;
            border-radius: 15px 0 0 15px;
            transform: translateZ(-10px);
          }
          
          .sacred-scroll::after {
            right: -15px;
            border-radius: 0 15px 15px 0;
            transform: translateZ(-10px);
          }
          
          .sacred-scroll p {
            opacity: 0;
            animation: reveal-text 2s ease-out 1.5s forwards;
            position: relative;
            padding: 1rem 0;
            text-align: center;
          }
          
          @keyframes reveal-text {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
          }
          
          .imperial-seal {
            width: 150px;
            height: 150px;
            margin: 3rem auto;
            position: relative;
            animation: seal-appear 2s ease-out forwards, seal-glow 3s infinite alternate;
          }
          
          @keyframes seal-appear {
            0% { transform: scale(0.8); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
          }
          
          @keyframes seal-glow {
            0% { filter: drop-shadow(0 0 8px rgba(212, 175, 55, 0.7)); }
            100% { filter: drop-shadow(0 0 15px rgba(212, 175, 55, 0.9)) drop-shadow(0 0 30px rgba(212, 175, 55, 0.5)); }
          }
          
          .gate-button {
            display: inline-block;
            padding: 0.75rem 2rem;
            font-family: 'Cinzel Decorative', cursive;
            font-size: 1.25rem;
            color: var(--dark-stone);
            background: var(--ancient-gold);
            border: none;
            cursor: pointer;
            text-decoration: none;
            letter-spacing: 0.1em;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.5);
            margin-top: 2rem;
          }
          
          .gate-button:hover {
            box-shadow: 0 0 25px rgba(212, 175, 55, 0.8);
            color: var(--dark-stone);
          }
          
          .torch {
            position: absolute;
            width: 60px;
            height: 100px;
            opacity: 0.9;
            animation: torch-flicker 3s infinite alternate;
          }
          
          .torch-left {
            top: 20%;
            left: 8%;
            transform: rotate(-5deg);
          }
          
          .torch-right {
            top: 20%;
            right: 8%;
            transform: rotate(5deg);
          }
          
          .torch-flame {
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 30px;
            height: 50px;
            background: radial-gradient(ellipse at bottom, #ff6a00, #ff9900, transparent 80%);
            border-radius: 50% 50% 20% 20%;
            box-shadow: 0 0 20px 5px rgba(255, 106, 0, 0.6);
            animation: flame-flicker 0.5s infinite alternate;
          }
          
          .torch-base {
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 15px;
            height: 60px;
            background: linear-gradient(to right, #333, #777, #333);
            border-radius: 5px;
          }
          
          .torch-holder {
            position: absolute;
            bottom: 50px;
            left: 50%;
            transform: translateX(-50%);
            width: 25px;
            height: 10px;
            background: #444;
            border-radius: 5px;
          }
          
          @keyframes flame-flicker {
            0%, 100% { transform: translateX(-50%) scale(1, 1); }
            25% { transform: translateX(-55%) scale(1.1, 0.9); }
            50% { transform: translateX(-45%) scale(0.9, 1.1); }
            75% { transform: translateX(-50%) scale(1, 1); }
          }
          
          @keyframes torch-flicker {
            0% { opacity: 0.7; }
            25% { opacity: 0.8; }
            50% { opacity: 1; }
            75% { opacity: 0.9; }
            100% { opacity: 0.7; }
          }
          
          .imperial-crest {
            position: relative;
            width: 120px;
            height: 120px;
            margin: 0 auto 2rem;
          }
          
          .crest-rays {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(ellipse at center, rgba(212, 175, 55, 0.4) 0%, rgba(0, 0, 0, 0) 70%);
            animation: glow 4s infinite alternate;
            border-radius: 50%;
            transform: scale(1.2);
          }
          
          @keyframes glow {
            0% { opacity: 0.3; }
            100% { opacity: 0.7; }
          }
          
          .dust {
            position: absolute;
            width: 100%;
            height: 100%;
            pointer-events: none;
            background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='10' cy='10' r='1'/%3E%3Ccircle cx='30' cy='50' r='1'/%3E%3Ccircle cx='70' cy='30' r='1'/%3E%3Ccircle cx='90' cy='80' r='1'/%3E%3Ccircle cx='50' cy='20' r='1'/%3E%3Ccircle cx='20' cy='80' r='1'/%3E%3Ccircle cx='80' cy='50' r='1'/%3E%3C/g%3E%3C/svg%3E");
          }
          
          .bg-ornament {
            position: absolute;
            pointer-events: none;
            opacity: 0.15;
          }
          
          .ornament-top {
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 3rem;
            color: var(--ancient-gold);
          }
          
          .ornament-bottom {
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 3rem;
            color: var(--ancient-gold);
          }
          
          .flag-text {
            font-family: 'MedievalSharp', cursive;
            color: #8b0000;
            background: none;
            -webkit-text-fill-color: initial;
            font-weight: bold;
            font-size: 2 rem;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
            letter-spacing: 1.2px;
            
            display: inline-block;
            padding: 0.5rem 1.5rem;
            position: relative;
            z-index: 1;
          }
          
          .flag-text::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: -1;
          }
        `}</style>
      </Head>

      <div className="dust"></div>

      <div className={`torch torch-left ${torchFlicker ? "flicker" : ""}`}>
        <div className="torch-flame"></div>
        <div className="torch-holder"></div>
        <div className="torch-base"></div>
      </div>

      <div className={`torch torch-right ${!torchFlicker ? "flicker" : ""}`}>
        <div className="torch-flame"></div>
        <div className="torch-holder"></div>
        <div className="torch-base"></div>
      </div>

      <div className="bg-ornament ornament-top">✦ ♱ ✦</div>
      <div className="bg-ornament ornament-bottom">✦ ♱ ✦</div>

      <div className="will-container">
        <div className="imperial-crest">
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
          <div className="crest-rays" />
        </div>

        <h1 className="will-title">The Emperor's Will</h1>
        <h2 className="will-subtitle">Sacred Knowledge of the Ancients</h2>

        <div className="sacred-scroll">
          {revealWill ? (
            <p className="flag-text">
              {flag || "Loading the Emperor's sacred message..."}
            </p>
          ) : (
            <p style={{ visibility: "hidden" }}>
              Loading the Emperor's sacred message...
            </p>
          )}
        </div>

        <div className="imperial-seal">
          <svg width="150" height="150" viewBox="0 0 150 150">
            <defs>
              <radialGradient id="sealGlow" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="#b8860b" stopOpacity="1" />
                <stop offset="100%" stopColor="#8b0000" stopOpacity="0.2" />
              </radialGradient>
              <linearGradient id="sealGold" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stopColor="#d4af37" />
                <stop offset="50%" stopColor="#ffdc73" />
                <stop offset="100%" stopColor="#d4af37" />
              </linearGradient>
            </defs>
            <circle
              cx="75"
              cy="75"
              r="65"
              fill="url(#sealGlow)"
              opacity="0.3"
            />
            <circle
              cx="75"
              cy="75"
              r="55"
              fill="none"
              stroke="url(#sealGold)"
              strokeWidth="8"
            />
            <path
              d="M40 55 L75 30 L110 55 M50 65 C65 50, 85 50, 100 65 M45 90 C65 120, 85 120, 105 90"
              stroke="url(#sealGold)"
              strokeWidth="5"
              fill="none"
            />
            <circle cx="75" cy="75" r="10" fill="url(#sealGold)" />
          </svg>
        </div>

        <Link href="/" className="gate-button">
          Return to the Imperial Gate
        </Link>
      </div>
    </div>
  );
}
