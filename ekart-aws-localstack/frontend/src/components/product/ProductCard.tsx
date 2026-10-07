'use client'

import { Card, CardContent } from '@/components/ui/Card';
import Link from 'next/link';
import { ShoppingCart } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { useState } from 'react';

interface Product {
  product_id: string;
  title: string;
  description: string;
  price: number;
  currency: string;
  images?: Array<{ url: string; alt_text?: string }>;
  rating?: number;
  review_count: number;
}

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
  const [adding, setAdding] = useState(false);
  const imageUrl = product.images && product.images.length > 0 
    ? product.images[0].url 
    : '/images/placeholder-product.png';

  const handleAddToCart = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    const token = localStorage.getItem('access_token');
    if (!token) {
      alert('Please login to add items to cart');
      window.location.href = '/auth/login';
      return;
    }

    setAdding(true);
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/api/cart/items`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          product_id: product.product_id,
          quantity: 1
        })
      });

      if (response.ok) {
        alert('Added to cart!');
      } else {
        alert('Failed to add to cart');
      }
    } catch (error) {
      console.error('Error adding to cart:', error);
      alert('Failed to add to cart');
    } finally {
      setAdding(false);
    }
  };

  return (
    <Card className="group overflow-hidden transition-shadow hover:shadow-lg">
      <Link href={`/products/${product.product_id}`}>
        <div className="aspect-square overflow-hidden bg-gray-100">
          <img
            src={imageUrl}
            alt={product.title}
            className="h-full w-full object-cover object-center group-hover:scale-105 transition-transform duration-300"
            onError={(e) => {
              e.currentTarget.src = '/images/placeholder-product.png';
            }}
          />
        </div>
      </Link>
      <CardContent className="p-4">
        <Link href={`/products/${product.product_id}`}>
          <h3 className="text-lg font-semibold text-gray-900 hover:text-blue-600 line-clamp-2 mb-2">
            {product.title}
          </h3>
        </Link>
        <p className="text-sm text-gray-600 line-clamp-2 mb-3">{product.description}</p>
        
        <div className="flex items-center justify-between">
          <div>
            <p className="text-2xl font-bold text-gray-900">
              {product.currency === 'USD' ? '$' : product.currency}
              {typeof product.price === 'number' ? product.price.toFixed(2) : '0.00'}
            </p>
            {product.rating && (
              <div className="flex items-center mt-1">
                <span className="text-yellow-500 text-sm">★</span>
                <span className="text-sm text-gray-600 ml-1">
                  {typeof product.rating === 'number' ? product.rating.toFixed(1) : product.rating} ({product.review_count || 0})
                </span>
              </div>
            )}
          </div>
          <Button 
            size="sm" 
            className="flex items-center" 
            onClick={handleAddToCart}
            disabled={adding}
          >
            <ShoppingCart className="w-4 h-4 mr-1" />
            {adding ? 'Adding...' : 'Add'}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
