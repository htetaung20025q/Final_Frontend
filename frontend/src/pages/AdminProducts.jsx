import React, { useState, useEffect } from 'react';
import api from '../api';
import { Plus, Edit2, Trash2 } from 'lucide-react';

const AdminProducts = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({ name: '', description: '', price: '', stock: '', category_id: '' });
  const [imageFile, setImageFile] = useState(null);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const res = await api.get('/product/list');
      setProducts(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      let image_url = null;
      if (imageFile) {
        const uploadData = new FormData();
        uploadData.append('file', imageFile);
        const uploadRes = await api.post('/product/upload-image', uploadData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        image_url = uploadRes.data.image_url;
      }

      await api.post('/product/create', {
        ...formData,
        price: parseInt(formData.price),
        stock: parseInt(formData.stock),
        category_id: formData.category_id ? parseInt(formData.category_id) : null,
        image_url: image_url
      });
      setShowModal(false);
      setFormData({ name: '', description: '', price: '', stock: '', category_id: '' });
      setImageFile(null);
      fetchProducts();
    } catch (err) {
      console.error(err);
      alert('Failed to create product');
    }
  };

  const handleDelete = async (id) => {
    if (confirm('Are you sure you want to delete this product?')) {
      try {
        await api.delete(`/product/${id}`);
        fetchProducts();
      } catch (err) {
        console.error(err);
      }
    }
  };

  return (
    <div className="animate-fade-in max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-slate-800">Manage Products</h1>
        <button onClick={() => setShowModal(true)} className="btn-primary">
          <Plus className="w-5 h-5" /> Add Product
        </button>
      </div>

      <div className="glass-card overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="p-4 font-semibold text-slate-600">ID</th>
              <th className="p-4 font-semibold text-slate-600">Name</th>
              <th className="p-4 font-semibold text-slate-600">Price</th>
              <th className="p-4 font-semibold text-slate-600">Stock</th>
              <th className="p-4 font-semibold text-slate-600 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {products.map(p => (
              <tr key={p.id} className="hover:bg-slate-50/50 transition-colors">
                <td className="p-4 text-slate-500">#{p.id}</td>
                <td className="p-4 font-medium text-slate-800">{p.name}</td>
                <td className="p-4 text-primary-600 font-bold">${p.price}</td>
                <td className="p-4">
                  <span className={`px-2 py-1 rounded text-xs font-bold ${p.stock > 0 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                    {p.stock} in stock
                  </span>
                </td>
                <td className="p-4 text-right">
                  <button className="text-blue-500 hover:text-blue-700 p-2"><Edit2 className="w-4 h-4"/></button>
                  <button onClick={() => handleDelete(p.id)} className="text-red-500 hover:text-red-700 p-2"><Trash2 className="w-4 h-4"/></button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 animate-fade-in">
          <div className="glass-card p-6 w-full max-w-md animate-slide-up">
            <h2 className="text-2xl font-bold mb-4">Add Product</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <input type="text" placeholder="Name" required className="input-field" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} />
              <input type="text" placeholder="Description" required className="input-field" value={formData.description} onChange={e => setFormData({...formData, description: e.target.value})} />
              <div className="flex gap-4">
                <input type="number" placeholder="Price" required className="input-field flex-1" value={formData.price} onChange={e => setFormData({...formData, price: e.target.value})} />
                <input type="number" placeholder="Stock" required className="input-field flex-1" value={formData.stock} onChange={e => setFormData({...formData, stock: e.target.value})} />
              </div>
              <input type="number" placeholder="Category ID (Optional)" className="input-field" value={formData.category_id} onChange={e => setFormData({...formData, category_id: e.target.value})} />
              <input type="file" accept="image/*" className="input-field bg-white" onChange={e => setImageFile(e.target.files[0])} />
              <div className="flex gap-4 mt-6">
                <button type="button" onClick={() => setShowModal(false)} className="btn-secondary flex-1">Cancel</button>
                <button type="submit" className="btn-primary flex-1">Save</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminProducts;
