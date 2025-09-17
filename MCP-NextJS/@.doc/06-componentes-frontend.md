# Componentes Frontend React/Next.js

## 🎨 Visão Geral dos Componentes

Nossa aplicação utiliza componentes React modernos com:

- ✅ TypeScript para type-safety
- ✅ React Hooks para estado e efeitos
- ✅ Server e Client Components do Next.js 15
- ✅ Componentes do Clerk para autenticação
- ✅ CSS Modules e estilos globais
- ✅ Componentes reutilizáveis e compostos

## 📁 Estrutura de Componentes

```
src/
├── app/                      # Pages e layouts
│   ├── layout.tsx           # Layout raiz
│   └── page.tsx             # Página inicial
├── components/              # Componentes reutilizáveis
│   ├── BookmarkForm.tsx     # Formulário de criação
│   ├── BookmarkCard.tsx     # Card individual
│   ├── BookmarkList.tsx     # Lista de bookmarks
│   ├── Header.tsx           # Cabeçalho da aplicação
│   ├── SearchBar.tsx        # Barra de pesquisa
│   └── ui/                  # Componentes UI genéricos
│       ├── Button.tsx
│       ├── Input.tsx
│       ├── Modal.tsx
│       └── Spinner.tsx
└── hooks/                   # Custom hooks
    ├── useBookmarks.tsx     # Hook principal
    ├── useDebounce.tsx      # Debounce para inputs
    └── useAuth.tsx          # Hook de autenticação
```

## 🏗️ Layout Principal

### Layout Raiz com ClerkProvider

`src/app/layout.tsx`:

```typescript
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { ClerkProvider } from "@clerk/nextjs";
import { ptBR } from "@clerk/localizations";
import { Header } from "@/components/Header";
import { Toaster } from "@/components/ui/Toaster";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: {
    default: "Bookmark Manager",
    template: "%s | Bookmark Manager",
  },
  description: "Gerencie seus bookmarks favoritos com integração MCP",
  keywords: ["bookmarks", "favoritos", "links", "MCP", "AI"],
  authors: [{ name: "Seu Nome" }],
  creator: "Bookmark Manager Team",
  openGraph: {
    type: "website",
    locale: "pt_BR",
    url: "https://bookmarks.example.com",
    title: "Bookmark Manager",
    description: "Gerencie seus bookmarks favoritos",
    siteName: "Bookmark Manager",
  },
};

interface RootLayoutProps {
  children: React.ReactNode;
  modal: React.ReactNode; // Para rotas paralelas
}

export default function RootLayout({ children, modal }: RootLayoutProps) {
  return (
    <ClerkProvider
      localization={ptBR}
      appearance={{
        baseTheme: undefined, // ou 'dark' para tema escuro
        layout: {
          socialButtonsPlacement: "bottom",
          socialButtonsVariant: "iconButton",
        },
        variables: {
          colorPrimary: "#0070f3",
          colorBackground: "#ffffff",
          colorText: "#000000",
          colorTextSecondary: "#666666",
          colorDanger: "#ee0000",
          colorSuccess: "#10b981",
          colorWarning: "#f59e0b",
          borderRadius: "0.5rem",
          fontFamily: "var(--font-inter)",
        },
        elements: {
          formButtonPrimary: "bg-blue-600 hover:bg-blue-700 transition-colors",
          card: "shadow-lg border border-gray-200",
          headerTitle: "text-2xl font-bold",
          headerSubtitle: "text-gray-600",
        },
      }}
    >
      <html lang="pt-BR" className={inter.variable}>
        <body className={inter.className}>
          <div className="min-h-screen bg-gray-50">
            <Header />
            <main className="main-content">{children}</main>
            {modal}
            <Toaster />
          </div>
        </body>
      </html>
    </ClerkProvider>
  );
}
```

## 🎯 Página Principal

`src/app/page.tsx`:

