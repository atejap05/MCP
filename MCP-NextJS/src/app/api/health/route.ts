import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET() {
  const startTime = Date.now()

  try {
    // Verifica conexão com banco de dados
    await prisma.$queryRaw`SELECT 1`

    // Verifica variáveis de ambiente críticas
    const requiredEnvVars = [
      'NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY',
      'CLERK_SECRET_KEY',
      'DATABASE_URL',
    ]

    const missingEnvVars = requiredEnvVars.filter((varName) => !process.env[varName])

    if (missingEnvVars.length > 0) {
      return NextResponse.json(
        {
          status: 'unhealthy',
          message: 'Missing required environment variables',
          details: {
            missing: missingEnvVars,
          },
          timestamp: new Date().toISOString(),
          responseTime: Date.now() - startTime,
        },
        { status: 503 }
      )
    }

    return NextResponse.json({
      status: 'healthy',
      message: 'All systems operational',
      version: process.env.npm_package_version || '1.0.0',
      environment: process.env.NODE_ENV,
      timestamp: new Date().toISOString(),
      responseTime: Date.now() - startTime,
      checks: {
        database: 'connected',
        auth: 'configured',
      },
    })
  } catch (error) {
    console.error('Health check failed:', error)

    return NextResponse.json(
      {
        status: 'unhealthy',
        message: 'Health check failed',
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString(),
        responseTime: Date.now() - startTime,
      },
      { status: 503 }
    )
  }
}
