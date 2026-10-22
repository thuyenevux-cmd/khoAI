import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Warehouse, Lock, User, Sparkles, AlertCircle } from 'lucide-react';

export default function LoginPage() {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('Admin@123');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(username, password);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Đăng nhập thất bại. Vui lòng kiểm tra lại thông tin.');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickFill = (u, p) => {
    setUsername(u);
    setPassword(p);
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background Orbs */}
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-indigo-600/20 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-purple-600/20 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-md bg-slate-900/90 border border-slate-800 rounded-2xl p-8 shadow-2xl backdrop-blur-xl z-10">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 bg-indigo-600/20 border border-indigo-500/30 text-indigo-400 rounded-2xl mb-3 shadow-inner">
            <Warehouse className="w-8 h-8" />
          </div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">HỆ THỐNG QUẢN LÝ KHO AI</h1>
          <p className="text-xs text-indigo-400 font-semibold mt-1">AIA331 - ĐẠI HỌC CÔNG NGHỆ THÔNG TIN & TRUYỀN THÔNG</p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-rose-500/10 border border-rose-500/30 rounded-xl flex items-center space-x-3 text-rose-300 text-sm">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Tên đăng nhập</label>
            <div className="relative">
              <User className="w-5 h-5 absolute left-3 top-3 text-slate-500" />
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-white focus:outline-none focus:border-indigo-500 text-sm transition"
                placeholder="Nhập username"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Mật khẩu</label>
            <div className="relative">
              <Lock className="w-5 h-5 absolute left-3 top-3 text-slate-500" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-white focus:outline-none focus:border-indigo-500 text-sm transition"
                placeholder="Nhập mật khẩu"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl shadow-lg shadow-indigo-600/30 transition duration-200 flex items-center justify-center space-x-2 text-sm"
          >
            {loading ? (
              <span>Đang xử lý...</span>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>ĐĂNG NHẬP HỆ THỐNG</span>
              </>
            )}
          </button>
        </form>

        {/* Quick Demo Accounts */}
        <div className="mt-8 pt-6 border-t border-slate-800">
          <p className="text-xs font-semibold text-slate-400 mb-3 text-center uppercase tracking-wider">Chọn nhanh tài khoản Demo:</p>
          <div className="grid grid-cols-3 gap-2">
            <button
              onClick={() => handleQuickFill('admin', 'Admin@123')}
              className="px-2 py-2 bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 rounded-xl text-rose-300 text-xs font-medium transition text-center"
            >
              ADMIN
            </button>
            <button
              onClick={() => handleQuickFill('warehouse', 'Warehouse@123')}
              className="px-2 py-2 bg-sky-500/10 hover:bg-sky-500/20 border border-sky-500/30 rounded-xl text-sky-300 text-xs font-medium transition text-center"
            >
              THỦ KHO
            </button>
            <button
              onClick={() => handleQuickFill('accountant', 'Accountant@123')}
              className="px-2 py-2 bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/30 rounded-xl text-emerald-300 text-xs font-medium transition text-center"
            >
              KẾ TOÁN
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
