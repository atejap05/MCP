import { forwardRef, TextareaHTMLAttributes } from 'react'
import { cn } from '@/lib/utils'

export interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  error?: string
}

const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, error, ...props }, ref) => {
    return (
      <div className="w-full">
        <textarea
          className={cn(
            'flex min-h-[80px] w-full rounded-md border bg-white px-3 py-2 text-sm',
            'placeholder:text-gray-400',
            'focus:outline-none focus:ring-2 focus:ring-offset-2',
            'disabled:cursor-not-allowed disabled:opacity-50',
            error
              ? 'border-red-300 focus:ring-red-600'
              : 'border-gray-300 focus:ring-blue-600',
            className
          )}
          ref={ref}
          {...props}
        />
        {error && <p className="mt-1 text-xs text-red-600">{error}</p>}
      </div>
    )
  }
)
Textarea.displayName = 'Textarea'

export { Textarea }
