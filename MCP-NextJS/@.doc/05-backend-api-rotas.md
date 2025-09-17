# Backend API e Rotas

## 🚀 Visão Geral da API

Nossa API RESTful segue as convenções do Next.js App Router com:

- ✅ Rotas baseadas em arquivos
- ✅ Handlers assíncronos
- ✅ Autenticação via Clerk
- ✅ Validação de dados
- ✅ Tratamento de erros
- ✅ Respostas padronizadas

## 📁 Estrutura das Rotas

```
src/app/api/
├── bookmarks/
│   ├── route.ts              # GET (listar) e POST (criar)
│   └── [id]/
│       └── route.ts          # GET, PUT, DELETE por ID
├── [transport]/              # Servidor MCP
│   └── route.ts              # Ferramentas MCP
└── webhooks/
    └── clerk/
        └── route.ts          # Webhooks do Clerk
```

## 🔐 Autenticação e Middleware

### Middleware Global

`src/middleware.ts`:

```typescript
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Rotas que não precisam de autenticação
const isPublicRoute = createRouteMatcher([
  "/",
  "/sign-in(.*)",
  "/sign-up(.*)",
  "/.well-known/(.*)", // OAuth discovery
  "/api/webhooks/(.*)", // Webhooks externos
  "/api/health", // Health check
]);

// Rotas de API que precisam de autenticação
const isApiRoute = createRouteMatcher(["/api/(.*)"]);

export default clerkMiddleware(async (auth, request: NextRequest) => {
  const { userId, sessionId } = await auth();

  // Log para debug (remover em produção)
  if (process.env.NODE_ENV === "development") {
    console.log(`[Middleware] ${request.method} ${request.nextUrl.pathname}`, {
      userId,
      isPublic: isPublicRoute(request),
      isApi: isApiRoute(request),
    });
  }

  // Se é rota de API e não está autenticado
  if (isApiRoute(request) && !isPublicRoute(request) && !userId) {
    return NextResponse.json(
      {
        error: "Unauthorized",
        message: "Authentication required",
        code: "AUTH_REQUIRED",
      },
      { status: 401 }
    );
  }

  // Adiciona headers de segurança
  const response = NextResponse.next();

  // CORS headers para API
  if (isApiRoute(request)) {
    response.headers.set("X-Content-Type-Options", "nosniff");
    response.headers.set("X-Frame-Options", "DENY");
    response.headers.set("X-XSS-Protection", "1; mode=block");
  }

  return response;
});

export const config = {
  matcher: ["/((?!.*\\..*|_next).*)", "/(api|trpc)(.*)"],
};
```

## 📚 Rotas de Bookmarks

### GET /api/bookmarks - Listar Bookmarks

`src/app/api/bookmarks/route.ts`:

```typescript
import { NextRequest, NextResponse } from "next/server";
import { auth } from "@clerk/nextjs/server";
import { z } from "zod";
import { getUserBookmarks } from "@/lib/bookmark-utils";

// Schema de validação para query params
const listBookmarksSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  search: z.string().optional(),
  sort: z.enum(["createdAt", "updatedAt", "title"]).default("createdAt"),
  order: z.enum(["asc", "desc"]).default("desc"),
});

/**
 * GET /api/bookmarks
 * Lista todos os bookmarks do usuário autenticado
 *
 * Query params:
 * - page: número da página (default: 1)
 * - limit: itens por página (default: 20, max: 100)
 * - search: termo de busca (opcional)
 * - sort: campo para ordenação (default: createdAt)
 * - order: direção da ordenação (default: desc)
 */
export async function GET(request: NextRequest) {
  try {
    // 1. Verificar autenticação
    const { userId } = await auth();
    if (!userId) {
      return NextResponse.json(
        {
          error: "Unauthorized",
          message: "Please sign in to access your bookmarks",
          code: "AUTH_REQUIRED",
        },
        { status: 401 }
      );
    }

    // 2. Validar query params
    const searchParams = Object.fromEntries(
      request.nextUrl.searchParams.entries()
    );
    const validationResult = listBookmarksSchema.safeParse(searchParams);

    if (!validationResult.success) {
      return NextResponse.json(
        {
          error: "Bad Request",
          message: "Invalid query parameters",
          code: "INVALID_PARAMS",
          details: validationResult.error.flatten(),
        },
        { status: 400 }
      );
    }

    const { page, limit, search, sort, order } = validationResult.data;

    // 3. Buscar bookmarks
    const bookmarks = await getUserBookmarks(userId, {
      pagination: { page, limit },
      search,
      orderBy: { [sort]: order },
    });

    // 4. Retornar resposta padronizada
    return NextResponse.json({
      success: true,
      data: bookmarks.items,
      pagination: {
        page,
        limit,
        total: bookmarks.total,
        totalPages: Math.ceil(bookmarks.total / limit),
        hasNext: page < Math.ceil(bookmarks.total / limit),
        hasPrev: page > 1,
      },
      meta: {
        timestamp: new Date().toISOString(),
        version: "1.0.0",
      },
    });
  } catch (error) {
    console.error("[GET /api/bookmarks] Error:", error);

    return NextResponse.json(
      {
        error: "Internal Server Error",
        message: "Failed to fetch bookmarks",
        code: "INTERNAL_ERROR",
      },
      { status: 500 }
    );
  }
}
```

