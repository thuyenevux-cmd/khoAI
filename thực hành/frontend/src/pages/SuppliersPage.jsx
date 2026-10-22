import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { Truck, Plus, Trash2, Edit, X } from 'lucide-react';

export default function SuppliersPage() {
  const { hasRole } = useAuth();
  const [suppliers, setSuppliers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingSupplier, setEditingSupplier] = useState(null);
  const [formData, setFormData] = useState({
    code: '', name: '', contact_person: '', phone: '', email: '', address: '', note: ''
  });
  const [error, setError] = useState('');

  const fetchSuppliers = () => {
    setLoading(true);
    api.get('/suppliers')
      .then(res => setSuppliers(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchSuppliers(); }, []);

  const handleOpenModal = (sup = null) => {
    setError('');
    if (sup) {
      setEditingSupplier(sup);
      setFormData({
        code: sup.code, name: sup.name, contact_person: sup.contact_person || '',
        phone: sup.phone || '', email: sup.email || '', address: sup.address || '', note: sup.note || ''
      });
    } else {
      setEditingSupplier(null);
      setFormData({ code: '', name: '', contact_person: '', phone: '', email: '', address: '', note: '' });
    }
    setModalOpen(true);
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setError('');
    try {
      if (editingSupplier) {
        await api.put(`/suppliers/${editingSupplier.id}`, formData);
      } else {
        await api.post('/suppliers', formData);
      }
      setModalOpen(false);
      fetchSuppliers();
    } catch (err) {
      setError(err.response?.data?.detail || 'Không thể lưu nhà cung cấp');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Xóa nhà cung cấp này?')) return;
    try {
      await api.delete(`/suppliers/${id}`);
      fetchSuppliers();
    } catch (err) {
      alert(err.response?.data?.detail || 'Không thể xóa');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
            <Truck className="w-6 h-6 text-purple-400" />
            <span>Quản Lý Nhà Cung Cấp</span>
          </h1>
          <p className="text-sm text-slate-400">Danh sách các đối tác cung ứng vật tư, thiết bị</p>
        </div>
        {hasRole(['ADMIN']) && (
          <button onClick={() => handleOpenModal()} className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm rounded-xl">
            <Plus className="w-4 h-4" />
            <span>THÊM NCC MỚI</span>
          </button>
        )}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="text-xs text-slate-400 uppercase bg-slate-950 border-b border-slate-800">
            <tr>
              <th className="p-4">Mã NCC</th>
              <th className="p-4">Tên Nhà Cung Cấp</th>
              <th className="p-4">Người liên hệ</th>
              <th className="p-4">Số điện thoại</th>
              <th className="p-4">Email / Địa chỉ</th>
              <th className="p-4 text-right">Thao tác</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {loading ? (
              <tr><td colSpan="6" className="p-8 text-center text-slate-500">Đang tải...</td></tr>
            ) : (
              suppliers.map(s => (
                <tr key={s.id} className="hover:bg-slate-800/40">
                  <td className="p-4 font-mono font-semibold text-purple-400">{s.code}</td>
                  <td className="p-4 font-medium text-white">{s.name}</td>
                  <td className="p-4 text-slate-300">{s.contact_person || '—'}</td>
                  <td className="p-4 text-slate-300">{s.phone || '—'}</td>
                  <td className="p-4 text-slate-400 text-xs">
                    <div>{s.email}</div>
                    <div className="text-slate-500">{s.address}</div>
                  </td>
                  <td className="p-4 text-right space-x-2">
                    {hasRole(['ADMIN']) && (
                      <>
                        <button onClick={() => handleOpenModal(s)} className="p-1.5 hover:bg-slate-800 text-indigo-400 rounded-lg">
                          <Edit className="w-4 h-4" />
                        </button>
                        <button onClick={() => handleDelete(s.id)} className="p-1.5 hover:bg-slate-800 text-rose-400 rounded-lg">
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </>
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
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-lg font-bold text-white">{editingSupplier ? 'Sửa Nhà Cung Cấp' : 'Thêm Nhà Cung Cấp Mới'}</h3>
              <button onClick={() => setModalOpen(false)} className="text-slate-400 hover:text-white"><X className="w-5 h-5" /></button>
            </div>
            {error && <div className="p-3 bg-rose-500/10 text-rose-300 text-xs rounded-xl">{error}</div>}
            <form onSubmit={handleSave} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Mã NCC</label>
                  <input type="text" required disabled={!!editingSupplier} value={formData.code} onChange={e => setFormData({ ...formData, code: e.target.value })} className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white disabled:opacity-50" placeholder="SUP004" />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Tên Nhà Cung Cấp</label>
                  <input type="text" required value={formData.name} onChange={e => setFormData({ ...formData, name: e.target.value })} className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white" placeholder="Công ty CNTT..." />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Người liên hệ</label>
                  <input type="text" value={formData.contact_person} onChange={e => setFormData({ ...formData, contact_person: e.target.value })} className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white" />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Số điện thoại</label>
                  <input type="text" value={formData.phone} onChange={e => setFormData({ ...formData, phone: e.target.value })} className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white" />
                </div>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Email</label>
                <input type="email" value={formData.email} onChange={e => setFormData({ ...formData, email: e.target.value })} className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white" />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Địa chỉ</label>
                <input type="text" value={formData.address} onChange={e => setFormData({ ...formData, address: e.target.value })} className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white" />
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
