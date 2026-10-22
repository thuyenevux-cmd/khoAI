from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.product import Product
from app.models.receipt import ImportReceiptDetail, ExportReceiptDetail, ImportReceipt, ExportReceipt
from app.models.inventory import Inventory
from app.schemas.ai import (
    AIAnalysisRequest,
    AIAnalysisResponse,
    AIAssistantRequest,
    AIAssistantResponse
)
from app.schemas.chatbot import ChatbotRequest, ChatbotResponse
from app.services.ai_service import ai_service
from app.services.warehouse_grounding import warehouse_grounding
from app.services.gemini_service import gemini_chatbot_service
from app.routers.deps import require_roles
from app.models.user import User

router = APIRouter(prefix="/ai", tags=["AI Analytics & Reports"])

@router.post("/inventory-report", response_model=AIAnalysisResponse)
def get_ai_inventory_report(
    req: AIAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "ACCOUNTANT", "WAREHOUSE"]))
):
    now = datetime.now(timezone.utc)
    thirty_days_ago = now - timedelta(days=30)

    total_items = db.query(Product).filter(Product.is_active == True).count()
    
    total_import = db.query(func.sum(ImportReceiptDetail.quantity)).join(ImportReceipt).filter(
        ImportReceipt.receipt_date >= thirty_days_ago
    ).scalar() or 0

    total_export = db.query(func.sum(ExportReceiptDetail.quantity)).join(ExportReceipt).filter(
        ExportReceipt.receipt_date >= thirty_days_ago
    ).scalar() or 0

    # Low stock items list
    low_products = db.query(Product).join(Inventory).filter(
        Product.is_active == True,
        Inventory.quantity <= Product.minimum_stock
    ).all()

    low_stock_details = []
    for p in low_products:
        exp_30 = db.query(func.sum(ExportReceiptDetail.quantity)).join(ExportReceipt).filter(
            ExportReceiptDetail.product_id == p.id,
            ExportReceipt.receipt_date >= thirty_days_ago
        ).scalar() or 0

        low_stock_details.append({
            "code": p.code,
            "name": p.name,
            "stock": p.inventory.quantity if p.inventory else 0,
            "minimum_stock": p.minimum_stock,
            "export_30_days": int(exp_30)
        })

    # Data snapshot
    snapshot = {
        "period": "30 Ngày Gần Nhất",
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "total_items": total_items,
        "total_import": int(total_import),
        "total_export": int(total_export),
        "low_stock_items": low_stock_details
    }

    markdown_report, provider_name = ai_service.generate_inventory_report(snapshot)

    return {
        "success": True,
        "feature": "Báo cáo kho AI",
        "period": req.period or "30_DAYS",
        "markdown_report": markdown_report,
        "data_snapshot": snapshot,
        "provider": provider_name
    }

@router.post("/restock-recommendation", response_model=AIAnalysisResponse)
def get_ai_restock_recommendation(
    req: AIAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "ACCOUNTANT", "WAREHOUSE"]))
):
    now = datetime.now(timezone.utc)
    thirty_days_ago = now - timedelta(days=30)

    # Focus on products below or near minimum stock or high movement
    products = db.query(Product).filter(Product.is_active == True).all()

    items_snapshot = []
    for p in products:
        stock = p.inventory.quantity if p.inventory else 0
        exp_30 = db.query(func.sum(ExportReceiptDetail.quantity)).join(ExportReceipt).filter(
            ExportReceiptDetail.product_id == p.id,
            ExportReceipt.receipt_date >= thirty_days_ago
        ).scalar() or 0

        items_snapshot.append({
            "code": p.code,
            "name": p.name,
            "stock": stock,
            "minimum_stock": p.minimum_stock,
            "export_30_days": int(exp_30)
        })

    snapshot = {
        "period": "30 Ngày Gần Nhất",
        "items": items_snapshot
    }

    markdown_report, provider_name = ai_service.generate_restock_recommendations(snapshot)

    return {
        "success": True,
        "feature": "Gợi ý nhập hàng AI",
        "period": req.period or "30_DAYS",
        "markdown_report": markdown_report,
        "data_snapshot": snapshot,
        "provider": provider_name
    }

