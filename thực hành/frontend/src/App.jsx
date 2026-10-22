import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import MainLayout from './layouts/MainLayout';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import ProductsPage from './pages/ProductsPage';
import CategoriesPage from './pages/CategoriesPage';
import UnitsPage from './pages/UnitsPage';
import SuppliersPage from './pages/SuppliersPage';
import ImportReceiptsPage from './pages/ImportReceiptsPage';
import ExportReceiptsPage from './pages/ExportReceiptsPage';
import InventoryPage from './pages/InventoryPage';
import StockHistoryPage from './pages/StockHistoryPage';
import ReportsPage from './pages/ReportsPage';
import AIAnalysisPage from './pages/AIAnalysisPage';
import UsersPage from './pages/UsersPage';

const ProtectedRoute = ({ children, roles }) => {
  const { user, loading, hasRole } = useAuth();
  if (loading) return <div className="p-8 text-center text-slate-500">Đang tải ứng dụng...</div>;
  if (!user) return <Navigate to="/login" replace />;
  if (roles && !hasRole(roles)) return <div className="p-8 text-center text-rose-400 font-bold">403 Forbidden: Bạn không có quyền truy cập trang này.</div>;
  return children;
};

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />

          <Route path="/" element={<ProtectedRoute><MainLayout /></ProtectedRoute>}>
            <Route index element={<DashboardPage />} />
            <Route path="products" element={<ProductsPage />} />
            <Route path="categories" element={<CategoriesPage />} />
            <Route path="units" element={<UnitsPage />} />
            <Route path="suppliers" element={<SuppliersPage />} />
            <Route path="imports" element={<ImportReceiptsPage />} />
            <Route path="exports" element={<ExportReceiptsPage />} />
            <Route path="inventory" element={<InventoryPage />} />
            <Route path="history" element={<StockHistoryPage />} />
            <Route path="reports" element={<ReportsPage />} />
            <Route path="ai-analysis" element={<AIAnalysisPage />} />
            <Route path="users" element={<ProtectedRoute roles={['ADMIN']}><UsersPage /></ProtectedRoute>} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
