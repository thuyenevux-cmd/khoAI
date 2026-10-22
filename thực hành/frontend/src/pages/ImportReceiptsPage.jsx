import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { ArrowDownLeft, Plus, X, Trash2, Eye, Calendar, User, Truck } from 'lucide-react';

export default function ImportReceiptsPage() {
  const { hasRole } = useAuth();
  const [receipts, setReceipts] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Create Modal State
  const [modalOpen, setModalOpen] = useState(false);
  const [viewingReceipt, setViewingReceipt] = useState(null);
  const [selectedSupplier, setSelectedSupplier] = useState('');
  const [note, setNote] = useState('');
  const [details, setDetails] = useState([
    { product_id: '', quantity: 10, unit_price: 100000 }
  ]);
  const [error, setError] = useState('');

  const fetchReceipts = () => {
    setLoading(true);
    api.get('/imports')
      .then(res => setReceipts(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchReceipts();
    api.get('/suppliers').then(res => setSuppliers(res.data));
    api.get('/products').then(res => setProducts(res.data));
  }, []);

  const handleOpenModal = () => {
    setError('');
    setSelectedSupplier(suppliers[0]?.id || '');
    setNote('');
    setDetails([{ product_id: products[0]?.id || '', quantity: 10, unit_price: 100000 }]);
    setModalOpen(true);
  };

  const handleAddLine = () => {
    setDetails([...details, { product_id: products[0]?.id || '', quantity: 1, unit_price: 0 }]);
  };

  const handleRemoveLine = (idx) => {
    if (details.length === 1) return;
    setDetails(details.filter((_, i) => i !== idx));
  };

  const handleDetailChange = (idx, field, val) => {
    const next = [...details];
    next[idx][field] = val;
    setDetails(next);
  };

  const calculateTotal = () => {
    return details.reduce((sum, item) => sum + (Number(item.quantity) * Number(item.unit_price)), 0);
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await api.post('/imports', {
        supplier_id: Number(selectedSupplier),
        note,
        details: details.map(d => ({
          product_id: Number(d.product_id),
          quantity: Number(d.quantity),
          unit_price: Number(d.unit_price)
        }))
      });
      setModalOpen(false);
      fetchReceipts();
    } catch (err) {
      setError(err.response?.data?.detail || 'Lỗi khi tạo phiếu nhập kho');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
            <ArrowDownLeft className="w-6 h-6 text-sky-400" />
            <span>Quản Lý Phiếu Nhập Kho</span>
          </h1>
          <p className="text-sm text-slate-400">Lập phiếu nhập kho hàng hóa và tự động cập nhật tồn kho (Transaction ACID)</p>
        </div>
        {hasRole(['ADMIN', 'WAREHOUSE']) && (
          <button onClick={handleOpenModal} className="flex items-center space-x-2 px-4 py-2.5 bg-sky-600 hover:bg-sky-500 text-white font-semibold text-sm rounded-xl shadow-lg shadow-sky-600/30 transition">
            <Plus className="w-4 h-4" />
            <span>LẬP PHIẾU NHẬP KHO</span>
          </button>
        )}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="text-xs text-slate-400 uppercase bg-slate-950 border-b border-slate-800">
            <tr>
              <th className="p-4">Mã phiếu</th>
              <th className="p-4">Ngày nhập</th>
              <th className="p-4">Nhà cung cấp</th>
              <th className="p-4">Người lập</th>
              <th className="p-4 text-right">Tổng thành tiền</th>
              <th className="p-4 text-center">Trạng thái</th>
              <th className="p-4 text-right">Xem</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {loading ? (
              <tr><td colSpan="7" className="p-8 text-center text-slate-500">Đang tải...</td></tr>
            ) : receipts.length === 0 ? (
              <tr><td colSpan="7" className="p-8 text-center text-slate-500">Chưa có phiếu nhập kho nào.</td></tr>
            ) : (
              receipts.map(r => (
                <tr key={r.id} className="hover:bg-slate-800/40">
                  <td className="p-4 font-mono font-semibold text-sky-400">{r.receipt_code}</td>
                  <td className="p-4 text-slate-300">{new Date(r.receipt_date).toLocaleString('vi-VN')}</td>
                  <td className="p-4 font-medium text-white">{r.supplier?.name}</td>
                  <td className="p-4 text-slate-300">{r.creator?.full_name}</td>
                  <td className="p-4 text-right font-extrabold text-emerald-400">{r.total_amount?.toLocaleString('vi-VN')} đ</td>
                  <td className="p-4 text-center">
                    <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2.5 py-1 rounded-full text-xs font-semibold">HOÀN THÀNH</span>
                  </td>
                  <td className="p-4 text-right">
                    <button onClick={() => setViewingReceipt(r)} className="p-1.5 hover:bg-slate-800 text-sky-400 rounded-lg">
                      <Eye className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Modal Add Import Receipt */}
      {modalOpen && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-3xl p-6 space-y-4 shadow-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-lg font-bold text-white flex items-center space-x-2">
                <ArrowDownLeft className="w-5 h-5 text-sky-400" />
                <span>Tạo Phiếu Nhập Kho Mới</span>
              </h3>
              <button onClick={() => setModalOpen(false)} className="text-slate-400 hover:text-white"><X className="w-5 h-5" /></button>
            </div>

            {error && <div className="p-3 bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs rounded-xl">{error}</div>}

            <form onSubmit={handleSave} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Nhà cung cấp</label>
                  <select
                    value={selectedSupplier}
                    onChange={e => setSelectedSupplier(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white"
                  >
                    {suppliers.map(s => <option key={s.id} value={s.id}>{s.name} ({s.code})</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Ghi chú phiếu nhập</label>
                  <input
                    type="text"
                    value={note}
                    onChange={e => setNote(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white"
                    placeholder="Nhập kho bổ sung..."
                  />
                </div>
              </div>

              {/* Detail Rows */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold text-slate-300 uppercase">Danh sách hàng nhập</span>
                  <button type="button" onClick={handleAddLine} className="text-xs text-sky-400 hover:text-sky-300 flex items-center space-x-1">
                    <Plus className="w-3.5 h-3.5" />
                    <span>Thêm dòng</span>
                  </button>
                </div>

                <div className="space-y-2">
                  {details.map((d, idx) => (
                    <div key={idx} className="flex items-center space-x-2 bg-slate-950 p-2.5 rounded-xl border border-slate-800">
                      <select
                        value={d.product_id}
                        onChange={e => handleDetailChange(idx, 'product_id', e.target.value)}
                        className="flex-1 bg-slate-900 border border-slate-800 rounded-lg text-sm text-white p-2"
                      >
                        {products.map(p => <option key={p.id} value={p.id}>{p.code} - {p.name}</option>)}
                      </select>
                      <input
                        type="number"
                        min="1"
                        placeholder="Số lượng"
                        value={d.quantity}
                        onChange={e => handleDetailChange(idx, 'quantity', e.target.value)}
                        className="w-24 bg-slate-900 border border-slate-800 rounded-lg text-sm text-white p-2 text-center"
                      />
                      <input
                        type="number"
                        min="0"
                        placeholder="Đơn giá"
                        value={d.unit_price}
                        onChange={e => handleDetailChange(idx, 'unit_price', e.target.value)}
                        className="w-32 bg-slate-900 border border-slate-800 rounded-lg text-sm text-white p-2 text-right"
                      />
                      <span className="w-28 text-right text-xs font-bold text-emerald-400">
                        {(Number(d.quantity) * Number(d.unit_price)).toLocaleString('vi-VN')} đ
                      </span>
                      {details.length > 1 && (
                        <button type="button" onClick={() => handleRemoveLine(idx)} className="p-1 text-rose-400 hover:bg-slate-800 rounded">
                          <Trash2 className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              <div className="flex items-center justify-between pt-4 border-t border-slate-800">
                <div>
                  <span className="text-xs text-slate-400 block">Tổng cộng phiếu nhập:</span>
                  <span className="text-lg font-extrabold text-emerald-400">{calculateTotal().toLocaleString('vi-VN')} đ</span>
                </div>
                <div className="space-x-3">
                  <button type="button" onClick={() => setModalOpen(false)} className="px-4 py-2 bg-slate-800 text-slate-300 rounded-xl text-sm font-semibold">Hủy</button>
                  <button type="submit" className="px-4 py-2 bg-sky-600 text-white rounded-xl text-sm font-semibold hover:bg-sky-500">XÁC NHẬN NHẬP KHO (TRANSACTION)</button>
                </div>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal View Receipt Details */}
      {viewingReceipt && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-2xl p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <h3 className="text-lg font-bold text-white font-mono text-sky-400">{viewingReceipt.receipt_code}</h3>
                <span className="text-xs text-slate-400">Chi tiết phiếu nhập kho</span>
              </div>
              <button onClick={() => setViewingReceipt(null)} className="text-slate-400 hover:text-white"><X className="w-5 h-5" /></button>
            </div>

            <div className="grid grid-cols-2 gap-4 text-xs bg-slate-950 p-3 rounded-xl border border-slate-800">
              <div><span className="text-slate-500">Nhà cung cấp:</span> <span className="font-semibold text-white">{viewingReceipt.supplier?.name}</span></div>
              <div><span className="text-slate-500">Người lập:</span> <span className="font-semibold text-white">{viewingReceipt.creator?.full_name}</span></div>
              <div><span className="text-slate-500">Ngày nhập:</span> <span className="font-semibold text-white">{new Date(viewingReceipt.receipt_date).toLocaleString('vi-VN')}</span></div>
              <div><span className="text-slate-500">Ghi chú:</span> <span className="font-semibold text-white">{viewingReceipt.note || '—'}</span></div>
            </div>

            <table className="w-full text-left text-xs">
              <thead className="text-slate-400 uppercase bg-slate-950 border-b border-slate-800">
                <tr>
                  <th className="p-3">Sản phẩm</th>
                  <th className="p-3 text-center">Số lượng</th>
                  <th className="p-3 text-right">Đơn giá</th>
                  <th className="p-3 text-right">Thành tiền</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {viewingReceipt.details?.map(d => (
                  <tr key={d.id}>
                    <td className="p-3 text-white font-medium">{d.product?.name} ({d.product?.code})</td>
                    <td className="p-3 text-center font-bold text-sky-400">{d.quantity}</td>
                    <td className="p-3 text-right text-slate-300">{d.unit_price?.toLocaleString('vi-VN')} đ</td>
                    <td className="p-3 text-right text-emerald-400 font-semibold">{d.total_price?.toLocaleString('vi-VN')} đ</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
