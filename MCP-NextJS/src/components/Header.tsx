'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import {
  SignInButton,
  SignUpButton,
  SignedIn,
  SignedOut,
  UserButton,
  useUser,
} from '@clerk/nextjs'
import { BookmarkIcon, Cog6ToothIcon } from '@heroicons/react/24/outline'
import { Button } from '@/components/ui/Button'

export function Header() {
  const pathname = usePathname()
  const { user } = useUser()

  const navigation = [
    { name: 'Home', href: '/' },
    { name: 'Categorias', href: '/categories' },
    { name: 'Configurações', href: '/settings', icon: Cog6ToothIcon },
  ]

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <BookmarkIcon className="w-8 h-8 text-blue-600" />
            <span className="text-xl font-bold text-gray-900">Bookmark Manager</span>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center gap-6">
            <SignedIn>
              {navigation.map(item => {
                const isActive = pathname === item.href
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={`
                      flex items-center gap-1 px-3 py-2 text-sm font-medium rounded-md
                      transition-colors duration-200
                      ${
                        isActive
                          ? 'text-blue-600 bg-blue-50'
                          : 'text-gray-700 hover:text-gray-900 hover:bg-gray-50'
                      }
                    `}
                  >
                    {item.icon && <item.icon className="w-4 h-4" />}
                    {item.name}
                  </Link>
                )
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
                Olá, {user?.firstName || 'Usuário'}
              </span>

              <UserButton
                afterSignOutUrl="/"
                appearance={{
                  elements: {
                    avatarBox: 'w-10 h-10 border-2 border-gray-200',
                  },
                }}
              />
            </SignedIn>
          </div>
        </div>
      </div>
    </header>
  )
}
