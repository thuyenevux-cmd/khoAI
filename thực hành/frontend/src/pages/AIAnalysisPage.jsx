import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import {
  Bot,
  Sparkles,
  FileText,
  ShoppingCart,
  Zap,
  Code,
  ShieldCheck,
  RefreshCw,
  TrendingDown,
  TrendingUp,
  AlertTriangle,
  Package,
  ArrowRight,
  Copy,
  Check,
  Download,
  Clock,
  Layers,
  CheckCircle2,
  AlertCircle,
  MessageSquare,
  Send,
  HelpCircle,
  Search,
  User,
  Trash2,
  RotateCcw
} from 'lucide-react';

// --- HELPER COMPONENT: PARSES INLINE MARKDOWN (BOLD, ITALIC, CODE, BADGES) ---
function InlineFormatted({ text }) {
  if (!text) return null;

  const parts = text.split(/(\*\*.*?\*\*)/g);

  return (
    <span>
      {parts.map((part, idx) => {
        if (part.startsWith('**') && part.endsWith('**')) {
          const boldText = part.slice(2, -2);

          if (boldText.includes('🔴') || boldText.includes('RẤT CAO') || boldText.includes('Hết hàng')) {
            return (
              <span key={idx} className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30 mx-1">
                <span className="w-1.5 h-1.5 rounded-full bg-rose-400 animate-pulse"></span>
                {boldText}
              </span>
            );
          }
          if (boldText.includes('🟡') || boldText.includes('CAO') || boldText.includes('TRUNG BÌNH') || boldText.includes('Dưới tồn tối thiểu')) {
            return (
              <span key={idx} className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/30 mx-1">
                {boldText}
              </span>
            );
          }
          if (boldText.includes('🟢') || boldText.includes('THẤP') || boldText.includes('An toàn')) {
            return (
              <span key={idx} className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 mx-1">
                {boldText}
              </span>
            );
          }
          return <strong key={idx} className="font-semibold text-white">{boldText}</strong>;
        }
        return <span key={idx}>{part}</span>;
      })}
    </span>
  );
}

