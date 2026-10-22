import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { History, ArrowDownLeft, ArrowUpRight, Filter } from 'lucide-react';

export default function StockHistoryPage() {
  const [movements, setMovements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [movementType, setMovementType] = useState('');

  const fetchMovements = () => {
    setLoading(true);
    let url = '/stock-movements';
    if (movementType) url += `?movement_type=${movementType}`;
    api.get(url)
      .then(res => setMovements(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchMovements();
  }, [movementType]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
            <History className="w-6 h-6 text-purple-400" />
            <span>Lịch Sử Giao Dịch & Truy Vết Audit Log</span>
          </h1>
          <p className="text-sm text-slate-400">Nhật ký toàn bộ các biến động Nhập / Xuất kho (Nhân sự thực hiện, thời gian, số lượng)</p>
        </div>

        <div className="flex items-center space-x-3 bg-slate-900 border border-slate-800 p-2 rounded-xl">
          <Filter className="w-4 h-4 text-slate-400" />
          <select
            value={movementType}
            onChange={e => setMovementType(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-lg text-sm text-white px-3 py-1.5 focus:outline-none"
          >
            <option value="">Tất cả loại giao dịch</option>
            <option value="IMPORT">NHẬP KHO (+)</option>
            <option value="EXPORT">XUẤT KHO (-)</option>
          </select>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="text-xs text-slate-400 uppercase bg-slate-950 border-b border-slate-800">
            <tr>
              <th className="p-4">Thời gian</th>
              <th className="p-4">Loại giao dịch</th>
              <th className="p-4">Mã sản phẩm</th>
              <th className="p-4">Tên sản phẩm</th>
              <th className="p-4 text-center">Số lượng</th>
              <th className="p-4">Người thực hiện</th>
              <th className="p-4">Loại chứng từ tham chiếu</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {loading ? (
              <tr><td colSpan="7" className="p-8 text-center text-slate-500">Đang tải...</td></tr>
            ) : movements.length === 0 ? (
              <tr><td colSpan="7" className="p-8 text-center text-slate-500">Chưa có lịch sử giao dịch.</td></tr>
            ) : (
              movements.map(m => (
                <tr key={m.id} className="hover:bg-slate-800/40">
                  <td className="p-4 text-slate-400 font-mono text-xs">{new Date(m.created_at).toLocaleString('vi-VN')}</td>
                  <td className="p-4">
                    {m.movement_type === 'IMPORT' ? (
                      <span className="bg-sky-500/20 text-sky-300 border border-sky-500/30 px-2.5 py-1 rounded-full text-xs font-bold flex items-center w-max space-x-1">
                        <ArrowDownLeft className="w-3.5 h-3.5" /><span>NHẬP KHO</span>
                      </span>
                    ) : (
                      <span className="bg-purple-500/20 text-purple-300 border border-purple-500/30 px-2.5 py-1 rounded-full text-xs font-bold flex items-center w-max space-x-1">
                        <ArrowUpRight className="w-3.5 h-3.5" /><span>XUẤT KHO</span>
                      </span>
                    )}
                  </td>
                  <td className="p-4 font-mono font-semibold text-indigo-400">{m.product?.code}</td>
                  <td className="p-4 font-medium text-white">{m.product?.name}</td>
                  <td className="p-4 text-center">
                    <span className={`font-extrabold text-base ${m.movement_type === 'IMPORT' ? 'text-sky-400' : 'text-purple-400'}`}>
                      {m.movement_type === 'IMPORT' ? `+${m.quantity}` : `-${m.quantity}`}
                    </span>
                  </td>
                  <td className="p-4 text-slate-300">{m.user?.full_name} ({m.user?.username})</td>
                  <td className="p-4 text-xs font-mono text-slate-400">{m.reference_type} #{m.reference_id}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
