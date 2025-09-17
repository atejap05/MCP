# Banco de Dados com Prisma

## 🗄️ Visão Geral do Prisma

O Prisma é um ORM (Object-Relational Mapping) moderno que oferece:

- ✅ Type-safety completo com TypeScript
- ✅ Migrações automáticas
- ✅ Cliente gerado automaticamente
- ✅ Interface visual (Prisma Studio)
- ✅ Suporte para múltiplos bancos de dados
- ✅ Query builder intuitivo

## 📋 Configuração Inicial

### 1. Instalação

```bash
# Dependências de produção
npm install @prisma/client

# Dependências de desenvolvimento
npm install -D prisma
```

### 2. Inicialização

```bash
# Inicializa o Prisma no projeto
npx prisma init

# Isso cria:
# - prisma/schema.prisma (arquivo de schema)
# - .env (se não existir)
```

### 3. Configuração do Schema

#### `prisma/schema.prisma`:

```prisma
// Configuração do gerador de cliente
generator client {
  provider = "prisma-client-js"
  // Otimizações para produção
  binaryTargets = ["native", "linux-musl-openssl-3.0.x"]
  previewFeatures = ["fullTextSearch", "fullTextIndex"]
}

// Configuração da fonte de dados
datasource db {
  // Para desenvolvimento (SQLite)
  provider = "sqlite"
  url      = env("DATABASE_URL")

  // Para produção (PostgreSQL)
  // provider = "postgresql"
  // url      = env("DATABASE_URL")
}

// ===================================
// MODELOS DE DADOS
// ===================================

// Modelo principal: Bookmark
model Bookmark {
  // Identificador único
  id        String   @id @default(uuid())

  // Campos obrigatórios
  url       String
  title     String
  userId    String   // ID do usuário do Clerk

  // Campos opcionais
  notes     String?  // ? indica opcional
  tags      String?  // Tags separadas por vírgula
  favicon   String?  // URL do favicon

  // Timestamps automáticos
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  // Índices para performance
  @@index([userId])
  @@index([createdAt])
  @@index([userId, createdAt])
}

// Modelo futuro: Categoria (exemplo)
model Category {
  id        String   @id @default(uuid())
  name      String
  color     String   @default("#0070f3")
  userId    String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  // Relacionamento com bookmarks
  bookmarks BookmarkCategory[]

  @@unique([userId, name])
  @@index([userId])
}

// Tabela de relacionamento N:N
model BookmarkCategory {
  bookmarkId String
  categoryId String
  assignedAt DateTime @default(now())

  bookmark   Bookmark @relation(fields: [bookmarkId], references: [id], onDelete: Cascade)
  category   Category @relation(fields: [categoryId], references: [id], onDelete: Cascade)

  @@id([bookmarkId, categoryId])
  @@index([bookmarkId])
  @@index([categoryId])
}
```

### 4. Configuração para Diferentes Ambientes

#### Desenvolvimento (SQLite)

`.env`:

```bash
DATABASE_URL="file:./dev.db"
```

#### Produção (PostgreSQL)

`.env.production`:

```bash
DATABASE_URL="postgresql://usuario:senha@host:5432/bookmark_manager?schema=public"
```

#### Produção (MySQL)

`.env.production`:

```bash
DATABASE_URL="mysql://usuario:senha@host:3306/bookmark_manager"
```

## 🔄 Migrações

### Criando Migrações

```bash
# Criar uma nova migração
npx prisma migrate dev --name init

# Isso faz:
# 1. Gera SQL baseado no schema
# 2. Aplica no banco de dados
# 3. Gera o cliente Prisma
```

### Estrutura de Migrações

```
prisma/
├── migrations/
│   ├── 20240115120000_init/
│   │   └── migration.sql
│   ├── 20240116140000_add_categories/
│   │   └── migration.sql
│   └── migration_lock.toml
```

### Comandos de Migração

```bash
# Desenvolvimento - cria e aplica migrações
npx prisma migrate dev

# Produção - apenas aplica migrações existentes
npx prisma migrate deploy

# Reset do banco (CUIDADO! Apaga todos os dados)
npx prisma migrate reset

# Criar migração sem aplicar
npx prisma migrate dev --create-only

# Status das migrações
npx prisma migrate status
```