```typescript
"use client";

import { useState, useCallback, useMemo } from "react";
import { SignedIn, SignedOut } from "@clerk/nextjs";
import { useBookmarks } from "@/hooks/useBookmarks";
import { BookmarkForm } from "@/components/BookmarkForm";
import { BookmarkList } from "@/components/BookmarkList";
import { SearchBar } from "@/components/SearchBar";
import { Button } from "@/components/ui/Button";
import { Modal } from "@/components/ui/Modal";
import { PlusIcon, BookmarkIcon } from "@heroicons/react/24/outline";
import type { CreateBookmarkData } from "@/types/bookmark";

export default function HomePage() {
  const {
    bookmarks,
    loading,
    error,
    addBookmark,
    deleteBookmark,
    updateBookmark,
    refetch,
  } = useBookmarks();

  const [showAddModal, setShowAddModal] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Filtrar bookmarks baseado na pesquisa
  const filteredBookmarks = useMemo(() => {
    if (!searchTerm.trim()) return bookmarks;

    const search = searchTerm.toLowerCase();
    return bookmarks.filter(
      bookmark =>
        bookmark.title.toLowerCase().includes(search) ||
        bookmark.notes?.toLowerCase().includes(search) ||
        bookmark.url.toLowerCase().includes(search)
    );
  }, [bookmarks, searchTerm]);

  // Handler para adicionar bookmark
  const handleAddBookmark = useCallback(
    async (data: CreateBookmarkData) => {
      setIsSubmitting(true);
      try {
        await addBookmark(data);
        setShowAddModal(false);
        // Mostrar notificação de sucesso
      } catch (error) {
        // Erro já é tratado no hook
      } finally {
        setIsSubmitting(false);
      }
    },
    [addBookmark]
  );

  // Handler para deletar com confirmação
  const handleDeleteBookmark = useCallback(
    async (id: string) => {
      if (!confirm("Tem certeza que deseja excluir este bookmark?")) {
        return;
      }

      try {
        await deleteBookmark(id);
        // Mostrar notificação de sucesso
      } catch (error) {
        // Erro já é tratado no hook
      }
    },
    [deleteBookmark]
  );

  return (
    <>
      <SignedOut>
        <div className="flex flex-col items-center justify-center min-h-[60vh] px-4">
          <BookmarkIcon className="w-16 h-16 text-gray-400 mb-4" />
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Bem-vindo ao Bookmark Manager
          </h1>
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
                <h1 className="text-3xl font-bold text-gray-900">
                  Meus Bookmarks
                </h1>
                <p className="mt-1 text-gray-600">
                  {bookmarks.length}{" "}
                  {bookmarks.length === 1
                    ? "bookmark salvo"
                    : "bookmarks salvos"}
                </p>
              </div>

              <Button
                onClick={() => setShowAddModal(true)}
                size="lg"
                className="flex items-center gap-2"
              >
                <PlusIcon className="w-5 h-5" />
                Adicionar Bookmark
              </Button>
            </div>
          </div>

          {/* Search Bar */}
          <div className="mb-6">
            <SearchBar
              value={searchTerm}
              onChange={setSearchTerm}
              placeholder="Pesquisar bookmarks..."
            />
          </div>

          {/* Error State */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800">{error}</p>
              <Button
                variant="outline"
                size="sm"
                onClick={refetch}
                className="mt-2"
              >
                Tentar Novamente
              </Button>
            </div>
          )}

          {/* Bookmarks List */}
          <BookmarkList
            bookmarks={filteredBookmarks}
            loading={loading}
            onDelete={handleDeleteBookmark}
            onUpdate={updateBookmark}
            emptyMessage={
              searchTerm
                ? "Nenhum bookmark encontrado para sua pesquisa"
                : "Você ainda não tem bookmarks salvos"
            }
          />
        </div>

        {/* Add Bookmark Modal */}
        <Modal
          isOpen={showAddModal}
          onClose={() => setShowAddModal(false)}
          title="Adicionar Novo Bookmark"
        >
          <BookmarkForm
            onSubmit={handleAddBookmark}
            onCancel={() => setShowAddModal(false)}
            isSubmitting={isSubmitting}
          />
        </Modal>
      </SignedIn>
    </>
  );
}
```

## 🧩 Componentes Principais

### Header Component

`src/components/Header.tsx`:

