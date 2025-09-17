export interface Bookmark {
  id: string
  url: string
  title: string
  notes?: string
  tags?: string[]
  favicon?: string
  userId: string
  createdAt: string
  updatedAt: string
}

export interface CreateBookmarkData {
  url: string
  title: string
  notes?: string
  tags?: string[]
}

export interface UpdateBookmarkData {
  url?: string
  title?: string
  notes?: string
  tags?: string[]
}

export interface BookmarkFilters {
  search?: string
  tags?: string[]
  startDate?: Date
  endDate?: Date
}

export interface BookmarkPagination {
  page: number
  limit: number
  total: number
  totalPages: number
  hasNext: boolean
  hasPrev: boolean
}

export interface BookmarkListResponse {
  success: boolean
  data: Bookmark[]
  pagination: BookmarkPagination
  meta: {
    timestamp: string
    version: string
  }
}

export interface BookmarkResponse {
  success: boolean
  data: Bookmark
  message?: string
}

export interface ErrorResponse {
  error: string
  message: string
  code: string
  details?: unknown
}