## 💻 Cliente Prisma

### Gerando o Cliente

```bash
# Gera o cliente TypeScript
npx prisma generate

# Adicione ao package.json para gerar após install
"postinstall": "prisma generate"
```

### Inicializando o Cliente

`src/lib/prisma.ts`:

```typescript
import { PrismaClient } from "@prisma/client";

// Função para criar instância do Prisma
const prismaClientSingleton = () => {
  return new PrismaClient({
    log:
      process.env.NODE_ENV === "development"
        ? ["query", "error", "warn"]
        : ["error"],
  });
};

// Type helper
type PrismaClientSingleton = ReturnType<typeof prismaClientSingleton>;

// Globalização para evitar múltiplas instâncias em desenvolvimento
const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClientSingleton | undefined;
};

// Exporta instância única
export const prisma = globalForPrisma.prisma ?? prismaClientSingleton();

// Em desenvolvimento, preserva a instância
if (process.env.NODE_ENV !== "production") {
  globalForPrisma.prisma = prisma;
}

// Tipos úteis exportados
export type { Bookmark, Category } from "@prisma/client";
```

## 📊 Operações CRUD

### Create (Criar)

```typescript
import { prisma } from "@/lib/prisma";

// Criar um bookmark
const newBookmark = await prisma.bookmark.create({
  data: {
    url: "https://example.com",
    title: "Example Site",
    notes: "Great resource",
    userId: "user_123",
  },
});

// Criar múltiplos
const bookmarks = await prisma.bookmark.createMany({
  data: [
    { url: "...", title: "...", userId: "..." },
    { url: "...", title: "...", userId: "..." },
  ],
});

// Criar com validação
async function createBookmark(data: CreateBookmarkInput) {
  // Validação
  if (!isValidURL(data.url)) {
    throw new Error("URL inválida");
  }

  return await prisma.bookmark.create({
    data: {
      ...data,
      url: normalizeURL(data.url),
    },
  });
}
```

### Read (Ler)

```typescript
// Buscar todos os bookmarks de um usuário
const userBookmarks = await prisma.bookmark.findMany({
  where: {
    userId: "user_123",
  },
  orderBy: {
    createdAt: "desc",
  },
});

// Buscar com paginação
const paginatedBookmarks = await prisma.bookmark.findMany({
  where: { userId },
  skip: (page - 1) * pageSize,
  take: pageSize,
  orderBy: { createdAt: "desc" },
});

// Buscar por ID
const bookmark = await prisma.bookmark.findUnique({
  where: {
    id: bookmarkId,
  },
});

// Buscar com filtros complexos
const filteredBookmarks = await prisma.bookmark.findMany({
  where: {
    userId,
    AND: [
      {
        OR: [
          { title: { contains: searchTerm, mode: "insensitive" } },
          { notes: { contains: searchTerm, mode: "insensitive" } },
          { url: { contains: searchTerm, mode: "insensitive" } },
        ],
      },
      {
        createdAt: {
          gte: startDate,
          lte: endDate,
        },
      },
    ],
  },
  orderBy: [{ createdAt: "desc" }, { title: "asc" }],
});

// Contar registros
const count = await prisma.bookmark.count({
  where: { userId },
});
```

### Update (Atualizar)

```typescript
// Atualizar um bookmark
const updated = await prisma.bookmark.update({
  where: {
    id: bookmarkId,
  },
  data: {
    title: "Novo Título",
    notes: "Notas atualizadas",
  },
});

// Atualizar com verificação de propriedade
async function updateBookmark(
  userId: string,
  bookmarkId: string,
  data: UpdateData
) {
  // Verifica se o bookmark pertence ao usuário
  const bookmark = await prisma.bookmark.findFirst({
    where: {
      id: bookmarkId,
      userId,
    },
  });

  if (!bookmark) {
    throw new Error("Bookmark não encontrado ou sem permissão");
  }

  return await prisma.bookmark.update({
    where: { id: bookmarkId },
    data,
  });
}

// Atualizar múltiplos
await prisma.bookmark.updateMany({
  where: {
    userId,
    createdAt: {
      lt: new Date("2024-01-01"),
    },
  },
  data: {
    tags: "archived",
  },
});
```

