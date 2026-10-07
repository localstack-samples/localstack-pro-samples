'use client'

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { Button } from '@/components/ui/Button';

interface Product {
  product_id: string;
  title: string;
  description?: string;
  price: number;
  category?: string;
  subcategory?: string;
  brand?: string;
  images?: { url: string; alt_text?: string }[];
}

export default function ProductDetailPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetch(`${API}/api/products/${params.id}`);
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        setProduct(data);
      } catch (e) {
        router.push('/products');
      } finally {
        setLoading(false);
      }
    };
    if (params?.id) load();
  }, [params?.id]);

  if (loading) return <div className="container mx-auto px-4 py-8">Loading...</div>;
  if (!product) return null;

  const price = Number((product as any).price) || 0;
  const img = product.images && product.images[0]?.url;

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white rounded-lg shadow p-6">
          {img ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={img} alt={product.title} className="w-full h-auto rounded" />
          ) : (
            <div className="w-full h-64 bg-gray-100 rounded" />
          )}
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h1 className="text-2xl font-bold mb-2">{product.title}</h1>
          <p className="text-gray-500 mb-4">{product.brand} {product.category ? `• ${product.category}` : ''}</p>
          <p className="text-3xl font-bold text-blue-600 mb-6">${price.toFixed(2)}</p>
          <p className="text-gray-700 leading-relaxed mb-8">{product.description}</p>
          <div className="flex gap-4">
            <Button onClick={() => router.push('/products')}>Back</Button>
          </div>
        </div>
      </div>
    </div>
  );
}
