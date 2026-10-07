'use client'

import Link from 'next/link';
import { ShoppingCart, User, Search, LogOut } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Header() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  const [userType, setUserType] = useState('');
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const email = localStorage.getItem('user_email');
    const type = localStorage.getItem('user_type');
    
    setIsLoggedIn(!!token);
    setUserEmail(email || '');
    setUserType(type || '');
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_email');
    localStorage.removeItem('user_type');
    setIsLoggedIn(false);
    router.push('/');
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-gray-200 bg-white shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="text-2xl font-bold text-blue-600">EKart</div>
          </Link>

          {/* Search Bar */}
          <div className="flex-1 max-w-xl mx-8">
            <div className="relative">
              <input
                type="text"
                placeholder="Search for products..."
                className="w-full h-10 pl-10 pr-4 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex items-center space-x-4">
            <Link href="/products">
              <Button variant="ghost">Products</Button>
            </Link>
            <Link href="/cart">
              <Button variant="ghost" className="relative">
                <ShoppingCart className="w-5 h-5" />
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  0
                </span>
              </Button>
            </Link>
            
            {isLoggedIn ? (
              <>
                {userType === 'seller' && (
                  <Link href="/seller/dashboard">
                    <Button variant="ghost">Dashboard</Button>
                  </Link>
                )}
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-600">{userEmail}</span>
                  <Button variant="ghost" onClick={handleLogout}>
                    <LogOut className="w-5 h-5" />
                  </Button>
                </div>
              </>
            ) : (
              <>
                <Link href="/auth/login">
                  <Button variant="ghost">
                    <User className="w-5 h-5 mr-2" />
                    Login
                  </Button>
                </Link>
                <Link href="/auth/register">
                  <Button variant="primary">Sign Up</Button>
                </Link>
              </>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
}
