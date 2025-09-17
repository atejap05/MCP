# Estrutura Detalhada do Projeto MCP Server

## 📁 Estrutura Completa de Arquivos

```
bookmark-manager/
├── 📁 src/                              # Código fonte principal
│   ├── 📁 app/                          # App Router do Next.js
│   │   ├── 📁 api/                      # Rotas de API backend
│   │   │   ├── 📁 bookmarks/            # Endpoints de bookmarks
│   │   │   │   ├── 📄 route.ts          # GET (listar) e POST (criar)
│   │   │   │   └── 📁 [id]/             # Rotas dinâmicas
│   │   │   │       └── 📄 route.ts      # DELETE bookmark específico
│   │   │   └── 📁 [transport]/          # Servidor MCP dinâmico
│   │   │       └── 📄 route.ts          # Handler principal MCP
│   │   │
│   │   ├── 📁 .well-known/              # Metadados OAuth (padrão RFC)
│   │   │   ├── 📁 oauth-authorization-server/
│   │   │   │   └── 📄 route.ts          # Descoberta OAuth
│   │   │   └── 📁 oauth-protected-resource/
│   │   │       └── 📁 mcp/
│   │   │           └── 📄 route.ts      # Metadados do recurso MCP
│   │   │
│   │   ├── 📄 layout.tsx                # Layout raiz com Clerk
│   │   ├── 📄 page.tsx                  # Página inicial
│   │   ├── 📄 globals.css               # Estilos globais
│   │   └── 📄 page.module.css           # Estilos modulares
│   │
│   ├── 📁 components/                   # Componentes React reutilizáveis
│   │   ├── 📄 BookmarkForm.tsx          # Formulário para adicionar
│   │   ├── 📄 BookmarkCard.tsx          # Card individual de bookmark
│   │   └── 📄 BookmarkList.tsx          # Lista/grid de bookmarks
│   │
│   ├── 📁 hooks/                        # React Hooks customizados
│   │   └── 📄 useBookmarks.tsx          # Hook para estado de bookmarks
│   │
│   ├── 📁 lib/                          # Bibliotecas e utilitários
│   │   └── 📄 bookmark-utils.ts         # Funções do banco de dados
│   │
│   ├── 📁 types/                        # Definições TypeScript
│   │   └── 📄 bookmark.ts               # Interfaces e tipos
│   │
│   └── 📄 middleware.ts                 # Middleware de autenticação
│
├── 📁 prisma/                           # Configuração do banco de dados
│   ├── 📄 schema.prisma                 # Schema do banco
│   ├── 📄 dev.db                        # Banco SQLite (gerado)
│   └── 📁 migrations/                   # Migrações (gerado)
│
├── 📁 public/                           # Arquivos estáticos
│   └── 📄 favicon.ico
│
├── 📄 .env                              # Variáveis de ambiente
├── 📄 .env.example                      # Exemplo de variáveis
├── 📄 .gitignore                        # Arquivos ignorados pelo Git
├── 📄 package.json                      # Dependências e scripts
├── 📄 package-lock.json                 # Lock file do npm
├── 📄 tsconfig.json                     # Configuração TypeScript
├── 📄 next.config.js                    # Configuração Next.js
├── 📄 README.md                         # Documentação principal
└── 📄 .eslintrc.json                    # Configuração ESLint
```

## 🔍 Detalhamento dos Diretórios

### `/src/app/` - App Router

O diretório principal do Next.js 15 usando o novo App Router:

- **`api/`**: Todas as rotas de API backend

  - `bookmarks/`: CRUD completo de bookmarks
  - `[transport]/`: Servidor MCP com rotas dinâmicas

- **`.well-known/`**: Endpoints padronizados para descoberta OAuth

  - Seguem as RFCs do OAuth 2.1
  - Necessários para autenticação MCP

- **Arquivos principais**:
  - `layout.tsx`: Wrapper com ClerkProvider
  - `page.tsx`: Componente da página inicial
  - `globals.css`: Estilos CSS globais

