/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  output: "standalone", // Optimizes build for production deployment
  // You can add environment variable configurations here if needed
  env: {
    // Add environment variables that should be accessible by the browser
  },
};

module.exports = nextConfig;
