import React from 'react';
import { Link } from 'react-router-dom';
import { PackageOpen, ClipboardList } from 'lucide-react';

const AdminDashboard = () => {
  return (
    <div className="animate-fade-in max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold text-slate-800 mb-8">Admin Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <Link to="/admin/products" className="glass-card p-8 flex flex-col items-center justify-center gap-4 hover:border-primary-500 hover:shadow-xl transition-all group">
          <PackageOpen className="w-16 h-16 text-primary-500 group-hover:scale-110 transition-transform" />
          <h2 className="text-2xl font-bold text-slate-800">Manage Products</h2>
          <p className="text-slate-500 text-center">Create, update, or delete products in the catalog.</p>
        </Link>

        <Link to="/admin/orders" className="glass-card p-8 flex flex-col items-center justify-center gap-4 hover:border-primary-500 hover:shadow-xl transition-all group">
          <ClipboardList className="w-16 h-16 text-primary-500 group-hover:scale-110 transition-transform" />
          <h2 className="text-2xl font-bold text-slate-800">Manage Orders</h2>
          <p className="text-slate-500 text-center">View all customer orders and update their fulfillment status.</p>
        </Link>
      </div>
    </div>
  );
};

export default AdminDashboard;
