/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  compress: true,
  images: {
    domains: [
      'www.google.com',
      'google.com',
      'youtube.com',
      'www.youtube.com',
      'github.com',
      'www.github.com',
      'stackoverflow.com',
      'www.stackoverflow.com',
      'medium.com',
      'www.medium.com',
      'dev.to',
      'www.dev.to',
    ],
    formats: ['image/avif', 'image/webp'],
  },
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ]
  },
  async redirects() {
    return []
  },
  experimental: {
    // serverActions: true, // Já habilitado por padrão no Next.js 15
    // typedRoutes: true, // Rotas tipadas (experimental)
  },
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    return config
  },
}

module.exports = nextConfig
