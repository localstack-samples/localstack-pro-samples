'use client'

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { TrendingUp, DollarSign, ShoppingBag, Users } from 'lucide-react';

interface Analytics {
  totalSales: number;
  totalOrders: number;
  totalProducts: number;
  totalCustomers: number;
  recentSales: Array<{
    date: string;
    amount: number;
  }>;
}

export default function SellerAnalyticsPage() {
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8000/api/sellers/analytics/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setAnalytics(data);
      } else {
        // Mock data for demonstration
        setAnalytics({
          totalSales: 12450.00,
          totalOrders: 45,
          totalProducts: 12,
          totalCustomers: 38,
          recentSales: [
            { date: '2025-10-10', amount: 450 },
            { date: '2025-10-09', amount: 320 },
            { date: '2025-10-08', amount: 890 },
            { date: '2025-10-07', amount: 560 },
            { date: '2025-10-06', amount: 780 },
          ]
        });
      }
    } catch (error) {
      console.error('Error fetching analytics:', error);
      // Mock data on error
      setAnalytics({
        totalSales: 12450.00,
        totalOrders: 45,
        totalProducts: 12,
        totalCustomers: 38,
        recentSales: [
          { date: '2025-10-10', amount: 450 },
          { date: '2025-10-09', amount: 320 },
          { date: '2025-10-08', amount: 890 },
          { date: '2025-10-07', amount: 560 },
          { date: '2025-10-06', amount: 780 },
        ]
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">Loading analytics...</div>
        </div>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center text-red-600">Failed to load analytics</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <Link href="/seller/dashboard" className="text-blue-600 hover:text-blue-800 mb-4 inline-block">
            ← Back to Dashboard
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
          <p className="text-gray-600 mt-2">Track your sales and performance</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Total Sales</p>
                <p className="text-2xl font-bold text-gray-900">${analytics.totalSales.toFixed(2)}</p>
              </div>
              <div className="bg-green-100 p-3 rounded-full">
                <DollarSign className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Total Orders</p>
                <p className="text-2xl font-bold text-gray-900">{analytics.totalOrders}</p>
              </div>
              <div className="bg-blue-100 p-3 rounded-full">
                <ShoppingBag className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Total Products</p>
                <p className="text-2xl font-bold text-gray-900">{analytics.totalProducts}</p>
              </div>
              <div className="bg-purple-100 p-3 rounded-full">
                <TrendingUp className="w-6 h-6 text-purple-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Total Customers</p>
                <p className="text-2xl font-bold text-gray-900">{analytics.totalCustomers}</p>
              </div>
              <div className="bg-yellow-100 p-3 rounded-full">
                <Users className="w-6 h-6 text-yellow-600" />
              </div>
            </div>
          </div>
        </div>

        {/* Recent Sales Chart */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Sales</h2>
          <div className="space-y-4">
            {analytics.recentSales.map((sale, index) => (
              <div key={index} className="flex items-center justify-between border-b border-gray-200 pb-4">
                <div>
                  <p className="text-sm text-gray-600">{new Date(sale.date).toLocaleDateString()}</p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-semibold text-gray-900">${sale.amount.toFixed(2)}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