```typescript
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  SignInButton,
  SignUpButton,
  SignedIn,
  SignedOut,
  UserButton,
  useUser,
} from "@clerk/nextjs";
import { BookmarkIcon, Cog6ToothIcon } from "@heroicons/react/24/outline";
import { Button } from "@/components/ui/Button";

export function Header() {
  const pathname = usePathname();
  const { user } = useUser();

  const navigation = [
    { name: "Home", href: "/" },
    { name: "Categorias", href: "/categories" },
    { name: "Configurações", href: "/settings", icon: Cog6ToothIcon },
  ];

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <BookmarkIcon className="w-8 h-8 text-blue-600" />
            <span className="text-xl font-bold text-gray-900">
              Bookmark Manager
            </span>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center gap-6">
            <SignedIn>
              {navigation.map(item => {
                const isActive = pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={`
                      flex items-center gap-1 px-3 py-2 text-sm font-medium rounded-md
                      transition-colors duration-200
                      ${
                        isActive
                          ? "text-blue-600 bg-blue-50"
                          : "text-gray-700 hover:text-gray-900 hover:bg-gray-50"
                      }
                    `}
                  >
                    {item.icon && <item.icon className="w-4 h-4" />}
                    {item.name}
                  </Link>
                );
              })}
            </SignedIn>
          </nav>

          {/* Auth Section */}
          <div className="flex items-center gap-4">
            <SignedOut>
              <SignInButton mode="modal">
                <Button variant="ghost">Entrar</Button>
              </SignInButton>

              <SignUpButton mode="modal">
                <Button>Cadastrar</Button>
              </SignUpButton>
            </SignedOut>

            <SignedIn>
              <span className="hidden sm:block text-sm text-gray-600">
                Olá, {user?.firstName || "Usuário"}
              </span>

              <UserButton
                afterSignOutUrl="/"
                appearance={{
                  elements: {
                    avatarBox: "w-10 h-10 border-2 border-gray-200",
                  },
                }}
              />
            </SignedIn>
          </div>
        </div>
      </div>
    </header>
  );
}
```

### BookmarkForm Component

`src/components/BookmarkForm.tsx`:

