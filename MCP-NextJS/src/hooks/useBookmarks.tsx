'use client'

import { useEffect, useState, useCallback } from 'react'
import { useAuth } from '@clerk/nextjs'
import type { Bookmark, CreateBookmarkData } from '@/types/bookmark'

interface UseBookmarksReturn {
  bookmarks: Bookmark[]
  loading: boolean
  error: string | null
  addBookmark: (data: CreateBookmarkData) => Promise<void>
  updateBookmark: (id: string, data: Partial<Bookmark>) => Promise<void>
  deleteBookmark: (id: string) => Promise<void>
  refetch: () => Promise<void>
}

export function useBookmarks(): UseBookmarksReturn {
  const { getToken, isLoaded, isSignedIn } = useAuth()
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Debug logs
  console.log('useBookmarks - isLoaded:', isLoaded, 'isSignedIn:', isSignedIn)

  // Função para fazer requisições autenticadas
  const fetchWithAuth = useCallback(
    async (url: string, options?: RequestInit) => {
      const token = await getToken()
      console.log('Auth token:', token ? 'Present' : 'Missing')
      
      return fetch(url, {
        ...options,
        headers: {
          ...options?.headers,
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })
    },
    [getToken]
  )

  // Buscar bookmarks
  const fetchBookmarks = useCallback(async () => {
    try {
      setError(null)
      const response = await fetchWithAuth('/api/bookmarks')

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        console.error('API Error:', {
          status: response.status,
          statusText: response.statusText,
          error: errorData
        })
        throw new Error(`Falha ao buscar bookmarks: ${response.status} ${response.statusText}`)
      }

      const data = await response.json()
      setBookmarks(data.data || [])
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Erro desconhecido ao buscar bookmarks'
      setError(errorMessage)
      console.error('Error fetching bookmarks:', error)
    } finally {
      setLoading(false)
    }
  }, [fetchWithAuth])

  // Adicionar bookmark
  const addBookmark = useCallback(
    async (data: CreateBookmarkData) => {
      try {
        const response = await fetchWithAuth('/api/bookmarks', {
          method: 'POST',
          body: JSON.stringify(data),
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.message || 'Falha ao criar bookmark')
        }

        const result = await response.json()
        setBookmarks(prev => [result.data, ...prev])
      } catch (error) {
        console.error('Error creating bookmark:', error)
        throw error
      }
    },
    [fetchWithAuth]
  )

  // Atualizar bookmark
  const updateBookmark = useCallback(
    async (id: string, data: Partial<Bookmark>) => {
      try {
        const response = await fetchWithAuth(`/api/bookmarks/${id}`, {
          method: 'PUT',
          body: JSON.stringify(data),
        })

        if (!response.ok) {
          throw new Error('Falha ao atualizar bookmark')
        }

        const result = await response.json()
        setBookmarks(prev => prev.map(b => (b.id === id ? result.data : b)))
      } catch (error) {
        console.error('Error updating bookmark:', error)
        throw error
      }
    },
    [fetchWithAuth]
  )

  // Deletar bookmark
  const deleteBookmark = useCallback(
    async (id: string) => {
      try {
        const response = await fetchWithAuth(`/api/bookmarks/${id}`, {
          method: 'DELETE',
        })

        if (!response.ok) {
          throw new Error('Falha ao deletar bookmark')
        }

        setBookmarks(prev => prev.filter(b => b.id !== id))
      } catch (error) {
        console.error('Error deleting bookmark:', error)
        throw error
      }
    },
    [fetchWithAuth]
  )

  // Carregar bookmarks ao montar
  useEffect(() => {
    if (isLoaded && isSignedIn) {
      fetchBookmarks()
    } else if (isLoaded && !isSignedIn) {
      setLoading(false)
      setBookmarks([])
    }
  }, [fetchBookmarks, isLoaded, isSignedIn])

  return {
    bookmarks,
    loading,
    error,
    addBookmark,
    updateBookmark,
    deleteBookmark,
    refetch: fetchBookmarks,
  }
}
