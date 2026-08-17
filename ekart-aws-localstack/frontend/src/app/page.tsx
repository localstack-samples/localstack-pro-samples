export default function HomePage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="text-center space-y-8">
        <h1 className="text-5xl font-bold text-blue-600">
          Welcome to <span className="text-yellow-400">EKart</span>
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Discover millions of products from trusted sellers worldwide. 
          Shop with confidence and enjoy lightning-fast delivery.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
          <div className="p-6 bg-white rounded-lg shadow-md">
            <div className="text-4xl mb-4">🛍️</div>
            <h3 className="text-2xl font-bold mb-2">1M+ Products</h3>
            <p className="text-gray-600">Wide variety across all categories</p>
          </div>
          
          <div className="p-6 bg-white rounded-lg shadow-md">
            <div className="text-4xl mb-4">🚚</div>
            <h3 className="text-2xl font-bold mb-2">Fast Delivery</h3>
            <p className="text-gray-600">Same day delivery in major cities</p>
          </div>
          
          <div className="p-6 bg-white rounded-lg shadow-md">
            <div className="text-4xl mb-4">🔒</div>
            <h3 className="text-2xl font-bold mb-2">Secure Shopping</h3>
            <p className="text-gray-600">100% secure payments & returns</p>
          </div>
        </div>

        <div className="mt-12 space-x-4">
          <a href="/products" className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition">
            Browse Products
          </a>
          <a href="/seller/register" className="inline-block bg-gray-200 text-gray-800 px-8 py-3 rounded-lg hover:bg-gray-300 transition">
            Become a Seller
          </a>
        </div>
      </div>
    </div>
  )
}
