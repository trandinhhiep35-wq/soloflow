import streamlit as st
import os
import json
import google.generativeai as genai

# ==========================================
# 1. ĐỌC & CẤU HÌNH KEY AQ DỰ ÁN
# ==========================================
# Hệ thống ưu tiên tìm Key tên 'AQ' hoặc 'AQ_KEY' trong Streamlit Secrets / Env
aq_key_secret = (
    st.secrets.get("AQ") or 
    st.secrets.get("AQ_KEY") or 
    st.secrets.get("GEMINI_API_KEY", os.getenv("AQ", ""))
)

if 'gemini_key' not in st.session_state or not st.session_state['gemini_key']:
    st.session_state['gemini_key'] = aq_key_secret

# ==========================================
# 2. KHU VỰC NHẬP KEY AQ TRÊN SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("### 🔑 Cấu Hình Key AQ")
    
    # Ô nhập Key hỗ trợ định dạng AQ
    input_aq = st.text_input(
        "Nhập Key AQ của bạn:",
        value=st.session_state.get('gemini_key', ''),
        type="password",
        placeholder="AQxxxxxxxxxxxx...",
        help="Nhập Key định dạng AQ vào đây hoặc cấu hình file Secrets với tên AQ"
    )
    
    if st.button("💾 Lưu Key AQ"):
        st.session_state['gemini_key'] = input_aq
        st.success("Đã lưu Key AQ thành công!")
        st.rerun()

    if st.session_state.get('gemini_key'):
        st.caption("🟢 Key AQ: **Đã sẵn sàng hoạt động**")
    else:
        st.caption("🔴 Chưa có Key AQ (Đang chạy chế độ mô phỏng)")
