import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { ArrowUpRight, Plus, X, Trash2, Eye, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function ExportReceiptsPage() {
  const { hasRole } = useAuth();
  const [receipts, setReceipts] = useState([]);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Create Modal State
  const [modalOpen, setModalOpen] = useState(false);
  const [viewingReceipt, setViewingReceipt] = useState(null);
  const [receiver, setReceiver] = useState('');
  const [note, setNote] = useState('');
  const [details, setDetails] = useState([
    { product_id: '', quantity: 1 }
  ]);
  const [error, setError] = useState('');

  const fetchReceipts = () => {
    setLoading(true);
    api.get('/exports')
      .then(res => setReceipts(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchReceipts();
    api.get('/products').then(res => setProducts(res.data));
  }, []);

  const handleOpenModal = () => {
    setError('');
    setReceiver('Phòng Hành Chính Kế Toán');
    setNote('Xuất trang thiết bị vận hành');
    setDetails([{ product_id: products[0]?.id || '', quantity: 1 }]);
    setModalOpen(true);
  };

  const handleAddLine = () => {
    setDetails([...details, { product_id: products[0]?.id || '', quantity: 1 }]);
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

  const getProductStock = (prodId) => {
    const p = products.find(item => item.id === Number(prodId));
    return p ? p.current_stock : 0;
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await api.post('/exports', {
        receiver,
        note,
        details: details.map(d => ({
          product_id: Number(d.product_id),
          quantity: Number(d.quantity)
        }))
      });
      setModalOpen(false);
      fetchReceipts();
      // refresh products stock
      api.get('/products').then(res => setProducts(res.data));
    } catch (err) {
      setError(err.response?.data?.detail || 'Lỗi khi tạo phiếu xuất kho');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
            <ArrowUpRight className="w-6 h-6 text-purple-400" />
            <span>Quản Lý Phiếu Xuất Kho</span>
          </h1>
          <p className="text-sm text-slate-400">Lập phiếu xuất kho và kiểm soát nghiêm ngặt chống tồn kho âm (Pessimistic Lock)</p>
        </div>
        {hasRole(['ADMIN', 'WAREHOUSE']) && (
          <button onClick={handleOpenModal} className="flex items-center space-x-2 px-4 py-2.5 bg-purple-600 hover:bg-purple-500 text-white font-semibold text-sm rounded-xl shadow-lg shadow-purple-600/30 transition">
            <Plus className="w-4 h-4" />
            <span>LẬP PHIẾU XUẤT KHO</span>
          </button>
        )}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="text-xs text-slate-400 uppercase bg-slate-950 border-b border-slate-800">
            <tr>
              <th className="p-4">Mã phiếu</th>
              <th className="p-4">Ngày xuất</th>
              <th className="p-4">Người/Bộ phận nhận</th>
              <th className="p-4">Người lập</th>
              <th className="p-4 text-center">Trạng thái</th>
              <th className="p-4 text-right">Xem</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {loading ? (
              <tr><td colSpan="6" className="p-8 text-center text-slate-500">Đang tải...</td></tr>
            ) : receipts.length === 0 ? (
              <tr><td colSpan="6" className="p-8 text-center text-slate-500">Chưa có phiếu xuất kho nào.</td></tr>
            ) : (
              receipts.map(r => (
                <tr key={r.id} className="hover:bg-slate-800/40">
                  <td className="p-4 font-mono font-semibold text-purple-400">{r.receipt_code}</td>
                  <td className="p-4 text-slate-300">{new Date(r.receipt_date).toLocaleString('vi-VN')}</td>
                  <td className="p-4 font-medium text-white">{r.receiver || '—'}</td>
                  <td className="p-4 text-slate-300">{r.creator?.full_name}</td>
                  <td className="p-4 text-center">
                    <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2.5 py-1 rounded-full text-xs font-semibold">ĐÃ XUẤT KHO</span>
                  </td>
                  <td className="p-4 text-right">
                    <button onClick={() => setViewingReceipt(r)} className="p-1.5 hover:bg-slate-800 text-purple-400 rounded-lg">
                      <Eye className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Modal Add Export Receipt */}
      {modalOpen && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-3xl p-6 space-y-4 shadow-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-lg font-bold text-white flex items-center space-x-2">
                <ArrowUpRight className="w-5 h-5 text-purple-400" />
                <span>Tạo Phiếu Xuất Kho Mới</span>
              </h3>
              <button onClick={() => setModalOpen(false)} className="text-slate-400 hover:text-white"><X className="w-5 h-5" /></button>
            </div>

            {error && (
              <div className="p-4 bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm rounded-xl flex items-center space-x-3">
                <AlertTriangle className="w-6 h-6 text-rose-400 flex-shrink-0" />
                <div>
                  <span className="font-bold block">TỪ CHỐI TẠO PHIẾU XUẤT KHO:</span>
                  <span>{error}</span>
                </div>
              </div>
            )}

            <form onSubmit={handleSave} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Người / Bộ phận nhận</label>
                  <input
                    type="text"
                    required
                    value={receiver}
                    onChange={e => setReceiver(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white"
                    placeholder="Phòng CNTT / Dự án A"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Ghi chú phiếu xuất</label>
                  <input
                    type="text"
                    value={note}
                    onChange={e => setNote(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white"
                    placeholder="Lý do xuất kho..."
                  />
                </div>
              </div>

              {/* Detail Rows */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold text-slate-300 uppercase">Danh sách hàng xuất</span>
                  <button type="button" onClick={handleAddLine} className="text-xs text-purple-400 hover:text-purple-300 flex items-center space-x-1">
                    <Plus className="w-3.5 h-3.5" />
                    <span>Thêm dòng</span>
                  </button>
                </div>

                <div className="space-y-2">
                  {details.map((d, idx) => {
                    const currentStock = getProductStock(d.product_id);
                    const isOverflow = Number(d.quantity) > currentStock;

                    return (
                      <div key={idx} className={`flex items-center space-x-2 bg-slate-950 p-2.5 rounded-xl border ${isOverflow ? 'border-rose-500/50 bg-rose-500/5' : 'border-slate-800'}`}>
                        <select
                          value={d.product_id}
                          onChange={e => handleDetailChange(idx, 'product_id', e.target.value)}
                          className="flex-1 bg-slate-900 border border-slate-800 rounded-lg text-sm text-white p-2"
                        >
                          {products.map(p => <option key={p.id} value={p.id}>{p.code} - {p.name} (Tồn: {p.current_stock})</option>)}
                        </select>
                        
                        <div className="flex items-center space-x-1">
                          <span className="text-xs text-slate-400">Xuất:</span>
                          <input
                            type="number"
                            min="1"
                            placeholder="Số lượng"
                            value={d.quantity}
                            onChange={e => handleDetailChange(idx, 'quantity', e.target.value)}
                            className="w-24 bg-slate-900 border border-slate-800 rounded-lg text-sm text-white p-2 text-center font-bold"
                          />
                        </div>

                        <div className="w-36 text-right">
                          <span className="text-xs text-slate-500 block">Tồn kho hiện tại:</span>
                          <span className={`text-xs font-bold ${isOverflow ? 'text-rose-400' : 'text-emerald-400'}`}>
                            {currentStock} đơn vị
                          </span>
                        </div>

                        {details.length > 1 && (
                          <button type="button" onClick={() => handleRemoveLine(idx)} className="p-1 text-rose-400 hover:bg-slate-800 rounded">
                            <Trash2 className="w-4 h-4" />
                          </button>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>

              <div className="flex items-center justify-between pt-4 border-t border-slate-800">
                <div className="flex items-center space-x-2 text-xs text-emerald-400">
                  <ShieldCheck className="w-4 h-4" />
                  <span>Cơ chế DB Transaction khóa dòng chống tồn âm được kích hoạt</span>
                </div>
                <div className="space-x-3">
                  <button type="button" onClick={() => setModalOpen(false)} className="px-4 py-2 bg-slate-800 text-slate-300 rounded-xl text-sm font-semibold">Hủy</button>
                  <button type="submit" className="px-4 py-2 bg-purple-600 text-white rounded-xl text-sm font-semibold hover:bg-purple-500">XÁC NHẬN XUẤT KHO</button>
                </div>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal View Export Details */}
      {viewingReceipt && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-2xl p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <h3 className="text-lg font-bold text-white font-mono text-purple-400">{viewingReceipt.receipt_code}</h3>
                <span className="text-xs text-slate-400">Chi tiết phiếu xuất kho</span>
              </div>
              <button onClick={() => setViewingReceipt(null)} className="text-slate-400 hover:text-white"><X className="w-5 h-5" /></button>
            </div>

            <div className="grid grid-cols-2 gap-4 text-xs bg-slate-950 p-3 rounded-xl border border-slate-800">
              <div><span className="text-slate-500">Người/Bộ phận nhận:</span> <span className="font-semibold text-white">{viewingReceipt.receiver}</span></div>
              <div><span className="text-slate-500">Người lập:</span> <span className="font-semibold text-white">{viewingReceipt.creator?.full_name}</span></div>
              <div><span className="text-slate-500">Ngày xuất:</span> <span className="font-semibold text-white">{new Date(viewingReceipt.receipt_date).toLocaleString('vi-VN')}</span></div>
              <div><span className="text-slate-500">Ghi chú:</span> <span className="font-semibold text-white">{viewingReceipt.note || '—'}</span></div>
            </div>

            <table className="w-full text-left text-xs">
              <thead className="text-slate-400 uppercase bg-slate-950 border-b border-slate-800">
                <tr>
                  <th className="p-3">Sản phẩm</th>
                  <th className="p-3 text-center">Số lượng xuất</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {viewingReceipt.details?.map(d => (
                  <tr key={d.id}>
                    <td className="p-3 text-white font-medium">{d.product?.name} ({d.product?.code})</td>
                    <td className="p-3 text-center font-bold text-purple-400">{d.quantity}</td>
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
