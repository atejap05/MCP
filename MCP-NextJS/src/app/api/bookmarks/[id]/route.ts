import { NextRequest, NextResponse } from 'next/server'
import { auth } from '@clerk/nextjs/server'
import { z } from 'zod'
import { getBookmarkById, updateBookmark, deleteBookmark } from '@/lib/bookmark-utils'

// Schema para validar ID
const idSchema = z.string().uuid('Invalid bookmark ID format')

// Schema para atualização
const updateBookmarkSchema = z
  .object({
    url: z.string().url().optional(),
    title: z.string().min(1).max(200).optional(),
    notes: z.string().max(1000).optional(),
    tags: z.array(z.string()).max(10).optional(),
  })
  .refine((data) => Object.keys(data).length > 0, {
    message: 'At least one field must be provided for update',
  })

/**
 * GET /api/bookmarks/[id]
 * Obtém detalhes de um bookmark específico
 */
export async function GET(_request: NextRequest, { params }: { params: { id: string } }) {
  try {
    // 1. Verificar autenticação
    const { userId } = await auth()
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // 2. Validar ID
    const idResult = idSchema.safeParse(params.id)
    if (!idResult.success) {
      return NextResponse.json(
        {
          error: 'Bad Request',
          message: 'Invalid bookmark ID',
          code: 'INVALID_ID',
        },
        { status: 400 }
      )
    }

    // 3. Buscar bookmark
    const bookmark = await getBookmarkById(idResult.data, userId)

    if (!bookmark) {
      return NextResponse.json(
        {
          error: 'Not Found',
          message: 'Bookmark not found',
          code: 'NOT_FOUND',
        },
        { status: 404 }
      )
    }

    // 4. Retornar bookmark
    return NextResponse.json({
      success: true,
      data: bookmark,
    })
  } catch (error) {
    console.error('[GET /api/bookmarks/[id]] Error:', error)
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
  }
}

/**
 * PUT /api/bookmarks/[id]
 * Atualiza um bookmark
 */
export async function PUT(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    // 1. Verificar autenticação
    const { userId } = await auth()
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // 2. Validar ID
    const idResult = idSchema.safeParse(params.id)
    if (!idResult.success) {
      return NextResponse.json({ error: 'Invalid bookmark ID' }, { status: 400 })
    }

    // 3. Parse e validar body
    const body = await request.json()
    const dataResult = updateBookmarkSchema.safeParse(body)

    if (!dataResult.success) {
      return NextResponse.json(
        {
          error: 'Bad Request',
          message: 'Invalid update data',
          details: dataResult.error.flatten(),
        },
        { status: 400 }
      )
    }

    // 4. Atualizar bookmark
    const updated = await updateBookmark(idResult.data, userId, dataResult.data)

    if (!updated) {
      return NextResponse.json({ error: 'Bookmark not found or access denied' }, { status: 404 })
    }

    // 5. Retornar bookmark atualizado
    return NextResponse.json({
      success: true,
      data: updated,
      message: 'Bookmark updated successfully',
    })
  } catch (error) {
    console.error('[PUT /api/bookmarks/[id]] Error:', error)
    return NextResponse.json({ error: 'Failed to update bookmark' }, { status: 500 })
  }
}

/**
 * DELETE /api/bookmarks/[id]
 * Deleta um bookmark
 */
export async function DELETE(_request: NextRequest, { params }: { params: { id: string } }) {
  try {
    // 1. Verificar autenticação
    const { userId } = await auth()
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // 2. Validar ID
    const idResult = idSchema.safeParse(params.id)
    if (!idResult.success) {
      return NextResponse.json({ error: 'Invalid bookmark ID' }, { status: 400 })
    }

    // 3. Deletar bookmark
    const deleted = await deleteBookmark(idResult.data, userId)

    if (!deleted) {
      return NextResponse.json({ error: 'Bookmark not found or access denied' }, { status: 404 })
    }

    // 4. Retornar sucesso
    return NextResponse.json({
      success: true,
      message: 'Bookmark deleted successfully',
    })
  } catch (error) {
    console.error('[DELETE /api/bookmarks/[id]] Error:', error)
    return NextResponse.json({ error: 'Failed to delete bookmark' }, { status: 500 })
  }
}