### `/src/components/` - Componentes React

Componentes reutilizáveis da UI:

- **`BookmarkForm.tsx`**:

  - Formulário controlado
  - Validação de campos
  - Estados de loading

- **`BookmarkCard.tsx`**:

  - Display individual
  - Botão de delete
  - Formatação de data/domínio

- **`BookmarkList.tsx`**:
  - Grid responsivo
  - Estado vazio
  - Mapeamento de cards

### `/src/hooks/` - Custom Hooks

- **`useBookmarks.tsx`**:
  - Gerenciamento de estado
  - Chamadas à API
  - Loading e erro states
  - Operações CRUD

### `/src/lib/` - Utilitários

- **`bookmark-utils.ts`**:
  - Funções do Prisma
  - Validação de dados
  - Tratamento de erros
  - Queries otimizadas

### `/src/types/` - TypeScript

- **`bookmark.ts`**:
  - Interface `Bookmark`
  - Interface `CreateBookmarkData`
  - Types compartilhados

### `/prisma/` - Banco de Dados

- **`schema.prisma`**:
  - Modelo Bookmark
  - Configuração SQLite
  - Índices para performance

## 📋 Arquivos de Configuração

### `package.json`

```json
{
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "prisma:generate": "prisma generate",
    "prisma:migrate": "prisma migrate dev",
    "prisma:studio": "prisma studio"
  }
}
```

### `.env.example`

```bash
# Clerk (obtenha em dashboard.clerk.com)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# Banco de Dados
DATABASE_URL="file:./dev.db"

# URLs do Clerk (opcionais)
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
```

### `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### `next.config.js`

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Configurações opcionais
  reactStrictMode: true,
  experimental: {
    // Habilita features experimentais se necessário
  },
};

module.exports = nextConfig;
```

## 🔄 Fluxo de Dados

```mermaid
graph LR
    A[Cliente MCP] --> B[/api/[transport]]
    B --> C{Autenticado?}
    C -->|Não| D[/.well-known/]
    D --> E[OAuth Flow]
    E --> C
    C -->|Sim| F[Ferramentas MCP]
    F --> G[bookmark-utils]
    G --> H[(Prisma DB)]

    I[Browser] --> J[page.tsx]
    J --> K[useBookmarks]
    K --> L[/api/bookmarks]
    L --> G
```

## 🎯 Convenções de Nomenclatura

1. **Arquivos TypeScript**: `camelCase.ts` ou `kebab-case.ts`
2. **Componentes React**: `PascalCase.tsx`
3. **Hooks**: `use` + `PascalCase.tsx`
4. **Utilitários**: `kebab-case.ts`
5. **Tipos/Interfaces**: `PascalCase`
6. **Variáveis de ambiente**: `UPPER_SNAKE_CASE`

## 🚀 Scripts NPM Úteis

```bash
# Desenvolvimento
npm run dev              # Inicia servidor de desenvolvimento

# Banco de dados
npm run prisma:generate  # Gera cliente Prisma
npm run prisma:migrate   # Aplica migrações
npm run prisma:studio    # Interface visual do BD

# Produção
npm run build           # Build para produção
npm run start          # Inicia servidor de produção

# Qualidade
npm run lint           # Verifica problemas de código
npm run type-check     # Verifica tipos TypeScript
```

## 📝 Notas Importantes

1. **App Router**: Usamos o novo App Router do Next.js 15
2. **Server Components**: Por padrão, componentes são server-side
3. **'use client'**: Necessário para hooks e interatividade
4. **Rotas dinâmicas**: `[param]` para parâmetros de rota
5. **Middleware**: Roda antes de todas as requisições
6. **`.well-known`**: Padrão RFC para descoberta de serviços

---

Esta estrutura segue as melhores práticas do Next.js 15 e foi otimizada para manutenibilidade e escalabilidade do projeto MCP Server.