### Delete (Deletar)

```typescript
// Deletar um bookmark
await prisma.bookmark.delete({
  where: {
    id: bookmarkId,
  },
});

// Deletar com verificação
async function deleteBookmark(userId: string, bookmarkId: string) {
  const result = await prisma.bookmark.deleteMany({
    where: {
      id: bookmarkId,
      userId, // Garante que só deleta do próprio usuário
    },
  });

  if (result.count === 0) {
    throw new Error("Bookmark não encontrado ou sem permissão");
  }

  return true;
}

// Deletar múltiplos
await prisma.bookmark.deleteMany({
  where: {
    userId,
    createdAt: {
      lt: new Date(Date.now() - 365 * 24 * 60 * 60 * 1000), // 1 ano atrás
    },
  },
});
```

## 🔍 Queries Avançadas

### Relacionamentos

```typescript
// Se tivéssemos categorias
const bookmarksWithCategories = await prisma.bookmark.findMany({
  where: { userId },
  include: {
    categories: {
      include: {
        category: true,
      },
    },
  },
});

// Agregações
const stats = await prisma.bookmark.groupBy({
  by: ["userId"],
  _count: {
    id: true,
  },
  _max: {
    createdAt: true,
  },
  _min: {
    createdAt: true,
  },
});
```

### Transações

```typescript
// Transação simples
const [bookmark, log] = await prisma.$transaction([
  prisma.bookmark.create({ data: bookmarkData }),
  prisma.activityLog.create({ data: logData }),
]);

// Transação interativa
await prisma.$transaction(async tx => {
  // 1. Criar bookmark
  const bookmark = await tx.bookmark.create({
    data: bookmarkData,
  });

  // 2. Atualizar contador do usuário
  await tx.userStats.update({
    where: { userId },
    data: {
      bookmarkCount: {
        increment: 1,
      },
    },
  });

  // 3. Criar log
  await tx.activityLog.create({
    data: {
      userId,
      action: "bookmark_created",
      bookmarkId: bookmark.id,
    },
  });

  return bookmark;
});
```

### Full-Text Search (se habilitado)

```typescript
// Para PostgreSQL com extensão de busca
const results = await prisma.bookmark.findMany({
  where: {
    userId,
    OR: [
      { title: { search: searchQuery } },
      { notes: { search: searchQuery } },
    ],
  },
});
```

## 🛠️ Utilitários Helper

`src/lib/bookmark-utils.ts`:

```typescript
import { prisma } from "@/lib/prisma";
import type { Bookmark, Prisma } from "@prisma/client";

export interface BookmarkFilters {
  search?: string;
  tags?: string[];
  startDate?: Date;
  endDate?: Date;
}

export class BookmarkService {
  /**
   * Busca bookmarks com filtros avançados
   */
  static async findBookmarks(
    userId: string,
    filters: BookmarkFilters = {},
    pagination: { page: number; limit: number } = { page: 1, limit: 20 }
  ) {
    const where: Prisma.BookmarkWhereInput = {
      userId,
    };

    // Adiciona filtro de busca
    if (filters.search) {
      where.OR = [
        { title: { contains: filters.search, mode: "insensitive" } },
        { notes: { contains: filters.search, mode: "insensitive" } },
        { url: { contains: filters.search, mode: "insensitive" } },
      ];
    }

    // Adiciona filtro de tags
    if (filters.tags && filters.tags.length > 0) {
      where.tags = {
        in: filters.tags,
      };
    }

    // Adiciona filtro de data
    if (filters.startDate || filters.endDate) {
      where.createdAt = {};
      if (filters.startDate) {
        where.createdAt.gte = filters.startDate;
      }
      if (filters.endDate) {
        where.createdAt.lte = filters.endDate;
      }
    }

    // Executa queries em paralelo
    const [bookmarks, total] = await Promise.all([
      prisma.bookmark.findMany({
        where,
        skip: (pagination.page - 1) * pagination.limit,
        take: pagination.limit,
        orderBy: { createdAt: "desc" },
      }),
      prisma.bookmark.count({ where }),
    ]);

    return {
      bookmarks,
      pagination: {
        page: pagination.page,
        limit: pagination.limit,
        total,
        totalPages: Math.ceil(total / pagination.limit),
      },
    };
  }

  /**
   * Verifica se URL já existe
   */
  static async isURLBookmarked(userId: string, url: string): Promise<boolean> {
    const normalized = this.normalizeURL(url);
    const exists = await prisma.bookmark.findFirst({
      where: {
        userId,
        url: normalized,
      },
      select: { id: true },
    });
    return !!exists;
  }

  /**
   * Normaliza URLs para comparação
   */
  static normalizeURL(url: string): string {
    try {
      const urlObj = new URL(url);
      // Remove trailing slash
      return urlObj.href.replace(/\/$/, "");
    } catch {
      return url;
    }
  }

  /**
   * Extrai domínio da URL
   */
  static getDomain(url: string): string {
    try {
      const urlObj = new URL(url);
      return urlObj.hostname.replace("www.", "");
    } catch {
      return "invalid-url";
    }
  }
}
```

