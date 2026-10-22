import React, { useState } from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { 
  LayoutDashboard, Package, Tags, Ruler, Truck, 
  ArrowDownLeft, ArrowUpRight, Warehouse, History, 
  FileSpreadsheet, Bot, Users, LogOut, Menu, X, ShieldAlert 
} from 'lucide-react';

export default function MainLayout() {
  const { user, logout, hasRole } = useAuth();
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { to: '/', label: 'Tổng quan Dashboard', icon: LayoutDashboard, roles: ['ADMIN', 'WAREHOUSE', 'ACCOUNTANT'] },
    { to: '/products', label: 'Quản lý Hàng hóa', icon: Package, roles: ['ADMIN', 'WAREHOUSE', 'ACCOUNTANT'] },
    { to: '/categories', label: 'Nhóm Hàng hóa', icon: Tags, roles: ['ADMIN', 'WAREHOUSE', 'ACCOUNTANT'] },
    { to: '/units', label: 'Đơn vị tính', icon: Ruler, roles: ['ADMIN', 'WAREHOUSE', 'ACCOUNTANT'] },
    { to: '/suppliers', label: 'Nhà cung cấp', icon: Truck, roles: ['ADMIN', 'WAREHOUSE', 'ACCOUNTANT'] },
    { to: '/imports', label: 'Phiếu Nhập kho', icon: ArrowDownLeft, roles: ['ADMIN', 'WAREHOUSE', 'ACCOUNTANT'] },
    { to: '/exports', label: 'Phiếu Xuất kho', icon: ArrowUpRight, roles: ['ADMIN', 'WAREHOUSE', 'ACCOUNTANT'] },
    { to: '/inventory', label: 'Theo dõi Tồn kho', icon: Warehouse, roles: ['ADMIN', 'WAREHOUSE', 'ACCOUNTANT'] },
    { to: '/history', label: 'Lịch sử Nhập / Xuất', icon: History, roles: ['ADMIN', 'WAREHOUSE', 'ACCOUNTANT'] },
    { to: '/reports', label: 'Báo cáo Xuất-Nhập-Tồn', icon: FileSpreadsheet, roles: ['ADMIN', 'WAREHOUSE', 'ACCOUNTANT'] },
    { to: '/ai-analysis', label: 'Phân tích AI Pro', icon: Bot, roles: ['ADMIN', 'WAREHOUSE', 'ACCOUNTANT'], highlight: true },
    { to: '/users', label: 'Quản trị Người dùng', icon: Users, roles: ['ADMIN'] },
  ];

  const getRoleBadge = (role) => {
    switch (role) {
      case 'ADMIN':
        return <span className="bg-rose-500/20 text-rose-300 border border-rose-500/30 text-xs px-2.5 py-1 rounded-full font-semibold">ADMIN</span>;
      case 'WAREHOUSE':
        return <span className="bg-sky-500/20 text-sky-300 border border-sky-500/30 text-xs px-2.5 py-1 rounded-full font-semibold">THỦ KHO</span>;
      case 'ACCOUNTANT':
        return <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs px-2.5 py-1 rounded-full font-semibold">KẾ TOÁN</span>;
      default:
        return null;
    }
  };

  return (
    <div className="flex h-screen bg-slate-950 overflow-hidden text-slate-100">
      {/* Sidebar */}
      <aside className={`${sidebarOpen ? 'w-64' : 'w-20'} bg-slate-900 border-r border-slate-800 transition-all duration-300 flex flex-col z-20`}>
        {/* Sidebar Header */}
        <div className="h-16 flex items-center justify-between px-4 border-b border-slate-800">
          {sidebarOpen ? (
            <div className="flex items-center space-x-2">
              <div className="bg-indigo-600 p-2 rounded-lg text-white">
                <Warehouse className="w-5 h-5" />
              </div>
              <div>
                <h1 className="font-bold text-sm text-white tracking-wide leading-none">INVENTORY AI</h1>
                <span className="text-[10px] text-indigo-400 font-semibold tracking-wider">AIA331 PROJECT</span>
              </div>
            </div>
          ) : (
            <div className="bg-indigo-600 p-2 rounded-lg text-white mx-auto">
              <Warehouse className="w-5 h-5" />
            </div>
          )}
          <button 
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="text-slate-400 hover:text-white p-1 rounded border border-slate-700 hover:bg-slate-800"
          >
            {sidebarOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
          </button>
        </div>

        {/* Nav Links */}
        <nav className="flex-1 overflow-y-auto p-3 space-y-1">
          {navItems.filter(item => hasRole(item.roles)).map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) => `
                  flex items-center space-x-3 px-3 py-2.5 rounded-xl font-medium text-sm transition-all
                  ${isActive 
                    ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30' 
                    : item.highlight 
                      ? 'bg-purple-900/30 text-purple-300 border border-purple-500/30 hover:bg-purple-800/40' 
                      : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                  }
                `}
              >
                <Icon className={`w-5 h-5 flex-shrink-0 ${item.highlight ? 'text-purple-400 animate-pulse' : ''}`} />
                {sidebarOpen && <span className="truncate">{item.label}</span>}
              </NavLink>
            );
          })}
        </nav>

        {/* User Info Footer */}
        {sidebarOpen && user && (
          <div className="p-3 border-t border-slate-800 bg-slate-900/50">
            <div className="flex items-center justify-between">
              <div className="truncate pr-2">
                <p className="text-xs font-semibold text-white truncate">{user.full_name}</p>
                <div className="mt-1">{getRoleBadge(user.role)}</div>
              </div>
              <button 
                onClick={handleLogout}
                title="Đăng xuất"
                className="p-2 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-lg transition"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Header */}
        <header className="h-16 bg-slate-900/80 backdrop-blur border-b border-slate-800 flex items-center justify-between px-6 z-10">
          <div className="flex items-center space-x-3">
            <h2 className="text-lg font-bold text-white">Đại học Thái Nguyên – Trường ĐH CNTT & TT</h2>
            <span className="text-xs bg-slate-800 text-slate-400 border border-slate-700 px-2.5 py-0.5 rounded-full">AIA331</span>
          </div>

          <div className="flex items-center space-x-4">
            <div className="text-right">
              <span className="text-xs text-slate-400 block">Xin chào,</span>
              <span className="text-sm font-semibold text-slate-200">{user?.full_name}</span>
            </div>
            {getRoleBadge(user?.role)}
          </div>
        </header>

        {/* Dynamic Page View */}
        <main className="flex-1 overflow-y-auto p-6 bg-slate-950">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