```typescript
"use client";

import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Textarea } from "@/components/ui/Textarea";
import { TagInput } from "@/components/ui/TagInput";
import { extractURLMetadata } from "@/lib/metadata";
import type { CreateBookmarkData } from "@/types/bookmark";

// Schema de validação
const bookmarkSchema = z.object({
  url: z.string().url("URL inválida"),
  title: z.string().min(1, "Título é obrigatório").max(200),
  notes: z.string().max(1000).optional(),
  tags: z.array(z.string()).max(10).optional(),
});

type BookmarkFormData = z.infer<typeof bookmarkSchema>;

interface BookmarkFormProps {
  onSubmit: (data: CreateBookmarkData) => Promise<void>;
  onCancel?: () => void;
  isSubmitting?: boolean;
  initialData?: Partial<BookmarkFormData>;
}

export function BookmarkForm({
  onSubmit,
  onCancel,
  isSubmitting = false,
  initialData,
}: BookmarkFormProps) {
  const [isLoadingMetadata, setIsLoadingMetadata] = useState(false);

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
      url: initialData?.url || "",
      title: initialData?.title || "",
      notes: initialData?.notes || "",
      tags: initialData?.tags || [],
    },
  });

  const watchUrl = watch("url");

  // Auto-preencher título quando URL muda
  useEffect(() => {
    const fetchMetadata = async () => {
      if (!watchUrl || !isValidUrl(watchUrl)) return;

      setIsLoadingMetadata(true);
      try {
        const metadata = await extractURLMetadata(watchUrl);
        if (metadata?.title && !watch("title")) {
          setValue("title", metadata.title);
        }
      } catch (error) {
        console.error("Failed to fetch metadata:", error);
      } finally {
        setIsLoadingMetadata(false);
      }
    };

    const timeoutId = setTimeout(fetchMetadata, 500);
    return () => clearTimeout(timeoutId);
  }, [watchUrl, setValue, watch]);

  const onFormSubmit = async (data: BookmarkFormData) => {
    await onSubmit(data);
    reset();
  };

  return (
    <form onSubmit={handleSubmit(onFormSubmit)} className="space-y-6">
      {/* URL Field */}
      <div>
        <label
          htmlFor="url"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          URL *
        </label>
        <Input
          id="url"
          type="url"
          placeholder="https://exemplo.com"
          {...register("url")}
          error={errors.url?.message}
          disabled={isSubmitting}
          autoFocus
        />
      </div>

      {/* Title Field */}
      <div>
        <label
          htmlFor="title"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Título *
        </label>
        <div className="relative">
          <Input
            id="title"
            type="text"
            placeholder="Título do bookmark"
            {...register("title")}
            error={errors.title?.message}
            disabled={isSubmitting || isLoadingMetadata}
          />
          {isLoadingMetadata && (
            <div className="absolute right-2 top-1/2 -translate-y-1/2">
              <Spinner size="sm" />
            </div>
          )}
        </div>
      </div>

      {/* Notes Field */}
      <div>
        <label
          htmlFor="notes"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Notas
        </label>
        <Textarea
          id="notes"
          placeholder="Adicione notas ou descrição..."
          rows={3}
          {...register("notes")}
          error={errors.notes?.message}
          disabled={isSubmitting}
        />
      </div>

      {/* Tags Field */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Tags
        </label>
        <TagInput
          value={watch("tags") || []}
          onChange={tags => setValue("tags", tags)}
          placeholder="Adicione tags..."
          maxTags={10}
          disabled={isSubmitting}
        />
      </div>

      {/* Actions */}
      <div className="flex gap-3 pt-4">
        <Button
          type="submit"
          disabled={isSubmitting || isLoadingMetadata}
          loading={isSubmitting}
          className="flex-1"
        >
          {isSubmitting ? "Salvando..." : "Salvar Bookmark"}
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
  );
}

// Função auxiliar
function isValidUrl(string: string) {
  try {
    new URL(string);
    return true;
  } catch {
    return false;
  }
}
```

### BookmarkCard Component

`src/components/BookmarkCard.tsx`:

