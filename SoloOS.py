import streamlit as st
import pandas as pd
import json
import time
from supabase import create_client

# 1. CẤU HÌNH & KHỞI TẠO AN TOÀN
if "tasks" not in st.session_state:
    st.session_state.tasks = []

def safe_get_tasks(tasks_data):
    if not isinstance(tasks_data, list): return []
    return [t for t in tasks_data if isinstance(t, dict) and not t.get("archived", False)]

st.set_page_config(page_title="SoloFlow OS v5.5", layout="wide", page_icon="⚡")

# 2. SIDEBAR (Giao diện cũ v5.5 chuẩn)
st.sidebar.markdown("# ⚡ SoloFlow v5.5")
st.sidebar.info("👤 **Tài khoản:** hiepcuto20")
if st.sidebar.button("🚪 Đăng xuất", use_container_width=True):
    st.session_state.clear()
st.sidebar.markdown("---")
gemini_key = st.sidebar.text_input("Nhập Gemini API Key:", type="password")
st.sidebar.markdown("### 🏆 Zen Focus Level")
st.sidebar.write("Cấp độ: **Level 2 (Flow Practitioner 🌀)**")
st.sidebar.progress(40)

# 3. TABS GIAO DIỆN CHÍNH
tabs = st.tabs(["📊 Dashboard", "📋 Nhiệm vụ", "💬 SoloMind AI", "📦 Lưu trữ", "⚙️ Hệ thống"])

# TAB DASHBOARD (Đã fix lỗi dòng 241)
with tabs[0]:
    st.title("📊 Dashboard Tổng quan")
    active_tasks = safe_get_tasks(st.session_state.tasks)
    col1, col2, col3 = st.columns(3)
    col1.metric("Nhiệm vụ đang thực hiện", len(active_tasks))
    col2.metric("Thời gian tập trung", "5h 15m")
    col3.metric("Kết nối", "Cloud")
    st.line_chart([15, 30, 25, 45, 50, 65])

# TAB NHIỆM VỤ
with tabs[1]:
    st.title("📋 Quản lý Nhiệm vụ")
    new_task = st.text_input("Việc cần làm:")
    if st.button("➕ Thêm Task"):
        st.session_state.tasks.append({"task": new_task, "archived": False})
        st.rerun()
    for t in active_tasks:
        st.write(f"- {t.get('task', 'N/A')}")

# TAB SOLOMIND AI
with tabs[2]:
    st.title("💬 Trợ lý thông minh SoloMind AI")
    st.text_area("Hỏi đáp:")

# TAB LƯU TRỮ
with tabs[3]:
    st.title("📦 Không gian lưu trữ")
    st.info("Dữ liệu cục bộ đang được đồng bộ.")

# TAB HỆ THỐNG
with tabs[4]:
    st.title("⚙️ Hệ thống & Cấu hình Profile")
    st.markdown("---")
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("### 👤 Hồ sơ")
        st.text_input("Tên:", "hiepcuto20")
    with col_r:
        st.markdown("### 💾 Backup")
        st.download_button("📥 Tải bản sao lưu", data=json.dumps(st.session_state.tasks), file_name="backup.json")
