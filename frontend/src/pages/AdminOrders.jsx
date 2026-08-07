import React, { useState, useEffect } from 'react';
import api from '../api';
import { RefreshCcw, CheckCircle, Package, Clock } from 'lucide-react';

const AdminOrders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(null);

  const fetchOrders = async () => {
    setLoading(true);
    try {
      const res = await api.get('/order/all');
      setOrders(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const handleStatusUpdate = async (orderId, newStatus) => {
    setUpdating(orderId);
    try {
      await api.patch(`/order/${orderId}/status`, { status: newStatus });
      fetchOrders();
    } catch (err) {
      console.error(err);
      alert('Failed to update status');
    } finally {
      setUpdating(null);
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'paid': return <span className="bg-green-100 text-green-700 px-2 py-1 rounded text-xs font-bold uppercase flex items-center gap-1 w-fit"><CheckCircle className="w-3 h-3"/> Paid</span>;
      case 'shipped': return <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs font-bold uppercase flex items-center gap-1 w-fit"><Package className="w-3 h-3"/> Shipped</span>;
      default: return <span className="bg-orange-100 text-orange-700 px-2 py-1 rounded text-xs font-bold uppercase flex items-center gap-1 w-fit"><Clock className="w-3 h-3"/> {status}</span>;
    }
  };

  return (
    <div className="animate-fade-in max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-slate-800">Manage Orders</h1>
        <button onClick={fetchOrders} className="btn-secondary">
          <RefreshCcw className="w-5 h-5" /> Refresh
        </button>
      </div>

      <div className="glass-card overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="p-4 font-semibold text-slate-600">Order ID</th>
              <th className="p-4 font-semibold text-slate-600">User ID</th>
              <th className="p-4 font-semibold text-slate-600">Total Price</th>
              <th className="p-4 font-semibold text-slate-600">Status</th>
              <th className="p-4 font-semibold text-slate-600">Update Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {orders.map(order => (
              <tr key={order.id} className="hover:bg-slate-50/50 transition-colors">
                <td className="p-4 text-slate-500 font-medium">#{order.id}</td>
                <td className="p-4 text-slate-500">{order.user_id}</td>
                <td className="p-4 font-bold text-slate-800">${order.total_price}</td>
                <td className="p-4">{getStatusBadge(order.status)}</td>
                <td className="p-4">
                  <select 
                    className="input-field py-1 text-sm w-32"
                    value={order.status}
                    onChange={(e) => handleStatusUpdate(order.id, e.target.value)}
                    disabled={updating === order.id}
                  >
                    <option value="pending">Pending</option>
                    <option value="paid">Paid</option>
                    <option value="shipped">Shipped</option>
                    <option value="cancelled">Cancelled</option>
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {orders.length === 0 && !loading && (
          <div className="p-8 text-center text-slate-500">No orders found.</div>
        )}
      </div>
    </div>
  );
};

export default AdminOrders;
