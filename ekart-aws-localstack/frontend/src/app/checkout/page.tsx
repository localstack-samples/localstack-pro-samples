'use client'

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { ArrowLeft } from 'lucide-react';
import { API_URL } from '@/lib/config';

interface CartItem {
  product_id: string;
  quantity: number;
  added_at: string;
}

interface Cart {
  user_id: string;
  items: CartItem[];
}

interface Product {
  product_id: string;
  title: string;
  price: number;
  image_url?: string;
}

export default function CheckoutPage() {
  const [cart, setCart] = useState<Cart | null>(null);
  const [products, setProducts] = useState<Map<string, Product>>(new Map());
  const [loading, setLoading] = useState(true);
  const [totalAmount, setTotalAmount] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [processing, setProcessing] = useState(false);
  const router = useRouter();

  useEffect(() => {
    initializeCheckout();
  }, []);

  const initializeCheckout = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/auth/login');
        return;
      }

      // Fetch cart
      const cartResponse = await fetch(`${API_URL}/api/cart`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!cartResponse.ok) {
        throw new Error('Failed to fetch cart');
      }

      const cartData = await cartResponse.json();
      setCart(cartData);

      if (!cartData.items || cartData.items.length === 0) {
        router.push('/cart');
        return;
      }

      // Use backend-provided total to avoid mismatches
      const backendTotal = Number((cartData as any).total_amount) || 0;
      setTotalAmount(backendTotal);

      // Build quantity map by product_id for names
      const qtyById: Record<string, number> = {};
      (cartData.items as CartItem[]).forEach((ci) => {
        qtyById[ci.product_id] = Number(ci.quantity) || 0;
      });

      // Fetch product details for all items
      const productPromises = Object.keys(qtyById).map((pid) =>
        fetch(`${API_URL}/api/products/${pid}`).then(res => res.json())
      );

      const productsData: Product[] = await Promise.all(productPromises);
      const productsMap = new Map<string, Product>();
      productsData.forEach((product: Product) => {
        productsMap.set(product.product_id, product);
      });

      setProducts(productsMap);
      // totalAmount already set from backend

    } catch (err: any) {
      console.error('Error initializing checkout:', err);
      setError('Failed to initialize checkout. Please try again.');
      router.push('/cart');
    } finally {
      setLoading(false);
    }
  };

  const handlePayNow = async () => {
    try {
      setProcessing(true);
      setError(null);

      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/auth/login');
        return;
      }

      // Create payment via backend (LocalStack Stripe handled server-side)
      const amountCents = Math.round(totalAmount * 100);
      const response = await fetch(`${API_URL}/api/payments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ amount: amountCents, currency: 'usd' })
      });

      if (!response.ok) {
        const t = await response.text();
        throw new Error(t || 'Payment failed');
      }

      // Optionally consume response
      await response.json();

      // Navigate to success
      router.push('/checkout/success');
    } catch (e: any) {
      setError(e?.message || 'Payment failed');
    } finally {
      setProcessing(false);
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading checkout...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <h1 className="text-3xl font-bold mb-8">Checkout</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Order Summary */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow p-6 sticky top-8">
              <h2 className="text-xl font-bold mb-4">Order Summary</h2>
              {error && (
                <div className="mt-2 p-3 bg-red-50 border border-red-200 rounded text-red-600 text-sm">
                  {error}
                </div>
              )}
              <div className="space-y-3 mb-4">
                {cart?.items.map((item) => {
                  const product = products.get(item.product_id);
                  if (!product) return null;

                  return (
                    <div key={item.product_id} className="flex justify-between text-sm">
                      <div className="flex-1">
                        <p className="font-medium truncate">{product.title}</p>
                        <p className="text-gray-500">Qty: {item.quantity}</p>
                      </div>
                      <p className="font-semibold ml-4">
                        ${(product.price * item.quantity).toFixed(2)}
                      </p>
                    </div>
                  );
                })}
              </div>

              <div className="border-t pt-4 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Subtotal:</span>
                  <span>${totalAmount.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Shipping:</span>
                  <span>Free</span>
                </div>
                <div className="flex justify-between text-lg font-bold border-t pt-2">
                  <span>Total:</span>
                  <span className="text-blue-600">${totalAmount.toFixed(2)}</span>
                </div>
              </div>

              <div className="mt-6 flex gap-4">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => router.back()}
                  disabled={processing}
                  className="flex-1"
                >
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Back to Cart
                </Button>
                <Button
                  type="button"
                  onClick={handlePayNow}
                  disabled={processing}
                  className="flex-1"
                >
                  {processing ? 'Processing...' : 'Pay Now'}
                </Button>
              </div>
            </div>
          </div>

          {/* Placeholder for payment form area (no Stripe Elements with LocalStack) */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-bold mb-4">Payment</h2>
              <p className="text-gray-600">Your payment will be processed via the test gateway.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
