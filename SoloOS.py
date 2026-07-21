import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from supabase import create_client, Client
import google.generativeai as genai

# ==========================================
# 1. CẤU HÌNH TRANG & THEME DYNAMIC (BASIC / PLUS VIP)
# ==========================================
st.set_page_config(
    page_title="SoloFlow OS - Smart AI Task Decomposition",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Đọc Key AQ ưu tiên từ Streamlit Secrets hoặc biến môi trường
aq_key_secret = (
    st.secrets.get("AQ") or 
    st.secrets.get("AQ_KEY") or 
    st.secrets.get("GEMINI_API_KEY", os.getenv("AQ", ""))
)

if 'gemini_key' not in st.session_state:
    st.session_state['gemini_key'] = aq_key_secret if aq_key_secret else ""

if 'user_plan' not in st.session_state:
    st.session_state['user_plan'] = 'Basic'

is_plus = (st.session_state['user_plan'] != 'Basic')

# Tùy chỉnh CSS theo từng phiên bản
plus_css = """
    .stApp { background-color: #050811; }
    .glass-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.5) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.15) !important;
    }
    .vip-badge-active {
        background: linear-gradient(90deg, #ec4899, #8b5cf6, #3b82f6);
        color: white; padding: 6px 14px; border-radius: 20px;
        font-weight: 800; font-size: 0.85rem; text-align: center;
        letter-spacing: 0.5px;
    }
""" if is_plus else """
    .stApp { background-color: #0f172a; }
    .glass-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
"""

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
    .glass-card {{
        border-radius: 12px; padding: 18px; margin-bottom: 15px;
        backdrop-filter: blur(12px);
    }}
    .p-high {{ color: #f87171; background: rgba(248, 113, 113, 0.12); padding: 4px 10px; border-radius: 6px; font-size: 0.78rem; font-weight:600; }}
    .p-med {{ color: #fbbf24; background: rgba(251, 191, 36, 0.12); padding: 4px 10px; border-radius: 6px; font-size: 0.78rem; font-weight:600; }}
    .p-low {{ color: #34d399; background: rgba(52, 211, 153, 0.12); padding: 4px 10px; border-radius: 6px; font-size: 0.78rem; font-weight:600; }}
    {plus_css}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. KHỞI TẠO SUPABASE & AI GEMINI (KEY AQ)
# ==========================================
@st.cache_resource
def init_supabase():
    url = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL", ""))
    key = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY", ""))
    if url and key:
        try:
            return create_client(url, key)
        except Exception:
            return None
    return None

supabase: Client = init_supabase()

def call_gemini_ai_wbs(prompt_text, category, depth_str, is_vip=False):
    api_key = st.session_state.get('gemini_key')
    
    # Dự phòng dữ liệu mẫu nếu chưa có Key
    if not api_key:
        return [
            {"step": 1, "title": f"Phân tích & Lập kế hoạch: {prompt_text[:30]}", "description": "Xác định mục tiêu cốt lõi, chuẩn bị công cụ và đầu ra dự án.", "time": "2.0 giờ", "priority": "Cao"},
            {"step": 2, "title": "Thiết kế kiến trúc / Kịch bản chi tiết", "description": "Phân chia module, tối ưu quy trình và dữ liệu xử lý.", "time": "3.5 giờ", "priority": "Cao"},
            {"step": 3, "title": "Thực thi & Xây dựng sản phẩm", "description": "Lập trình/triển khai các chức năng theo đúng thiết kế.", "time": "5.0 giờ", "priority": "Trung bình"},
            {"step": 4, "title": "Kiểm thử, tối ưu & Nghiệm thu", "description": "Rà soát lỗi, tối ưu hiệu năng và đóng gói hoàn tất.", "time": "1.5 giờ", "priority": "Thấp"}
        ]
    
    try:
        genai.configure(api_key=api_key)
        model_name = "gemini-1.5-pro" if is_vip else "gemini-1.5-flash"
        model = genai.GenerativeModel(model_name)
        
        vip_instruction = "Phân tích chiều sâu, rủi ro tiềm ẩn, khuyến nghị công nghệ và liệt kê chi tiết từng hành động." if is_vip else "Trả về các bước ngắn gọn, thực tế và dễ áp dụng."

        sys_prompt = f"""
        Bạn là một chuyên gia Quản lý dự án (Project Manager) cấp cao. Hãy phân rã công việc sau thành danh sách WBS chi tiết:
        Công việc: "{prompt_text}"
        Lĩnh vực: "{category}"
        Mức độ chi tiết: "{depth_str}"
        Yêu cầu chuyên sâu: {vip_instruction}

        BẮT BUỘC trả về duy nhất định dạng JSON Array chứa các Object, KHÔNG kèm bất kỳ lời dẫn hay định dạng markdown ngoài JSON.
        Cấu trúc JSON từng phần tử:
        [
            {{
                "step": 1,
                "title": "Tên bước thực hiện ngắn gọn",
                "description": "Mô tả chi tiết hành động cụ thể",
                "time": "Ví dụ: 2.0 giờ",
                "priority": "Cao"
            }}
        ]
        Chỉ sử dụng giá trị priority là: "Cao", "Trung bình", hoặc "Thấp".
        """
        
        response = model.generate_content(sys_prompt)
        clean_text = response.text.replace("```json", "").replace("
