import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { Tags, Plus, Trash2, Edit, X } from 'lucide-react';

export default function CategoriesPage() {
  const { hasRole } = useAuth();
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [formData, setFormData] = useState({ code: '', name: '', description: '' });
  const [error, setError] = useState('');

  const fetchCategories = () => {
    setLoading(true);
    api.get('/categories')
      .then(res => setCategories(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchCategories(); }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await api.post('/categories', formData);
      setModalOpen(false);
      setFormData({ code: '', name: '', description: '' });
      fetchCategories();
    } catch (err) {
      setError(err.response?.data?.detail || 'Không thể thêm nhóm hàng');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Xóa nhóm hàng này?')) return;
    try {
      await api.delete(`/categories/${id}`);
      fetchCategories();
    } catch (err) {
      alert(err.response?.data?.detail || 'Không thể xóa');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
            <Tags className="w-6 h-6 text-purple-400" />
            <span>Quản Lý Nhóm Hàng</span>
          </h1>
          <p className="text-sm text-slate-400">Phân loại nhóm vật tư và hàng hóa</p>
        </div>
        {hasRole(['ADMIN']) && (
          <button onClick={() => setModalOpen(true)} className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm rounded-xl">
            <Plus className="w-4 h-4" />
            <span>THÊM NHÓM HÀNG</span>
          </button>
        )}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="text-xs text-slate-400 uppercase bg-slate-950 border-b border-slate-800">
            <tr>
              <th className="p-4">Mã nhóm</th>
              <th className="p-4">Tên nhóm hàng</th>
              <th className="p-4">Mô tả</th>
              <th className="p-4 text-right">Thao tác</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {loading ? (
              <tr><td colSpan="4" className="p-8 text-center text-slate-500">Đang tải...</td></tr>
            ) : (
              categories.map(c => (
                <tr key={c.id} className="hover:bg-slate-800/40">
                  <td className="p-4 font-mono font-semibold text-purple-400">{c.code}</td>
                  <td className="p-4 font-medium text-white">{c.name}</td>
                  <td className="p-4 text-slate-400">{c.description || '—'}</td>
                  <td className="p-4 text-right">
                    {hasRole(['ADMIN']) && (
                      <button onClick={() => handleDelete(c.id)} className="p-1.5 text-rose-400 hover:bg-slate-800 rounded-lg">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    )}
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
              <h3 className="text-lg font-bold text-white">Thêm Nhóm Hàng Mới</h3>
              <button onClick={() => setModalOpen(false)} className="text-slate-400 hover:text-white"><X className="w-5 h-5" /></button>
            </div>
            {error && <div className="p-3 bg-rose-500/10 text-rose-300 text-xs rounded-xl">{error}</div>}
            <form onSubmit={handleSave} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Mã nhóm hàng</label>
                <input type="text" required value={formData.code} onChange={e => setFormData({ ...formData, code: e.target.value })} className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white" placeholder="CAT005" />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Tên nhóm hàng</label>
                <input type="text" required value={formData.name} onChange={e => setFormData({ ...formData, name: e.target.value })} className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white" placeholder="Thiết bị văn phòng" />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Mô tả</label>
                <textarea rows="2" value={formData.description} onChange={e => setFormData({ ...formData, description: e.target.value })} className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white" />
              </div>
              <div className="flex justify-end space-x-3 pt-3">
                <button type="button" onClick={() => setModalOpen(false)} className="px-4 py-2 bg-slate-800 text-slate-300 rounded-xl text-sm">Hủy</button>
                <button type="submit" className="px-4 py-2 bg-indigo-600 text-white rounded-xl text-sm font-semibold">Lưu</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
