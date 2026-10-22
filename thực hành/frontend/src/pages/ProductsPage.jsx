import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { Package, Plus, Search, Filter, Edit, Trash2, X, AlertCircle } from 'lucide-react';

export default function ProductsPage() {
  const { hasRole } = useAuth();
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [units, setUnits] = useState([]);
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [loading, setLoading] = useState(true);

  // Modal State
  const [modalOpen, setModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [formData, setFormData] = useState({
    code: '', name: '', category_id: '', unit_id: '', minimum_stock: 0, initial_stock: 0, description: ''
  });
  const [error, setError] = useState('');

  const fetchProducts = () => {
    setLoading(true);
    let url = `/products?search=${encodeURIComponent(search)}`;
    if (selectedCategory) url += `&category_id=${selectedCategory}`;
    api.get(url)
      .then(res => setProducts(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    api.get('/categories').then(res => setCategories(res.data));
    api.get('/units').then(res => setUnits(res.data));
  }, []);

  useEffect(() => {
    fetchProducts();
  }, [search, selectedCategory]);

  const handleOpenModal = (prod = null) => {
    setError('');
    if (prod) {
      setEditingProduct(prod);
      setFormData({
        code: prod.code,
        name: prod.name,
        category_id: prod.category_id,
        unit_id: prod.unit_id,
        minimum_stock: prod.minimum_stock,
        initial_stock: prod.current_stock,
        description: prod.description || ''
      });
    } else {
      setEditingProduct(null);
      setFormData({
        code: '', name: '', category_id: categories[0]?.id || '', unit_id: units[0]?.id || '', minimum_stock: 10, initial_stock: 0, description: ''
      });
    }
    setModalOpen(true);
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setError('');
    try {
      if (editingProduct) {
        await api.put(`/products/${editingProduct.id}`, {
          name: formData.name,
          category_id: Number(formData.category_id),
          unit_id: Number(formData.unit_id),
          minimum_stock: Number(formData.minimum_stock),
          description: formData.description
        });
      } else {
        await api.post('/products', {
          code: formData.code,
          name: formData.name,
          category_id: Number(formData.category_id),
          unit_id: Number(formData.unit_id),
          minimum_stock: Number(formData.minimum_stock),
          initial_stock: Number(formData.initial_stock),
          description: formData.description
        });
      }
      setModalOpen(false);
      fetchProducts();
    } catch (err) {
      setError(err.response?.data?.detail || 'Đã có lỗi xảy ra');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Bạn có chắc chắn muốn xóa sản phẩm này?')) return;
    try {
      await api.delete(`/products/${id}`);
      fetchProducts();
    } catch (err) {
      alert(err.response?.data?.detail || 'Không thể xóa sản phẩm');
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
            <Package className="w-6 h-6 text-indigo-400" />
            <span>Quản Lý Hàng Hóa & Sản Phẩm</span>
          </h1>
          <p className="text-sm text-slate-400">Danh mục vật tư, hàng hóa và mức tồn tối thiểu an toàn</p>
        </div>
        {hasRole(['ADMIN']) && (
          <button
            onClick={() => handleOpenModal()}
            className="flex items-center space-x-2 px-4 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm rounded-xl shadow-lg shadow-indigo-600/30 transition"
          >
            <Plus className="w-4 h-4" />
            <span>THÊM HÀNG HÓA MỚI</span>
          </button>
        )}
      </div>

      {/* Filter & Search Bar */}
      <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
          <input
            type="text"
            placeholder="Tìm theo tên hoặc mã hàng..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-indigo-500"
          />
        </div>
        <div className="flex items-center space-x-3 w-full md:w-auto">
          <Filter className="w-4 h-4 text-slate-400" />
          <select
            value={selectedCategory}
            onChange={e => setSelectedCategory(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-xl text-sm text-slate-200 px-3 py-2 focus:outline-none focus:border-indigo-500"
          >
            <option value="">Tất cả nhóm hàng</option>
            {categories.map(c => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="text-xs text-slate-400 uppercase bg-slate-950 border-b border-slate-800">
            <tr>
              <th className="p-4">Mã hàng</th>
              <th className="p-4">Tên sản phẩm</th>
              <th className="p-4">Nhóm hàng</th>
              <th className="p-4">Đơn vị tính</th>
              <th className="p-4 text-center">Tồn tối thiểu</th>
              <th className="p-4 text-center">Tồn hiện tại</th>
              <th className="p-4 text-right">Thao tác</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {loading ? (
              <tr><td colSpan="7" className="p-8 text-center text-slate-500">Đang tải...</td></tr>
            ) : products.length === 0 ? (
              <tr><td colSpan="7" className="p-8 text-center text-slate-500">Không tìm thấy sản phẩm nào.</td></tr>
            ) : (
              products.map(p => (
                <tr key={p.id} className="hover:bg-slate-800/40">
                  <td className="p-4 font-mono font-semibold text-indigo-400">{p.code}</td>
                  <td className="p-4 font-medium text-white">{p.name}</td>
                  <td className="p-4 text-slate-300">{p.category?.name}</td>
                  <td className="p-4 text-slate-300">{p.unit?.name}</td>
                  <td className="p-4 text-center font-semibold text-slate-400">{p.minimum_stock}</td>
                  <td className="p-4 text-center">
                    <span className={`font-bold ${p.current_stock <= p.minimum_stock ? 'text-rose-400' : 'text-emerald-400'}`}>
                      {p.current_stock}
                    </span>
                  </td>
                  <td className="p-4 text-right space-x-2">
                    {hasRole(['ADMIN']) && (
                      <>
                        <button onClick={() => handleOpenModal(p)} className="p-1.5 hover:bg-slate-800 text-indigo-400 rounded-lg">
                          <Edit className="w-4 h-4" />
                        </button>
                        <button onClick={() => handleDelete(p.id)} className="p-1.5 hover:bg-slate-800 text-rose-400 rounded-lg">
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

      {/* Modal Add/Edit */}
      {modalOpen && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-lg font-bold text-white">
                {editingProduct ? 'Chỉnh Sửa Sản Phẩm' : 'Thêm Sản Phẩm Mới'}
              </h3>
              <button onClick={() => setModalOpen(false)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            {error && (
              <div className="p-3 bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs rounded-xl flex items-center space-x-2">
                <AlertCircle className="w-4 h-4" />
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleSave} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Mã sản phẩm</label>
                <input
                  type="text"
                  required
                  disabled={!!editingProduct}
                  value={formData.code}
                  onChange={e => setFormData({ ...formData, code: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-indigo-500 disabled:opacity-50"
                  placeholder="Ví dụ: HH001"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Tên sản phẩm</label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={e => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-indigo-500"
                  placeholder="Ví dụ: Bàn phím cơ AKKO"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Nhóm hàng</label>
                  <select
                    value={formData.category_id}
                    onChange={e => setFormData({ ...formData, category_id: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-indigo-500"
                  >
                    {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Đơn vị tính</label>
                  <select
                    value={formData.unit_id}
                    onChange={e => setFormData({ ...formData, unit_id: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-indigo-500"
                  >
                    {units.map(u => <option key={u.id} value={u.id}>{u.name}</option>)}
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Tồn tối thiểu</label>
                  <input
                    type="number"
                    min="0"
                    value={formData.minimum_stock}
                    onChange={e => setFormData({ ...formData, minimum_stock: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
                {!editingProduct && (
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Tồn ban đầu</label>
                    <input
                      type="number"
                      min="0"
                      value={formData.initial_stock}
                      onChange={e => setFormData({ ...formData, initial_stock: e.target.value })}
                      className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-indigo-500"
                    />
                  </div>
                )}
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Mô tả sản phẩm</label>
                <textarea
                  rows="2"
                  value={formData.description}
                  onChange={e => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="flex justify-end space-x-3 pt-4 border-t border-slate-800">
                <button type="button" onClick={() => setModalOpen(false)} className="px-4 py-2 bg-slate-800 text-slate-300 rounded-xl text-sm font-semibold hover:bg-slate-700">Hủy</button>
                <button type="submit" className="px-4 py-2 bg-indigo-600 text-white rounded-xl text-sm font-semibold hover:bg-indigo-500">Lưu thông tin</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
