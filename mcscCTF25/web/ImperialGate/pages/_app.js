import Head from "next/head";
import "../styles/globals.css";

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        {/* Preload fonts to prevent FOUC */}
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
        {/* Set default background color to prevent flashing */}
        <style>{`
          body {
            margin: 0;
            padding: 0;
            background-color: #1a1a1a;
            color: #f2e8c9;
          }
        `}</style>
      </Head>
      <Component {...pageProps} />
    </>
  );
}

export default MyApp;