## 🎭 Prisma Studio

Interface visual para gerenciar dados:

```bash
# Abrir Prisma Studio
npx prisma studio

# Abre no navegador: http://localhost:5555
```

Funcionalidades:

- Visualizar todos os modelos
- Criar, editar e deletar registros
- Filtrar e ordenar dados
- Exportar dados

## 🌱 Seed Data (Dados Iniciais)

`prisma/seed.ts`:

```typescript
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  console.log("🌱 Iniciando seed...");

  // Criar bookmarks de exemplo
  const bookmarks = await prisma.bookmark.createMany({
    data: [
      {
        url: "https://nextjs.org/docs",
        title: "Next.js Documentation",
        notes: "Documentação oficial do Next.js",
        userId: "user_example",
      },
      {
        url: "https://www.prisma.io/docs",
        title: "Prisma Documentation",
        notes: "Guia completo do Prisma ORM",
        userId: "user_example",
      },
      {
        url: "https://clerk.com/docs",
        title: "Clerk Documentation",
        notes: "Autenticação com Clerk",
        userId: "user_example",
      },
    ],
    skipDuplicates: true,
  });

  console.log(`✅ ${bookmarks.count} bookmarks criados`);
}

main()
  .catch(e => {
    console.error("❌ Erro no seed:", e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

Adicione ao `package.json`:

```json
{
  "prisma": {
    "seed": "ts-node --compiler-options {\"module\":\"CommonJS\"} prisma/seed.ts"
  },
  "scripts": {
    "db:seed": "prisma db seed"
  }
}
```

## 🚀 Deploy e Produção

### Checklist para Produção

1. **Use PostgreSQL ou MySQL** em vez de SQLite
2. **Configure Connection Pooling**:

   ```typescript
   new PrismaClient({
     datasources: {
       db: {
         url: process.env.DATABASE_URL,
       },
     },
   });
   ```

3. **Otimize queries**:

   - Use `select` para buscar apenas campos necessários
   - Use índices apropriados
   - Evite N+1 queries

4. **Configure logs apropriados**:

   ```typescript
   new PrismaClient({
     log: ["error", "warn"],
   });
   ```

5. **Use transações para operações críticas**

### Backup e Restore

```bash
# Backup (SQLite)
cp prisma/dev.db prisma/backup-$(date +%Y%m%d).db

# Backup (PostgreSQL)
pg_dump bookmark_manager > backup-$(date +%Y%m%d).sql

# Restore (PostgreSQL)
psql bookmark_manager < backup-20240115.sql
```

## 🔧 Troubleshooting

### Erro: "The table does not exist"

```bash
# Recrie as migrações
npx prisma migrate reset
npx prisma migrate dev
```

### Erro: "Cannot find module '@prisma/client'"

```bash
# Gere o cliente
npx prisma generate
```

### Performance lenta

1. Adicione índices apropriados
2. Use `select` para campos específicos
3. Implemente paginação
4. Use `findFirst` em vez de `findMany` quando apropriado

---

Com o Prisma configurado, você tem um banco de dados type-safe e pronto para escalar!
