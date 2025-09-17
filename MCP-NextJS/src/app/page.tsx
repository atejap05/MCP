'use client'

import { useState, useCallback } from 'react'
import { SignedIn, SignedOut } from '@clerk/nextjs'
import { useBookmarks } from '@/hooks/useBookmarks'
import { BookmarkForm } from '@/components/BookmarkForm'
import { BookmarkList } from '@/components/BookmarkList'
import { Button } from '@/components/ui/Button'
import { BookmarkIcon, PlusIcon } from '@heroicons/react/24/outline'
import type { CreateBookmarkData } from '@/types/bookmark'

export default function HomePage() {
  const { bookmarks, loading, error, addBookmark, deleteBookmark, updateBookmark, refetch } =
    useBookmarks()

  const [showAddForm, setShowAddForm] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Debug logs
  console.log('HomePage - bookmarks:', bookmarks.length, 'loading:', loading, 'error:', error)

  // Handler para adicionar bookmark
  const handleAddBookmark = useCallback(
    async (data: CreateBookmarkData) => {
      setIsSubmitting(true)
      try {
        await addBookmark(data)
        setShowAddForm(false)
      } catch (error) {
        console.error('Error adding bookmark:', error)
      } finally {
        setIsSubmitting(false)
      }
    },
    [addBookmark]
  )

  // Handler para deletar com confirmação
  const handleDeleteBookmark = useCallback(
    async (id: string) => {
      if (!confirm('Tem certeza que deseja excluir este bookmark?')) {
        return
      }

      try {
        await deleteBookmark(id)
      } catch (error) {
        console.error('Error deleting bookmark:', error)
      }
    },
    [deleteBookmark]
  )

  return (
    <>
      <SignedOut>
        <div className="flex flex-col items-center justify-center min-h-[60vh] px-4">
          <BookmarkIcon className="w-16 h-16 text-gray-400 mb-4" />
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Bem-vindo ao Bookmark Manager</h1>
          <p className="text-lg text-gray-600 text-center max-w-md">
            Faça login para começar a salvar e organizar seus links favoritos
          </p>
        </div>
      </SignedOut>

      <SignedIn>
        <div className="container mx-auto px-4 py-8 max-w-7xl">
          {/* Header Section */}
          <div className="mb-8">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Meus Bookmarks</h1>
                <p className="mt-1 text-gray-600">
                  {bookmarks.length}{' '}
                  {bookmarks.length === 1 ? 'bookmark salvo' : 'bookmarks salvos'}
                </p>
              </div>

              <Button
                onClick={() => setShowAddForm(true)}
                size="lg"
                className="flex items-center gap-2"
              >
                <PlusIcon className="w-5 h-5" />
                Adicionar Bookmark
              </Button>
            </div>
          </div>

          {/* Error State */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800">{error}</p>
              <Button variant="outline" size="sm" onClick={refetch} className="mt-2">
                Tentar Novamente
              </Button>
            </div>
          )}

          {/* Bookmarks List */}
          <BookmarkList
            bookmarks={bookmarks}
            loading={loading}
            onDelete={handleDeleteBookmark}
            onUpdate={updateBookmark}
            emptyMessage="Você ainda não tem bookmarks salvos"
          />
        </div>

        {/* Add Bookmark Form */}
        {showAddForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md">
              <h2 className="text-xl font-semibold mb-4">Adicionar Novo Bookmark</h2>
              <BookmarkForm
                onSubmit={handleAddBookmark}
                onCancel={() => setShowAddForm(false)}
                isSubmitting={isSubmitting}
              />
            </div>
          </div>
        )}
      </SignedIn>
    </>
  )
}
