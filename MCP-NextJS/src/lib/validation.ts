import { z } from 'zod'

// Schemas reutilizáveis
export const urlSchema = z
  .string()
  .url()
  .transform((url) => {
    // Normaliza URLs
    try {
      const urlObj = new URL(url)
      return urlObj.href
    } catch {
      return url
    }
  })

// Rate limiting simples
const rateLimitMap = new Map<string, { count: number; resetTime: number }>()

export const checkRateLimit = (
  userId: string,
  limit: number = 60,
  windowMs: number = 60000
): boolean => {
  const now = Date.now()
  const userLimit = rateLimitMap.get(userId)

  if (!userLimit || now > userLimit.resetTime) {
    rateLimitMap.set(userId, {
      count: 1,
      resetTime: now + windowMs,
    })
    return true
  }

  if (userLimit.count >= limit) {
    return false
  }

  userLimit.count++
  return true
}
