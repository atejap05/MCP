import { JSDOM } from 'jsdom'

interface URLMetadata {
  title?: string
  description?: string
  favicon?: string
  image?: string
}

export async function extractURLMetadata(url: string): Promise<URLMetadata | null> {
  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 5000)

    const response = await fetch(url, {
      signal: controller.signal,
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; BookmarkBot/1.0)',
      },
    })

    clearTimeout(timeout)

    if (!response.ok) {
      return null
    }

    const html = await response.text()
    const dom = new JSDOM(html)
    const doc = dom.window.document

    // Extrair metadados
    const metadata: URLMetadata = {}

    // Título
    metadata.title =
      doc.querySelector('meta[property="og:title"]')?.getAttribute('content') ||
      doc.querySelector('meta[name="twitter:title"]')?.getAttribute('content') ||
      doc.querySelector('title')?.textContent ||
      undefined

    // Descrição
    metadata.description =
      doc.querySelector('meta[property="og:description"]')?.getAttribute('content') ||
      doc.querySelector('meta[name="description"]')?.getAttribute('content') ||
      undefined

    // Favicon
    const favicon =
      doc.querySelector('link[rel="icon"]')?.getAttribute('href') ||
      doc.querySelector('link[rel="shortcut icon"]')?.getAttribute('href') ||
      '/favicon.ico'

    metadata.favicon = new URL(favicon, url).href

    // Imagem
    metadata.image =
      doc.querySelector('meta[property="og:image"]')?.getAttribute('content') ||
      doc.querySelector('meta[name="twitter:image"]')?.getAttribute('content') ||
      undefined

    return metadata
  } catch (error) {
    console.error('Failed to extract metadata:', error)
    return null
  }
}
