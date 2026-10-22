import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { FileSpreadsheet, Download, Calendar, RefreshCw } from 'lucide-react';

export default function ReportsPage() {
  const [period, setPeriod] = useState('30_DAYS');
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchReport = () => {
    setLoading(true);
    api.get(`/reports/inventory?period=${period}`)
      .then(res => setReportData(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchReport();
  }, [period]);

  const handleDownloadCSV = () => {
    window.open(`/api/reports/inventory/export-csv?period=${period}`, '_blank');
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
            <FileSpreadsheet className="w-6 h-6 text-emerald-400" />
            <span>Báo Cáo Tổng Hợp Nhập - Xuất - Tồn</span>
          </h1>
          <p className="text-sm text-slate-400">Bảng tổng hợp chi tiết biến động tồn kho theo từng kỳ báo cáo</p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 bg-slate-900 border border-slate-800 p-1.5 rounded-xl">
            <Calendar className="w-4 h-4 text-slate-400 ml-1" />
            <select
              value={period}
              onChange={e => setPeriod(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-lg text-sm text-white px-3 py-1.5 focus:outline-none"
            >
              <option value="30_DAYS">30 Ngày Gần Nhất</option>
              <option value="THIS_MONTH">Tháng Hiện Tại</option>
              <option value="LAST_MONTH">Tháng Trước</option>
              <option value="ALL">Tất Cả Thời Gian</option>
            </select>
          </div>

          <button
            onClick={handleDownloadCSV}
            className="flex items-center space-x-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-sm rounded-xl shadow-lg shadow-emerald-600/30 transition"
          >
            <Download className="w-4 h-4" />
            <span>XUẤT BÁO CÁO CSV</span>
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
              <th className="p-4 text-center">Tồn đầu kỳ</th>
              <th className="p-4 text-center text-sky-400">Tổng nhập</th>
              <th className="p-4 text-center text-purple-400">Tổng xuất</th>
              <th className="p-4 text-center text-emerald-400 font-bold">Tồn cuối kỳ</th>
              <th className="p-4 text-right">Trạng thái</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {loading ? (
              <tr><td colSpan="8" className="p-8 text-center text-slate-500">Đang tính toán số liệu báo cáo...</td></tr>
            ) : reportData?.items?.length === 0 ? (
              <tr><td colSpan="8" className="p-8 text-center text-slate-500">Không có dữ liệu trong kỳ này.</td></tr>
            ) : (
              reportData?.items?.map(row => (
                <tr key={row.product_id} className="hover:bg-slate-800/40">
                  <td className="p-4 font-mono font-semibold text-indigo-400">{row.product_code}</td>
                  <td className="p-4 font-medium text-white">{row.product_name}</td>
                  <td className="p-4 text-slate-300">{row.category_name}</td>
                  <td className="p-4 text-center font-semibold text-slate-400">{row.beginning_stock}</td>
                  <td className="p-4 text-center font-semibold text-sky-400">+{row.import_quantity}</td>
                  <td className="p-4 text-center font-semibold text-purple-400">-{row.export_quantity}</td>
                  <td className="p-4 text-center font-extrabold text-emerald-400 text-base">{row.ending_stock}</td>
                  <td className="p-4 text-right">
                    <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${row.ending_stock <= row.minimum_stock ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' : 'bg-slate-800 text-slate-300'}`}>
                      {row.status}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
