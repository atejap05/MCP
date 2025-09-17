'use client'

import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Textarea } from '@/components/ui/Textarea'
import type { CreateBookmarkData } from '@/types/bookmark'

// Schema de validação
const bookmarkSchema = z.object({
  url: z.string().url('URL inválida'),
  title: z.string().min(1, 'Título é obrigatório').max(200),
  notes: z.string().max(1000).optional(),
  tags: z.string().optional(),
})

type BookmarkFormData = z.infer<typeof bookmarkSchema>

interface BookmarkFormProps {
  onSubmit: (data: CreateBookmarkData) => Promise<void>
  onCancel?: () => void
  isSubmitting?: boolean
  initialData?: Partial<BookmarkFormData>
}

export function BookmarkForm({
  onSubmit,
  onCancel,
  isSubmitting = false,
  initialData,
}: BookmarkFormProps) {
  const [isLoadingMetadata, setIsLoadingMetadata] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    watch,
    reset,
  } = useForm<BookmarkFormData>({
    resolver: zodResolver(bookmarkSchema),
    defaultValues: {
      url: initialData?.url || '',
      title: initialData?.title || '',
      notes: initialData?.notes || '',
      tags: initialData?.tags || '',
    },
  })

  const watchUrl = watch('url')

  // Auto-preencher título quando URL muda
  useEffect(() => {
    const fetchMetadata = async () => {
      if (!watchUrl || !isValidUrl(watchUrl)) return

      setIsLoadingMetadata(true)
      try {
        const response = await fetch(`/api/metadata?url=${encodeURIComponent(watchUrl)}`)
        if (response.ok) {
          const metadata = await response.json()
          if (metadata.title && !watch('title')) {
            setValue('title', metadata.title)
          }
        }
      } catch (error) {
        console.error('Failed to fetch metadata:', error)
      } finally {
        setIsLoadingMetadata(false)
      }
    }

    const timeoutId = setTimeout(fetchMetadata, 500)
    return () => clearTimeout(timeoutId)
  }, [watchUrl, setValue, watch])

  const onFormSubmit = async (data: BookmarkFormData) => {
    const bookmarkData: CreateBookmarkData = {
      ...data,
      tags: data.tags ? data.tags.split(',').map(tag => tag.trim()).filter(Boolean) : [],
    }
    await onSubmit(bookmarkData)
    reset()
  }

  return (
    <form onSubmit={handleSubmit(onFormSubmit)} className="space-y-6">
      {/* URL Field */}
      <div>
        <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-1">
          URL *
        </label>
        <Input
          id="url"
          type="url"
          placeholder="https://exemplo.com"
          {...register('url')}
          error={errors.url?.message}
          disabled={isSubmitting}
          autoFocus
        />
      </div>

      {/* Title Field */}
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
          Título *
        </label>
        <div className="relative">
          <Input
            id="title"
            type="text"
            placeholder="Título do bookmark"
            {...register('title')}
            error={errors.title?.message}
            disabled={isSubmitting || isLoadingMetadata}
          />
          {isLoadingMetadata && (
            <div className="absolute right-2 top-1/2 -translate-y-1/2">
              <svg className="h-4 w-4 animate-spin text-gray-400" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
            </div>
          )}
        </div>
      </div>

      {/* Notes Field */}
      <div>
        <label htmlFor="notes" className="block text-sm font-medium text-gray-700 mb-1">
          Notas
        </label>
        <Textarea
          id="notes"
          placeholder="Adicione notas ou descrição..."
          rows={3}
          {...register('notes')}
          error={errors.notes?.message}
          disabled={isSubmitting}
        />
      </div>

      {/* Tags Field */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Tags
        </label>
        <Input
          placeholder="tag1, tag2, tag3"
          {...register('tags')}
          disabled={isSubmitting}
        />
        <p className="mt-1 text-xs text-gray-500">Separe as tags por vírgula</p>
      </div>

      {/* Actions */}
      <div className="flex gap-3 pt-4">
        <Button
          type="submit"
          disabled={isSubmitting || isLoadingMetadata}
          loading={isSubmitting}
          className="flex-1"
        >
          {isSubmitting ? 'Salvando...' : 'Salvar Bookmark'}
        </Button>

        {onCancel && (
          <Button
            type="button"
            variant="outline"
            onClick={onCancel}
            disabled={isSubmitting}
          >
            Cancelar
          </Button>
        )}
      </div>
    </form>
  )
}

// Função auxiliar
function isValidUrl(string: string) {
  try {
    new URL(string)
    return true
  } catch {
    return false
  }
}
