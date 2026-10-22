import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Warehouse, AlertTriangle, CheckCircle, XCircle, Search } from 'lucide-react';

export default function InventoryPage() {
  const [inventories, setInventories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('');

  const fetchInventories = () => {
    setLoading(true);
    let url = '/inventory';
    if (statusFilter) url += `?stock_status=${statusFilter}`;
    api.get(url)
      .then(res => setInventories(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchInventories();
  }, [statusFilter]);

  const getStatusBadge = (status) => {
    switch (status) {
      case 'OUT_OF_STOCK':
        return <span className="bg-rose-500/20 text-rose-300 border border-rose-500/30 px-2.5 py-1 rounded-full text-xs font-bold flex items-center w-max space-x-1"><XCircle className="w-3.5 h-3.5" /><span>HẾT HÀNG (0)</span></span>;
      case 'LOW_STOCK':
        return <span className="bg-amber-500/20 text-amber-300 border border-amber-500/30 px-2.5 py-1 rounded-full text-xs font-bold flex items-center w-max space-x-1"><AlertTriangle className="w-3.5 h-3.5" /><span>DƯỚI MỨC TỒN TỐI THIỂU</span></span>;
      default:
        return <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2.5 py-1 rounded-full text-xs font-bold flex items-center w-max space-x-1"><CheckCircle className="w-3.5 h-3.5" /><span>BÌNH THƯỜNG</span></span>;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
            <Warehouse className="w-6 h-6 text-indigo-400" />
            <span>Theo Dõi Tồn Kho Thực Tế</span>
          </h1>
          <p className="text-sm text-slate-400">Giám sát trạng thái tồn kho thời gian thực và phát hiện điểm nóng đứt gãy cung ứng</p>
        </div>

        <div className="flex items-center space-x-2 bg-slate-900 border border-slate-800 p-1.5 rounded-xl">
          <button
            onClick={() => setStatusFilter('')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${statusFilter === '' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'}`}
          >
            TẤT CẢ
          </button>
          <button
            onClick={() => setStatusFilter('LOW_STOCK')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${statusFilter === 'LOW_STOCK' ? 'bg-amber-600 text-white' : 'text-slate-400 hover:text-white'}`}
          >
            CẢNH BÁO SẮP HẾT
          </button>
          <button
            onClick={() => setStatusFilter('OUT_OF_STOCK')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${statusFilter === 'OUT_OF_STOCK' ? 'bg-rose-600 text-white' : 'text-slate-400 hover:text-white'}`}
          >
            HẾT HÀNG
          </button>
        </div>
      </div>

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
              <th className="p-4 text-left">Trạng thái kho</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {loading ? (
              <tr><td colSpan="7" className="p-8 text-center text-slate-500">Đang tải...</td></tr>
            ) : inventories.length === 0 ? (
              <tr><td colSpan="7" className="p-8 text-center text-slate-500">Không có dữ liệu tồn kho theo bộ lọc.</td></tr>
            ) : (
              inventories.map(inv => (
                <tr key={inv.id} className="hover:bg-slate-800/40">
                  <td className="p-4 font-mono font-semibold text-indigo-400">{inv.product?.code}</td>
                  <td className="p-4 font-medium text-white">{inv.product?.name}</td>
                  <td className="p-4 text-slate-300">{inv.product?.category?.name}</td>
                  <td className="p-4 text-slate-300">{inv.product?.unit?.name}</td>
                  <td className="p-4 text-center text-slate-400 font-semibold">{inv.product?.minimum_stock}</td>
                  <td className="p-4 text-center">
                    <span className={`text-base font-extrabold ${inv.quantity <= inv.product?.minimum_stock ? 'text-rose-400' : 'text-emerald-400'}`}>
                      {inv.quantity}
                    </span>
                  </td>
                  <td className="p-4">{getStatusBadge(inv.status)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
