'use client'

import { BookmarkCard } from './BookmarkCard'
import { BookmarkIcon } from '@heroicons/react/24/outline'
import type { Bookmark } from '@/types/bookmark'

interface BookmarkListProps {
  bookmarks: Bookmark[]
  loading?: boolean
  onDelete: (id: string) => void
  onUpdate?: (id: string, data: Partial<Bookmark>) => Promise<void>
  emptyMessage?: string
}

export function BookmarkList({
  bookmarks,
  loading = false,
  onDelete,
  onUpdate,
  emptyMessage = 'Nenhum bookmark encontrado',
}: BookmarkListProps) {
  // Loading State
  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent motion-reduce:animate-[spin_1.5s_linear_infinite]">
            <span className="sr-only">Loading...</span>
          </div>
          <p className="mt-4 text-gray-600">Carregando bookmarks...</p>
        </div>
      </div>
    )
  }

  // Empty State
  if (bookmarks.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 px-4">
        <BookmarkIcon className="w-12 h-12 text-gray-400 mb-4" />
        <p className="text-lg text-gray-600 text-center">{emptyMessage}</p>
      </div>
    )
  }

  // Lista de Bookmarks
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {bookmarks.map(bookmark => (
        <BookmarkCard
          key={bookmark.id}
          bookmark={bookmark}
          onDelete={onDelete}
          onUpdate={onUpdate}
        />
      ))}
    </div>
  )
}
