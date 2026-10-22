import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { Ruler, Plus, Trash2, X } from 'lucide-react';

export default function UnitsPage() {
  const { hasRole } = useAuth();
  const [units, setUnits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [formData, setFormData] = useState({ code: '', name: '' });
  const [error, setError] = useState('');

  const fetchUnits = () => {
    setLoading(true);
    api.get('/units')
      .then(res => setUnits(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchUnits(); }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await api.post('/units', formData);
      setModalOpen(false);
      setFormData({ code: '', name: '' });
      fetchUnits();
    } catch (err) {
      setError(err.response?.data?.detail || 'Không thể thêm');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Xóa đơn vị tính này?')) return;
    try {
      await api.delete(`/units/${id}`);
      fetchUnits();
    } catch (err) {
      alert(err.response?.data?.detail || 'Không thể xóa');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
            <Ruler className="w-6 h-6 text-sky-400" />
            <span>Quản Lý Đơn Vị Tính</span>
          </h1>
          <p className="text-sm text-slate-400">Danh mục đơn vị đo lường (Cái, Hộp, Kg, Thùng, Chiếc...)</p>
        </div>
        {hasRole(['ADMIN']) && (
          <button onClick={() => setModalOpen(true)} className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm rounded-xl">
            <Plus className="w-4 h-4" />
            <span>THÊM ĐƠN VỊ TÍNH</span>
          </button>
        )}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="text-xs text-slate-400 uppercase bg-slate-950 border-b border-slate-800">
            <tr>
              <th className="p-4">Mã ĐVT</th>
              <th className="p-4">Tên đơn vị tính</th>
              <th className="p-4 text-right">Thao tác</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {loading ? (
              <tr><td colSpan="3" className="p-8 text-center text-slate-500">Đang tải...</td></tr>
            ) : (
              units.map(u => (
                <tr key={u.id} className="hover:bg-slate-800/40">
                  <td className="p-4 font-mono font-semibold text-sky-400">{u.code}</td>
                  <td className="p-4 font-medium text-white">{u.name}</td>
                  <td className="p-4 text-right">
                    {hasRole(['ADMIN']) && (
                      <button onClick={() => handleDelete(u.id)} className="p-1.5 text-rose-400 hover:bg-slate-800 rounded-lg">
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
              <h3 className="text-lg font-bold text-white">Thêm Đơn Vị Tính Mới</h3>
              <button onClick={() => setModalOpen(false)} className="text-slate-400 hover:text-white"><X className="w-5 h-5" /></button>
            </div>
            {error && <div className="p-3 bg-rose-500/10 text-rose-300 text-xs rounded-xl">{error}</div>}
            <form onSubmit={handleSave} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Mã đơn vị tính</label>
                <input type="text" required value={formData.code} onChange={e => setFormData({ ...formData, code: e.target.value })} className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white" placeholder="UNIT006" />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Tên đơn vị tính</label>
                <input type="text" required value={formData.name} onChange={e => setFormData({ ...formData, name: e.target.value })} className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white" placeholder="Bộ" />
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
