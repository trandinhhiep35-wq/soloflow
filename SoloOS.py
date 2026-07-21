import streamlit as st
import pandas as pd
import plotly.express as px
import json
import time
import os
from supabase import create_client, Client
import google.generativeai as genai

# ==========================================
# 1. CẤU HÌNH TRANG & THEME HYBRID (NORMAL / PLUS VIP)
# ==========================================
st.set_page_config(
    page_title="SoloFlow OS - Smart AI Task Decomposition",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Quản lý Key AQ
aq_key_secret = (
    st.secrets.get("AQ") or 
    st.secrets.get("AQ_KEY") or 
    st.secrets.get("GEMINI_API_KEY", os.getenv("AQ", ""))
)

if 'gemini_key' not in st.session_state or not st.session_state['gemini_key']:
    st.session_state['gemini_key'] = aq_key_secret

if 'user_plan' not in st.session_state:
    st.session_state['user_plan'] = 'Basic'

is_plus = (st.session_state['user_plan'] != 'Basic')

# Custom CSS
plus_css = """
    .stApp { background-color: #050811; }
    .glass-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.5) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.15) !important;
    }
    .vip-badge-active {
        background: linear-gradient(90deg, #ec4899, #8b5cf6, #3b82f6);
        color: white; padding: 4px 12px; border-radius: 20px;
        font-weight: 800; font-size: 0.8rem; text-align: center;
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
    .p-high {{ color: #f87171; background: rgba(248, 113, 113, 0.12); padding: 3px 8px; border-radius: 6px; font-size: 0.78rem; font-weight:600; }}
    .p-med {{ color: #fbbf24; background: rgba(251, 191, 36, 0.12); padding: 3px 8px; border-radius: 6px; font-size: 0.78rem; font-weight:600; }}
    .p-low {{ color: #34d399; background: rgba(52, 211, 153, 0.12); padding: 3px 8px; border-radius: 6px; font-size: 0.78rem; font-weight:600; }}
    {plus_css}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. KHỞI TẠO KẾT NỐI SUPABASE & GEMINI AI
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
    if not api_key:
        return [
            {"step": 1, "title": f"Khảo sát & Lập kế hoạch: {prompt_text[:30]}...", "description": "Xác định mục tiêu cốt lõi và đầu ra.", "time": "2.0 giờ", "priority": "Cao"},
            {"step": 2, "title": "Thiết kế kịch bản thực thi", "description": "Phân chia module và tối ưu quy trình.", "time": "3.5 giờ", "priority": "Cao"},
            {"step": 3, "title": "Thực thi & Tạo mẫu thử", "description": "Xây dựng các phần tử chính.", "time": "5.0 giờ", "priority": "Trung bình"},
            {"step": 4, "title": "Đánh giá & Nghiệm thu", "description": "Hoàn thiện chi tiết.", "time": "1.5 giờ", "priority": "Thấp"}
        ]
    
    try:
        genai.configure(api_key=api_key)
        model_name = "gemini-1.5-pro" if is_vip else "gemini-1.5-flash"
        model = genai.GenerativeModel(model_name)
        
        vip_instruction = "Phân tích rủi ro, liệt kê hành động cụ thể cho từng bước." if is_vip else "Trả về các bước gọn gàng, thực tế."

        sys_prompt = f"""
        Bạn là chuyên gia quản lý dự án. Hãy phân rã công việc sau thành danh sách WBS:
        Công việc: "{prompt_text}"
        Danh mục: "{category}"
        Độ chi tiết: "{depth_str}"
        Yêu cầu: {vip_instruction}

        BẮT BUỘC trả về định dạng JSON Array chứa các Object, không thêm văn bản khác.
        Cấu trúc JSON:
        [
            {{
                "step": 1,
                "title": "Tên bước ngắn gọn",
                "description": "Mô tả chi tiết",
                "time": "1.5 giờ",
                "priority": "Cao"
            }}
        ]
        """
        response = model.generate_content(sys_prompt)
        clean_text = response.text.replace("```json", "").replace("
