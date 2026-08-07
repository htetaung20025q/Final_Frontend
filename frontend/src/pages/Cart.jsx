import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { CartContext } from '../contexts/CartContext';
import { Trash2, Plus, Minus, ArrowRight } from 'lucide-react';

const Cart = () => {
  const { cart, updateQuantity, removeFromCart, totalItems, totalPrice } = useContext(CartContext);
  const navigate = useNavigate();

  if (cart.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 animate-fade-in glass-card max-w-2xl mx-auto">
        <h2 className="text-2xl font-bold text-slate-800 mb-4">Your Cart is Empty</h2>
        <p className="text-slate-500 mb-8">Looks like you haven't added anything to your cart yet.</p>
        <Link to="/" className="btn-primary">Start Shopping</Link>
      </div>
    );
  }

  return (
    <div className="animate-fade-in">
      <h1 className="text-3xl font-bold text-slate-800 mb-8">Shopping Cart</h1>
      
      <div className="flex flex-col lg:flex-row gap-8">
        <div className="flex-1 space-y-4">
          {cart.map((item) => (
            <div key={item.product.id} className="glass-card p-4 flex items-center gap-6">
              <div className="w-24 h-24 bg-slate-100 rounded-lg overflow-hidden shrink-0">
                <img src={`https://picsum.photos/seed/${item.product.id}/150/150`} alt={item.product.name} className="w-full h-full object-cover" />
              </div>
              
              <div className="flex-1">
                <h3 className="font-semibold text-lg text-slate-800">{item.product.name}</h3>
                <p className="text-primary-600 font-bold">${item.product.price}</p>
              </div>

              <div className="flex items-center gap-3 bg-slate-50 border border-slate-200 rounded-lg p-1">
                <button 
                  onClick={() => updateQuantity(item.product.id, item.quantity - 1)}
                  className="p-1 hover:bg-slate-200 rounded text-slate-600 transition-colors"
                >
                  <Minus className="w-4 h-4" />
                </button>
                <span className="w-8 text-center font-medium">{item.quantity}</span>
                <button 
                  onClick={() => updateQuantity(item.product.id, item.quantity + 1)}
                  className="p-1 hover:bg-slate-200 rounded text-slate-600 transition-colors"
                >
                  <Plus className="w-4 h-4" />
                </button>
              </div>

              <button 
                onClick={() => removeFromCart(item.product.id)}
                className="text-red-400 hover:text-red-500 p-2 transition-colors"
                title="Remove Item"
              >
                <Trash2 className="w-5 h-5" />
              </button>
            </div>
          ))}
        </div>

        <div className="w-full lg:w-96 shrink-0">
          <div className="glass-card p-6 sticky top-24">
            <h3 className="text-xl font-bold text-slate-800 mb-6">Order Summary</h3>
            
            <div className="space-y-3 text-slate-600 mb-6">
              <div className="flex justify-between">
                <span>Items ({totalItems})</span>
                <span>${totalPrice}</span>
              </div>
              <div className="flex justify-between">
                <span>Shipping</span>
                <span className="text-green-500 font-medium">Free</span>
              </div>
              <div className="border-t border-slate-200 pt-3 flex justify-between font-bold text-lg text-slate-800">
                <span>Total</span>
                <span>${totalPrice}</span>
              </div>
            </div>

            <button 
              onClick={() => navigate('/checkout')}
              className="btn-primary w-full py-3 text-lg"
            >
              Proceed to Checkout <ArrowRight className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;