### POST /api/bookmarks - Criar Bookmark

```typescript
// Schema de validação para criar bookmark
const createBookmarkSchema = z.object({
  url: z.string().url("Invalid URL format"),
  title: z.string().min(1, "Title is required").max(200),
  notes: z.string().max(1000).optional(),
  tags: z.array(z.string()).max(10).optional(),
});

/**
 * POST /api/bookmarks
 * Cria um novo bookmark
 *
 * Body:
 * - url: URL válida (obrigatório)
 * - title: título do bookmark (obrigatório)
 * - notes: notas adicionais (opcional)
 * - tags: array de tags (opcional)
 */
export async function POST(request: NextRequest) {
  try {
    // 1. Verificar autenticação
    const { userId } = await auth();
    if (!userId) {
      return NextResponse.json(
        {
          error: "Unauthorized",
          message: "Please sign in to create bookmarks",
          code: "AUTH_REQUIRED",
        },
        { status: 401 }
      );
    }

    // 2. Parse do body
    let body: unknown;
    try {
      body = await request.json();
    } catch {
      return NextResponse.json(
        {
          error: "Bad Request",
          message: "Invalid JSON body",
          code: "INVALID_JSON",
        },
        { status: 400 }
      );
    }

    // 3. Validar dados
    const validationResult = createBookmarkSchema.safeParse(body);
    if (!validationResult.success) {
      return NextResponse.json(
        {
          error: "Bad Request",
          message: "Invalid bookmark data",
          code: "VALIDATION_ERROR",
          details: validationResult.error.flatten(),
        },
        { status: 400 }
      );
    }

    const bookmarkData = validationResult.data;

    // 4. Verificar se URL já existe
    const existingBookmark = await checkDuplicateURL(userId, bookmarkData.url);
    if (existingBookmark) {
      return NextResponse.json(
        {
          error: "Conflict",
          message: "This URL is already bookmarked",
          code: "DUPLICATE_URL",
          existingId: existingBookmark.id,
        },
        { status: 409 }
      );
    }

    // 5. Extrair metadados da URL (opcional)
    const metadata = await extractURLMetadata(bookmarkData.url);

    // 6. Criar bookmark
    const bookmark = await createUserBookmark(userId, {
      ...bookmarkData,
      favicon: metadata?.favicon,
      // Se não tiver título, usar o da página
      title: bookmarkData.title || metadata?.title || "Untitled",
    });

    // 7. Retornar bookmark criado
    return NextResponse.json(
      {
        success: true,
        data: bookmark,
        message: "Bookmark created successfully",
      },
      { status: 201 }
    );
  } catch (error) {
    console.error("[POST /api/bookmarks] Error:", error);

    return NextResponse.json(
      {
        error: "Internal Server Error",
        message: "Failed to create bookmark",
        code: "INTERNAL_ERROR",
      },
      { status: 500 }
    );
  }
}
```

### GET /api/bookmarks/[id] - Obter Bookmark Específico

`src/app/api/bookmarks/[id]/route.ts`:

