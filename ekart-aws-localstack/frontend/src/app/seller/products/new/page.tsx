'use client'

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { ArrowLeft } from 'lucide-react';

export default function NewProductPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'Electronics',
    price: '',
    stock_quantity: '',
    brand: '',
    tags: '',
    currency: 'USD'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const categories = [
    'Electronics',
    'Home & Kitchen',
    'Sports & Fitness',
    'Gaming',
    'Fashion',
    'Books',
    'Office',
    'Toys & Games',
    'Health & Beauty',
    'Automotive'
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const token = localStorage.getItem('access_token');
      const userId = localStorage.getItem('user_id');
      
      if (!token || !userId) {
        router.push('/auth/login');
        return;
      }

      const tagsArray = formData.tags.split(',').map(tag => tag.trim()).filter(tag => tag);

      const response = await fetch('http://localhost:8000/api/products/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          title: formData.title,
          description: formData.description,
          category: formData.category,
          price: parseFloat(formData.price),
          stock_quantity: parseInt(formData.stock_quantity),
          brand: formData.brand,
          tags: tagsArray,
          currency: formData.currency
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to create product');
      }

      router.push('/seller/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create product');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-6">
          <Link href="/seller/dashboard">
            <Button variant="ghost" className="flex items-center gap-2">
              <ArrowLeft className="w-4 h-4" />
              Back to Dashboard
            </Button>
          </Link>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">Add New Product</CardTitle>
            <p className="text-sm text-gray-600 mt-1">
              Fill in the details below to list your product
            </p>
          </CardHeader>

          <CardContent>
            {error && (
              <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Basic Information */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900">Basic Information</h3>
                
                <Input
                  label="Product Title"
                  type="text"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  placeholder="e.g., Apple MacBook Pro 16-inch"
                  required
                />

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Description
                  </label>
                  <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                    rows={4}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Describe your product in detail..."
                    required
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Category
                    </label>
                    <select
                      name="category"
                      value={formData.category}
                      onChange={handleChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    >
                      {categories.map(cat => (
                        <option key={cat} value={cat}>{cat}</option>
                      ))}
                    </select>
                  </div>

                  <Input
                    label="Brand"
                    type="text"
                    name="brand"
                    value={formData.brand}
                    onChange={handleChange}
                    placeholder="e.g., Apple, Samsung"
                  />
                </div>
              </div>

              {/* Pricing & Inventory */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900">Pricing & Inventory</h3>
                
                <div className="grid grid-cols-2 gap-4">
                  <Input
                    label="Price"
                    type="number"
                    name="price"
                    value={formData.price}
                    onChange={handleChange}
                    placeholder="0.00"
                    step="0.01"
                    min="0"
                    required
                  />

                  <Input
                    label="Stock Quantity"
                    type="number"
                    name="stock_quantity"
                    value={formData.stock_quantity}
                    onChange={handleChange}
                    placeholder="0"
                    min="0"
                    required
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Currency
                    </label>
                    <select
                      name="currency"
                      value={formData.currency}
                      onChange={handleChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="USD">USD ($)</option>
                      <option value="EUR">EUR (€)</option>
                      <option value="GBP">GBP (£)</option>
                      <option value="INR">INR (₹)</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Additional Details */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900">Additional Details</h3>
                
                <Input
                  label="Tags (comma-separated)"
                  type="text"
                  name="tags"
                  value={formData.tags}
                  onChange={handleChange}
                  placeholder="e.g., laptop, macbook, portable"
                />
                <p className="text-xs text-gray-500">
                  Add tags to help customers find your product. Separate with commas.
                </p>
              </div>

              {/* Submit Buttons */}
              <div className="flex gap-4 pt-4 border-t">
                <Button
                  type="submit"
                  disabled={loading}
                  className="flex-1"
                >
                  {loading ? 'Creating Product...' : 'Create Product'}
                </Button>
                <Link href="/seller/dashboard" className="flex-1">
                  <Button type="button" variant="outline" className="w-full">
                    Cancel
                  </Button>
                </Link>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
