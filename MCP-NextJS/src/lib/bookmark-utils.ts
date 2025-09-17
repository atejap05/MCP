import { prisma } from '@/lib/prisma'
import type { Bookmark, Prisma } from '@prisma/client'
import type { CreateBookmarkData, UpdateBookmarkData } from '@/types/bookmark'

export interface BookmarkServiceOptions {
  pagination?: { page: number; limit: number }
  search?: string
  orderBy?: Record<string, 'asc' | 'desc'>
}

export class BookmarkService {
  /**
   * Busca bookmarks com filtros avançados
   */
  static async findBookmarks(userId: string, options: BookmarkServiceOptions = {}) {
    const { pagination = { page: 1, limit: 20 }, search, orderBy = { createdAt: 'desc' } } = options

    const where: Prisma.BookmarkWhereInput = {
      userId,
    }

    // Adiciona filtro de busca
    if (search) {
      where.OR = [
        { title: { contains: search } },
        { notes: { contains: search } },
        { url: { contains: search } },
      ]
    }

    // Executa queries em paralelo
    const [bookmarks, total] = await Promise.all([
      prisma.bookmark.findMany({
        where,
        skip: (pagination.page - 1) * pagination.limit,
        take: pagination.limit,
        orderBy,
      }),
      prisma.bookmark.count({ where }),
    ])

    return {
      items: bookmarks,
      total,
      pagination: {
        page: pagination.page,
        limit: pagination.limit,
        total,
        totalPages: Math.ceil(total / pagination.limit),
        hasNext: pagination.page < Math.ceil(total / pagination.limit),
        hasPrev: pagination.page > 1,
      },
    }
  }

  /**
   * Busca um bookmark por ID
   */
  static async getBookmarkById(id: string, userId: string): Promise<Bookmark | null> {
    return await prisma.bookmark.findFirst({
      where: {
        id,
        userId,
      },
    })
  }

  /**
   * Cria um novo bookmark
   */
  static async createBookmark(userId: string, data: CreateBookmarkData): Promise<Bookmark> {
    return await prisma.bookmark.create({
      data: {
        ...data,
        userId,
        tags: data.tags?.join(','),
      },
    })
  }

  /**
   * Atualiza um bookmark
   */
  static async updateBookmark(
    id: string,
    userId: string,
    data: UpdateBookmarkData
  ): Promise<Bookmark | null> {
    // Verifica se o bookmark pertence ao usuário
    const bookmark = await prisma.bookmark.findFirst({
      where: {
        id,
        userId,
      },
    })

    if (!bookmark) {
      return null
    }

    return await prisma.bookmark.update({
      where: { id },
      data: {
        ...data,
        tags: data.tags?.join(','),
      },
    })
  }

  /**
   * Deleta um bookmark
   */
  static async deleteBookmark(id: string, userId: string): Promise<boolean> {
    const result = await prisma.bookmark.deleteMany({
      where: {
        id,
        userId,
      },
    })

    return result.count > 0
  }

  /**
   * Verifica se URL já existe
   */
  static async isURLBookmarked(userId: string, url: string): Promise<boolean> {
    const normalized = this.normalizeURL(url)
    const exists = await prisma.bookmark.findFirst({
      where: {
        userId,
        url: normalized,
      },
      select: { id: true },
    })
    return !!exists
  }

  /**
   * Busca bookmark existente por URL
   */
  static async findExistingBookmark(userId: string, url: string): Promise<Bookmark | null> {
    const normalized = this.normalizeURL(url)
    return await prisma.bookmark.findFirst({
      where: {
        userId,
        url: normalized,
      },
    })
  }

  /**
   * Normaliza URLs para comparação
   */
  static normalizeURL(url: string): string {
    try {
      const urlObj = new URL(url)
      // Remove trailing slash
      return urlObj.href.replace(/\/$/, '')
    } catch {
      return url
    }
  }

  /**
   * Extrai domínio da URL
   */
  static getDomain(url: string): string {
    try {
      const urlObj = new URL(url)
      return urlObj.hostname.replace('www.', '')
    } catch {
      return 'invalid-url'
    }
  }
}

// Funções de conveniência para compatibilidade
export const getUserBookmarks = BookmarkService.findBookmarks
export const getBookmarkById = BookmarkService.getBookmarkById
export const createUserBookmark = BookmarkService.createBookmark
export const updateBookmark = BookmarkService.updateBookmark
export const deleteBookmark = BookmarkService.deleteBookmark
export const checkDuplicateURL = BookmarkService.isURLBookmarked
