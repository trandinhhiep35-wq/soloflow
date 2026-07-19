import streamlit as st
import pandas as pd
import json

# --- 1. CẤU HÌNH TỐI GIẢN & AN TOÀN ---
# Loại bỏ các thư viện phức tạp gây lỗi nếu server chưa cài đặt
st.set_page_config(page_title="SoloFlow OS v6.0", layout="wide", page_icon="⚡")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

def safe_get_tasks(tasks_data):
    if not isinstance(tasks_data, list):
        return []
    return [t for t in tasks_data if isinstance(t, dict) and not t.get("archived", False)]

# --- 2. GIAO DIỆN CHÍNH ---
st.sidebar.markdown("# ⚡ SoloFlow v6.0")
st.sidebar.info("👤 Tài khoản: hiepcuto20")

tabs = st.tabs(["📊 Dashboard", "📋 Nhiệm vụ", "💬 SoloMind AI", "📦 Lưu trữ", "⚙️ Hệ thống"])

# --- 3. CÁC TAB CHỨC NĂNG ---
with tabs[0]:
    st.title("📊 Dashboard Tổng quan")
    active_tasks = safe_get_tasks(st.session_state.tasks)
    st.metric("Nhiệm vụ đang thực hiện", len(active_tasks))

with tabs[1]:
    st.title("📋 Quản lý Nhiệm vụ")
    new_task = st.text_input("Việc cần làm:")
    if st.button("➕ Thêm"):
        if new_task:
            st.session_state.tasks.append({"task": new_task, "archived": False})
            st.rerun()
    for t in active_tasks:
        st.write(f"- {t.get('task', 'N/A')}")

with tabs[2]:
    st.title("💬 SoloMind AI")
    st.write("Đang tải module AI...")

with tabs[3]:
    st.title("📦 Lưu trữ")
    st.write("Dữ liệu được lưu tại session.")

with tabs[4]:
    st.title("⚙️ Hệ thống")
    st.success("Hệ thống v6.0 ổn định.")