```typescript
import { NextRequest, NextResponse } from "next/server";
import { auth } from "@clerk/nextjs/server";
import { z } from "zod";
import {
  getBookmarkById,
  updateBookmark,
  deleteBookmark,
} from "@/lib/bookmark-utils";

// Schema para validar ID
const idSchema = z.string().uuid("Invalid bookmark ID format");

// Schema para atualização
const updateBookmarkSchema = z
  .object({
    url: z.string().url().optional(),
    title: z.string().min(1).max(200).optional(),
    notes: z.string().max(1000).optional(),
    tags: z.array(z.string()).max(10).optional(),
  })
  .refine(data => Object.keys(data).length > 0, {
    message: "At least one field must be provided for update",
  });

/**
 * GET /api/bookmarks/[id]
 * Obtém detalhes de um bookmark específico
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    // 1. Verificar autenticação
    const { userId } = await auth();
    if (!userId) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    // 2. Validar ID
    const idResult = idSchema.safeParse(params.id);
    if (!idResult.success) {
      return NextResponse.json(
        {
          error: "Bad Request",
          message: "Invalid bookmark ID",
          code: "INVALID_ID",
        },
        { status: 400 }
      );
    }

    // 3. Buscar bookmark
    const bookmark = await getBookmarkById(idResult.data, userId);

    if (!bookmark) {
      return NextResponse.json(
        {
          error: "Not Found",
          message: "Bookmark not found",
          code: "NOT_FOUND",
        },
        { status: 404 }
      );
    }

    // 4. Retornar bookmark
    return NextResponse.json({
      success: true,
      data: bookmark,
    });
  } catch (error) {
    console.error("[GET /api/bookmarks/[id]] Error:", error);
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    );
  }
}

/**
 * PUT /api/bookmarks/[id]
 * Atualiza um bookmark
 */
export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    // 1. Verificar autenticação
    const { userId } = await auth();
    if (!userId) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    // 2. Validar ID
    const idResult = idSchema.safeParse(params.id);
    if (!idResult.success) {
      return NextResponse.json(
        { error: "Invalid bookmark ID" },
        { status: 400 }
      );
    }

    // 3. Parse e validar body
    const body = await request.json();
    const dataResult = updateBookmarkSchema.safeParse(body);

    if (!dataResult.success) {
      return NextResponse.json(
        {
          error: "Bad Request",
          message: "Invalid update data",
          details: dataResult.error.flatten(),
        },
        { status: 400 }
      );
    }

    // 4. Atualizar bookmark
    const updated = await updateBookmark(
      idResult.data,
      userId,
      dataResult.data
    );

    if (!updated) {
      return NextResponse.json(
        { error: "Bookmark not found or access denied" },
        { status: 404 }
      );
    }

    // 5. Retornar bookmark atualizado
    return NextResponse.json({
      success: true,
      data: updated,
      message: "Bookmark updated successfully",
    });
  } catch (error) {
    console.error("[PUT /api/bookmarks/[id]] Error:", error);
    return NextResponse.json(
      { error: "Failed to update bookmark" },
      { status: 500 }
    );
  }
}

/**
 * DELETE /api/bookmarks/[id]
 * Deleta um bookmark
 */
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    // 1. Verificar autenticação
    const { userId } = await auth();
    if (!userId) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    // 2. Validar ID
    const idResult = idSchema.safeParse(params.id);
    if (!idResult.success) {
      return NextResponse.json(
        { error: "Invalid bookmark ID" },
        { status: 400 }
      );
    }

    // 3. Deletar bookmark
    const deleted = await deleteBookmark(idResult.data, userId);

    if (!deleted) {
      return NextResponse.json(
        { error: "Bookmark not found or access denied" },
        { status: 404 }
      );
    }

    // 4. Retornar sucesso
    return NextResponse.json({
      success: true,
      message: "Bookmark deleted successfully",
    });
  } catch (error) {
    console.error("[DELETE /api/bookmarks/[id]] Error:", error);
    return NextResponse.json(
      { error: "Failed to delete bookmark" },
      { status: 500 }
    );
  }
}
```

## 🛠️ Utilitários Auxiliares

### Validação e Sanitização

`src/lib/validation.ts`:

```typescript
import { z } from "zod";
import DOMPurify from "isomorphic-dompurify";

// Schemas reutilizáveis
export const urlSchema = z
  .string()
  .url()
  .transform(url => {
    // Normaliza URLs
    try {
      const urlObj = new URL(url);
      return urlObj.href;
    } catch {
      return url;
    }
  });

export const sanitizeHtml = (html: string): string => {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ["b", "i", "em", "strong", "a", "p", "br"],
    ALLOWED_ATTR: ["href", "target", "rel"],
  });
};

// Rate limiting simples
const rateLimitMap = new Map<string, { count: number; resetTime: number }>();

export const checkRateLimit = (
  userId: string,
  limit: number = 60,
  windowMs: number = 60000
): boolean => {
  const now = Date.now();
  const userLimit = rateLimitMap.get(userId);

  if (!userLimit || now > userLimit.resetTime) {
    rateLimitMap.set(userId, {
      count: 1,
      resetTime: now + windowMs,
    });
    return true;
  }

  if (userLimit.count >= limit) {
    return false;
  }

  userLimit.count++;
  return true;
};
```

### Extração de Metadados

`src/lib/metadata-extractor.ts`:

```typescript
import { JSDOM } from "jsdom";

interface URLMetadata {
  title?: string;
  description?: string;
  favicon?: string;
  image?: string;
}

export async function extractURLMetadata(
  url: string
): Promise<URLMetadata | null> {
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);

    const response = await fetch(url, {
      signal: controller.signal,
      headers: {
        "User-Agent": "Mozilla/5.0 (compatible; BookmarkBot/1.0)",
      },
    });

    clearTimeout(timeout);

    if (!response.ok) {
      return null;
    }

    const html = await response.text();
    const dom = new JSDOM(html);
    const doc = dom.window.document;

    // Extrair metadados
    const metadata: URLMetadata = {};

    // Título
    metadata.title =
      doc.querySelector('meta[property="og:title"]')?.getAttribute("content") ||
      doc
        .querySelector('meta[name="twitter:title"]')
        ?.getAttribute("content") ||
      doc.querySelector("title")?.textContent ||
      undefined;

    // Descrição
    metadata.description =
      doc
        .querySelector('meta[property="og:description"]')
        ?.getAttribute("content") ||
      doc.querySelector('meta[name="description"]')?.getAttribute("content") ||
      undefined;

    // Favicon
    const favicon =
      doc.querySelector('link[rel="icon"]')?.getAttribute("href") ||
      doc.querySelector('link[rel="shortcut icon"]')?.getAttribute("href") ||
      "/favicon.ico";

    metadata.favicon = new URL(favicon, url).href;

    // Imagem
    metadata.image =
      doc.querySelector('meta[property="og:image"]')?.getAttribute("content") ||
      doc
        .querySelector('meta[name="twitter:image"]')
        ?.getAttribute("content") ||
      undefined;

    return metadata;
  } catch (error) {
    console.error("Failed to extract metadata:", error);
    return null;
  }
}
```

## 🔄 Webhooks

### Webhook do Clerk

`src/app/api/webhooks/clerk/route.ts`:

```typescript
import { Webhook } from "svix";
import { headers } from "next/headers";
import { WebhookEvent } from "@clerk/nextjs/server";
import { prisma } from "@/lib/prisma";

// Desabilita bodyParser para webhooks
export const runtime = "edge";

export async function POST(req: Request) {
  // Obtém o webhook secret
  const WEBHOOK_SECRET = process.env.CLERK_WEBHOOK_SECRET;

  if (!WEBHOOK_SECRET) {
    console.error("Missing CLERK_WEBHOOK_SECRET");
    return new Response("Server configuration error", { status: 500 });
  }

  // Obtém headers
  const headerPayload = await headers();
  const svix_id = headerPayload.get("svix-id");
  const svix_timestamp = headerPayload.get("svix-timestamp");
  const svix_signature = headerPayload.get("svix-signature");

  // Valida presença dos headers
  if (!svix_id || !svix_timestamp || !svix_signature) {
    return new Response("Missing svix headers", { status: 400 });
  }

  // Obtém o body
  const payload = await req.json();
  const body = JSON.stringify(payload);

  // Cria instância do verificador
  const wh = new Webhook(WEBHOOK_SECRET);
  let evt: WebhookEvent;

  // Verifica a assinatura
  try {
    evt = wh.verify(body, {
      "svix-id": svix_id,
      "svix-timestamp": svix_timestamp,
      "svix-signature": svix_signature,
    }) as WebhookEvent;
  } catch (err) {
    console.error("Webhook signature verification failed:", err);
    return new Response("Invalid signature", { status: 400 });
  }

  // Processa o evento
  const eventType = evt.type;
  console.log(`Webhook received: ${eventType}`);

  try {
    switch (eventType) {
      case "user.created":
        await handleUserCreated(evt.data);
        break;

      case "user.updated":
        await handleUserUpdated(evt.data);
        break;

      case "user.deleted":
        await handleUserDeleted(evt.data);
        break;

      case "session.created":
        console.log("New session created:", evt.data.id);
        break;

      default:
        console.log(`Unhandled webhook event: ${eventType}`);
    }

    return new Response("Webhook processed", { status: 200 });
  } catch (error) {
    console.error("Error processing webhook:", error);
    return new Response("Processing error", { status: 500 });
  }
}

// Handlers para eventos específicos
async function handleUserCreated(user: any) {
  console.log("Creating user records for:", user.id);

  // Exemplo: criar registro de configurações do usuário
  await prisma.userSettings.create({
    data: {
      userId: user.id,
      emailNotifications: true,
      theme: "light",
    },
  });
}

async function handleUserUpdated(user: any) {
  console.log("Updating user:", user.id);
  // Atualizar dados locais se necessário
}

async function handleUserDeleted(user: any) {
  console.log("Deleting user data for:", user.id);

  // Deletar todos os dados do usuário
  await prisma.$transaction([
    prisma.bookmark.deleteMany({ where: { userId: user.id } }),
    prisma.userSettings.deleteMany({ where: { userId: user.id } }),
  ]);
}
```