```typescript
"use client";

import { useState } from "react";
import Image from "next/image";
import { formatDistanceToNow } from "date-fns";
import { ptBR } from "date-fns/locale";
import {
  TrashIcon,
  PencilIcon,
  LinkIcon,
  ClockIcon,
  TagIcon,
} from "@heroicons/react/24/outline";
import { Button } from "@/components/ui/Button";
import { BookmarkForm } from "./BookmarkForm";
import { Modal } from "@/components/ui/Modal";
import type { Bookmark } from "@/types/bookmark";

interface BookmarkCardProps {
  bookmark: Bookmark;
  onDelete: (id: string) => void;
  onUpdate?: (id: string, data: Partial<Bookmark>) => Promise<void>;
}

export function BookmarkCard({
  bookmark,
  onDelete,
  onUpdate,
}: BookmarkCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [imageError, setImageError] = useState(false);

  const domain = new URL(bookmark.url).hostname.replace("www.", "");
  const faviconUrl = `https://www.google.com/s2/favicons?domain=${domain}&sz=64`;

  const handleUpdate = async (data: any) => {
    if (onUpdate) {
      await onUpdate(bookmark.id, data);
      setIsEditing(false);
    }
  };

  return (
    <>
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
              />
            ) : (
              <div className="w-12 h-12 bg-gray-200 rounded-lg flex items-center justify-center">
                <LinkIcon className="w-6 h-6 text-gray-400" />
              </div>
            )}
          </div>

          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-semibold text-gray-900 truncate">
              {bookmark.title}
            </h3>

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
                onClick={() => setIsEditing(true)}
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
          <p className="mt-3 text-sm text-gray-600 line-clamp-2">
            {bookmark.notes}
          </p>
        )}

        {/* Tags */}
        {bookmark.tags && bookmark.tags.length > 0 && (
          <div className="mt-3 flex items-center gap-2">
            <TagIcon className="w-4 h-4 text-gray-400" />
            <div className="flex flex-wrap gap-1">
              {bookmark.tags.map(tag => (
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

      {/* Modal de Edição */}
      {onUpdate && (
        <Modal
          isOpen={isEditing}
          onClose={() => setIsEditing(false)}
          title="Editar Bookmark"
        >
          <BookmarkForm
            onSubmit={handleUpdate}
            onCancel={() => setIsEditing(false)}
            initialData={bookmark}
          />
        </Modal>
      )}
    </>
  );
}
```

### BookmarkList Component

`src/components/BookmarkList.tsx`:

```typescript
"use client";

import { BookmarkCard } from "./BookmarkCard";
import { Spinner } from "@/components/ui/Spinner";
import { BookmarkIcon } from "@heroicons/react/24/outline";
import type { Bookmark } from "@/types/bookmark";

interface BookmarkListProps {
  bookmarks: Bookmark[];
  loading?: boolean;
  onDelete: (id: string) => void;
  onUpdate?: (id: string, data: Partial<Bookmark>) => Promise<void>;
  emptyMessage?: string;
}

export function BookmarkList({
  bookmarks,
  loading = false,
  onDelete,
  onUpdate,
  emptyMessage = "Nenhum bookmark encontrado",
}: BookmarkListProps) {
  // Loading State
  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <Spinner size="lg" className="mx-auto mb-4" />
          <p className="text-gray-600">Carregando bookmarks...</p>
        </div>
      </div>
    );
  }

  // Empty State
  if (bookmarks.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 px-4">
        <BookmarkIcon className="w-12 h-12 text-gray-400 mb-4" />
        <p className="text-lg text-gray-600 text-center">{emptyMessage}</p>
      </div>
    );
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
  );
}
```

## 🎨 Componentes UI Reutilizáveis

### Button Component

`src/components/ui/Button.tsx`:

```typescript
import { forwardRef, ButtonHTMLAttributes } from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
import { Spinner } from "./Spinner";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default:
          "bg-blue-600 text-white hover:bg-blue-700 focus-visible:ring-blue-600",
        destructive:
          "bg-red-600 text-white hover:bg-red-700 focus-visible:ring-red-600",
        outline:
          "border border-gray-300 bg-white hover:bg-gray-50 focus-visible:ring-gray-400",
        secondary:
          "bg-gray-100 text-gray-900 hover:bg-gray-200 focus-visible:ring-gray-400",
        ghost:
          "hover:bg-gray-100 hover:text-gray-900 focus-visible:ring-gray-400",
        link: "text-blue-600 underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-8 px-3 text-xs",
        lg: "h-12 px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  loading?: boolean;
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    { className, variant, size, loading, children, disabled, ...props },
    ref
  ) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        disabled={disabled || loading}
        {...props}
      >
        {loading && <Spinner size="sm" className="mr-2" />}
        {children}
      </button>
    );
  }
);
Button.displayName = "Button";

export { Button, buttonVariants };
```

### Input Component

`src/components/ui/Input.tsx`:

```typescript
import { forwardRef, InputHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  error?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, error, ...props }, ref) => {
    return (
      <div className="w-full">
        <input
          type={type}
          className={cn(
            "flex h-10 w-full rounded-md border bg-white px-3 py-2 text-sm",
            "placeholder:text-gray-400",
            "focus:outline-none focus:ring-2 focus:ring-offset-2",
            "disabled:cursor-not-allowed disabled:opacity-50",
            error
              ? "border-red-300 focus:ring-red-600"
              : "border-gray-300 focus:ring-blue-600",
            className
          )}
          ref={ref}
          {...props}
        />
        {error && <p className="mt-1 text-xs text-red-600">{error}</p>}
      </div>
    );
  }
);
Input.displayName = "Input";

export { Input };
```

### Modal Component

`src/components/ui/Modal.tsx`:

```typescript
"use client";

import { Fragment } from "react";
import { Dialog, Transition } from "@headlessui/react";
import { XMarkIcon } from "@heroicons/react/24/outline";
import { Button } from "./Button";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: "sm" | "md" | "lg" | "xl";
}

