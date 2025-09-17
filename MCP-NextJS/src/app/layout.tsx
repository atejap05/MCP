import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { ClerkProvider } from '@clerk/nextjs'
import { Header } from '@/components/Header'
import './globals.css'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

export const metadata: Metadata = {
  title: {
    default: 'Bookmark Manager',
    template: '%s | Bookmark Manager',
  },
  description: 'Gerencie seus bookmarks favoritos com integração MCP',
  keywords: ['bookmarks', 'favoritos', 'links', 'MCP', 'AI'],
  authors: [{ name: 'Seu Nome' }],
  creator: 'Bookmark Manager Team',
  openGraph: {
    type: 'website',
    locale: 'pt_BR',
    url: 'https://bookmarks.example.com',
    title: 'Bookmark Manager',
    description: 'Gerencie seus bookmarks favoritos',
    siteName: 'Bookmark Manager',
  },
}

interface RootLayoutProps {
  children: React.ReactNode
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <ClerkProvider
      appearance={{
        baseTheme: undefined, // ou 'dark' para tema escuro
        layout: {
          socialButtonsPlacement: 'bottom',
          socialButtonsVariant: 'iconButton',
        },
        variables: {
          colorPrimary: '#0070f3',
          colorBackground: '#ffffff',
          colorText: '#000000',
          colorTextSecondary: '#666666',
          colorDanger: '#ee0000',
          colorSuccess: '#10b981',
          colorWarning: '#f59e0b',
          borderRadius: '0.5rem',
          fontFamily: 'var(--font-inter)',
        },
        elements: {
          formButtonPrimary: 'bg-blue-600 hover:bg-blue-700 transition-colors',
          card: 'shadow-lg border border-gray-200',
          headerTitle: 'text-2xl font-bold',
          headerSubtitle: 'text-gray-600',
        },
      }}
    >
      <html lang="pt-BR" className={inter.variable}>
        <body className={inter.className}>
          <div className="min-h-screen bg-gray-50">
            <Header />
            <main className="main-content">{children}</main>
          </div>
        </body>
      </html>
    </ClerkProvider>
  )
}