## 🏥 Health Check e Status

`src/app/api/health/route.ts`:

```typescript
import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

export async function GET() {
  const startTime = Date.now();

  try {
    // Verifica conexão com banco de dados
    await prisma.$queryRaw`SELECT 1`;

    // Verifica variáveis de ambiente críticas
    const requiredEnvVars = [
      "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY",
      "CLERK_SECRET_KEY",
      "DATABASE_URL",
    ];

    const missingEnvVars = requiredEnvVars.filter(
      varName => !process.env[varName]
    );

    if (missingEnvVars.length > 0) {
      return NextResponse.json(
        {
          status: "unhealthy",
          message: "Missing required environment variables",
          details: {
            missing: missingEnvVars,
          },
          timestamp: new Date().toISOString(),
          responseTime: Date.now() - startTime,
        },
        { status: 503 }
      );
    }

    return NextResponse.json({
      status: "healthy",
      message: "All systems operational",
      version: process.env.npm_package_version || "1.0.0",
      environment: process.env.NODE_ENV,
      timestamp: new Date().toISOString(),
      responseTime: Date.now() - startTime,
      checks: {
        database: "connected",
        auth: "configured",
      },
    });
  } catch (error) {
    console.error("Health check failed:", error);

    return NextResponse.json(
      {
        status: "unhealthy",
        message: "Health check failed",
        error: error instanceof Error ? error.message : "Unknown error",
        timestamp: new Date().toISOString(),
        responseTime: Date.now() - startTime,
      },
      { status: 503 }
    );
  }
}
```

## 📊 Exemplo de Resposta da API

### Sucesso

```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "url": "https://example.com",
    "title": "Example Site",
    "notes": "Great resource",
    "userId": "user_2NNEqL2nrIRdJ07",
    "createdAt": "2024-01-15T10:30:00Z",
    "updatedAt": "2024-01-15T10:30:00Z"
  },
  "message": "Bookmark created successfully"
}
```

### Erro

```json
{
  "error": "Bad Request",
  "message": "Invalid bookmark data",
  "code": "VALIDATION_ERROR",
  "details": {
    "fieldErrors": {
      "url": ["Invalid URL format"],
      "title": ["Title is required"]
    }
  }
}
```

### Lista com Paginação

```json
{
  "success": true,
  "data": [
    {
      "id": "...",
      "url": "...",
      "title": "..."
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "totalPages": 8,
    "hasNext": true,
    "hasPrev": false
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "1.0.0"
  }
}
```

## 🛡️ Segurança e Boas Práticas

1. **Sempre valide entrada**: Use Zod para validação
2. **Rate limiting**: Implemente limites por usuário
3. **Sanitize dados**: Especialmente HTML e URLs
4. **Log apropriado**: Log erros mas não dados sensíveis
5. **Timeouts**: Configure timeouts para operações externas
6. **CORS**: Configure apenas para domínios necessários
7. **Headers de segurança**: Use CSP, X-Frame-Options, etc.

---

Com esta API robusta, você tem endpoints seguros e bem estruturados para seu aplicativo!
