import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShoppingCart, User, LogOut, PackageSearch, ShieldCheck } from 'lucide-react';
import { AuthContext } from '../contexts/AuthContext';
import { CartContext } from '../contexts/CartContext';

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const { totalItems } = useContext(CartContext);
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <header className="bg-white/80 backdrop-blur-md sticky top-0 z-50 border-b border-slate-200">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/" className="text-2xl font-bold text-primary-600 flex items-center gap-2">
          <PackageSearch className="w-8 h-8" />
          <span>LuxeCommerce</span>
        </Link>
        
        <nav className="flex items-center gap-6">
          <Link to="/" className="text-slate-600 hover:text-primary-600 transition-colors font-medium">Shop</Link>
          
          {user ? (
            <>
              {user.is_admin && (
                <Link to="/admin" className="text-slate-600 hover:text-primary-600 transition-colors font-medium flex items-center gap-1">
                  <ShieldCheck className="w-4 h-4" />
                  Admin
                </Link>
              )}
              <Link to="/dashboard" className="text-slate-600 hover:text-primary-600 transition-colors font-medium flex items-center gap-1">
                <User className="w-4 h-4" />
                {user.username}
              </Link>
              <button 
                onClick={handleLogout}
                className="text-slate-600 hover:text-red-500 transition-colors flex items-center gap-1"
                title="Logout"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-slate-600 hover:text-primary-600 transition-colors font-medium">Login</Link>
              <Link to="/register" className="btn-primary py-1.5 px-4 rounded-full">Sign Up</Link>
            </>
          )}

          <Link to="/cart" className="relative text-slate-700 hover:text-primary-600 transition-colors">
            <ShoppingCart className="w-6 h-6" />
            {totalItems > 0 && (
              <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center shadow-sm">
                {totalItems}
              </span>
            )}
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Navbar;
