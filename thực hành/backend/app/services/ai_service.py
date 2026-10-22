import os
import json
from typing import Dict, Any, Tuple
from app.core.config import settings

class AIService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL

    def _load_prompt_template(self, filename: str) -> str:
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", filename)
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    def generate_inventory_report(self, data_snapshot: Dict[str, Any]) -> Tuple[str, str]:
        system_prompt = self._load_prompt_template("inventory_report.txt")
        user_prompt = f"Dữ liệu nhập xuất tồn kho thực tế từ CSDL:\n```json\n{json.dumps(data_snapshot, ensure_ascii=False, indent=2)}\n```\nHãy lập báo cáo kho theo đúng hướng dẫn hệ thống."

        if self.api_key and len(self.api_key.strip()) > 10:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=self.api_key)
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2
                )
                return response.choices[0].message.content, "OpenAI API (" + self.model + ")"
            except Exception as e:
                print(f"[AI Service Warning] OpenAI call failed: {e}. Falling back to Rule Engine.")

        # Offline Rule Engine Fallback (Strictly reading input JSON)
        report_md = self._rule_engine_inventory_report(data_snapshot)
        return report_md, "Engine AI Nội Bộ (Strict JSON Analyzer)"

    def generate_restock_recommendations(self, data_snapshot: Dict[str, Any]) -> Tuple[str, str]:
        system_prompt = self._load_prompt_template("stock_recommendation.txt")
        user_prompt = f"Dữ liệu tồn kho và tình hình xuất hàng:\n```json\n{json.dumps(data_snapshot, ensure_ascii=False, indent=2)}\n```\nHãy đưa ra danh sách gợi ý nhập hàng."

        if self.api_key and len(self.api_key.strip()) > 10:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=self.api_key)
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2
                )
                return response.choices[0].message.content, "OpenAI API (" + self.model + ")"
            except Exception as e:
                print(f"[AI Service Warning] OpenAI call failed: {e}. Falling back to Rule Engine.")

        recommendation_md = self._rule_engine_restock_recommendation(data_snapshot)
        return recommendation_md, "Engine AI Nội Bộ (Strict JSON Analyzer)"

    def generate_anomaly_summary(self, data_snapshot: Dict[str, Any]) -> Tuple[str, str]:
        system_prompt = self._load_prompt_template("anomaly_detection.txt")
        user_prompt = f"Dữ liệu biến động kho:\n```json\n{json.dumps(data_snapshot, ensure_ascii=False, indent=2)}\n```\nHãy tóm tắt điểm bất thường."

        if self.api_key and len(self.api_key.strip()) > 10:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=self.api_key)
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2
                )
                return response.choices[0].message.content, "OpenAI API (" + self.model + ")"
            except Exception as e:
                print(f"[AI Service Warning] OpenAI call failed: {e}. Falling back to Rule Engine.")

        anomaly_md = self._rule_engine_anomaly_detection(data_snapshot)
        return anomaly_md, "Engine AI Nội Bộ (Strict JSON Analyzer)"

    # --- Rule Engine Fallback Implementations (Reading ONLY DB JSON Snapshot) ---

    def _rule_engine_inventory_report(self, snapshot: Dict[str, Any]) -> str:
        total = snapshot.get("total_items", 0)
        total_imp = snapshot.get("total_import", 0)
        total_exp = snapshot.get("total_export", 0)
        low_items = snapshot.get("low_stock_items", [])

        md = f"### 📊 Tình Trạng Tổng Quan Kho ({snapshot.get('period', 'Kỳ báo cáo')})\n\n"
        md += f"- **Tổng số mặt hàng quản lý**: {total} sản phẩm\n"
        md += f"- **Tổng số lượng nhập trong kỳ**: {total_imp} đơn vị\n"
        md += f"- **Tổng số lượng xuất trong kỳ**: {total_exp} đơn vị\n"
        md += f"- **Số lượng mặt hàng dưới tồn tối thiểu**: {len(low_items)} sản phẩm\n\n"

        md += "### ⚠️ Các Mặt Hàng Cần Chú Ý (Dưới Tồn Tối Thiểu / Cảnh Báo)\n\n"
        if low_items:
            md += "| Mã hàng | Tên sản phẩm | Tồn hiện tại | Tồn tối thiểu | Lượng xuất 30 ngày | Trạng thái |\n"
            md += "| :--- | :--- | :---: | :---: | :---: | :--- |\n"
            for item in low_items:
                status = "🔴 Hết hàng" if item['stock'] == 0 else "🟡 Dưới tồn tối thiểu"
                md += f"| {item['code']} | {item['name']} | **{item['stock']}** | {item['minimum_stock']} | {item['export_30_days']} | {status} |\n"
        else:
            md += "Tất cả mặt hàng đều đảm bảo mức tồn kho an toàn.\n"

        md += "\n### ⚡ Các Điểm Bất Thường & Biến Động Xuất Nhập\n\n"
        high_exp = [i for i in low_items if i.get("export_30_days", 0) > 20]
        if high_exp:
            for i in high_exp:
                md += f"- 💥 **{i['name']} ({i['code']})**: Có tốc độ xuất cao ({i['export_30_days']} sản phẩm/30 ngày) trong khi tồn kho hiện tại chỉ còn **{i['stock']}** (dưới mức tối thiểu {i['minimum_stock']}). Cần xử lý ngay tránh đứt gãy cung ứng.\n"
        else:
            md += "- Chưa phát hiện biến động xuất kho bất thường trong kỳ.\n"

        md += "\n### 💡 Khuyến Nghị Vận Hành\n\n"
        if low_items:
            md += "1. Lập phiếu nhập kho ưu tiên cho các sản phẩm đang hết hàng hoặc dưới mức tối thiểu.\n"
            md += "2. Kiểm tra lại kế hoạch mua hàng với các Nhà cung cấp đối với các mặt hàng có tốc độ xuất cao.\n"
        else:
            md += "1. Duy trì định mức tồn kho hiện tại.\n"
            md += "2. Rà soát định kỳ các mặt hàng tồn kho trên 60 ngày.\n"

        return md

    def _rule_engine_restock_recommendation(self, snapshot: Dict[str, Any]) -> str:
        items = snapshot.get("items", [])
        md = "### 🚀 Gợi Ý Kế Hoạch Nhập Hàng Dựa Trên Số Liệu CSDL\n\n"
        md += "| Mã | Tên sản phẩm | Tồn hiện tại | Tồn tối thiểu | Xuất 30 ngày | Ưu tiên | Số lượng đề xuất tham khảo |\n"
        md += "| :--- | :--- | :---: | :---: | :---: | :---: | :---: |\n"

        for item in items:
            stock = item.get("stock", 0)
            min_stock = item.get("minimum_stock", 0)
            exp_30 = item.get("export_30_days", 0)

            if stock == 0:
                priority = "🔴 RẤT CAO"
                suggested_qty = max(min_stock * 2, 20)
            elif stock <= min_stock:
                priority = "🔴 CAO"
                suggested_qty = (min_stock * 2) - stock
            elif stock <= min_stock * 1.5 and exp_30 > 10:
                priority = "🟡 TRUNG BÌNH"
                suggested_qty = min_stock
            else:
                priority = "🟢 THẤP"
                suggested_qty = 0

            md += f"| {item['code']} | {item['name']} | {stock} | {min_stock} | {exp_30} | **{priority}** | {suggested_qty} |\n"

        md += "\n### 📝 Căn Cứ & Lý Do Suy Luận\n\n"
        for item in items:
            stock = item.get("stock", 0)
            min_stock = item.get("minimum_stock", 0)
            exp_30 = item.get("export_30_days", 0)
            if stock <= min_stock:
                burn_rate = round(exp_30 / 30.0, 2)
                if stock == 0:
                    status_text = "⚠️ **ĐÃ HẾT HÀNG TRONG KHO**. Cần lập phiếu nhập khẩn cấp ngay."
                elif burn_rate > 0:
                    days_left = round(stock / burn_rate, 1)
                    status_text = f"Tốc độ xuất là {burn_rate} sp/ngày. Dự kiến lượng hàng tồn chỉ đủ vận hành trong **{days_left} ngày**."
                else:
                    status_text = "Chưa phát sinh lượt xuất trong 30 ngày qua nhưng tồn kho đang thấp hơn ngưỡng an toàn."
        return md

    def _rule_engine_anomaly_detection(self, snapshot: Dict[str, Any]) -> str:
        anomalies = snapshot.get("anomalies", [])
        md = "### ⚡ Báo Cáo Phân Tích Biến Động Bất Thường Cho Quản Lý Kho\n\n"
        if anomalies:
            for idx, a in enumerate(anomalies, 1):
                md += f"#### {idx}. {a.get('title', 'Biến động')}\n"
                md += f"- **Sản phẩm liên quan**: {a.get('product_name')} ({a.get('product_code')})\n"
                md += f"- **Dữ liệu đối chứng**: {a.get('evidence')}\n"
                md += f"- **Mức độ rủi ro**: **{a.get('risk_level', 'CẦN CHÚ Ý')}**\n"
                md += f"- **Đề xuất hành động**: {a.get('action')}\n\n"
        else:
            md += "Hiện tại không phát hiện bất kỳ biến động bất thường nào về lượng nhập/xuất hoặc hàng tồn lâu trong CSDL kho.\n"

        return md

    def answer_user_question(self, question: str, data_context: Dict[str, Any]) -> Tuple[str, str]:
        system_prompt = (
            "Bạn là Trợ lý AI Quản Lý Kho thông minh (Warehouse AI Assistant).\n"
            "Chỉ trả lời câu hỏi của người dùng dựa DUY NHẤT vào dữ liệu JSON kho hàng thực tế được cung cấp.\n"
            "Không tự bịa dữ liệu. Trả lời bằng tiếng Việt, ngắn gọn, có cấu trúc, sử dụng gạch đầu dòng, "
            "bảng số liệu hoặc số tiền rõ ràng (VND). Tuyệt đối không hallucination."
        )
        user_prompt = (
            f"Dữ liệu kho hàng thực tế:\n```json\n{json.dumps(data_context, ensure_ascii=False, indent=2)}\n```\n\n"
            f"Câu hỏi của người quản trị: \"{question}\"\n"
            f"Hãy trả lời chính xác, ngắn gọn và có cấu trúc."
        )

        if self.api_key and len(self.api_key.strip()) > 10:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=self.api_key)
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2
                )
                return response.choices[0].message.content, "OpenAI API (" + self.model + ")"
            except Exception as e:
                print(f"[AI Service Warning] OpenAI call failed: {e}. Falling back to Rule Engine.")

        answer_md = self._rule_engine_qa(question, data_context)
        return answer_md, "Engine AI Nội Bộ (Strict JSON Analyzer)"

    def _rule_engine_qa(self, question: str, data: Dict[str, Any]) -> str:
        q = question.lower().strip()
        products = data.get("products", [])

        # Case 1: Ask about specific product by name or code
        matched = []
        for p in products:
            p_code = p.get("code", "").lower()
            p_name = p.get("name", "").lower()
            # check words
            words = [w for w in p_name.split() if len(w) > 2]
            if p_code in q or p_name in q or any(w in q for w in words):
                matched.append(p)

        if matched and not any(k in q for k in ["sắp hết", "hết hàng", "cảnh báo", "tổng giá trị", "bán chạy", "top"]):
            md = f"### 📦 Kết Quả Tra Cứu Mặt Hàng ({len(matched)} sản phẩm phù hợp)\n\n"
            md += "| Mã SKU | Tên sản phẩm | Tồn hiện tại | Ngưỡng an toàn | Giá tham khảo | Tình trạng |\n"
            md += "| :--- | :--- | :---: | :---: | :---: | :--- |\n"
            for p in matched:
                stock = p.get("stock", 0)
                min_s = p.get("minimum_stock", 0)
                price = f"{p.get('latest_price', 0):,} đ"
                status = "🔴 Hết hàng" if stock == 0 else ("🟡 Dưới tồn tối thiểu" if stock <= min_s else "🟢 An toàn")
                md += f"| {p['code']} | {p['name']} | **{stock} {p.get('unit', '')}** | {min_s} | {price} | {status} |\n"
            
            p0 = matched[0]
            val = p0.get("stock", 0) * p0.get("latest_price", 0)
            md += f"\n💡 **Chi tiết nhanh**: Mặt hàng **{p0['name']} ({p0['code']})** hiện có **{p0.get('stock', 0)} {p0.get('unit', '')}** trong kho. Tổng giá trị lưu kho ước tính là **{val:,} VNĐ**."
            return md

        # Case 2: Ask about low stock / sắp hết / cảnh báo
        if any(k in q for k in ["sắp hết", "hết hàng", "cảnh báo", "dưới mức", "thiếu hàng", "cần nhập"]):
            low_items = [p for p in products if p.get("stock", 0) <= p.get("minimum_stock", 0)]
            md = f"### ⚠️ Danh Sách Mặt Hàng Cần Chú Ý (Có {len(low_items)} sản phẩm dưới mức an toàn)\n\n"
            if low_items:
                md += "| Mã SKU | Tên sản phẩm | Tồn kho | Ngưỡng tối thiểu | Xuất 30 ngày | Trạng thái |\n"
                md += "| :--- | :--- | :---: | :---: | :---: | :--- |\n"
                for p in low_items:
                    stock = p.get("stock", 0)
                    status = "🔴 Hết hàng" if stock == 0 else "🟡 Dưới tồn tối thiểu"
                    md += f"| {p['code']} | {p['name']} | **{stock}** | {p['minimum_stock']} | {p.get('export_30_days', 0)} | {status} |\n"
                md += "\n👉 **Khuyến nghị**: Nên tạo ngay phiếu nhập hàng cho các sản phẩm đang hiển thị trạng thái màu đỏ và vàng."
            else:
                md += "Hiện tại tất cả mặt hàng trong kho đều đang duy trì mức tồn trên ngưỡng an toàn tối thiểu."
            return md

        # Case 3: Ask about total value / giá trị kho
        if any(k in q for k in ["giá trị", "tổng tiền", "tiền hàng", "bao nhiêu tiền", "trị giá"]):
            total_val = data.get("estimated_total_value", 0)
            total_qty = data.get("total_stock", 0)
            total_p = data.get("total_products", len(products))
            md = "### 💰 Báo Cáo Định Giá Tồn Kho Toàn Hệ Thống\n\n"
            md += f"- **Tổng số lượng sản phẩm quản lý**: **{total_p}** mặt hàng\n"
            md += f"- **Tổng số đơn vị hàng hóa tồn kho**: **{total_qty:,}** đơn vị\n"
            md += f"- **Tổng giá trị kho hàng ước tính**: **{total_val:,} VNĐ**\n\n"
            md += "#### Top 3 mặt hàng chiếm giá trị lưu kho lớn nhất:\n"
            sorted_by_val = sorted(products, key=lambda x: x.get("stock", 0) * x.get("latest_price", 0), reverse=True)[:3]
            for idx, p in enumerate(sorted_by_val, 1):
                p_val = p.get("stock", 0) * p.get("latest_price", 0)
                md += f"{idx}. **{p['name']} ({p['code']})**: {p.get('stock', 0)} {p.get('unit', '')} × {p.get('latest_price', 0):,} đ = **{p_val:,} VNĐ**\n"
            return md

        # Case 4: Top exported / hàng bán chạy
        if any(k in q for k in ["bán chạy", "xuất nhiều", "top xuất", "chạy nhất", "tốc độ xuất"]):
            sorted_exp = sorted(products, key=lambda x: x.get("export_30_days", 0), reverse=True)[:5]
            md = "### 🔥 Top Mặt Hàng Có Tốc Độ Xuất Kho Cao Nhất (30 Ngày Qua)\n\n"
            md += "| Hạng | Mã SKU | Tên sản phẩm | Đã xuất 30 ngày | Tồn kho còn lại | Tốc độ xuất |\n"
            md += "| :---: | :--- | :--- | :---: | :---: | :---: |\n"
            for rank, p in enumerate(sorted_exp, 1):
                rate = round(p.get("export_30_days", 0) / 30.0, 2)
                md += f"| #{rank} | {p['code']} | {p['name']} | **{p.get('export_30_days', 0)}** | {p.get('stock', 0)} | {rate} sp/ngày |\n"
            return md

        # Default overview
        total_p = data.get("total_products", len(products))
        total_qty = data.get("total_stock", 0)
        total_val = data.get("estimated_total_value", 0)
        low_count = len([p for p in products if p.get("stock", 0) <= p.get("minimum_stock", 0)])

        md = "### 🤖 Trợ Lý Kho AI Đã Nhận Yêu Cầu\n\n"
        md += f"Dữ liệu kho hàng thực tế ghi nhận hiện có **{total_p}** danh mục sản phẩm, tổng cộng **{total_qty:,}** đơn vị hàng hóa tồn kho, ước tính tổng giá trị **{total_val:,} VNĐ**.\n\n"
        md += f"- **Số mặt hàng cần chú ý/bổ sung**: **{low_count}** mặt hàng.\n"
        md += "- Bạn có thể thử các câu hỏi mẫu sau:\n"
        md += "  - *\"Kho còn bao nhiêu bàn phím cơ?\"*\n"
        md += "  - *\"Những sản phẩm nào đang sắp hết hàng?\"*\n"
        md += "  - *\"Tổng giá trị tồn kho là bao nhiêu?\"*\n"
        md += "  - *\"Top sản phẩm xuất chạy nhất 30 ngày qua?\"*\n"
        return md

ai_service = AIService()

