import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'
import { NextResponse, type NextRequest } from 'next/server'

// Rotas que não precisam de autenticação
const isPublicRoute = createRouteMatcher([
  '/',
  '/sign-in(.*)',
  '/sign-up(.*)',
  '/.well-known/(.*)', // OAuth discovery
  '/api/webhooks/(.*)', // Webhooks externos
  '/api/health', // Health check
])

// Rotas de API que precisam de autenticação
const isApiRoute = createRouteMatcher(['/api/(.*)'])

export default clerkMiddleware(async (auth, request: NextRequest) => {
  const { userId } = await auth()

  // Log para debug (remover em produção)
  if (process.env.NODE_ENV === 'development') {
    console.warn(`[Middleware] ${request.method} ${request.nextUrl.pathname}`, {
      userId,
      isPublic: isPublicRoute(request),
      isApi: isApiRoute(request),
    })
  }

  // Se é rota de API e não está autenticado
  if (isApiRoute(request) && !isPublicRoute(request) && !userId) {
    console.warn(`[Middleware] Unauthorized API access: ${request.method} ${request.nextUrl.pathname}`)
    return NextResponse.json(
      {
        error: 'Unauthorized',
        message: 'Authentication required',
        code: 'AUTH_REQUIRED',
      },
      { status: 401 }
    )
  }

  // Adiciona headers de segurança
  const response = NextResponse.next()

  // CORS headers para API
  if (isApiRoute(request)) {
    response.headers.set('X-Content-Type-Options', 'nosniff')
    response.headers.set('X-Frame-Options', 'DENY')
    response.headers.set('X-XSS-Protection', '1; mode=block')
  }

  return response
})

export const config = {
  matcher: ['/((?!.*\\..*|_next).*)', '/(api|trpc)(.*)'],
}
