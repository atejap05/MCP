'use client'

import { useState } from 'react'
import Image from 'next/image'
import { formatDistanceToNow } from 'date-fns'
import { ptBR } from 'date-fns/locale'
import { TrashIcon, PencilIcon, LinkIcon, ClockIcon, TagIcon } from '@heroicons/react/24/outline'
import { Button } from '@/components/ui/Button'
import type { Bookmark } from '@/types/bookmark'

interface BookmarkCardProps {
  bookmark: Bookmark
  onDelete: (id: string) => void
  onUpdate?: (id: string, data: Partial<Bookmark>) => Promise<void>
}

export function BookmarkCard({ bookmark, onDelete, onUpdate }: BookmarkCardProps) {
  const [imageError, setImageError] = useState(false)

  const domain = new URL(bookmark.url).hostname.replace('www.', '')
  const faviconUrl = `https://www.google.com/s2/favicons?domain=${domain}&sz=64`

  return (
    <article className="bookmark-card group">
      {/* Favicon e Info */}
      <div className="flex items-start gap-4">
        <div className="flex-shrink-0">
          {!imageError ? (
            <Image
              src={faviconUrl}
              alt={`${domain} favicon`}
              width={48}
              height={48}
              className="rounded-lg"
              onError={() => setImageError(true)}
              unoptimized
            />
          ) : (
            <div className="w-12 h-12 bg-gray-200 rounded-lg flex items-center justify-center">
              <LinkIcon className="w-6 h-6 text-gray-400" />
            </div>
          )}
        </div>

        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-semibold text-gray-900 truncate">{bookmark.title}</h3>

          <a
            href={bookmark.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-blue-600 hover:text-blue-800 hover:underline truncate block"
          >
            {bookmark.url}
          </a>

          {/* Metadados */}
          <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
            <span className="flex items-center gap-1">
              <LinkIcon className="w-3 h-3" />
              {domain}
            </span>
            <span className="flex items-center gap-1">
              <ClockIcon className="w-3 h-3" />
              {formatDistanceToNow(new Date(bookmark.createdAt), {
                addSuffix: true,
                locale: ptBR,
              })}
            </span>
          </div>
        </div>

        {/* Ações */}
        <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
          {onUpdate && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => {
                // TODO: Implementar edição inline ou modal
                console.warn('Edit bookmark:', bookmark.id)
              }}
              title="Editar bookmark"
            >
              <PencilIcon className="w-4 h-4" />
            </Button>
          )}

          <Button
            variant="ghost"
            size="sm"
            onClick={() => onDelete(bookmark.id)}
            title="Excluir bookmark"
            className="text-red-600 hover:text-red-700 hover:bg-red-50"
          >
            <TrashIcon className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Notas */}
      {bookmark.notes && (
        <p className="mt-3 text-sm text-gray-600 line-clamp-2">{bookmark.notes}</p>
      )}

      {/* Tags */}
      {bookmark.tags && bookmark.tags.length > 0 && (
        <div className="mt-3 flex items-center gap-2">
          <TagIcon className="w-4 h-4 text-gray-400" />
          <div className="flex flex-wrap gap-1">
            {bookmark.tags.map((tag) => (
              <span
                key={tag}
                className="inline-flex items-center px-2 py-1 text-xs font-medium text-blue-700 bg-blue-100 rounded-full"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      )}
    </article>
  )
}
