'use client'

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { API_URL } from '@/lib/config';

interface OrderItem {
  product_id: string;
  product_name?: string;
  price: number;
  quantity: number;
}

interface Order {
  order_id: string;
  buyer_id: string;
  seller_id?: string;
  items: OrderItem[];
  total_amount: number;
  status: string;
  payment_method?: string;
  payment_status?: string;
  created_at?: string;
}

export default function OrdersPage() {
  const router = useRouter();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          router.push('/auth/login');
          return;
        }
        const res = await fetch(`${API_URL}/api/orders`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error('Failed to load orders');
        const data = await res.json();
        setOrders(Array.isArray(data) ? data : []);
      } catch (e: any) {
        setError(e?.message || 'Failed to load orders');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">Loading your orders...</div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded">{error}</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Your Orders</h1>
      {orders.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-8 text-center">
          <p className="text-gray-600 mb-4">You have no orders yet.</p>
          <button
            onClick={() => router.push('/products')}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Browse Products
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          {orders.map((order) => {
            const total = Number((order as any).total_amount) || 0;
            return (
              <div key={order.order_id} className="bg-white rounded-lg shadow p-6">
                <div className="flex items-start justify-between flex-wrap gap-4 mb-4">
                  <div>
                    <p className="text-sm text-gray-500">Order ID</p>
                    <p className="font-mono text-sm">{order.order_id}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Placed</p>
                    <p>{order.created_at ? new Date(order.created_at).toLocaleString() : '-'}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Status</p>
                    <span className="inline-block px-2 py-1 rounded text-sm bg-gray-100 text-gray-700">{order.status}</span>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Total</p>
                    <p className="text-lg font-semibold text-blue-600">${total.toFixed(2)}</p>
                  </div>
                </div>

                <div className="border-t pt-4">
                  <h3 className="text-lg font-semibold mb-3">Items</h3>
                  <div className="divide-y">
                    {order.items.map((it, idx) => {
                      const unit = Number((it as any).price) || 0;
                      const qty = Number(it.quantity || 0);
                      return (
                        <div key={`${it.product_id}-${idx}`} className="py-3 flex items-center justify-between">
                          <div className="flex-1 pr-4">
                            <p className="font-medium">{it.product_name || `Product ${it.product_id.substring(0,8)}...`}</p>
                            <p className="text-sm text-gray-500">Qty: {qty}</p>
                          </div>
                          <div className="text-right">
                            <p className="text-sm text-gray-600">${unit.toFixed(2)} each</p>
                            <p className="font-semibold">${(unit * qty).toFixed(2)}</p>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}


