# Configuração Inicial do Projeto

## 📋 Arquivos de Configuração Completos

### 1. `package.json`

```json
{
  "name": "bookmark-manager",
  "version": "0.1.0",
  "private": true,
  "description": "Gerenciador de bookmarks com servidor MCP integrado",
  "author": "Seu Nome",
  "license": "MIT",
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit",
    "format": "prettier --write \"src/**/*.{ts,tsx,js,jsx,json,css,md}\"",
    "prisma:generate": "prisma generate",
    "prisma:migrate": "prisma migrate dev",
    "prisma:migrate:prod": "prisma migrate deploy",
    "prisma:studio": "prisma studio",
    "prisma:seed": "ts-node prisma/seed.ts",
    "postinstall": "prisma generate"
  },
  "dependencies": {
    "@clerk/mcp-tools": "^0.0.3",
    "@clerk/nextjs": "^6.13.0",
    "@prisma/client": "^6.2.0",
    "@vercel/mcp-adapter": "^0.1.1",
    "next": "15.1.0",
    "react": "19.0.0",
    "react-dom": "19.0.0",
    "zod": "^3.24.1"
  },
  "devDependencies": {
    "@types/node": "^22.10.0",
    "@types/react": "^19.0.1",
    "@types/react-dom": "^19.0.1",
    "@typescript-eslint/eslint-plugin": "^8.0.0",
    "@typescript-eslint/parser": "^8.0.0",
    "eslint": "^9.0.0",
    "eslint-config-next": "15.1.0",
    "eslint-config-prettier": "^9.1.0",
    "prettier": "^3.4.1",
    "prisma": "^6.2.0",
    "ts-node": "^10.9.2",
    "typescript": "^5.7.2"
  },
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  }
}
```

### 2. `tsconfig.json`

```json
{
  "compilerOptions": {
    // Versão do JavaScript alvo
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],

    // Configurações de módulo
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "allowJs": true,

    // Configurações de tipo
    "strict": true,
    "noEmit": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "esModuleInterop": true,
    "isolatedModules": true,

    // JSX
    "jsx": "preserve",

    // Caminhos e aliases
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/lib/*": ["./src/lib/*"],
      "@/hooks/*": ["./src/hooks/*"],
      "@/types/*": ["./src/types/*"]
    },

    // Next.js
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],

    // Opções adicionais de tipo
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "allowUnusedLabels": false,
    "allowUnreachableCode": false
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules", ".next", "out", "build", "dist"],
  "ts-node": {
    "compilerOptions": {
      "module": "commonjs"
    }
  }
}
```

### 3. `next.config.js`

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Modo estrito do React para detectar problemas
  reactStrictMode: true,

  // Otimizações de produção
  poweredByHeader: false,
  compress: true,

  // Configuração de imagens (se usar next/image)
  images: {
    domains: [
      // Adicione domínios de imagens externas aqui
    ],
    formats: ["image/avif", "image/webp"],
  },

  // Headers de segurança
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          {
            key: "X-DNS-Prefetch-Control",
            value: "on",
          },
          {
            key: "X-XSS-Protection",
            value: "1; mode=block",
          },
          {
            key: "X-Frame-Options",
            value: "SAMEORIGIN",
          },
          {
            key: "X-Content-Type-Options",
            value: "nosniff",
          },
          {
            key: "Referrer-Policy",
            value: "origin-when-cross-origin",
          },
        ],
      },
    ];
  },

  // Redirecionamentos (se necessário)
  async redirects() {
    return [
      // Exemplo:
      // {
      //   source: '/old-route',
      //   destination: '/new-route',
      //   permanent: true,
      // }
    ];
  },

  // Configurações experimentais
  experimental: {
    // serverActions: true, // Já habilitado por padrão no Next.js 15
    // typedRoutes: true, // Rotas tipadas (experimental)
  },

  // Configuração do Webpack (se necessário)
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Modificações customizadas do webpack
    return config;
  },
};

module.exports = nextConfig;
```

### 4. `.env.example`

```bash
# ===================================
# CLERK - Autenticação
# ===================================
# Obtenha essas chaves em: https://dashboard.clerk.com
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
CLERK_SECRET_KEY=sk_test_your_secret_key_here

# URLs do Clerk (opcionais - defaults são usados se não especificados)
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/

# ===================================
# BANCO DE DADOS
# ===================================
# SQLite para desenvolvimento (arquivo local)
DATABASE_URL="file:./dev.db"

# Para produção com PostgreSQL:
# DATABASE_URL="postgresql://user:password@localhost:5432/bookmark_manager?schema=public"

# ===================================
# APLICAÇÃO
# ===================================
# URL base da aplicação (importante para OAuth callbacks)
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Ambiente (development, production)
NODE_ENV=development

