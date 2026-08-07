import React, { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api';
import { AuthContext } from '../contexts/AuthContext';
import { UserPlus } from 'lucide-react';

const Register = () => {
  const [formData, setFormData] = useState({ username: '', email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useContext(AuthContext);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    
    try {
      const res = await api.post('/auth/register', formData);
      const { access_token, user } = res.data;
      login(user, access_token);
      navigate('/');
    } catch (err) {
      // Handle FastAPI validation errors or custom errors
      const detail = err.response?.data?.detail;
      const errMsg = Array.isArray(detail) ? detail[0].msg : detail;
      setError(errMsg || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-16 animate-fade-in">
      <div className="glass-card p-8">
        <div className="flex justify-center mb-6 text-primary-500">
          <UserPlus className="w-12 h-12" />
        </div>
        <h2 className="text-2xl font-bold text-center mb-6 text-slate-800">Create Account</h2>
        
        {error && <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm">{error}</div>}
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Username</label>
            <input 
              type="text" 
              required
              minLength={5}
              maxLength={30}
              className="input-field"
              value={formData.username}
              onChange={(e) => setFormData({...formData, username: e.target.value})}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
            <input 
              type="email" 
              required
              className="input-field"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Password</label>
            <input 
              type="password" 
              required
              minLength={5}
              maxLength={30}
              className="input-field"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
            />
          </div>
          <button type="submit" disabled={loading} className="btn-primary w-full mt-6">
            {loading ? 'Creating account...' : 'Sign Up'}
          </button>
        </form>
        
        <p className="text-center mt-6 text-slate-600 text-sm">
          Already have an account? <Link to="/login" className="text-primary-600 hover:underline font-medium">Log in</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
