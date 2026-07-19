# -*- coding: utf-8 -*-
"""
SoloFlow OS v5.5 Ultimate Auth - Phiên bản Tích hợp Đa nền tảng và AI 2.5
Hệ điều hành quản trị năng suất cá nhân kết hợp trợ lý thông minh SoloMind.
"""

import streamlit as st
import pandas as pd
import json
import os
import time
import random
from datetime import date, datetime, timedelta
from dotenv import load_dotenv

# Thử nạp thư viện Google Generative AI
try:
    import google.generativeai as genai
    HAS_AI = True
except ImportError:
    HAS_AI = False

# Cấu hình hiển thị trang Streamlit chuẩn cao cấp
st.set_page_config(
    page_title="SoloFlow OS v5.5 Ultimate Auth",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Nạp file môi trường cục bộ (.env)
load_dotenv()

def inject_premium_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
        
        /* Đồng bộ phông chữ hệ thống */
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        /* Hiệu ứng kính mờ (Glassmorphism) cao cấp */
        .glass-panel {
            background: rgba(255, 255, 255, 0.75);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(226, 232, 240, 0.8);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.04);
            margin-bottom: 20px;
        }
        
        /* Thẻ chỉ số nâng cấp */
        .metric-container {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
            transition: transform 0.2s ease;
        }
        .metric-container:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        }
        
        /* Cảnh báo kiệt sức (Burnout Protection Panel) */
        .burnout-card {
            background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 16px;
            border-radius: 12px;
            font-weight: 500;
            margin-bottom: 15px;
        }
        
        /* Bo góc nút bấm và hiệu ứng di chuột */
        .stButton>button {
            border-radius: 10px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1.5rem !important;
            transition: all 0.2s ease-in-out !important;
        }
        .stButton>button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
        }
        
        /* Khung chat tinh tế */
        .chat-assistant {
            background-color: #f1f5f9;
            padding: 15px;
            border-radius: 14px;
            border-bottom-left-radius: 2px;
            margin-bottom: 10px;
            color: #1e293b;
        }
        .chat-user {
            background-color: #3b82f6;
            padding: 15px;
            border-radius: 14px;
            border-bottom-right-radius: 2px;
            margin-bottom: 10px;
            color: white;
            text-align: right;
        }
        </style>
    """, unsafe_allow_html=True)

inject_premium_css()

DB_FILE = "tasks_v5.json"

def load_tasks():
    """Tải dữ liệu công việc từ tệp tin JSON an toàn."""
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_tasks(tasks_list):
    """Ghi đè lưu trữ dữ liệu an toàn."""
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks_list, f, indent=4, ensure_ascii=False)
    except Exception as e:
        st.error(f"Lỗi sao lưu cơ sở dữ liệu: {e}")

# Ưu tiên 1: Đọc từ Streamlit Cloud Secrets (Dành cho bản web)
# Ưu tiên 2: Đọc từ file cục bộ .env (Dành cho bản chạy ở máy tính local)
if "GEMINI_API_KEY" in st.secrets:
    CLOUD_KEY = st.secrets["GEMINI_API_KEY"]
else:
    CLOUD_KEY = os.getenv("GEMINI_API_KEY", "")

# Khởi tạo khóa trong session_state
if "api_key" not in st.session_state:
    st.session_state.api_key = CLOUD_KEY

# Định nghĩa mô hình chuẩn thế hệ mới trong năm 2026: gemini-2.5-flash
ACTIVE_MODEL_NAME = "gemini-2.5-flash"

def call_gemini(prompt: str, system_instruction: str = "") -> str:
    """Gọi công cụ AI thế hệ mới 2.5-Flash thông qua API Key an toàn."""
    if not HAS_AI:
        return "Lỗi: Chưa cài đặt thư viện 'google-generativeai' trên máy chủ."
    
    current_key = st.session_state.get("api_key", "").strip()
    if not current_key:
        return "Vui lòng nhập cấu hình API Key ở thanh Sidebar bên trái!"
        
    try:
        # Cấu hình bộ nạp động
        genai.configure(api_key=current_key)
        
        # Thiết lập cấu hình hệ thống
        config = {}
        if system_instruction:
            config["system_instruction"] = system_instruction
            
        # Khởi tạo mô hình thế hệ 2.5 mới thay thế cho bản 1.5 đã bị khai tử
        model = genai.GenerativeModel(
            model_name=ACTIVE_MODEL_NAME,
            **config
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Nhận diện tự động lỗi phân quyền hoặc lỗi máy chủ
        err_msg = str(e)
        if "API_KEY_INVALID" in err_msg or "403" in err_msg:
            return "Lỗi: Khóa API Key của bạn không chính xác hoặc đã bị vô hiệu hóa từ Google AI Studio."
        return f"Lỗi kết nối máy chủ Google AI: {err_msg}"

def parse_gemini_json(ai_text: str):
    """Bóc tách sạch sẽ chuỗi JSON trả về từ prompt của AI."""
    clean_text = ai_text.strip()
    # Loại bỏ dấu bọc mã code markdown ```json ... ``` nếu AI trả về dư thừa
    if clean_text.startswith("```"):
        lines = clean_text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines[-1].startswith("```"):
            lines = lines[:-1]
        clean_text = "\n".join(lines).strip()
    return json.loads(clean_text)

with st.sidebar:
    st.markdown("<h2 style='color: #2563eb;'>⚡ SoloFlow OS v5.5</h2>", unsafe_allow_html=True)
    st.caption("Phiên bản Trợ lý AI Đa nhiệm & Bảo mật")
    st.markdown("---")
    
    # Khu vực nạp API Key bảo mật
    api_key_input = st.text_input(
        "Nhập Gemini API Key:",
        type="password",
        value=st.session_state.api_key,
        help="Khóa tạo từ Google AI Studio bắt đầu bằng AQ... hoặc AIzaSy..."
    )
    
    # Đồng bộ hóa thay đổi khóa
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input
        st.toast("🔑 Đã cập nhật khóa bảo mật thành công!")
        
    # Trạng thái kết nối của hệ thống
    if HAS_AI:
        if st.session_state.api_key:
            st.success("🟢 Bộ não AI 2.5-Flash sẵn sàng!")
        else:
            st.warning("🟡 Đang chạy Offline (Thiếu API Key)")
    else:
        st.error("🔴 Thiếu thư viện AI. Vui lòng cài đặt!")
        
    st.markdown("---")
    
    # Menu điều hướng chính dạng Tabs lớn
    st.markdown("### 🗺️ Bảng điều khiển")
    menu_tabs = ["📊 Dashboard", "📋 Nhiệm vụ", "🧠 SoloMind Chat", "📦 Lưu trữ", "⚙️ Hệ thống"]

# Đọc dữ liệu công việc hiện hành
tasks = load_tasks()

# Phân chia luồng giao diện chính thông qua Tabs của Streamlit
tab_dashboard, tab_tasks, tab_ai, tab_archive, tab_system = st.tabs(menu_tabs)

with tab_dashboard:
    st.markdown("## 📊 Dashboard Tổng quan")
    st.write("Cập nhật tình hình công việc và năng lượng của bạn theo thời gian thực.")
    st.markdown("---")
    
    # Phân loại dữ liệu
    active_tasks = [t for t in tasks if not t.get("archived", False)]
    pending_tasks = [t for t in active_tasks if t["status"] == "Cần làm"]
    doing_tasks = [t for t in active_tasks if t["status"] == "Đang làm"]
    done_tasks = [t for t in active_tasks if t["status"] == "Đã xong"]
    
    # Chỉ số nguy cơ kiệt sức (Burnout Score) dựa trên các việc Ưu tiên cao còn tồn đọng
    high_priority_pending = [t for t in pending_tasks if t["priority"] == "Cao"]
    burnout_score = len(high_priority_pending)
    
    # Hiển thị 3 chỉ số chính
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <h4 style="margin:0; color: #475569;">Tổng Việc Đang Chạy</h4>
            <h1 style="margin:10px 0 0 0; color: #3b82f6; font-size: 36px;">{len(active_tasks)}</h1>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <h4 style="margin:0; color: #475569;">Đã Hoàn Thành</h4>
            <h1 style="margin:10px 0 0 0; color: #10b981; font-size: 36px;">{len(done_tasks)}</h1>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        # Màu sắc thay đổi cảnh báo động theo mức độ kiệt sức
        burn_color = "#10b981" if burnout_score <= 1 else ("#f59e0b" if burnout_score <= 3 else "#ef4444")
        st.markdown(f"""
        <div class="metric-container">
            <h4 style="margin:0; color: #475569;">Chỉ Số Kiệt Sức</h4>
            <h1 style="margin:10px 0 0 0; color: {burn_color}; font-size: 36px;">{burnout_score}/5</h1>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Đưa ra cảnh báo chủ động ngăn ngừa quá tải (Burnout Alert)
    if burnout_score >= 3:
        st.markdown(f"""
        <div class="burnout-card">
            ⚠️ <b>Cảnh Báo Quá Tải:</b> Bạn đang có <b>{burnout_score} việc Ưu tiên cao</b> chưa hoàn thành. 
            Mức độ áp lực não bộ đang ở mức đáng lo ngại. Hãy cân nhắc kéo giãn thời gian chót (Due date) 
            hoặc sử dụng công cụ rã việc AI ở Tab 'Nhiệm vụ' để bóc nhỏ việc ra xử lý dễ dàng hơn!
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Giao diện thêm việc nhanh tức thì
    st.subheader("🚀 Thêm nhiệm vụ tức thì")
    with st.form("quick_add"):
        col_q_title, col_q_proj, col_q_prio, col_q_btn = st.columns([4, 2, 2, 2])
        with col_q_title:
            q_title = st.text_input("Tên việc cần làm...", placeholder="Ví dụ: Lên kế hoạch tuần mới...", label_visibility="collapsed")
        with col_q_proj:
            q_proj = st.text_input("Tên Dự án...", placeholder="Tên dự án...", label_visibility="collapsed")
        with col_q_prio:
            q_prio = st.selectbox("Độ ưu tiên", ["Cao", "Trung bình", "Thấp"], index=1, label_visibility="collapsed")
        with col_q_btn:
            q_submit = st.form_submit_button("Thêm Ngay", use_container_width=True, type="primary")
            
        if q_submit and q_title:
            new_id = random.randint(10000, 99999)
            while any(t["id"] == new_id for t in tasks):
                new_id = random.randint(10000, 99999)
                
            tasks.append({
                "id": new_id,
                "title": q_title.strip(),
                "project": q_proj.strip() if q_proj.strip() != "" else "Mặc định",
                "status": "Cần làm",
                "priority": q_prio,
                "due_date": str(date.today()),
                "notes": "",
                "archived": False
            })
            save_tasks(tasks)
            st.toast("🎉 Đã lưu nhiệm vụ mới thành công!")
            st.rerun()

with tab_tasks:
    st.markdown("## 📋 Quản trị Nhiệm vụ & Phân tách AI")
    st.write("Tìm kiếm, phân loại và sử dụng Trí tuệ Nhân tạo 2.5-Flash thế hệ mới để tự động lập cấu trúc công việc.")
    st.markdown("---")
    
    # Các bộ lọc tìm kiếm nâng cao
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        search_query = st.text_input("🔍 Tìm kiếm theo tên:", placeholder="Nhập từ khóa...")
    with col_f2:
        project_list = ["Tất cả"] + list(set([t.get("project", "Mặc định") for t in active_tasks]))
        filter_project = st.selectbox("📂 Lọc theo Dự án:", project_list)
    with col_f3:
        filter_priority = st.selectbox("🔴 Lọc theo Độ ưu tiên:", ["Tất cả", "Cao", "Trung bình", "Thấp"])
    with col_f4:
        filter_status = st.selectbox("🎯 Lọc theo Trạng thái:", ["Tất cả", "Cần làm", "Đang làm", "Đã xong"])
        
    sort_by = st.selectbox("⇅ Sắp xếp theo thứ tự:", ["Mặc định", "Hạn chót (Gần nhất)", "Độ ưu tiên (Cao -> Thấp)"])
    st.markdown("---")
    
    # Công cụ rã việc siêu cấp AI 2.5-Flash
    st.subheader("🧠 Trình 'Rã Việc' Siêu Tốc - AI Task Splitter 2.5")
    st.write("Nếu bạn có một mục tiêu quá lớn khiến bạn lo lắng không biết bắt đầu từ đâu, hãy gõ vào đây để Trợ lý AI rã nhỏ mục tiêu thành các bước hành động cụ thể cho bạn.")
    
    with st.container(border=True):
        col_ai_g, col_ai_p, col_ai_b = st.columns([5, 3, 2])
        with col_ai_g:
            ai_goal = st.text_input("Nhập mục tiêu khổng lồ của bạn:", placeholder="Ví dụ: Thiết kế website bán hàng hoàn thiện...")
        with col_ai_p:
            ai_proj_name = st.text_input("Đặt tên Dự án để AI lưu:", placeholder="Ví dụ: WebBanhang...")
        with col_ai_b:
            st.write(" ") # Tạo khoảng trống căn lề nút bấm
            st.write(" ")
            ai_split_btn = st.button("🚀 Rã Việc Tự Động", use_container_width=True, type="primary")
            
        if ai_split_btn:
            if not ai_goal:
                st.warning("Vui lòng điền mục tiêu lớn cần rã!")
            elif not st.session_state.api_key:
                st.error("Vui lòng nhập API Key ở thanh bên để kích hoạt trí tuệ AI.")
            else:
                with st.spinner("Bộ não AI 2.5-Flash đang rã việc... Vui lòng đợi trong giây lát!"):
                    system_instr = (
                        "Bạn là mô hình phân tích hành vi và cấu trúc quản trị công việc cao cấp tích hợp trong SoloFlow OS. "
                        "Nhiệm vụ của bạn là nhận vào 1 mục tiêu lớn, sau đó rã nhỏ mục tiêu đó thành từ 3 đến 5 nhiệm vụ con thực tế. "
                        "Bạn BẮT BUỘC phải trả về kết quả dưới dạng chuỗi JSON nguyên bản duy nhất là một mảng danh sách các object, "
                        "không chứa thêm bất kỳ văn bản giải thích nào ngoài JSON. Cấu trúc JSON bắt buộc như sau:\n"
                        "[\n"
                        "  {\"title\": \"Tên nhiệm vụ con 1\", \"priority\": \"Cao\", \"notes\": \"Mô tả chi tiết cách thực hiện bước này\"},\n"
                        "  {\"title\": \"Tên nhiệm vụ con 2\", \"priority\": \"Trung bình\", \"notes\": \"Mô tả chi tiết cách thực hiện bước này\"}\n"
                        "]\n"
                        "Lưu ý: Trường priority chỉ được chọn một trong ba giá trị: 'Cao', 'Trung bình', 'Thấp'."
                    )
                    ai_response = call_gemini(f"Mục tiêu lớn: {ai_goal}", system_instruction=system_instr)
                    
                    try:
                        subtasks = parse_gemini_json(ai_response)
                        if isinstance(subtasks, list):
                            added_count = 0
                            for stask in subtasks:
                                new_id = random.randint(10000, 99999)
                                while any(t["id"] == new_id for t in tasks):
                                    new_id = random.randint(10000, 99999)
                                
                                new_t = {
                                    "id": new_id,
                                    "title": stask.get("title", "Việc con không tên").strip(),
                                    "project": ai_proj_name.strip() if ai_proj_name.strip() != "" else "Dự án AI",
                                    "status": "Cần làm",
                                    "priority": stask.get("priority", "Trung bình"),
                                    "due_date": str(date.today()),
                                    "notes": stask.get("notes", "").strip(),
                                    "archived": False
                                }
                                tasks.append(new_t)
                                added_count += 1
                            save_tasks(tasks)
                            st.success(f"🎉 Đã rã thành công và tự động thêm {added_count} task vào dự án '{ai_proj_name}'!")
                            st.rerun()
                        else:
                            st.error("AI không phản hồi đúng định dạng danh sách công việc. Hãy thử lại!")
                    except Exception as e:
                        st.error(f"Lỗi phân tích cú pháp AI: {e}")
                        with st.expander("Xem chi tiết lỗi phản hồi"):
                            st.code(ai_response)
                            
    st.markdown("---")
    st.subheader("📋 Danh sách công việc đang thực hiện")
    
    # Thực hiện lọc dữ liệu
    display_tasks = [t for t in tasks if not t.get("archived", False)]
    if search_query:
        display_tasks = [t for t in display_tasks if search_query.lower() in t["title"].lower() or search_query.lower() in t.get("notes", "").lower()]
    if filter_project != "Tất cả":
        display_tasks = [t for t in display_tasks if t.get("project", "Mặc định") == filter_project]
    if filter_priority != "Tất cả":
        display_tasks = [t for t in display_tasks if t["priority"] == filter_priority]
    if filter_status != "Tất cả":
        display_tasks = [t for t in display_tasks if t["status"] == filter_status]
        
    # Thực hiện sắp xếp dữ liệu
    if sort_by == "Hạn chót (Gần nhất)":
        display_tasks = sorted(display_tasks, key=lambda x: x.get("due_date", "9999-12-31"))
    elif sort_by == "Độ ưu tiên (Cao -> Thấp)":
        p_map = {"Cao": 1, "Trung bình": 2, "Thấp": 3}
        display_tasks = sorted(display_tasks, key=lambda x: p_map.get(x["priority"], 99))

    # Kết xuất danh sách hiển thị
    if len(display_tasks) == 0:
        st.info("Không tìm thấy nhiệm vụ nào phù hợp với bộ lọc!")
    else:
        for idx, task in enumerate(display_tasks):
            with st.container(border=True):
                col_head, col_info, col_actions = st.columns([4, 3, 3])
                
                with col_head:
                    st.markdown(f"### **{task['title']}**")
                    st.markdown(f"📂 Dự án: **`{task.get('project', 'Mặc định')}`**")
                    if task.get("notes"):
                        with st.expander("📝 Xem ghi chú chi tiết"):
                            st.write(task["notes"])
                            
                with col_info:
                    p_emoji = "🔴" if task["priority"] == "Cao" else ("🟡" if task["priority"] == "Trung bình" else "🟢")
                    st.markdown(f"**Độ ưu tiên:** {p_emoji} {task['priority']}")
                    
                    s_emoji = "🎯" if task["status"] == "Cần làm" else ("⏳" if task["status"] == "Đang làm" else "✅")
                    st.markdown(f"**Trạng thái:** {s_emoji} {task['status']}")
                    
                    if task.get("due_date"):
                        try:
                            due_dt = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                            today_dt = date.today()
                            days_left = (due_dt - today_dt).days
                            
                            if days_left < 0:
                                st.error(f"⌛ Hạn chót: {task['due_date']} (Quá hạn {abs(days_left)} ngày!)")
                            elif days_left == 0:
                                st.warning(f"⌛ Hạn chót: Hôm nay! 🔥")
                            else:
                                st.info(f"⌛ Hạn chót: {task['due_date']} (Còn {days_left} ngày)")
                        except ValueError:
                            st.text(f"⌛ Hạn chót: {task['due_date']}")
                    else:
                        st.text("⌛ Hạn chót: Không thiết lập")
                        
                with col_actions:
                    col_b1, col_b2, col_b3 = st.columns(3)
                    with col_b1:
                        next_map = {"Cần làm": "Đang làm", "Đang làm": "Đã xong", "Đã xong": "Cần làm"}
                        current_s = task["status"]
                        next_s = next_map[current_s]
                        if st.button(f"➔ {next_s}", key=f"state_btn_{task['id']}_{idx}", use_container_width=True):
                            for t in tasks:
                                if t["id"] == task["id"]:
                                    t["status"] = next_s
                                    break
                            save_tasks(tasks)
                            st.rerun()
                            
                    with col_b2:
                        if st.button("📦 Lưu trữ", key=f"archive_btn_{task['id']}_{idx}", use_container_width=True):
                            for t in tasks:
                                if t["id"] == task["id"]:
                                    t["archived"] = True
                                    break
                            save_tasks(tasks)
                            st.success("Đã lưu trữ!")
                            st.rerun()
                            
                    with col_b3:
                        if st.button("🗑️ Xóa bỏ", key=f"delete_btn_{task['id']}_{idx}", use_container_width=True):
                            tasks = [t for t in tasks if t["id"] != task["id"]]
                            save_tasks(tasks)
                            st.success("Đã xóa vĩnh viễn!")
                            st.rerun()

with tab_ai:
    st.subheader("🧠 Trợ lý AI - SoloMind Chatbot")
    st.write("Trò chuyện và nhận lời khuyên năng suất được cá nhân hóa sâu sắc từ SoloMind.")
    
    if HAS_AI and st.session_state.api_key:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        col_chat_title, col_chat_clear = st.columns([4, 1])
        with col_chat_clear:
            if st.button("🗑️ Xóa lịch sử chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
                
        st.markdown("---")
        
        # Kết xuất các khối tin nhắn đã chat
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">💬 <b>Bạn:</b> {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-assistant">🤖 <b>SoloMind:</b> {msg["content"]}</div>', unsafe_allow_html=True)
                
        # Khung nhập câu hỏi chat
        if user_input := st.chat_input("Nhập câu hỏi tại đây..."):
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.markdown(f'<div class="chat-user">💬 <b>Bạn:</b> {user_input}</div>', unsafe_allow_html=True)
            
            # Cung cấp ngữ cảnh danh sách công việc hiện hành cho trợ lý AI
            context = "Danh sách công việc của người dùng hiện tại:\n"
            for t in active_tasks:
                context += f"- [{t['status']}] {t['title']} (Dự án: {t.get('project','Mặc định')}, Độ ưu tiên: {t['priority']})\n"
                
            system_instruction = (
                f"Bạn là SoloMind, trợ lý ảo thông minh tích hợp sẵn trong ứng dụng SoloFlow OS. "
                f"Mô hình AI của bạn là {ACTIVE_MODEL_NAME}. "
                f"Dưới đây là danh sách công việc hiện hành của người dùng:\n{context}\n"
                f"Hãy trả lời người dùng một cách thân thiện, truyền động lực mạnh mẽ và sẵn sàng "
                f"đưa ra ý tưởng rã việc hoặc phân phối thời gian dựa trên các task trên khi được hỏi."
            )
            
            with st.spinner("SoloMind đang suy nghĩ..."):
                ai_reply = call_gemini(user_input, system_instruction=system_instruction)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
                st.markdown(f'<div class="chat-assistant">🤖 <b>SoloMind:</b> {ai_reply}</div>', unsafe_allow_html=True)
                st.rerun()
    else:
        st.warning("⚠️ Vui lòng cấu hình API Key thật ở thanh Sidebar bên trái để kích hoạt Trợ lý Chat AI SoloMind!")

with tab_archive:
    st.subheader("📦 Các công việc đã lưu trữ (Archive)")
    archived_tasks = [t for t in tasks if t.get("archived", False)]
    
    if len(archived_tasks) == 0:
        st.info("Kho lưu trữ hiện đang trống!")
    else:
        for idx, task in enumerate(archived_tasks):
            with st.container(border=True):
                col_arch_title, col_arch_info, col_arch_act = st.columns([5, 3, 2])
                with col_arch_title:
                    st.markdown(f"#### **{task['title']}**")
                    st.caption(f"📂 Dự án: {task.get('project', 'Mặc định')} | ID: {task['id']}")
                with col_arch_info:
                    st.write(f"Trạng thái lúc lưu trữ: **{task['status']}**")
                with col_arch_act:
                    col_ab1, col_ab2 = st.columns(2)
                    with col_ab1:
                        if st.button("↩️ Phục hồi", key=f"restore_btn_{task['id']}_{idx}", use_container_width=True):
                            for t in tasks:
                                if t["id"] == task["id"]:
                                    t["archived"] = False
                                    break
                            save_tasks(tasks)
                            st.success("Đã khôi phục!")
                            st.rerun()
                    with col_ab2:
                        if st.button("🗑️ Xóa hẳn", key=f"force_del_btn_{task['id']}_{idx}", use_container_width=True):
                            tasks = [t for t in tasks if t["id"] != task["id"]]
                            save_tasks(tasks)
                            st.success("Đã xóa vĩnh viễn!")
                            st.rerun()

with tab_system:
    st.subheader("⚙️ Quản lý Cơ sở Dữ liệu & Sao lưu dự phòng")
    st.markdown("---")
    col_sys1, col_sys2 = st.columns(2)
    
    with col_sys1:
        st.markdown("### 📥 Xuất tệp dữ liệu (Export Backup)")
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                json_data = f.read()
            st.download_button(
                label="💾 Tải về file tasks_v5.json",
                data=json_data,
                file_name="tasks_backup.json",
                mime="application/json",
                use_container_width=True
            )
        except Exception:
            st.error("Không thể đọc tệp dữ liệu cục bộ!")
            
    with col_sys2:
        st.markdown("### 📤 Nhập tệp dữ liệu (Import Backup)")
        uploaded_file = st.file_uploader("Chọn file backup (.json):", type=["json"])
        if uploaded_file is not None:
            try:
                uploaded_tasks = json.load(uploaded_file)
                if isinstance(uploaded_tasks, list):
                    if st.button("⚠️ Xác nhận khôi phục đè dữ liệu", use_container_width=True, type="primary"):
                        save_tasks(uploaded_tasks)
                        st.success("Khôi phục thành công!")
                        st.rerun()
               except Exception as e:
                   st.error("File backup không đúng cấu trúc dữ liệu")
