import React, { useEffect, useState } from 'react';
import api from '../api';
import { Package, Clock, CheckCircle } from 'lucide-react';

const Dashboard = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const res = await api.get('/orders/me');
        setOrders(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchOrders();
  }, []);

  const getStatusBadge = (status) => {
    switch (status) {
      case 'paid': return <span className="bg-green-100 text-green-700 px-2 py-1 rounded text-xs font-bold uppercase flex items-center gap-1"><CheckCircle className="w-3 h-3"/> Paid</span>;
      case 'shipped': return <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs font-bold uppercase flex items-center gap-1"><Package className="w-3 h-3"/> Shipped</span>;
      default: return <span className="bg-orange-100 text-orange-700 px-2 py-1 rounded text-xs font-bold uppercase flex items-center gap-1"><Clock className="w-3 h-3"/> {status}</span>;
    }
  };

  return (
    <div className="animate-fade-in max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold text-slate-800 mb-8">My Orders</h1>
      
      {loading ? (
        <div className="space-y-4">
          {[...Array(3)].map((_, i) => <div key={i} className="h-24 bg-slate-200 animate-pulse rounded-xl"></div>)}
        </div>
      ) : orders.length === 0 ? (
        <div className="glass-card p-12 text-center text-slate-500">
          <Package className="w-16 h-16 mx-auto mb-4 text-slate-300" />
          <p className="text-lg">You have no orders yet.</p>
        </div>
      ) : (
        <div className="space-y-6">
          {orders.map(order => (
            <div key={order.id} className="glass-card p-6 flex flex-col md:flex-row gap-6 items-start md:items-center justify-between">
              <div>
                <p className="text-sm text-slate-500 mb-1">Order #{order.id} • {new Date(order.created_at).toLocaleDateString()}</p>
                <p className="text-xl font-bold text-slate-800">${order.total_price}</p>
              </div>
              
              <div>
                {getStatusBadge(order.status)}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
