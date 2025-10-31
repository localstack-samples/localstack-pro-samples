'use client'

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { CheckCircle } from 'lucide-react';

export default function CheckoutSuccessPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [paymentIntentId, setPaymentIntentId] = useState<string | null>(null);

  useEffect(() => {
    const payment_intent = searchParams.get('payment_intent');
    if (payment_intent) {
      setPaymentIntentId(payment_intent);
      
      // Clear cart after successful payment
      clearCart();
    }
  }, [searchParams]);

  const clearCart = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) return;

      // You can implement a clear cart endpoint or handle this in the backend
      // For now, we'll just let the user navigate
    } catch (error) {
      console.error('Error clearing cart:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
        <div className="mb-6">
          <CheckCircle className="w-20 h-20 text-green-500 mx-auto" />
        </div>
        
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Payment Successful!
        </h1>
        
        <p className="text-gray-600 mb-2">
          Thank you for your purchase.
        </p>
        
        {paymentIntentId && (
          <p className="text-sm text-gray-500 mb-6">
            Payment ID: {paymentIntentId}
          </p>
        )}
        
        <p className="text-gray-600 mb-8">
          Your order has been confirmed and will be processed shortly.
          You will receive an email confirmation with your order details.
        </p>

        <div className="space-y-3">
          <Button 
            onClick={() => router.push('/products')} 
            className="w-full"
          >
            Continue Shopping
          </Button>
          
          <Button 
            onClick={() => router.push('/orders')} 
            variant="outline"
            className="w-full"
          >
            View Orders
          </Button>
        </div>
      </div>
    </div>
  );
}
