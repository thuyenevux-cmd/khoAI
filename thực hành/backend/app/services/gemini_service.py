import os
import json
import logging
import uuid
from typing import Dict, Any, List, Tuple, Optional
import httpx

from app.core.config import settings
from app.schemas.chatbot import ChatMessageTurn

logger = logging.getLogger(__name__)

class GeminiChatbotService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY.strip() if settings.GEMINI_API_KEY else ""
        self.model = settings.GEMINI_MODEL.strip() if settings.GEMINI_MODEL else "gemini-1.5-flash"
        self.timeout = settings.GEMINI_TIMEOUT_SECONDS

    def _load_system_prompt(self) -> str:
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "warehouse_assistant.txt")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        return (
            "Bạn là Trợ lý AI Quản Lý Kho thông minh (Warehouse AI Assistant).\n"
            "Chỉ trả lời dựa trên dữ liệu kho thực tế được cung cấp trong JSON. Không bịa số liệu."
        )

    def chat(
        self,
        message: str,
        grounding_data: Dict[str, Any],
        history: Optional[List[ChatMessageTurn]] = None,
        conversation_id: Optional[str] = None
    ) -> Tuple[str, str, Optional[str]]:
        """
        Gửi yêu cầu đến Gemini API hoặc chuyển sang Rule Engine nếu chưa có API Key / gặp lỗi.
        Trả về tuple: (reply_markdown, provider_name, error_message_if_any)
        """
        session_id = conversation_id or str(uuid.uuid4())
        history = history or []

        # 1. Kiểm tra cấu hình API Key
        if not self.api_key or len(self.api_key) < 15:
            fallback_text = self._generate_fallback_answer(message, grounding_data)
            notice = (
                "> [!NOTE]\n"
                "> Hệ thống đang chạy ở chế độ **Engine AI Nội Bộ (Ground Truth)** do biến môi trường "
                "`GEMINI_API_KEY` chưa được cấu hình trong file `.env`.\n\n"
            )
            return (
                notice + fallback_text,
                "Engine AI Nội Bộ (Chưa cấu hình GEMINI_API_KEY)",
                "GEMINI_API_KEY chưa được cấu hình. Đang dùng fallback nội bộ."
            )

        # 2. Xây dựng prompt kèm ngữ cảnh CSDL
        system_prompt = self._load_system_prompt()
        grounded_user_prompt = (
            f"Dữ liệu kho thực tế từ CSDL backend (Ground Truth):\n"
            f"```json\n{json.dumps(grounding_data, ensure_ascii=False, indent=2)}\n```\n\n"
            f"Câu hỏi của người dùng: \"{message}\"\n"
            f"Hãy trả lời chính xác, mạch lạc, sử dụng bảng hoặc bullet points rõ ràng."
        )

        # 3. Thử gọi qua official google-genai SDK hoặc httpx REST
        try:
            return self._call_gemini_api(system_prompt, grounded_user_prompt, history)
        except Exception as exc:
            err_str = str(exc)
            logger.warning(f"[Gemini Service Warning] Call failed: {err_str}. Fallback to internal engine.")
            
            fallback_ans = self._generate_fallback_answer(message, grounding_data)

            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "quota" in err_str.lower():
                err_msg = "Google Gemini API đã chạm giới hạn hạn mức (HTTP 429 Quota Exceeded)."
                notice = (
                    "> [!WARNING]\n"
                    "> **Google Gemini API**: Đã chạm giới hạn hạn mức yêu cầu (Rate Limit/Quota Exceeded). "
                    "Hệ thống đã tự động kích hoạt **Engine AI Nội Bộ** để trả lời chính xác dựa trên CSDL.\n\n"
                )
                return notice + fallback_ans, "Engine AI Nội Bộ (Quota Exceeded Fallback)", err_msg

            if "timeout" in err_str.lower() or "timed out" in err_str.lower():
                err_msg = f"Gemini API phản hồi quá thời gian quy định ({self.timeout}s)."
                notice = (
                    "> [!WARNING]\n"
                    "> **Gemini API**: Yêu cầu bị quá thời gian (Timeout). "
                    "Hệ thống tự động sử dụng Engine AI Nội Bộ để phản hồi ngay lập tức.\n\n"
                )
                return notice + fallback_ans, "Engine AI Nội Bộ (Timeout Fallback)", err_msg

            # Lỗi mạng hoặc lỗi model khác
            err_msg = f"Lỗi kết nối Gemini API: {type(exc).__name__}"
            notice = (
                "> [!WARNING]\n"
                "> Không thể hoàn tất yêu cầu tới Gemini API. "
                "Hệ thống tự động sử dụng Engine AI Nội Bộ để phân tích dữ liệu.\n\n"
            )
            return notice + fallback_ans, "Engine AI Nội Bộ (API Connection Fallback)", err_msg

    def _call_gemini_api(
        self,
        system_instruction: str,
        current_prompt: str,
        history: List[ChatMessageTurn]
    ) -> Tuple[str, str, Optional[str]]:
        """Gọi Gemini API thông qua SDK google-genai với fallback httpx REST."""
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            
            # Xây dựng lịch sử đối thoại
            contents = []
            for turn in history:
                role = "user" if turn.role == "user" else "model"
                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=turn.content)]
                    )
                )
            
            # Thêm prompt hiện tại
            contents.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=current_prompt)]
                )
            )

            response = client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.2,
                )
            )

            if response and response.text:
                return response.text.strip(), f"Google Gemini API ({self.model})", None
            else:
                raise ValueError("Gemini API trả về nội dung rỗng (Empty Response).")

        except ImportError:
            # Fallback sang HTTP REST trực tiếp nếu môi trường chưa nạp SDK
            return self._call_gemini_rest(system_instruction, current_prompt, history)
        except Exception as e:
            # Nếu lỗi là do SDK method signature, thử lại qua REST API chuẩn
            if "unexpected keyword argument" in str(e).lower() or "module" in str(e).lower():
                return self._call_gemini_rest(system_instruction, current_prompt, history)
            raise e

    def _call_gemini_rest(
        self,
        system_instruction: str,
        current_prompt: str,
        history: List[ChatMessageTurn]
    ) -> Tuple[str, str, Optional[str]]:
        """Gọi REST API chính thức của Gemini thông qua httpx."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

        contents = []
        for turn in history:
            role = "user" if turn.role == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": turn.content}]
            })
        
        contents.append({
            "role": "user",
            "parts": [{"text": current_prompt}]
        })

        payload = {
            "contents": contents,
            "systemInstruction": {
                "parts": [{"text": system_instruction}]
            },
            "generationConfig": {
                "temperature": 0.2
            }
        }

        with httpx.Client(timeout=float(self.timeout)) as client:
            res = client.post(url, json=payload)
            if res.status_code == 200:
                data = res.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        return parts[0]["text"].strip(), f"Google Gemini API ({self.model})", None
                raise ValueError("Gemini API REST trả về định dạng rỗng.")
            else:
                raise RuntimeError(f"HTTP {res.status_code}: {res.text}")

    # ==================== DETERMINISTIC FALLBACK ENGINE ====================
    def _generate_fallback_answer(self, question: str, data: Dict[str, Any]) -> str:
        """
        Bộ sinh câu trả lời dự phòng dựa 100% trên dữ liệu đối chứng của CSDL kho.
        Không hallucination. Trả về Markdown đẹp với bảng và số liệu cụ thể.
        """
        q = question.lower().strip()

        # 1. Hướng dẫn nghiệp vụ
        if "tạo phiếu nhập" in q or ("hướng dẫn" in q and "nhập" in q):
            guide = data.get("business_guidelines", {}).get("huong_dan_tao_phieu_nhap", [])
            lines = "\n".join(f"- {step}" for step in guide) if guide else "Vào mục Nhập Kho -> Bấm Tạo Phiếu Nhập."
            return (
                "### 📝 Hướng Dẫn Quy Trình Tạo Phiếu Nhập Kho\n\n"
                f"{lines}\n\n"
                "💡 **Lưu ý**: Sau khi lưu phiếu, tồn kho khả dụng của sản phẩm sẽ lập tức được cộng dồn."
            )

        if "từ chối" in q or "không đủ" in q or ("tại sao" in q and "xuất" in q):
            reasons = data.get("business_guidelines", {}).get("nguyen_nhan_tu_choi_xuat_kho", [])
            lines = "\n".join(f"- {r}" for r in reasons) if reasons else "Không đủ số lượng xuất kho hoặc hàng đã khóa."
            return (
                "### 🛑 Các Nguyên Nhân Hệ Thống Từ Chối Phiếu Xuất Kho\n\n"
                f"{lines}\n\n"
                "👉 **Khuyến nghị**: Hãy kiểm tra lại số lượng tồn kho khả dụng trước khi lập phiếu xuất."
            )

        # 2. Tra cứu mặt hàng cụ thể
        specific = data.get("product_search_results", [])
        if specific:
            md = f"### 📦 Kết Quả Tra Cứu Tồn Kho ({len(specific)} sản phẩm tìm thấy)\n\n"
            md += "| Mã SKU | Tên sản phẩm | Tồn hiện tại | Ngưỡng an toàn | Giá tham khảo | Tốc độ xuất | Tình trạng |\n"
            md += "| :--- | :--- | :---: | :---: | :---: | :---: | :--- |\n"
            for p in specific:
                status = "🔴 Hết hàng" if p["current_stock"] == 0 else ("🟡 Dưới tồn tối thiểu" if p["is_low_stock"] else "🟢 An toàn")
                md += (
                    f"| `{p['code']}` | **{p['name']}** | **{p['current_stock']} {p['unit']}** | "
                    f"{p['minimum_stock']} | {p['latest_price_vnd']:,} đ | {p['burn_rate_per_day']} sp/ngày | {status} |\n"
                )
            
            p0 = specific[0]
            md += f"\n💡 **Tổng giá trị lưu kho ước tính** cho `{p0['code']}`: **{p0['estimated_total_value_vnd']:,} VNĐ**."
            
            # Xử lý câu hỏi giả định nếu có (ví dụ "nếu xuất thêm X")
            import re
            m = re.search(r'nếu\s+xuất(?:\s+thêm)?\s+(\d+)', q)
            if m:
                hypo_qty = int(m.group(1))
                rem = p0["current_stock"] - hypo_qty
                if rem >= 0:
                    md += (
                        f"\n\n🔢 **Tính toán giả định**: Nếu xuất thêm **{hypo_qty} {p0['unit']}**, "
                        f"số lượng còn lại trên lý thuyết sẽ là **{rem} {p0['unit']}**.\n"
                        f"*Lưu ý: Đây chỉ là tính toán mô phỏng, tồn kho thực tế trong CSDL KHÔNG hề bị thay đổi.*"
                    )
                else:
                    md += (
                        f"\n\n⚠️ **Cảnh báo tính toán giả định**: Hiện chỉ còn **{p0['current_stock']} {p0['unit']}**, "
                        f"không đủ để xuất **{hypo_qty} {p0['unit']}** (Thiếu {abs(rem)} đơn vị)."
                    )
            return md

        # 3. Sản phẩm dưới tồn tối thiểu / sắp hết
        if any(w in q for w in ["sắp hết", "hết hàng", "cảnh báo", "tối thiểu", "cần nhập", "nhập thêm"]):
            low_items = data.get("low_stock_alert_items", [])
            if not low_items:
                return (
                    "### ✅ Trạng Thái Tồn Kho An Toàn\n\n"
                    "Hiện tại toàn bộ sản phẩm trong kho đều đang duy trì mức tồn trên ngưỡng an toàn tối thiểu. "
                    "Không có mặt hàng nào bị hết hàng."
                )
            md = f"### ⚠️ Danh Sách Mặt Hàng Cần Nhập Thêm (Có {len(low_items)} sản phẩm dưới mức an toàn)\n\n"
            md += "| Mã SKU | Tên sản phẩm | Tồn hiện tại | Ngưỡng an toàn | Đã xuất 30 ngày | Trạng thái |\n"
            md += "| :--- | :--- | :---: | :---: | :---: | :--- |\n"
            for item in low_items:
                st = "🔴 Hết hàng" if item["current_stock"] == 0 else "🟡 Dưới tồn tối thiểu"
                md += f"| `{item['code']}` | **{item['name']}** | **{item['current_stock']} {item['unit']}** | {item['minimum_stock']} | {item['export_30_days']} | {st} |\n"
            md += "\n👉 **Hành động đề xuất**: Hãy vào mục **Nhập Kho** để lập phiếu nhập khẩn cấp cho các mặt hàng trên."
            return md

        # 4. Top hàng xuất chạy
        if any(w in q for w in ["bán chạy", "xuất nhiều", "top xuất", "chạy nhất"]):
            top_items = data.get("top_exported_products", [])
            if not top_items:
                return "Chưa ghi nhận dữ liệu xuất kho trong khoảng thời gian này."
            md = "### 🔥 Top Mặt Hàng Có Lượng Xuất Kho Cao Nhất (30 Ngày Qua)\n\n"
            md += "| Xếp hạng | Mã SKU | Tên sản phẩm | Số lượng đã xuất | Tồn kho hiện tại | Tốc độ xuất |\n"
            md += "| :---: | :--- | :--- | :---: | :---: | :---: |\n"
            for idx, item in enumerate(top_items, 1):
                md += f"| #{idx} | `{item['code']}` | **{item['name']}** | **{item['exported_quantity']} {item['unit']}** | {item['current_stock']} | {item['burn_rate_per_day']} sp/ngày |\n"
            return md

        # 5. Tóm tắt định giá / tổng quan
        summary = data.get("warehouse_summary_30_days", {})
        if summary:
            return (
                f"### 📊 Báo Cáo Tổng Quan Tồn Kho ({summary.get('period', 'Hiện tại')})\n\n"
                f"- **Tổng số danh mục sản phẩm**: **{summary.get('total_products_managed', 0)}** mặt hàng\n"
                f"- **Tổng số lượng đơn vị trong kho**: **{summary.get('total_units_in_stock', 0):,}** sản phẩm\n"
                f"- **Tổng giá trị lưu kho ước tính**: **{summary.get('estimated_inventory_valuation_vnd', 0):,} VNĐ**\n"
                f"- **Số sản phẩm dưới mức an toàn**: **{summary.get('low_stock_product_count', 0)}** mặt hàng\n"
                f"- **Tổng lượng nhập 30 ngày**: **{summary.get('total_imported_quantity', 0):,}** đơn vị\n"
                f"- **Tổng lượng xuất 30 ngày**: **{summary.get('total_exported_quantity', 0):,}** đơn vị\n\n"
                "💡 Bạn có thể hỏi chi tiết hơn, ví dụ: *\"Sản phẩm nào cần nhập thêm?\"* hoặc *\"Kho còn bao nhiêu bàn phím?\"*."
            )

        return (
            "### 🤖 Trợ Lý Kho AI Đã Nhận Câu Hỏi\n\n"
            "Dữ liệu trong hệ thống hiện tại chưa đủ để phản hồi chi tiết cho câu hỏi này. "
            "Bạn hãy thử tra cứu theo các mẫu sau:\n"
            "- *\"Sản phẩm nào đang dưới mức tồn tối thiểu?\"*\n"
            "- *\"Kho còn bao nhiêu bàn phím cơ AKKO?\"*\n"
            "- *\"Tổng giá trị tồn kho là bao nhiêu?\"*\n"
            "- *\"Hướng dẫn tôi tạo phiếu nhập kho.\"*\n"
            "- *\"Vì sao hệ thống từ chối một phiếu xuất kho?\"*"
        )

gemini_chatbot_service = GeminiChatbotService()
