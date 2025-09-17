import { NextRequest, NextResponse } from 'next/server'
import { auth } from '@clerk/nextjs/server'
import { z } from 'zod'
import { getUserBookmarks, createUserBookmark, BookmarkService } from '@/lib/bookmark-utils'
import { extractURLMetadata } from '@/lib/metadata-extractor'

// Schema de validação para query params
const listBookmarksSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  search: z.string().optional(),
  sort: z.enum(['createdAt', 'updatedAt', 'title']).default('createdAt'),
  order: z.enum(['asc', 'desc']).default('desc'),
})

// Schema de validação para criar bookmark
const createBookmarkSchema = z.object({
  url: z.string().url('Invalid URL format'),
  title: z.string().min(1, 'Title is required').max(200),
  notes: z.string().max(1000).optional(),
  tags: z.array(z.string()).max(10).optional(),
})

/**
 * GET /api/bookmarks
 * Lista todos os bookmarks do usuário autenticado
 */
export async function GET(request: NextRequest) {
  try {
    // 1. Verificar autenticação
    const { userId } = await auth()
    if (!userId) {
      return NextResponse.json(
        {
          error: 'Unauthorized',
          message: 'Please sign in to access your bookmarks',
          code: 'AUTH_REQUIRED',
        },
        { status: 401 }
      )
    }

    // 2. Validar query params
    const searchParams = Object.fromEntries(request.nextUrl.searchParams.entries())
    const validationResult = listBookmarksSchema.safeParse(searchParams)

    if (!validationResult.success) {
      return NextResponse.json(
        {
          error: 'Bad Request',
          message: 'Invalid query parameters',
          code: 'INVALID_PARAMS',
          details: validationResult.error.flatten(),
        },
        { status: 400 }
      )
    }

    const { page, limit, search, sort, order } = validationResult.data

    // 3. Buscar bookmarks
    const bookmarks = await getUserBookmarks(userId, {
      pagination: { page, limit },
      search,
      orderBy: { [sort]: order },
    })

    // 4. Retornar resposta padronizada
    return NextResponse.json({
      success: true,
      data: bookmarks.items,
      pagination: {
        page,
        limit,
        total: bookmarks.total,
        totalPages: Math.ceil(bookmarks.total / limit),
        hasNext: page < Math.ceil(bookmarks.total / limit),
        hasPrev: page > 1,
      },
      meta: {
        timestamp: new Date().toISOString(),
        version: '1.0.0',
      },
    })
  } catch (error) {
    console.error('[GET /api/bookmarks] Error:', error)

    return NextResponse.json(
      {
        error: 'Internal Server Error',
        message: 'Failed to fetch bookmarks',
        code: 'INTERNAL_ERROR',
      },
      { status: 500 }
    )
  }
}

/**
 * POST /api/bookmarks
 * Cria um novo bookmark
 */
export async function POST(request: NextRequest) {
  try {
    // 1. Verificar autenticação
    const { userId } = await auth()
    if (!userId) {
      return NextResponse.json(
        {
          error: 'Unauthorized',
          message: 'Please sign in to create bookmarks',
          code: 'AUTH_REQUIRED',
        },
        { status: 401 }
      )
    }

    // 2. Parse do body
    let body: unknown
    try {
      body = await request.json()
    } catch {
      return NextResponse.json(
        {
          error: 'Bad Request',
          message: 'Invalid JSON body',
          code: 'INVALID_JSON',
        },
        { status: 400 }
      )
    }

    // 3. Validar dados
    const validationResult = createBookmarkSchema.safeParse(body)
    if (!validationResult.success) {
      return NextResponse.json(
        {
          error: 'Bad Request',
          message: 'Invalid bookmark data',
          code: 'VALIDATION_ERROR',
          details: validationResult.error.flatten(),
        },
        { status: 400 }
      )
    }

    const bookmarkData = validationResult.data

    // 4. Verificar se URL já existe
    const existingBookmark = await BookmarkService.findExistingBookmark(userId, bookmarkData.url)
    if (existingBookmark) {
      return NextResponse.json(
        {
          error: 'Conflict',
          message: 'This URL is already bookmarked',
          code: 'DUPLICATE_URL',
          existingId: existingBookmark.id,
        },
        { status: 409 }
      )
    }

    // 5. Extrair metadados da URL (opcional)
    const metadata = await extractURLMetadata(bookmarkData.url)

    // 6. Criar bookmark
    const bookmark = await createUserBookmark(userId, {
      ...bookmarkData,
      // Se não tiver título, usar o da página
      title: bookmarkData.title || metadata?.title || 'Untitled',
    })

    // 7. Retornar bookmark criado
    return NextResponse.json(
      {
        success: true,
        data: bookmark,
        message: 'Bookmark created successfully',
      },
      { status: 201 }
    )
  } catch (error) {
    console.error('[POST /api/bookmarks] Error:', error)

    return NextResponse.json(
      {
        error: 'Internal Server Error',
        message: 'Failed to create bookmark',
        code: 'INTERNAL_ERROR',
      },
      { status: 500 }
    )
  }
}
