/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ["lh3.googleusercontent.com"],
  },
  async redirects() {
    return [
      {
        source: "/github",
        destination: "https://github.com/hxu296/gt-chat",
        permanent: false,
      },
    ];
  },
};

module.exports = nextConfig;
