import React, { useState, useEffect, useContext } from 'react';
import api from '../api';
import { CartContext } from '../contexts/CartContext';
import { ShoppingBag, Filter, Search } from 'lucide-react';

const Home = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({ category_id: '', min_price: '', max_price: '', available: false });
  const { addToCart } = useContext(CartContext);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      // Build query string
      const params = new URLSearchParams();
      if (filters.category_id) params.append('category_id', filters.category_id);
      if (filters.min_price) params.append('min_price', filters.min_price);
      if (filters.max_price) params.append('max_price', filters.max_price);
      if (filters.available) params.append('available', 'true');

      const res = await api.get(`/product/list?${params.toString()}`);
      setProducts(res.data);
    } catch (err) {
      console.error('Failed to fetch products', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters]);

  const handleFilterChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFilters(prev => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
  };

  return (
    <div className="flex flex-col md:flex-row gap-8 animate-fade-in">
      {/* Sidebar Filters */}
      <aside className="w-full md:w-64 shrink-0">
        <div className="glass-card p-6 sticky top-24">
          <div className="flex items-center gap-2 mb-4 text-slate-800">
            <Filter className="w-5 h-5" />
            <h3 className="font-semibold text-lg">Filters</h3>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-slate-600 mb-1">Category ID</label>
              <input 
                type="number" 
                name="category_id"
                placeholder="All Categories"
                className="input-field py-1.5 text-sm"
                value={filters.category_id}
                onChange={handleFilterChange}
              />
            </div>
            
            <div className="flex gap-2">
              <div className="flex-1">
                <label className="block text-sm text-slate-600 mb-1">Min Price</label>
                <input 
                  type="number" 
                  name="min_price"
                  className="input-field py-1.5 text-sm"
                  value={filters.min_price}
                  onChange={handleFilterChange}
                />
              </div>
              <div className="flex-1">
                <label className="block text-sm text-slate-600 mb-1">Max Price</label>
                <input 
                  type="number" 
                  name="max_price"
                  className="input-field py-1.5 text-sm"
                  value={filters.max_price}
                  onChange={handleFilterChange}
                />
              </div>
            </div>

            <label className="flex items-center gap-2 cursor-pointer mt-4">
              <input 
                type="checkbox" 
                name="available"
                className="w-4 h-4 rounded text-primary-600 focus:ring-primary-500"
                checked={filters.available}
                onChange={handleFilterChange}
              />
              <span className="text-sm text-slate-700">In Stock Only</span>
            </label>
          </div>
        </div>
      </aside>

      {/* Product Grid */}
      <div className="flex-1">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-slate-800">New Arrivals</h1>
          <span className="text-sm text-slate-500">{products.length} Products</span>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="bg-slate-200 animate-pulse h-64 rounded-xl"></div>
            ))}
          </div>
        ) : products.length === 0 ? (
          <div className="text-center py-20 text-slate-500 glass-card">
            <Search className="w-12 h-12 mx-auto mb-4 text-slate-300" />
            <p>No products found matching your filters.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {products.map(product => (
              <div key={product.id} className="card-hover flex flex-col h-full animate-slide-up">
                <div className="aspect-square bg-slate-100 flex items-center justify-center p-6 relative group overflow-hidden">
                   {/* Placeholder Image for Premium Look */}
                   <img src={`https://picsum.photos/seed/${product.id}/400/400`} alt={product.name} className="w-full h-full object-cover rounded-lg group-hover:scale-105 transition-transform duration-500" />
                   {product.stock <= 0 && (
                     <span className="absolute top-2 left-2 bg-slate-900 text-white text-xs font-bold px-2 py-1 rounded">Out of Stock</span>
                   )}
                </div>
                <div className="p-4 flex-1 flex flex-col">
                  <h3 className="font-semibold text-slate-800 truncate mb-1">{product.name}</h3>
                  <p className="text-sm text-slate-500 line-clamp-2 mb-3 flex-1">{product.description}</p>
                  <div className="flex items-center justify-between mt-auto">
                    <span className="font-bold text-lg text-primary-600">${product.price}</span>
                    <button 
                      onClick={() => addToCart(product)}
                      disabled={product.stock <= 0}
                      className="btn-primary py-1.5 px-3 rounded-full text-sm disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <ShoppingBag className="w-4 h-4" />
                      Add
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;