# ===================================
# MCP SERVER (opcional)
# ===================================
# Configurações específicas do MCP se necessário
MCP_SERVER_NAME="Bookmark Manager MCP"
MCP_SERVER_VERSION="1.0.0"
```

### 5. `.gitignore`

```gitignore
# Dependências
/node_modules
/.pnp
.pnp.js

# Testing
/coverage
/.nyc_output

# Next.js
/.next/
/out/

# Produção
/build
/dist

# Diversos
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Variáveis de ambiente locais
.env
.env*.local
.env.development
.env.production

# Vercel
.vercel

# TypeScript
*.tsbuildinfo
next-env.d.ts

# Prisma
prisma/dev.db
prisma/dev.db-journal
prisma/migrations/dev/

# IDEs
.vscode/*
!.vscode/extensions.json
!.vscode/settings.json.example
.idea
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
logs
*.log

# Temporários
tmp/
temp/
```

### 6. `.eslintrc.json`

```json
{
  "extends": [
    "next/core-web-vitals",
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "root": true,
  "env": {
    "node": true,
    "browser": true,
    "es2021": true
  },
  "rules": {
    // TypeScript
    "@typescript-eslint/no-unused-vars": [
      "error",
      {
        "argsIgnorePattern": "^_",
        "varsIgnorePattern": "^_"
      }
    ],
    "@typescript-eslint/no-explicit-any": "warn",
    "@typescript-eslint/explicit-module-boundary-types": "off",
    "@typescript-eslint/no-non-null-assertion": "warn",

    // React
    "react/react-in-jsx-scope": "off",
    "react/prop-types": "off",

    // Geral
    "no-console": ["warn", { "allow": ["warn", "error"] }],
    "prefer-const": "error",
    "no-duplicate-imports": "error"
  },
  "ignorePatterns": [
    "node_modules",
    ".next",
    "out",
    "public",
    "prisma/migrations"
  ]
}
```

### 7. `.prettierrc.json`

```json
{
  "semi": false,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "bracketSpacing": true,
  "arrowParens": "always",
  "endOfLine": "lf",
  "jsxSingleQuote": false,
  "proseWrap": "preserve",
  "quoteProps": "as-needed",
  "htmlWhitespaceSensitivity": "css",
  "embeddedLanguageFormatting": "auto"
}
```

### 8. `.prettierignore`

```
# Ignorar arquivos gerados
.next
out
build
dist
coverage

# Dependências
node_modules

# Prisma
prisma/migrations

# Outros
*.min.js
*.min.css
```

### 9. `next-env.d.ts` (gerado automaticamente)

```typescript
/// <reference types="next" />
/// <reference types="next/image-types/global" />

// NOTE: This file should not be edited
// see https://nextjs.org/docs/app/building-your-application/configuring/typescript for more information.
```

### 10. `.vscode/settings.json.example` (opcional)

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true,
  "files.associations": {
    "*.css": "tailwindcss"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

## 🚀 Comandos de Inicialização

Após criar todos os arquivos de configuração:

```bash
# 1. Instalar dependências
npm install

# 2. Copiar arquivo de ambiente
cp .env.example .env

# 3. Configurar as variáveis no .env com suas chaves

# 4. Gerar cliente Prisma
npm run prisma:generate

# 5. Criar banco de dados e aplicar migrações
npm run prisma:migrate

# 6. (Opcional) Abrir Prisma Studio
npm run prisma:studio

# 7. Iniciar servidor de desenvolvimento
npm run dev
```

## ⚡ Scripts Úteis Explicados

- **`dev`**: Inicia o servidor de desenvolvimento com Turbopack (mais rápido)
- **`build`**: Cria build otimizado para produção
- **`start`**: Inicia servidor de produção (requer build)
- **`lint`**: Verifica problemas de código com ESLint
- **`type-check`**: Verifica tipos TypeScript sem compilar
- **`format`**: Formata código com Prettier
- **`prisma:generate`**: Gera cliente TypeScript do Prisma
- **`prisma:migrate`**: Cria/aplica migrações de desenvolvimento
- **`prisma:studio`**: Interface visual para o banco de dados
- **`postinstall`**: Roda automaticamente após npm install

## 📝 Notas de Configuração

1. **TypeScript Strict**: Configurado com todas as verificações stritas habilitadas
2. **Path Aliases**: Use `@/` para importações absolutas
3. **Prettier + ESLint**: Configurados para trabalhar juntos
4. **Headers de Segurança**: Já configurados no `next.config.js`
5. **Turbopack**: Habilitado no script dev para builds mais rápidos

---

Com essas configurações, o projeto está pronto para desenvolvimento com as melhores práticas e ferramentas modernas!