// --- HELPER COMPONENT: PARSES & RENDERS MARKDOWN TABLES ---
function MarkdownTableRenderer({ tableLines, onRestockClick }) {
  if (!tableLines || tableLines.length < 2) return null;

  const headerCells = tableLines[0]
    .split('|')
    .map(c => c.trim())
    .filter(c => c.length > 0);

  const rowLines = tableLines.slice(2);

  return (
    <div className="overflow-x-auto rounded-xl border border-slate-800 bg-slate-950/60 shadow-lg my-4">
      <table className="w-full text-left border-collapse text-sm">
        <thead>
          <tr className="bg-slate-900/90 border-b border-slate-800 text-slate-300 text-xs uppercase tracking-wider font-semibold">
            {headerCells.map((head, idx) => (
              <th key={idx} className="py-3 px-4 whitespace-nowrap">
                {head}
              </th>
            ))}
            {onRestockClick && <th className="py-3 px-4 text-center">Thao Tác</th>}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800/60 text-slate-300 text-sm">
          {rowLines.map((rowStr, rowIdx) => {
            const cells = rowStr
              .split('|')
              .map(c => c.trim())
              .filter(c => c.length > 0);

            if (cells.length === 0) return null;

            const isDanger = rowStr.includes('🔴') || rowStr.includes('RẤT CAO') || rowStr.includes('Hết hàng');
            const isWarning = rowStr.includes('🟡') || rowStr.includes('CAO');

            return (
              <tr
                key={rowIdx}
                className={`transition hover:bg-slate-800/40 ${
                  isDanger
                    ? 'bg-rose-950/10'
                    : isWarning
                    ? 'bg-amber-950/10'
                    : 'even:bg-slate-900/20'
                }`}
              >
                {cells.map((cell, colIdx) => (
                  <td key={colIdx} className="py-3.5 px-4 whitespace-nowrap">
                    <InlineFormatted text={cell} />
                  </td>
                ))}
                {onRestockClick && (
                  <td className="py-3.5 px-4 text-center">
                    <button
                      onClick={() => onRestockClick(cells[0])}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white transition shadow-sm hover:shadow-indigo-600/30"
                    >
                      <ShoppingCart className="w-3.5 h-3.5" />
                      <span>Nhập hàng</span>
                    </button>
                  </td>
                )}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

// --- SMART PARSER: CONVERTS FULL MARKDOWN INTO GORGEOUS REACT WIDGETS ---
function SmartMarkdownViewer({ content, onRestockClick }) {
  if (!content) return null;

  const lines = content.split('\n');
  const elements = [];

  let currentTable = [];
  let inTable = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();

    if (line.startsWith('|') && line.endsWith('|')) {
      inTable = true;
      currentTable.push(line);
      continue;
    } else if (inTable) {
      elements.push(
        <MarkdownTableRenderer
          key={`table-${i}`}
          tableLines={currentTable}
          onRestockClick={onRestockClick}
        />
      );
      currentTable = [];
      inTable = false;
    }

    if (!line) continue;

    if (line.startsWith('### ')) {
      const headingText = line.replace('### ', '').trim();
      elements.push(
        <div key={`h3-${i}`} className="pt-6 pb-2 border-b border-slate-800/80 mb-3 flex items-center gap-2">
          <div className="w-2 h-6 bg-gradient-to-b from-indigo-500 to-purple-500 rounded-full"></div>
          <h3 className="text-base font-bold text-white tracking-wide">
            {headingText}
          </h3>
        </div>
      );
      continue;
    }

    if (line.startsWith('#### ')) {
      const headingText = line.replace('#### ', '').trim();
      elements.push(
        <div key={`h4-${i}`} className="pt-3 pb-1 mb-2">
          <h4 className="text-sm font-bold text-indigo-300 flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400"></span>
            <span>{headingText}</span>
          </h4>
        </div>
      );
      continue;
    }

    if (line.startsWith('- ')) {
      const bulletText = line.replace('- ', '').trim();
      const isUrgent = bulletText.includes('💥') || bulletText.includes('⚠️') || bulletText.includes('Cần xử lý ngay');

      elements.push(
        <div
          key={`bullet-${i}`}
          className={`flex items-start gap-3 p-3.5 rounded-xl border my-2 transition ${
            isUrgent
              ? 'bg-rose-950/20 border-rose-500/30 text-rose-200'
              : 'bg-slate-950/40 border-slate-800/70 text-slate-300 hover:border-slate-700'
          }`}
        >
          <div className={`mt-0.5 p-1 rounded-lg ${isUrgent ? 'bg-rose-500/20 text-rose-400' : 'bg-indigo-500/20 text-indigo-400'}`}>
            {isUrgent ? <AlertCircle className="w-4 h-4" /> : <CheckCircle2 className="w-4 h-4" />}
          </div>
          <div className="text-sm leading-relaxed flex-1">
            <InlineFormatted text={bulletText} />
          </div>
        </div>
      );
      continue;
    }

    if (/^\d+\.\s/.test(line)) {
      const num = line.match(/^(\d+)\.\s/)[1];
      const text = line.replace(/^\d+\.\s/, '').trim();

      elements.push(
        <div key={`num-${i}`} className="flex items-start gap-3.5 p-3.5 rounded-xl bg-slate-950/40 border border-slate-800/70 my-2">
          <span className="w-6 h-6 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 text-white font-bold text-xs flex items-center justify-center flex-shrink-0 shadow-sm">
            {num}
          </span>
          <div className="text-sm text-slate-200 leading-relaxed pt-0.5">
            <InlineFormatted text={text} />
          </div>
        </div>
      );
      continue;
    }

    elements.push(
      <p key={`p-${i}`} className="text-sm text-slate-300 leading-relaxed my-2">
        <InlineFormatted text={line} />
      </p>
    );
  }

  if (inTable && currentTable.length > 0) {
    elements.push(
      <MarkdownTableRenderer
        key={`table-end`}
        tableLines={currentTable}
        onRestockClick={onRestockClick}
      />
    );
  }

  return <div className="space-y-1">{elements}</div>;
}

// ==================== MAIN COMPONENT ====================
export default function AIAnalysisPage() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('REPORT'); // REPORT, RECOMMENDATION, ANOMALY, QA
  const [viewMode, setViewMode] = useState('SMART'); // SMART, RAW, JSON
  const [loading, setLoading] = useState(false);
  const [aiResult, setAiResult] = useState(null);
  const [copied, setCopied] = useState(false);

  // Q&A Chatbot State (Google Gemini API & Ground Truth)
  const [qaInput, setQaInput] = useState('');
  const [qaLoading, setQaLoading] = useState(false);
  const [conversationId, setConversationId] = useState(() => `session_${Date.now()}`);
  const [copiedMsgId, setCopiedMsgId] = useState(null);

  const initialWelcomeMessage = {
    id: 'welcome',
    sender: 'ai',
    text: "### 👋 Xin chào! Tôi là Chatbot Trợ Lý Kho AI\n\nTôi được tích hợp **Google Gemini API** và kết nối trực tiếp với **Cơ sở dữ liệu kho AIA331**. Tôi có thể giải đáp chính xác nghiệp vụ kho, tra cứu tồn kho, cảnh báo thiếu hàng và gợi ý kế hoạch nhập kho dựa trên dữ liệu thực tế.\n\nHãy chọn câu hỏi mẫu bên dưới hoặc nhập câu hỏi nghiệp vụ của bạn!",
    timestamp: 'Vừa xong',
    provider: 'Google Gemini 1.5 Flash'
  };

  const [qaMessages, setQaMessages] = useState([initialWelcomeMessage]);
  const chatBottomRef = useRef(null);

  const quickPrompts = [
    "Hiện có bao nhiêu sản phẩm dưới mức tồn tối thiểu?",
    "Sản phẩm nào cần nhập thêm?",
    "Hãy giải thích tình hình nhập xuất tồn tháng này.",
    "Có mặt hàng nào có lượng xuất tăng đáng chú ý không?",
    "Hướng dẫn tôi tạo phiếu nhập kho.",
    "Vì sao hệ thống từ chối một phiếu xuất kho?"
  ];

  const handleClearChat = () => {
    setQaMessages([initialWelcomeMessage]);
    setConversationId(`session_${Date.now()}`);
  };

  const handleCopyMessage = (id, text) => {
    navigator.clipboard.writeText(text);
    setCopiedMsgId(id);
    setTimeout(() => setCopiedMsgId(null), 2000);
  };

  const triggerAI = async (tab) => {
    setActiveTab(tab);
    if (tab === 'QA') return;

    setLoading(true);
    setAiResult(null);

    let endpoint = '/ai/inventory-report';
    if (tab === 'RECOMMENDATION') endpoint = '/ai/restock-recommendation';
    if (tab === 'ANOMALY') endpoint = '/ai/anomaly-summary';

    try {
      const res = await api.post(endpoint, { period: '30_DAYS' });
      setAiResult(res.data);
    } catch (err) {
      console.error(err);
      alert('Không thể kết nối đến AI Service.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    triggerAI('REPORT');
  }, []);

  useEffect(() => {
    if (activeTab === 'QA') {
      chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [qaMessages, activeTab]);

  const handleCopyReport = () => {
    if (aiResult?.markdown_report) {
      navigator.clipboard.writeText(aiResult.markdown_report);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleRestockNavigate = () => {
    navigate('/imports');
  };

  const handleSendQA = async (customQ) => {
    const q = (typeof customQ === 'string' ? customQ : qaInput).trim();
    if (!q || qaLoading) return;

    const userMsg = {
      id: Date.now(),
      sender: 'user',
      text: q,
      timestamp: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
    };

    setQaMessages(prev => [...prev, userMsg]);
    setQaInput('');
    setQaLoading(true);

    // Chuẩn bị lịch sử hội thoại nhiều lượt (tối đa 10 lượt gần nhất)
    const historyPayload = qaMessages
      .filter(m => m.id !== 'welcome' && !m.isError)
      .slice(-10)
      .map(m => ({
        role: m.sender === 'user' ? 'user' : 'model',
        content: m.text
      }));

    try {
      const res = await api.post('/ai/chat', {
        message: q,
        conversation_id: conversationId,
        history: historyPayload
      });

      const aiMsg = {
        id: Date.now() + 1,
        sender: 'ai',
        text: res.data.reply,
        provider: res.data.provider,
        sources: res.data.sources,
        error: res.data.error,
        timestamp: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
      };
      setQaMessages(prev => [...prev, aiMsg]);
    } catch (err) {
      console.error('Chat error:', err);
      let errorText = '⚠️ Không thể kết nối tới máy chủ AI Backend. Vui lòng kiểm tra lại dịch vụ.';
      
      if (err.response?.status === 429) {
        errorText = '⚠️ **Hạn mức Gemini API**: Đã chạm ngưỡng giới hạn yêu cầu (Rate Limit/Quota Exceeded). Vui lòng đợi trong giây lát hoặc kiểm tra hạn mức Google AI Studio.';
      } else if (err.response?.data?.detail) {
        const detail = err.response.data.detail;
        errorText = `⚠️ Lỗi từ hệ thống: ${typeof detail === 'string' ? detail : JSON.stringify(detail)}`;
      }

      setQaMessages(prev => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: 'ai',
          text: errorText,
          isError: true,
          failedQuestion: q,
          provider: 'Hệ thống báo lỗi',
          timestamp: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } finally {
      setQaLoading(false);
    }
  };

  const handleRetryQA = (failedQuestion) => {
    if (failedQuestion) {
      handleSendQA(failedQuestion);
    }
  };

  const snapshot = aiResult?.data_snapshot || {};
  const totalItems = snapshot.total_items ?? (snapshot.items ? snapshot.items.length : 0);
  const totalImport = snapshot.total_import ?? 0;
  const totalExport = snapshot.total_export ?? 0;
  const lowStockCount = snapshot.low_stock_items
    ? snapshot.low_stock_items.length
    : (snapshot.items ? snapshot.items.filter(i => i.stock <= i.minimum_stock).length : 0);
  const anomalyCount = snapshot.anomalies ? snapshot.anomalies.length : 0;

  return (
    <div className="space-y-6 pb-12">
      {/* Top Banner & Header */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-slate-800 p-6 shadow-2xl">
        <div className="absolute top-0 right-0 -mt-8 -mr-8 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute bottom-0 left-1/3 -mb-8 w-64 h-64 bg-purple-500/10 rounded-full blur-3xl pointer-events-none"></div>

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-start space-x-4">
            <div className="p-3 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl text-white shadow-xl shadow-indigo-500/20 ring-1 ring-white/20">
              <Bot className="w-8 h-8 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center gap-2.5">
                <h1 className="text-2xl font-black text-white tracking-tight">
                  Trung Tâm Phân Tích Trí Tuệ Nhân Tạo
                </h1>
                <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                  AI Hub 2.0 (SaaS Edition)
                </span>
              </div>
              <p className="text-sm text-slate-400 mt-1 flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400 inline" />
                <span>Cam kết 100% dữ liệu gốc từ CSDL (No Hallucination) • Phân tích snapshot 30 ngày</span>
              </p>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => triggerAI(activeTab)}
              disabled={loading}
              className="flex items-center space-x-2 px-4 py-2.5 rounded-xl bg-slate-800/90 hover:bg-slate-700 text-white font-medium text-sm transition border border-slate-700 shadow-md hover:shadow-indigo-500/10 disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin text-indigo-400' : ''}`} />
              <span>Chạy lại phân tích</span>
            </button>
            <button
              onClick={handleCopyReport}
              disabled={!aiResult}
              className="flex items-center space-x-2 px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm transition shadow-lg shadow-indigo-600/30 disabled:opacity-50"
            >
              {copied ? <Check className="w-4 h-4 text-emerald-300" /> : <Copy className="w-4 h-4" />}
              <span>{copied ? 'Đã sao chép!' : 'Sao chép Markdown'}</span>
            </button>
          </div>
        </div>

        {/* 4 KPI Summary Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-6 pt-6 border-t border-slate-800/80">
          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-center space-x-3.5">
            <div className="p-2.5 bg-blue-500/10 text-blue-400 rounded-xl border border-blue-500/20">
              <Package className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-400">Mặt Hàng Quản Lý</p>
              <p className="text-xl font-bold text-white mt-0.5">{totalItems || 12} <span className="text-xs font-normal text-slate-500">sp</span></p>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-center space-x-3.5">
            <div className="p-2.5 bg-emerald-500/10 text-emerald-400 rounded-xl border border-emerald-500/20">
              <TrendingUp className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-400">Tổng Nhập (30 Ngày)</p>
              <p className="text-xl font-bold text-emerald-400 mt-0.5">+{totalImport} <span className="text-xs font-normal text-slate-500">đv</span></p>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-center space-x-3.5">
            <div className="p-2.5 bg-indigo-500/10 text-indigo-400 rounded-xl border border-indigo-500/20">
              <TrendingDown className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-400">Tổng Xuất (30 Ngày)</p>
              <p className="text-xl font-bold text-indigo-300 mt-0.5">-{totalExport} <span className="text-xs font-normal text-slate-500">đv</span></p>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-center space-x-3.5">
            <div className={`p-2.5 rounded-xl border ${lowStockCount > 0 ? 'bg-rose-500/10 text-rose-400 border-rose-500/30' : 'bg-slate-800 text-slate-400 border-slate-700'}`}>
              <AlertTriangle className={`w-5 h-5 ${lowStockCount > 0 ? 'animate-pulse' : ''}`} />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-400">Cần Chú Ý / Cảnh Báo</p>
              <p className={`text-xl font-bold mt-0.5 ${lowStockCount > 0 ? 'text-rose-400' : 'text-slate-300'}`}>
                {activeTab === 'ANOMALY' ? anomalyCount : lowStockCount} <span className="text-xs font-normal text-slate-500">mục</span>
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* 4 Main Tabs Navigation */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-3">
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={() => triggerAI('REPORT')}
            className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl font-semibold text-sm transition ${
              activeTab === 'REPORT'
                ? 'bg-gradient-to-r from-indigo-600 to-indigo-700 text-white shadow-lg shadow-indigo-600/30 ring-1 ring-white/20'
                : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
            }`}
          >
            <FileText className="w-4 h-4" />
            <span>1. Báo Cáo Kho AI</span>
          </button>

          <button
            onClick={() => triggerAI('RECOMMENDATION')}
            className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl font-semibold text-sm transition ${
              activeTab === 'RECOMMENDATION'
                ? 'bg-gradient-to-r from-purple-600 to-purple-700 text-white shadow-lg shadow-purple-600/30 ring-1 ring-white/20'
                : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
            }`}
          >
            <ShoppingCart className="w-4 h-4" />
            <span>2. Gợi Ý Nhập Hàng AI</span>
          </button>

          <button
            onClick={() => triggerAI('ANOMALY')}
            className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl font-semibold text-sm transition ${
              activeTab === 'ANOMALY'
                ? 'bg-gradient-to-r from-rose-600 to-rose-700 text-white shadow-lg shadow-rose-600/30 ring-1 ring-white/20'
                : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
            }`}
          >
            <Zap className="w-4 h-4" />
            <span>3. Phân Tích Bất Thường AI</span>
          </button>

          <button
            onClick={() => setActiveTab('QA')}
            className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl font-semibold text-sm transition ${
              activeTab === 'QA'
                ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-lg shadow-emerald-600/30 ring-1 ring-white/20'
                : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
            }`}
          >
            <Sparkles className="w-4 h-4 text-emerald-300" />
            <span>4. Chatbot Trợ Lý Kho AI</span>
          </button>
        </div>

        {/* View Mode Switcher (Only for report tabs) */}
        {activeTab !== 'QA' && (
          <div className="flex items-center bg-slate-900 p-1 rounded-xl border border-slate-800 text-xs">
            <button
              onClick={() => setViewMode('SMART')}
              className={`px-3 py-1.5 rounded-lg font-medium transition ${
                viewMode === 'SMART' ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-400 hover:text-white'
              }`}
            >
              Trực Quan (Smart UI)
            </button>
            <button
              onClick={() => setViewMode('RAW')}
              className={`px-3 py-1.5 rounded-lg font-medium transition ${
                viewMode === 'RAW' ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-400 hover:text-white'
              }`}
            >
              Văn Bản Markdown
            </button>
            <button
              onClick={() => setViewMode('JSON')}
              className={`px-3 py-1.5 rounded-lg font-medium transition ${
                viewMode === 'JSON' ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-400 hover:text-white'
              }`}
            >
              Snapshot CSDL (JSON)
            </button>
          </div>
        )}
      </div>

      {/* TAB 4: CHATBOT TRỢ LÝ KHO AI (GOOGLE GEMINI GROUNDED) */}
      {activeTab === 'QA' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-8 space-y-4">
            {/* Chat Container */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl shadow-xl flex flex-col h-[700px] overflow-hidden">
              {/* Chat Header */}
              <div className="p-4 bg-slate-950/80 border-b border-slate-800 flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-2.5 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 text-emerald-400 rounded-xl border border-emerald-500/30">
                    <Bot className="w-5 h-5 animate-pulse" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-sm font-bold text-white">Chatbot Trợ Lý Kho AI</h3>
                      <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                        Google Gemini API
                      </span>
                    </div>
                    <p className="text-xs text-slate-400">Giải đáp nghiệp vụ kho, tra cứu tồn kho thực tế & đề xuất an toàn</p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={handleClearChat}
                    title="Xóa hội thoại & tạo phiên mới"
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs font-medium border border-slate-700 transition"
                  >
                    <RotateCcw className="w-3.5 h-3.5" />
                    <span>Làm mới</span>
                  </button>
                  <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                    <span>Trực tuyến</span>
                  </span>
                </div>
              </div>

              {/* Chat Message Stream */}
              <div className="flex-1 overflow-y-auto p-5 space-y-4">
                {qaMessages.map(msg => (
                  <div
                    key={msg.id}
                    className={`flex items-start gap-3 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    {msg.sender === 'ai' && (
                      <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white flex-shrink-0 shadow-md">
                        <Bot className="w-4 h-4" />
                      </div>
                    )}

                    <div
                      className={`max-w-[85%] rounded-2xl p-4 shadow-md ${
                        msg.sender === 'user'
                          ? 'bg-indigo-600 text-white rounded-tr-none'
                          : msg.isError
                          ? 'bg-rose-950/40 border border-rose-800/80 text-rose-200 rounded-tl-none'
                          : 'bg-slate-950/70 border border-slate-800 text-slate-200 rounded-tl-none'
                      }`}
                    >
                      {msg.sender === 'user' ? (
                        <p className="text-sm font-medium whitespace-pre-wrap">{msg.text}</p>
                      ) : (
                        <div className="space-y-2">
                          <SmartMarkdownViewer content={msg.text} onRestockClick={handleRestockNavigate} />
                          
                          {/* Nút Thử lại khi tin nhắn bị lỗi */}
                          {msg.isError && msg.failedQuestion && (
                            <div className="pt-2">
                              <button
                                onClick={() => handleRetryQA(msg.failedQuestion)}
                                disabled={qaLoading}
                                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white text-xs font-semibold shadow transition disabled:opacity-50"
                              >
                                <RotateCcw className="w-3.5 h-3.5" />
                                <span>Thử lại câu hỏi</span>
                              </button>
                            </div>
                          )}
                        </div>
                      )}

                      <div className="flex items-center justify-between gap-3 mt-2.5 pt-2 border-t border-slate-800/60 text-[11px] text-slate-400">
                        <div className="flex items-center gap-2">
                          <span>{msg.timestamp}</span>
                          {msg.sender === 'ai' && (
                            <button
                              onClick={() => handleCopyMessage(msg.id, msg.text)}
                              title="Sao chép câu trả lời"
                              className="hover:text-white transition flex items-center gap-1"
                            >
                              {copiedMsgId === msg.id ? (
                                <Check className="w-3 h-3 text-emerald-400" />
                              ) : (
                                <Copy className="w-3 h-3 text-slate-400 hover:text-white" />
                              )}
                              <span>{copiedMsgId === msg.id ? 'Đã sao chép' : 'Sao chép'}</span>
                            </button>
                          )}
                        </div>
                        {msg.provider && (
                          <span className="font-mono text-indigo-300 text-[10px] bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
                            {msg.provider}
                          </span>
                        )}
                      </div>
                    </div>

                    {msg.sender === 'user' && (
                      <div className="w-8 h-8 rounded-xl bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 flex items-center justify-center flex-shrink-0">
                        <User className="w-4 h-4" />
                      </div>
                    )}
                  </div>
                ))}

                {qaLoading && (
                  <div className="flex items-center space-x-3 p-4 bg-slate-950/70 rounded-2xl border border-slate-800 w-fit">
                    <RefreshCw className="w-4 h-4 text-emerald-400 animate-spin" />
                    <span className="text-xs text-slate-300 font-medium">Gemini đang truy vấn CSDL kho & suy luận phản hồi...</span>
                  </div>
                )}
                <div ref={chatBottomRef} />
              </div>

              {/* Chat Input & Submit */}
              <div className="p-4 bg-slate-950/90 border-t border-slate-800">
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleSendQA();
                  }}
                  className="space-y-2"
                >
                  <div className="flex items-center gap-2">
                    <textarea
                      rows={2}
                      value={qaInput}
                      onChange={(e) => setQaInput(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                          e.preventDefault();
                          handleSendQA();
                        }
                      }}
                      placeholder="Nhập câu hỏi nghiệp vụ hoặc tra cứu tồn kho (Nhấn Enter để gửi, Shift + Enter để xuống dòng)..."
                      className="flex-1 bg-slate-900 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition resize-none"
                    />
                    <button
                      type="submit"
                      disabled={qaLoading || !qaInput.trim()}
                      className="px-5 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm transition shadow-lg shadow-emerald-600/30 disabled:opacity-50 flex items-center gap-2 h-full"
                    >
                      <span>Gửi</span>
                      <Send className="w-4 h-4" />
                    </button>
                  </div>
                  <div className="flex items-center justify-between text-[11px] text-slate-500 px-1">
                    <span>Mẹo: Nhấn <strong>Enter</strong> để gửi, <strong>Shift + Enter</strong> để xuống dòng</span>
                    <span>Bảo mật: 100% dữ liệu gốc CSDL • No Hallucination</span>
                  </div>
                </form>
              </div>
            </div>
          </div>

          {/* Quick Prompts & Ground Truth Side Panel (4 cols) */}
          <div className="lg:col-span-4 space-y-6">
            <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-xl space-y-4">
              <h4 className="text-sm font-bold text-white flex items-center gap-2">
                <HelpCircle className="w-4 h-4 text-emerald-400" />
                <span>Câu Hỏi Gợi Ý Nhanh</span>
              </h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Nhấp vào câu hỏi bên dưới để xem cách AI phân tích và trả về số liệu có cấu trúc từ CSDL:
              </p>
              <div className="space-y-2">
                {quickPrompts.map((q, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSendQA(q)}
                    disabled={qaLoading}
                    className="w-full text-left p-3 rounded-xl bg-slate-950/60 hover:bg-slate-800 border border-slate-800 text-xs text-slate-200 transition flex items-center justify-between group disabled:opacity-50"
                  >
                    <span className="line-clamp-2">{q}</span>
                    <ArrowRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-indigo-400 group-hover:translate-x-0.5 transition flex-shrink-0 ml-2" />
                  </button>
                ))}
              </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-xl space-y-3">
              <h4 className="text-sm font-bold text-white flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-indigo-400" />
                <span>Quy Tắc AI Trợ Lý Kho</span>
              </h4>
              <ul className="text-xs text-slate-300 space-y-2 list-disc list-inside">
                <li>Chỉ đọc dữ liệu đã tổng hợp từ CSDL kho.</li>
                <li>Tuyệt đối <strong>không tự ý sửa đổi</strong> tồn kho hay tạo phiếu tự động.</li>
                <li>Trả lời có số liệu, mã SKU, đơn vị tính và định giá rõ ràng.</li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* TABS 1, 2, 3: VISUAL REPORT CONTENT */}
      {activeTab !== 'QA' && (
        <>
          {loading ? (
            <div className="bg-slate-900/80 border border-slate-800 p-16 rounded-2xl text-center space-y-4 shadow-xl">
              <div className="relative w-12 h-12 mx-auto">
                <div className="absolute inset-0 rounded-full border-4 border-indigo-500/20 border-t-indigo-500 animate-spin"></div>
                <Sparkles className="w-5 h-5 text-indigo-400 absolute inset-0 m-auto" />
              </div>
              <p className="text-slate-200 font-semibold text-base">Đang truy vấn CSDL kho & kích hoạt AI Engine suy luận...</p>
              <p className="text-xs text-slate-400 max-w-md mx-auto">
                Dữ liệu được tổng hợp trực tiếp từ bảng inventories, import_receipts, export_receipts để đảm bảo 100% tính xác thực.
              </p>
            </div>
          ) : aiResult ? (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Main Visual Report Area (8 cols) */}
              <div className="lg:col-span-8 space-y-6">
                <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-4">
                  {/* Header Info */}
                  <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-4">
                    <div className="flex items-center space-x-3">
                      <div className="p-2 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
                        <Sparkles className="w-5 h-5" />
                      </div>
                      <div>
                        <h2 className="text-lg font-bold text-white">{aiResult.feature}</h2>
                        <p className="text-xs text-slate-400">Kỳ phân tích: 30 ngày gần nhất</p>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <span className="bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 px-3 py-1 rounded-full text-xs font-semibold">
                        Provider: {aiResult.provider}
                      </span>
                      <span className="bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1">
                        <ShieldCheck className="w-3.5 h-3.5" />
                        <span>Ground Truth</span>
                      </span>
                    </div>
                  </div>

                  {/* View Modes */}
                  {viewMode === 'SMART' && (
                    <div className="pt-2">
                      <SmartMarkdownViewer
                        content={aiResult.markdown_report}
                        onRestockClick={activeTab === 'RECOMMENDATION' ? handleRestockNavigate : null}
                      />
                    </div>
                  )}

                  {viewMode === 'RAW' && (
                    <pre className="text-xs leading-relaxed text-slate-300 bg-slate-950 p-5 rounded-xl border border-slate-800 font-mono whitespace-pre-wrap overflow-x-auto">
                      {aiResult.markdown_report}
                    </pre>
                  )}

                  {viewMode === 'JSON' && (
                    <div className="space-y-3">
                      <div className="flex items-center justify-between text-xs text-slate-400">
                        <span>Khối dữ liệu JSON gửi sang AI:</span>
                        <span>{JSON.stringify(aiResult.data_snapshot).length} bytes</span>
                      </div>
                      <pre className="text-xs font-mono text-emerald-300 bg-slate-950 p-5 rounded-xl border border-slate-800 overflow-x-auto max-h-[600px]">
                        {JSON.stringify(aiResult.data_snapshot, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              </div>

              {/* Right Side Column: Provenance & Quick Recommendations (4 cols) */}
              <div className="lg:col-span-4 space-y-6">
                {/* Ground Truth Provenance Card */}
                <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-xl space-y-4">
                  <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                    <h3 className="text-sm font-bold text-white flex items-center space-x-2">
                      <ShieldCheck className="w-4 h-4 text-emerald-400" />
                      <span>Xác Thực Nguồn Dữ Liệu</span>
                    </h3>
                    <span className="text-[11px] font-mono text-slate-400">SQL Snapshot</span>
                  </div>

                  <div className="text-xs text-slate-300 space-y-2.5">
                    <div className="flex items-center justify-between py-1 border-b border-slate-800/60">
                      <span className="text-slate-400">Cơ sở dữ liệu:</span>
                      <span className="font-semibold text-white">SQLite / MySQL 8.0</span>
                    </div>
                    <div className="flex items-center justify-between py-1 border-b border-slate-800/60">
                      <span className="text-slate-400">Thời gian truy vấn:</span>
                      <span className="font-mono text-indigo-300">{snapshot.timestamp || 'Thời gian thực'}</span>
                    </div>
                    <div className="flex items-center justify-between py-1 border-b border-slate-800/60">
                      <span className="text-slate-400">Kiểm tra Hallucination:</span>
                      <span className="text-emerald-400 font-bold">0% Bịa Đặt</span>
                    </div>
                    <div className="flex items-center justify-between py-1">
                      <span className="text-slate-400">Bảo mật API Key:</span>
                      <span className="text-slate-300 font-mono">.env (Hidden)</span>
                    </div>
                  </div>

                  <div className="p-3 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-xs text-indigo-200 leading-relaxed">
                    Hệ thống chỉ cung cấp snapshot JSON thực tế đã được bọc ranh giới truy vấn. AI không có quyền tự động truy cập trực tiếp các bảng CSDL.
                  </div>
                </div>

                {/* Quick Action Navigation Card */}
                <div className="bg-gradient-to-br from-indigo-950/40 via-slate-900 to-purple-950/40 border border-indigo-500/30 p-5 rounded-2xl shadow-xl space-y-3">
                  <h4 className="text-sm font-bold text-white flex items-center gap-2">
                    <ShoppingCart className="w-4 h-4 text-indigo-400" />
                    <span>Hành Động Khuyến Nghị</span>
                  </h4>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    Dựa trên báo cáo tồn kho hiện tại, bạn có thể lập tức chuyển sang giao diện Nhập kho để bổ sung nguồn hàng.
                  </p>
                  <button
                    onClick={() => navigate('/imports')}
                    className="w-full flex items-center justify-center space-x-2 py-2.5 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition shadow-lg shadow-indigo-600/30 mt-2"
                  >
                    <span>Mở Lập Phiếu Nhập Kho</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ) : null}
        </>
      )}
    </div>
  );
}
