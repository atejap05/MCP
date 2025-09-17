import { PrismaClient } from '@prisma/client'

// Função para criar instância do Prisma
const prismaClientSingleton = () => {
  return new PrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
  })
}

// Type helper
type PrismaClientSingleton = ReturnType<typeof prismaClientSingleton>

// Globalização para evitar múltiplas instâncias em desenvolvimento
const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClientSingleton | undefined
}

// Exporta instância única
export const prisma = globalForPrisma.prisma ?? prismaClientSingleton()

// Em desenvolvimento, preserva a instância
if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma
}

// Tipos úteis exportados
export type { Bookmark, Category } from '@prisma/client'