@router.post("/anomaly-summary", response_model=AIAnalysisResponse)
def get_ai_anomaly_summary(
    req: AIAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "ACCOUNTANT", "WAREHOUSE"]))
):
    now = datetime.now(timezone.utc)
    thirty_days_ago = now - timedelta(days=30)

    anomalies = []

    # Detect high export with low stock items
    products = db.query(Product).filter(Product.is_active == True).all()
    for p in products:
        stock = p.inventory.quantity if p.inventory else 0
        exp_30 = db.query(func.sum(ExportReceiptDetail.quantity)).join(ExportReceipt).filter(
            ExportReceiptDetail.product_id == p.id,
            ExportReceipt.receipt_date >= thirty_days_ago
        ).scalar() or 0

        if stock <= p.minimum_stock and exp_30 > 15:
            anomalies.append({
                "title": "Tồn kho sắp hết nhưng tốc độ xuất cao",
                "product_code": p.code,
                "product_name": p.name,
                "evidence": f"Tồn kho: {stock}, Tồn tối thiểu: {p.minimum_stock}, Xuất 30 ngày: {exp_30}",
                "risk_level": "CAO",
                "action": "Tạo ngay phiếu nhập khẩn cấp cho sản phẩm này."
            })
        elif stock == 0 and exp_30 > 0:
            anomalies.append({
                "title": "Đã đứt gãy cung ứng (Hết hàng)",
                "product_code": p.code,
                "product_name": p.name,
                "evidence": f"Tồn kho: 0, Xuất 30 ngày: {exp_30}",
                "risk_level": "RẤT CAO",
                "action": "Liên hệ ngay Nhà cung cấp để đặt hàng."
            })

    snapshot = {
        "period": "30 Ngày Gần Nhất",
        "anomalies": anomalies
    }

    markdown_report, provider_name = ai_service.generate_anomaly_summary(snapshot)

    return {
        "success": True,
        "feature": "Phân tích biến động bất thường AI",
        "period": req.period or "30_DAYS",
        "markdown_report": markdown_report,
        "data_snapshot": snapshot,
        "provider": provider_name
    }

@router.post("/ask", response_model=AIAssistantResponse)
def ask_ai_assistant(
    req: AIAssistantRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "ACCOUNTANT", "WAREHOUSE"]))
):
    now = datetime.now(timezone.utc)
    thirty_days_ago = now - timedelta(days=30)

    # Gather comprehensive product + inventory context
    products = db.query(Product).filter(Product.is_active == True).all()

    product_contexts = []
    total_stock_qty = 0
    estimated_total_val = 0

    for p in products:
        stock = p.inventory.quantity if p.inventory else 0
        total_stock_qty += stock

        latest_detail = db.query(ImportReceiptDetail).filter(
            ImportReceiptDetail.product_id == p.id
        ).order_by(ImportReceiptDetail.id.desc()).first()
        price = latest_detail.unit_price if latest_detail else 0.0
        estimated_total_val += int(stock * price)

        exp_30 = db.query(func.sum(ExportReceiptDetail.quantity)).join(ExportReceipt).filter(
            ExportReceiptDetail.product_id == p.id,
            ExportReceipt.receipt_date >= thirty_days_ago
        ).scalar() or 0

        product_contexts.append({
            "code": p.code,
            "name": p.name,
            "stock": stock,
            "unit": p.unit.name if p.unit else "Đơn vị",
            "category": p.category.name if p.category else "Chung",
            "minimum_stock": p.minimum_stock,
            "latest_price": int(price),
            "export_30_days": int(exp_30)
        })

    data_context = {
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "total_products": len(products),
        "total_stock": total_stock_qty,
        "estimated_total_value": estimated_total_val,
        "products": product_contexts
    }

    answer_md, provider = ai_service.answer_user_question(req.question, data_context)

    return {
        "success": True,
        "question": req.question,
        "answer_markdown": answer_md,
        "data_context": data_context,
        "provider": provider,
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S")
    }

@router.post("/chat", response_model=ChatbotResponse)
def warehouse_ai_chat(
    req: ChatbotRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "ACCOUNTANT", "WAREHOUSE"]))
):
    """
    Endpoint Chatbot Trợ Lý Kho AI kết nối Google Gemini API.
    - Truy vấn an toàn dữ liệu tồn kho qua các hàm nghiệp vụ (Ground Truth).
    - Ngăn chặn triệt để SQL Injection & AI Hallucination.
    - Hỗ trợ ngữ cảnh hội thoại đa lượt (Multi-turn chat).
    - Tự động chuyển đổi Fallback nếu thiếu API key, quota 429 hoặc timeout.
    """
    now = datetime.now(timezone.utc)
    conv_id = req.conversation_id or f"conv_{int(now.timestamp())}_{current_user.id}"

    # 1. Thu thập dữ liệu đối chứng nghiệp vụ an toàn từ CSDL
    grounding_data = warehouse_grounding.collect_grounding_context(db, req.message)

    # 2. Xây dựng danh sách nguồn dữ liệu đối chứng (provenance)
    sources = []
    if "product_search_results" in grounding_data:
        for p in grounding_data["product_search_results"]:
            sources.append({
                "type": "product_stock",
                "code": p["code"],
                "name": p["name"],
                "stock": p["current_stock"]
            })
    if "low_stock_alert_items" in grounding_data:
        sources.append({
            "type": "low_stock_summary",
            "count": len(grounding_data["low_stock_alert_items"])
        })
    if "warehouse_summary_30_days" in grounding_data:
        sources.append({
            "type": "inventory_summary_30d",
            "total_units": grounding_data["warehouse_summary_30_days"].get("total_units_in_stock", 0)
        })

    # 3. Gửi sang Gemini Chatbot Service (có hỗ trợ multi-turn và graceful fallback)
    reply_md, provider, error_msg = gemini_chatbot_service.chat(
        message=req.message,
        grounding_data=grounding_data,
        history=req.history,
        conversation_id=conv_id
    )

    return ChatbotResponse(
        success=True,
        conversation_id=conv_id,
        reply=reply_md,
        sources=sources,
        provider=provider,
        error=error_msg,
        timestamp=now.strftime("%Y-%m-%d %H:%M:%S")
    )


