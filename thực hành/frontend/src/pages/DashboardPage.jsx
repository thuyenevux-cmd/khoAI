import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Package, Truck, ArrowDownLeft, ArrowUpRight, AlertTriangle, TrendingUp, Sparkles } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from 'recharts';
import { Link } from 'react-router-dom';

export default function DashboardPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/dashboard')
      .then(res => setData(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="p-8 text-center text-slate-400">Đang tải dữ liệu Dashboard...</div>;
  }

  const { kpis, top_exported_items, low_stock_warnings, monthly_chart } = data || {};

  return (
    <div className="space-y-6">
      {/* Header Title */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Dashboard Báo Cáo Tổng Quan</h1>
          <p className="text-sm text-slate-400">Thống kê chỉ số vận hành kho hàng thời gian thực</p>
        </div>
        <Link
          to="/ai-analysis"
          className="flex items-center space-x-2 px-4 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white rounded-xl shadow-lg shadow-indigo-600/30 text-sm font-semibold transition"
        >
          <Sparkles className="w-4 h-4 animate-pulse" />
          <span>PHÂN TÍCH AI KHO HÀNG</span>
        </Link>
      </div>

      {/* AI Smart Advisory Banner */}
      <div className="p-4 rounded-2xl bg-gradient-to-r from-indigo-950/60 via-purple-950/40 to-slate-900 border border-indigo-500/30 flex flex-col md:flex-row items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center space-x-3.5">
          <div className="p-2.5 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl text-white shadow-md shadow-indigo-500/30">
            <Sparkles className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <span>Trợ Lý AI Đề Xuất Vận Hành</span>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">Live</span>
            </h3>
            <p className="text-xs text-slate-300 mt-0.5">
              Hệ thống phát hiện <strong className="text-rose-400">{kpis?.low_stock_count || 0} mặt hàng</strong> đang dưới ngưỡng an toàn tối thiểu. Đề xuất kiểm tra kế hoạch nhập hàng để tránh đứt gãy cung ứng.
            </p>
          </div>
        </div>
        <Link
          to="/ai-analysis"
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-bold transition shadow-md shadow-indigo-600/30 whitespace-nowrap flex items-center gap-1.5"
        >
          <span>Xem phân tích AI</span>
          <ArrowUpRight className="w-4 h-4" />
        </Link>
      </div>

      {/* KPI Cards Grid (6 cards) */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3.5">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[11px] font-semibold text-slate-400 uppercase">Mặt Hàng (SKU)</span>
            <div className="p-1.5 bg-indigo-500/10 text-indigo-400 rounded-lg">
              <Package className="w-4 h-4" />
            </div>
          </div>
          <p className="text-xl font-black text-white">{kpis?.total_products || 0}</p>
          <span className="text-[11px] text-slate-500 mt-0.5 block">Đang quản lý</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[11px] font-semibold text-slate-400 uppercase">Tổng Tồn Kho</span>
            <div className="p-1.5 bg-blue-500/10 text-blue-400 rounded-lg">
              <TrendingUp className="w-4 h-4" />
            </div>
          </div>
          <p className="text-xl font-black text-blue-400">{(kpis?.total_inventory_quantity || 0).toLocaleString()} <span className="text-xs font-normal text-slate-500">sp</span></p>
          <span className="text-[11px] text-slate-500 mt-0.5 block">Số lượng lưu kho</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[11px] font-semibold text-slate-400 uppercase">Giá Trị Kho Hàng</span>
            <div className="p-1.5 bg-emerald-500/10 text-emerald-400 rounded-lg">
              <span className="text-xs font-bold font-mono">₫</span>
            </div>
          </div>
          <p className="text-lg font-black text-emerald-400 tracking-tight">
            {(kpis?.estimated_inventory_value || 0).toLocaleString()} <span className="text-[10px] font-normal text-slate-400">đ</span>
          </p>
          <span className="text-[11px] text-slate-500 mt-0.5 block">Định giá ước tính</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[11px] font-semibold text-slate-400 uppercase">Phiếu Nhập</span>
            <div className="p-1.5 bg-sky-500/10 text-sky-400 rounded-lg">
              <ArrowDownLeft className="w-4 h-4" />
            </div>
          </div>
          <p className="text-xl font-black text-white">{kpis?.total_imports || 0}</p>
          <span className="text-[11px] text-slate-500 mt-0.5 block">Đã hoàn thành</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[11px] font-semibold text-slate-400 uppercase">Phiếu Xuất</span>
            <div className="p-1.5 bg-purple-500/10 text-purple-400 rounded-lg">
              <ArrowUpRight className="w-4 h-4" />
            </div>
          </div>
          <p className="text-xl font-black text-white">{kpis?.total_exports || 0}</p>
          <span className="text-[11px] text-slate-500 mt-0.5 block">Đã xuất kho</span>
        </div>

        <div className="bg-slate-900 border border-rose-500/30 p-4 rounded-2xl bg-rose-500/5">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[11px] font-semibold text-rose-300 uppercase">Cảnh Báo Tồn</span>
            <div className="p-1.5 bg-rose-500/20 text-rose-400 rounded-lg">
              <AlertTriangle className="w-4 h-4 animate-pulse" />
            </div>
          </div>
          <p className="text-xl font-black text-rose-400">{kpis?.low_stock_count || 0} <span className="text-xs font-normal text-rose-400/70">sp</span></p>
          <span className="text-[11px] text-rose-300/70 mt-0.5 block">Dưới ngưỡng min</span>
        </div>
      </div>

      {/* Chart Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 p-6 rounded-2xl">
          <h3 className="text-base font-bold text-white mb-4 flex items-center space-x-2">
            <TrendingUp className="w-5 h-5 text-indigo-400" />
            <span>Biểu đồ Xu Hướng Nhập / Xuất Kho Theo Tháng</span>
          </h3>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={monthly_chart}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="month" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#fff' }} />
                <Legend />
                <Bar dataKey="nhap" name="Số lượng nhập" fill="#38bdf8" radius={[4, 4, 0, 0]} />
                <Bar dataKey="xuat" name="Số lượng xuất" fill="#818cf8" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Top Exported List */}
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl flex flex-col justify-between">
          <div>
            <h3 className="text-base font-bold text-white mb-4">Top Hàng Xuất Chạy (30 Ngày)</h3>
            <div className="space-y-3">
              {top_exported_items?.map((item, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-slate-950/60 rounded-xl border border-slate-800">
                  <div>
                    <span className="text-xs font-mono text-indigo-400 block">{item.code}</span>
                    <span className="text-sm font-semibold text-slate-200">{item.name}</span>
                  </div>
                  <span className="text-sm font-extrabold text-emerald-400">{item.quantity} sp</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Low Stock Warning Section */}
      <div className="bg-slate-900 border border-rose-500/30 p-6 rounded-2xl">
        <h3 className="text-base font-bold text-rose-300 mb-4 flex items-center space-x-2">
          <AlertTriangle className="w-5 h-5 text-rose-400" />
          <span>Danh Sách Sản Phẩm Dưới Mức Tồn Tối Thiểu (Cần Nhập Hàng)</span>
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="text-xs text-slate-400 uppercase bg-slate-950 border-b border-slate-800">
              <tr>
                <th className="p-3">Mã hàng</th>
                <th className="p-3">Tên sản phẩm</th>
                <th className="p-3 text-center">Tồn kho hiện tại</th>
                <th className="p-3 text-center">Tồn tối thiểu</th>
                <th className="p-3 text-right">Trạng thái</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {low_stock_warnings?.map((w) => (
                <tr key={w.id} className="hover:bg-slate-800/50">
                  <td className="p-3 font-mono font-semibold text-indigo-400">{w.code}</td>
                  <td className="p-3 font-medium text-slate-200">{w.name}</td>
                  <td className="p-3 text-center font-bold text-rose-400">{w.current_stock}</td>
                  <td className="p-3 text-center text-slate-400">{w.minimum_stock}</td>
                  <td className="p-3 text-right">
                    <span className="bg-rose-500/20 text-rose-300 border border-rose-500/30 px-2.5 py-1 rounded-full text-xs font-semibold">
                      {w.current_stock === 0 ? '🔴 HẾT HÀNG' : '🟡 DƯỚI TỒN TỐI THIỂU'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