const sizeClasses = {
  sm: "max-w-md",
  md: "max-w-lg",
  lg: "max-w-2xl",
  xl: "max-w-4xl",
};

export function Modal({
  isOpen,
  onClose,
  title,
  children,
  size = "md",
}: ModalProps) {
  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        {/* Backdrop */}
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black bg-opacity-25" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4 text-center">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel
                className={cn(
                  "w-full transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all",
                  sizeClasses[size]
                )}
              >
                {/* Header */}
                {title && (
                  <div className="flex items-center justify-between mb-4">
                    <Dialog.Title
                      as="h3"
                      className="text-lg font-medium leading-6 text-gray-900"
                    >
                      {title}
                    </Dialog.Title>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={onClose}
                      className="rounded-full"
                    >
                      <XMarkIcon className="h-5 w-5" />
                    </Button>
                  </div>
                )}

                {/* Content */}
                <div>{children}</div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
}
```

## 🪝 Custom Hooks

### useBookmarks Hook

`src/hooks/useBookmarks.tsx`:

```typescript
"use client";

import { useEffect, useState, useCallback } from "react";
import { useAuth } from "@clerk/nextjs";
import { useToast } from "@/hooks/useToast";
import type { Bookmark, CreateBookmarkData } from "@/types/bookmark";

interface UseBookmarksReturn {
  bookmarks: Bookmark[];
  loading: boolean;
  error: string | null;
  addBookmark: (data: CreateBookmarkData) => Promise<void>;
  updateBookmark: (id: string, data: Partial<Bookmark>) => Promise<void>;
  deleteBookmark: (id: string) => Promise<void>;
  refetch: () => Promise<void>;
}

export function useBookmarks(): UseBookmarksReturn {
  const { getToken } = useAuth();
  const { showToast } = useToast();
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Função para fazer requisições autenticadas
  const fetchWithAuth = useCallback(
    async (url: string, options?: RequestInit) => {
      const token = await getToken();
      return fetch(url, {
        ...options,
        headers: {
          ...options?.headers,
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });
    },
    [getToken]
  );

  // Buscar bookmarks
  const fetchBookmarks = useCallback(async () => {
    try {
      setError(null);
      const response = await fetchWithAuth("/api/bookmarks");

      if (!response.ok) {
        throw new Error("Falha ao buscar bookmarks");
      }

      const data = await response.json();
      setBookmarks(data.data || []);
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Erro desconhecido";
      setError(message);
      showToast({
        title: "Erro",
        description: message,
        variant: "error",
      });
    } finally {
      setLoading(false);
    }
  }, [fetchWithAuth, showToast]);

  // Adicionar bookmark
  const addBookmark = useCallback(
    async (data: CreateBookmarkData) => {
      try {
        const response = await fetchWithAuth("/api/bookmarks", {
          method: "POST",
          body: JSON.stringify(data),
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.message || "Falha ao criar bookmark");
        }

        const result = await response.json();
        setBookmarks(prev => [result.data, ...prev]);

        showToast({
          title: "Sucesso",
          description: "Bookmark adicionado com sucesso",
          variant: "success",
        });
      } catch (error) {
        const message =
          error instanceof Error ? error.message : "Erro ao criar bookmark";
        showToast({
          title: "Erro",
          description: message,
          variant: "error",
        });
        throw error;
      }
    },
    [fetchWithAuth, showToast]
  );

  // Atualizar bookmark
  const updateBookmark = useCallback(
    async (id: string, data: Partial<Bookmark>) => {
      try {
        const response = await fetchWithAuth(`/api/bookmarks/${id}`, {
          method: "PUT",
          body: JSON.stringify(data),
        });

        if (!response.ok) {
          throw new Error("Falha ao atualizar bookmark");
        }

        const result = await response.json();
        setBookmarks(prev => prev.map(b => (b.id === id ? result.data : b)));

        showToast({
          title: "Sucesso",
          description: "Bookmark atualizado com sucesso",
          variant: "success",
        });
      } catch (error) {
        const message =
          error instanceof Error ? error.message : "Erro ao atualizar";
        showToast({
          title: "Erro",
          description: message,
          variant: "error",
        });
        throw error;
      }
    },
    [fetchWithAuth, showToast]
  );

  // Deletar bookmark
  const deleteBookmark = useCallback(
    async (id: string) => {
      try {
        const response = await fetchWithAuth(`/api/bookmarks/${id}`, {
          method: "DELETE",
        });

        if (!response.ok) {
          throw new Error("Falha ao deletar bookmark");
        }

        setBookmarks(prev => prev.filter(b => b.id !== id));

        showToast({
          title: "Sucesso",
          description: "Bookmark excluído com sucesso",
          variant: "success",
        });
      } catch (error) {
        const message =
          error instanceof Error ? error.message : "Erro ao deletar";
        showToast({
          title: "Erro",
          description: message,
          variant: "error",
        });
        throw error;
      }
    },
    [fetchWithAuth, showToast]
  );

  // Carregar bookmarks ao montar
  useEffect(() => {
    fetchBookmarks();
  }, [fetchBookmarks]);

  return {
    bookmarks,
    loading,
    error,
    addBookmark,
    updateBookmark,
    deleteBookmark,
    refetch: fetchBookmarks,
  };
}
```

### useDebounce Hook

`src/hooks/useDebounce.tsx`:

```typescript
import { useEffect, useState } from "react";

export function useDebounce<T>(value: T, delay: number = 500): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(timer);
    };
  }, [value, delay]);

  return debouncedValue;
}
```

## 🎨 Estilos CSS

### Estilos Globais

`src/app/globals.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Variáveis CSS */
@layer base {
  :root {
    --font-inter: "Inter", system-ui, -apple-system, sans-serif;

    /* Cores */
    --color-primary: 59 130 246; /* blue-500 */
    --color-primary-dark: 29 78 216; /* blue-700 */
    --color-success: 16 185 129; /* emerald-500 */
    --color-danger: 239 68 68; /* red-500 */
    --color-warning: 245 158 11; /* amber-500 */

    /* Sombras */
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  }
}

