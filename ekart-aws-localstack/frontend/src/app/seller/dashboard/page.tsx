'use client'

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Package, DollarSign, ShoppingCart, TrendingUp, Plus } from 'lucide-react';

interface SellerStats {
  totalProducts: number;
  totalOrders: number;
  totalRevenue: number;
  pendingOrders: number;
}

interface Product {
  product_id: string;
  title: string;
  price: number;
  stock_quantity?: number;
  stock?: number;
  is_active: boolean;
}

export default function SellerDashboard() {
  const router = useRouter();
  const [stats, setStats] = useState<SellerStats>({
    totalProducts: 0,
    totalOrders: 0,
    totalRevenue: 0,
    pendingOrders: 0
  });
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in and is a seller
    const userType = localStorage.getItem('user_type');
    if (userType !== 'seller') {
      router.push('/auth/login');
      return;
    }

    fetchSellerData();
  }, [router]);

  const fetchSellerData = async () => {
    try {
      // Fetch seller's products
      const response = await fetch('http://localhost:8000/api/products/');
      if (response.ok) {
        const allProducts = await response.json();
        setProducts(allProducts.slice(0, 5)); // Show first 5 products
        
        // Calculate stats
        setStats({
          totalProducts: allProducts.length,
          totalOrders: 0, // TODO: Fetch from orders API
          totalRevenue: 0, // TODO: Calculate from orders
          pendingOrders: 0 // TODO: Fetch from orders API
        });
      }
    } catch (error) {
      console.error('Error fetching seller data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_email');
    localStorage.removeItem('user_type');
    router.push('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Seller Dashboard</h1>
              <p className="text-sm text-gray-600">Manage your products and orders</p>
            </div>
            <div className="flex gap-4">
              <Link href="/">
                <Button variant="outline">View Store</Button>
              </Link>
              <Button variant="outline" onClick={handleLogout}>
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Products</p>
                  <p className="text-3xl font-bold text-gray-900">{stats.totalProducts}</p>
                </div>
                <div className="p-3 bg-blue-100 rounded-full">
                  <Package className="w-6 h-6 text-blue-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Orders</p>
                  <p className="text-3xl font-bold text-gray-900">{stats.totalOrders}</p>
                </div>
                <div className="p-3 bg-green-100 rounded-full">
                  <ShoppingCart className="w-6 h-6 text-green-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Revenue</p>
                  <p className="text-3xl font-bold text-gray-900">${stats.totalRevenue.toFixed(2)}</p>
                </div>
                <div className="p-3 bg-purple-100 rounded-full">
                  <DollarSign className="w-6 h-6 text-purple-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Pending Orders</p>
                  <p className="text-3xl font-bold text-gray-900">{stats.pendingOrders}</p>
                </div>
                <div className="p-3 bg-yellow-100 rounded-full">
                  <TrendingUp className="w-6 h-6 text-yellow-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className="flex flex-wrap gap-4">
            <Link href="/seller/products/new">
              <Button className="flex items-center gap-2">
                <Plus className="w-4 h-4" />
                Add New Product
              </Button>
            </Link>
            <Link href="/seller/products">
              <Button variant="outline">Manage Products</Button>
            </Link>
            <Link href="/seller/orders">
              <Button variant="outline">View Orders</Button>
            </Link>
            <Link href="/seller/analytics">
              <Button variant="outline">View Analytics</Button>
            </Link>
          </div>
        </div>

        {/* Recent Products */}
        <Card>
          <CardHeader>
            <div className="flex justify-between items-center">
              <CardTitle>Recent Products</CardTitle>
              <Link href="/seller/products">
                <Button variant="ghost" size="sm">View All</Button>
              </Link>
            </div>
          </CardHeader>
          <CardContent>
            {products.length === 0 ? (
              <div className="text-center py-12">
                <Package className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No products yet</h3>
                <p className="text-gray-600 mb-4">Start selling by adding your first product</p>
                <Link href="/seller/products/new">
                  <Button>Add Product</Button>
                </Link>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Product
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Price
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Stock
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Status
                      </th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Actions
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {products.map((product) => (
                      <tr key={product.product_id}>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900">{product.title}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900">
                            ${typeof product.price === 'number' ? product.price.toFixed(2) : '0.00'}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900">
                            {product.stock_quantity || product.stock || 0}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                            product.is_active 
                              ? 'bg-green-100 text-green-800' 
                              : 'bg-red-100 text-red-800'
                          }`}>
                            {product.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                          <Link href={`/seller/products/${product.product_id}/edit`}>
                            <Button variant="ghost" size="sm">Edit</Button>
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
