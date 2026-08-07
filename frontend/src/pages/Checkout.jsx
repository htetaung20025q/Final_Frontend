import React, { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { CartContext } from '../contexts/CartContext';
import { AuthContext } from '../contexts/AuthContext';
import api from '../api';
import { CheckCircle2 } from 'lucide-react';

const Checkout = () => {
  const { cart, totalPrice, clearCart } = useContext(CartContext);
  const { user } = useContext(AuthContext);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleCheckout = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // 1. Place the order
      const orderData = {
        user_id: user.id, // Assuming user context provides this
        items: cart.map(item => ({
          product_id: item.product.id,
          quantity: item.quantity
        }))
      };

      const orderRes = await api.post('/order/place', orderData);
      const order = orderRes.data.order;

      // 2. Simulate Payment
      const paymentData = {
        order_id: order.id,
        amount: totalPrice,
        payment_method: 'credit_card' // Simulated
      };

      await api.post('/payments/confirm', paymentData);

      setSuccess(true);
      clearCart();
    } catch (err) {
      setError('Checkout failed. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="flex flex-col items-center justify-center py-20 animate-fade-in glass-card max-w-xl mx-auto text-center">
        <CheckCircle2 className="w-20 h-20 text-green-500 mb-6" />
        <h2 className="text-3xl font-bold text-slate-800 mb-4">Payment Successful!</h2>
        <p className="text-slate-600 mb-8">Your order has been placed and is currently being processed.</p>
        <button onClick={() => navigate('/dashboard')} className="btn-primary">View My Orders</button>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto animate-fade-in">
      <h1 className="text-3xl font-bold text-slate-800 mb-8">Checkout</h1>
      
      {error && <div className="bg-red-50 text-red-600 p-4 rounded-lg mb-6">{error}</div>}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="glass-card p-6">
          <h3 className="text-xl font-bold mb-6 text-slate-800">Payment Details</h3>
          <form id="checkout-form" onSubmit={handleCheckout} className="space-y-4">
             <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Card Number (Simulated)</label>
              <input type="text" placeholder="1234 5678 9101 1121" className="input-field" required />
            </div>
            <div className="flex gap-4">
              <div className="flex-1">
                <label className="block text-sm font-medium text-slate-700 mb-1">Expiry</label>
                <input type="text" placeholder="MM/YY" className="input-field" required />
              </div>
              <div className="flex-1">
                <label className="block text-sm font-medium text-slate-700 mb-1">CVC</label>
                <input type="text" placeholder="123" className="input-field" required />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Name on Card</label>
              <input type="text" placeholder="John Doe" className="input-field" required />
            </div>
          </form>
        </div>

        <div className="glass-card p-6 h-fit bg-primary-50 border-primary-100">
          <h3 className="text-xl font-bold mb-6 text-primary-900">Summary</h3>
          <div className="space-y-3 text-primary-800 mb-6">
            <div className="flex justify-between font-bold text-2xl border-b border-primary-200 pb-4">
              <span>Total to Pay</span>
              <span>${totalPrice}</span>
            </div>
            <p className="text-sm opacity-80 pt-2">By clicking confirm, you agree to our terms and conditions.</p>
          </div>
          <button 
            type="submit" 
            form="checkout-form"
            disabled={loading} 
            className="btn-primary w-full py-3 text-lg"
          >
            {loading ? 'Processing...' : 'Confirm Payment'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Checkout;
