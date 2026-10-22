import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Users, Plus, X, Lock, UserCheck, UserX } from 'lucide-react';

export default function UsersPage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [formData, setFormData] = useState({ username: '', password: '', full_name: '', role: 'WAREHOUSE' });
  const [error, setError] = useState('');

  const fetchUsers = () => {
    setLoading(true);
    api.get('/auth/users')
      .then(res => setUsers(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchUsers(); }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await api.post('/auth/users', formData);
      setModalOpen(false);
      setFormData({ username: '', password: '', full_name: '', role: 'WAREHOUSE' });
      fetchUsers();
    } catch (err) {
      setError(err.response?.data?.detail || 'Không thể tạo người dùng');
    }
  };

  const toggleUserActive = async (user) => {
    try {
      await api.put(`/auth/users/${user.id}`, { is_active: !user.is_active });
      fetchUsers();
    } catch (err) {
      alert('Không thể thay đổi trạng thái tài khoản');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
            <Users className="w-6 h-6 text-rose-400" />
            <span>Quản Trị Người Dùng & Phân Quyền Vai Trò</span>
          </h1>
          <p className="text-sm text-slate-400">Danh sách tài khoản hệ thống (Chỉ Quản trị viên ADMIN có quyền truy cập)</p>
        </div>

        <button onClick={() => setModalOpen(true)} className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm rounded-xl">
          <Plus className="w-4 h-4" />
          <span>THÊM NGƯỜI DÙNG MỚI</span>
        </button>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="text-xs text-slate-400 uppercase bg-slate-950 border-b border-slate-800">
            <tr>
              <th className="p-4">ID</th>
              <th className="p-4">Username</th>
              <th className="p-4">Họ và tên</th>
              <th className="p-4">Vai trò (Role)</th>
              <th className="p-4 text-center">Trạng thái</th>
              <th className="p-4 text-right">Khóa / Mở tài khoản</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {loading ? (
              <tr><td colSpan="6" className="p-8 text-center text-slate-500">Đang tải...</td></tr>
            ) : (
              users.map(u => (
                <tr key={u.id} className="hover:bg-slate-800/40">
                  <td className="p-4 font-mono text-slate-500">{u.id}</td>
                  <td className="p-4 font-mono font-semibold text-white">{u.username}</td>
                  <td className="p-4 text-slate-200">{u.full_name}</td>
                  <td className="p-4">
                    <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${u.role === 'ADMIN' ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' : u.role === 'WAREHOUSE' ? 'bg-sky-500/20 text-sky-300 border border-sky-500/30' : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'}`}>
                      {u.role}
                    </span>
                  </td>
                  <td className="p-4 text-center">
                    <span className={`text-xs font-bold ${u.is_active ? 'text-emerald-400' : 'text-rose-400'}`}>
                      {u.is_active ? 'ĐANG HOẠT ĐỘNG' : 'ĐÃ BỊ KHÓA'}
                    </span>
                  </td>
                  <td className="p-4 text-right">
                    <button
                      onClick={() => toggleUserActive(u)}
                      className={`p-1.5 rounded-lg text-xs font-semibold ${u.is_active ? 'text-rose-400 hover:bg-rose-500/10' : 'text-emerald-400 hover:bg-emerald-500/10'}`}
                    >
                      {u.is_active ? <UserX className="w-4 h-4" /> : <UserCheck className="w-4 h-4" />}
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {modalOpen && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-md p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-lg font-bold text-white">Thêm Tài Khoản Mới</h3>
              <button onClick={() => setModalOpen(false)} className="text-slate-400 hover:text-white"><X className="w-5 h-5" /></button>
            </div>
            {error && <div className="p-3 bg-rose-500/10 text-rose-300 text-xs rounded-xl">{error}</div>}
            <form onSubmit={handleSave} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Username</label>
                <input type="text" required value={formData.username} onChange={e => setFormData({ ...formData, username: e.target.value })} className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white" placeholder="user123" />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Mật khẩu</label>
                <input type="password" required value={formData.password} onChange={e => setFormData({ ...formData, password: e.target.value })} className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white" placeholder="******" />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Họ và tên</label>
                <input type="text" required value={formData.full_name} onChange={e => setFormData({ ...formData, full_name: e.target.value })} className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white" placeholder="Nguyễn Văn C" />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Vai trò</label>
                <select value={formData.role} onChange={e => setFormData({ ...formData, role: e.target.value })} className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white">
                  <option value="WAREHOUSE">THỦ KHO (Warehouse)</option>
                  <option value="ACCOUNTANT">KẾ TOÁN (Accountant)</option>
                  <option value="ADMIN">QUẢN TRỊ VIÊN (Admin)</option>
                </select>
              </div>
              <div className="flex justify-end space-x-3 pt-3">
                <button type="button" onClick={() => setModalOpen(false)} className="px-4 py-2 bg-slate-800 text-slate-300 rounded-xl text-sm">Hủy</button>
                <button type="submit" className="px-4 py-2 bg-indigo-600 text-white rounded-xl text-sm font-semibold">Tạo tài khoản</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