/* Estilos base */
@layer base {
  body {
    @apply bg-gray-50 text-gray-900 antialiased;
  }

  /* Focus visível para acessibilidade */
  *:focus-visible {
    @apply outline-none ring-2 ring-blue-500 ring-offset-2;
  }
}

/* Componentes customizados */
@layer components {
  /* Container principal */
  .main-content {
    @apply min-h-[calc(100vh-4rem)] py-8;
  }

  /* Cards */
  .bookmark-card {
    @apply bg-white rounded-lg shadow-sm border border-gray-200 p-6;
    @apply hover:shadow-md transition-shadow duration-200;
  }

  /* Animações */
  .animate-slide-up {
    animation: slideUp 0.3s ease-out;
  }

  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Loading skeleton */
  .skeleton {
    @apply animate-pulse bg-gray-200 rounded;
  }

  /* Scrollbar customizada */
  .custom-scrollbar {
    scrollbar-width: thin;
    scrollbar-color: theme("colors.gray.400") theme("colors.gray.100");
  }

  .custom-scrollbar::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }

  .custom-scrollbar::-webkit-scrollbar-track {
    @apply bg-gray-100 rounded;
  }

  .custom-scrollbar::-webkit-scrollbar-thumb {
    @apply bg-gray-400 rounded hover:bg-gray-500;
  }
}

/* Utilitários */
@layer utilities {
  /* Line clamp */
  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  /* Gradientes */
  .gradient-primary {
    @apply bg-gradient-to-r from-blue-600 to-indigo-600;
  }

  .gradient-text {
    @apply bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600;
  }
}
```

## 🚀 Performance e Otimizações

1. **Code Splitting**: Componentes pesados com dynamic imports
2. **Memo e Callbacks**: Evitar re-renders desnecessários
3. **Lazy Loading**: Imagens e componentes não críticos
4. **Debounce**: Em campos de busca e inputs
5. **Virtual Scrolling**: Para listas muito grandes
6. **Skeleton Loading**: Melhor UX durante carregamento

---

Com esses componentes bem estruturados, você tem uma aplicação React/Next.js moderna e escalável!
