import streamlit as st
import pandas as pd
import json
import os
import time
import random
import hashlib
from datetime import date, datetime, timedelta

# --- CẤU HÌNH TRANG WEB CHUẨN PREMIUM ---
st.set_page_config(
    page_title="SoloFlow OS v5.5 Ultimate Auth",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- KHỞI TẠO ĐƯỜNG DẪN CƠ SỞ DỮ LIỆU ---
DB_FILE = "tasks.json"
USER_FILE = "users.json"

# --- KIỂM TRA THƯ VIỆN AI ---
try:
    import google.generativeai as genai
    HAS_AI = True
except ImportError:
    HAS_AI = False

def inject_premium_css():
    st.markdown("""
        <style>
        /* Nhập font chữ quốc tế */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
        
        /* Cấu hình Font mặc định */
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        /* Màu nền tối chủ đạo của hệ sinh thái Premium */
        .stApp {
            background-color: #0b0f19;
            color: #f1f5f9;
        }
        
        /* Khung Đăng nhập Glassmorphic Cosmic cực kỳ cao cấp */
        .auth-card {
            background: linear-gradient(135deg, rgba(17, 24, 39, 0.8) 0%, rgba(30, 41, 59, 0.8) 100%);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 24px;
            padding: 40px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), 0 0 40px rgba(59, 130, 246, 0.1);
            max-width: 500px;
            margin: 40px auto;
            text-align: center;
        }
        
        /* Thẻ Glassmorphism cao cấp */
        .glass-card {
            background: rgba(17, 24, 39, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            margin-bottom: 20px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .glass-card:hover {
            border-color: rgba(59, 130, 246, 0.5);
            box-shadow: 0 8px 32px 0 rgba(59, 130, 246, 0.1);
            transform: translateY(-2px);
        }
        
        /* Thanh chỉ số nổi bật */
        .metric-glow {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border-left: 5px solid #3b82f6;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }
        
        /* Phong cách nút nhấn đồng bộ */
        .stButton>button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important;
        }
        
        /* Nút phụ trong sidebar/hủy */
        .stButton>button[data-baseweb="button"]:has(span:contains("Đăng xuất")),
        .stButton>button[data-baseweb="button"]:has(span:contains("Hủy")),
        .stButton>button[data-baseweb="button"]:has(span:contains("Tắt âm")) {
            background: linear-gradient(135deg, #334155 0%, #1e293b 100%) !important;
            color: #cbd5e1 !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            box-shadow: none !important;
        }
        
        /* Thanh tiến trình tuỳ chỉnh */
        .stProgress > div > div > div > div {
            background-image: linear-gradient(to right, #3b82f6, #10b981) !important;
        }
        
        /* Kiểu chữ tiêu đề đẹp mắt */
        h1, h2, h3 {
            font-weight: 800 !important;
            letter-spacing: -0.025em !important;
            background: linear-gradient(to right, #ffffff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Làm nổi bật logo */
        .logo-text {
            font-size: 42px;
            font-weight: 800;
            background: linear-gradient(to right, #3b82f6, #10b981);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

def hash_password(password: str) -> str:
    """Băm bảo mật mật khẩu bằng thuật toán SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def load_users() -> dict:
    """Tải danh sách tài khoản người dùng từ file JSON bảo mật."""
    if not os.path.exists(USER_FILE):
        default_users = {
            "admin": {
                "password": hash_password("admin123"),
                "xp": 150,
                "created_at": str(datetime.now())
            }
        }
        save_users(default_users)
        return default_users
    try:
        with open(USER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_users(users: dict):
    """Lưu danh sách tài khoản người dùng an toàn."""
    try:
        with open(USER_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
    except Exception as e:
        st.error(f"Lỗi hệ thống tài khoản: {e}")

def load_tasks() -> list:
    """Tải tất cả danh sách nhiệm vụ từ cơ sở dữ liệu."""
    if not os.path.exists(DB_FILE):
        return [
            {"id": 10001, "title": "Thiết kế UI/UX hệ thống quản trị", "project": "SoloFlow 5.5", "status": "Đang làm", "priority": "Cao", "due_date": str(date.today()), "notes": "Cập nhật màn hình đăng nhập Glassmorphism", "archived": False, "owner": "admin"},
            {"id": 10002, "title": "Bảo mật hóa mật khẩu", "project": "Bảo mật", "status": "Đã xong", "priority": "Cao", "due_date": str(date.today()), "notes": "Băm mật khẩu người dùng với SHA-256", "archived": False, "owner": "admin"}
        ]
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_tasks(tasks_list: list):
    """Lưu danh sách nhiệm vụ xuống tệp cơ sở dữ liệu."""
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks_list, f, indent=4, ensure_ascii=False)
    except Exception as e:
        st.error(f"Lỗi ghi dữ liệu công việc: {e}")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "user_xp" not in st.session_state:
    st.session_state.user_xp = 0

all_users = load_users()
all_tasks = load_tasks()

def call_gemini(prompt: str, system_instruction: str = "") -> str:
    if not HAS_AI:
        return "Lỗi: Chưa cài đặt thư viện google-generativeai."
    
    current_key = st.session_state.get("gemini_key", "").strip()
    if not current_key or current_key == "AIzaSy...":
        return "Vui lòng nhập mã API Key hợp lệ trên Sidebar để kích hoạt AI!"
    
    try:
        genai.configure(api_key=current_key)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction if system_instruction else None
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lỗi kết nối máy chủ Google AI: {str(e)}"

def parse_gemini_json(raw_text: str):
    cleaned = raw_text.strip()
    if "```json" in cleaned:
        cleaned = cleaned.split("```json")[1].split("```")[0].strip()
    elif "```" in cleaned:
        cleaned = cleaned.split("```")[1].split("```")[0].strip()
    return json.loads(cleaned)

inject_premium_css()

if not st.session_state.logged_in:
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    
    with col_l2:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown('<div class="logo-text">⚡ SoloFlow OS</div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#64748b; margin-bottom: 25px;">Hệ thống năng suất đỉnh cao tích hợp AI & Trải nghiệm Game</p>', unsafe_allow_html=True)
        
        auth_mode = st.radio("Lựa chọn phương thức truy cập:", ["Đăng Nhập", "Đăng Ký Tài Khoản Mới"], horizontal=True, label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        
        username_input = st.text_input("👤 Tên tài khoản:", placeholder="Nhập tên đăng nhập của bạn...")
        password_input = st.text_input("🔑 Mật khẩu bảo mật:", type="password", placeholder="Nhập mật khẩu...")
        
        if auth_mode == "Đăng Nhập":
            if st.button("Đăng Nhập Ngay 🚀", use_container_width=True):
                user_clean = username_input.strip()
                pass_clean = password_input.strip()
                
                if not user_clean or not pass_clean:
                    st.error("⚠️ Vui lòng điền đầy đủ thông tin đăng nhập!")
                elif user_clean in all_users and all_users[user_clean]["password"] == hash_password(pass_clean):
                    st.session_state.logged_in = True
                    st.session_state.current_user = user_clean
                    st.session_state.user_xp = all_users[user_clean].get("xp", 100)
                    st.toast(f"🔥 Chào mừng bạn quay trở lại, {user_clean}!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ Tài khoản hoặc mật khẩu không chính xác!")
                    
        else:  # ĐĂNG KÝ
            confirm_password = st.text_input("🔄 Xác nhận mật khẩu:", type="password", placeholder="Nhập lại mật khẩu...")
            if st.button("Tạo Tài Khoản Mới ✨", use_container_width=True):
                user_clean = username_input.strip()
                pass_clean = password_input.strip()
                confirm_clean = confirm_password.strip()
                
                if len(user_clean) < 3:
                    st.error("⚠️ Tên tài khoản phải chứa ít nhất 3 ký tự!")
                elif len(pass_clean) < 6:
                    st.error("⚠️ Mật khẩu phải bảo mật tối thiểu 6 ký tự!")
                elif pass_clean != confirm_clean:
                    st.error("❌ Mật khẩu xác nhận không trùng khớp!")
                elif user_clean in all_users:
                    st.error("❌ Tên tài khoản này đã có người đăng ký!")
                else:
                    all_users[user_clean] = {
                        "password": hash_password(pass_clean),
                        "xp": 100,
                        "created_at": str(datetime.now())
                    }
                    save_users(all_users)
                    
                    new_starter_tasks = [
                        {"id": random.randint(10000, 99999), "title": "Khám phá SoloFlow OS v5.5", "project": "Bắt đầu", "status": "Cần làm", "priority": "Thấp", "due_date": str(date.today()), "notes": "Cài đặt khóa AI và trải nghiệm trình phát nhạc sóng não ở Sidebar.", "archived": False, "owner": user_clean},
                        {"id": random.randint(10000, 99999), "title": "Hoàn thành mục tiêu đầu tiên", "project": "Mục tiêu", "status": "Cần làm", "priority": "Trung bình", "due_date": str(date.today() + timedelta(days=1)), "notes": "Hoàn thành nhiệm vụ này để nhận điểm thưởng XP thăng cấp!", "archived": False, "owner": user_clean}
                    ]
                    all_tasks.extend(new_starter_tasks)
                    save_tasks(all_tasks)
                    
                    st.success(f"🎉 Đăng ký tài khoản thành công! Nhận được +100 XP Tân Thủ.")
                    st.balloons()
                    time.sleep(1)
                    st.session_state.logged_in = True
                    st.session_state.current_user = user_clean
                    st.session_state.user_xp = 100
                    st.rerun()
                    
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

current_user = st.session_state.current_user
user_tasks = [t for t in all_tasks if t.get("owner") == current_user]

with st.sidebar:
    st.markdown("<h2 style='color:#3b82f6;'>⚡ SoloFlow v5.5</h2>", unsafe_allow_html=True)
    st.markdown(f"👤 Tài khoản: **`{current_user}`**")
    
    if st.button("🚪 Đăng xuất khỏi hệ thống", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.user_xp = 0
        st.rerun()
        
    st.markdown("---")
    
    st.markdown("### 🔑 Cấu hình AI Engine")
    api_key_input = st.text_input(
        "Nhập Gemini API Key:", 
        type="password", 
        value=st.session_state.get("gemini_key", ""),
        placeholder="Bắt đầu bằng AIzaSy..."
    )
    if api_key_input:
        st.session_state["gemini_key"] = api_key_input

    if HAS_AI and api_key_input:
        st.success("Trí tuệ AI đã sẵn sàng hoạt động!")
    else:
        st.warning("AI đang tạm khóa (Thiếu API Key)")
        
    st.markdown("---")
    
    st.markdown("### 🏆 Zen Focus Level")
    user_xp = st.session_state.user_xp
    user_lvl = int((user_xp ** 0.5) / 10) + 1
    
    if user_lvl < 2:
        rank_name = "Focus Seeker 🌱"
    elif user_lvl < 4:
        rank_name = "Flow Practitioner 🌀"
    else:
        rank_name = "Zen Flow Master 🌌"
        
    st.markdown(f"**Cấp độ hiện tại:** Level {user_lvl} ({rank_name})")
    
    xp_floor = (10 * (user_lvl - 1)) ** 2
    xp_ceil = (10 * user_lvl) ** 2
    xp_range = max((xp_ceil - xp_floor), 1)
    current_progress = (user_xp - xp_floor) / xp_range
    current_progress = min(max(current_progress, 0.0), 1.0)
    
    st.markdown(f"<small>Tiến trình cấp độ: {user_xp} / {xp_ceil} XP</small>", unsafe_allow_html=True)
    st.progress(current_progress)
    st.markdown("---")
    
    st.markdown("### 🎵 Không gian Sóng não")
    sound_choice = st.selectbox(
        "Chọn âm thanh nền hỗ trợ tập trung:", 
        ["Tắt âm", "Nhạc Lofi thư giãn", "Tiếng mưa rơi rào rào", "Tiếng ồn trắng (White Noise)", "Nhạc tùy chỉnh (Custom ID)"]
    )
    
    custom_id = ""
    if sound_choice == "Nhạc tùy chỉnh (Custom ID)":
        custom_id = st.text_input("Nhập YouTube Video ID (Ví dụ: DWcJYXZMstU):", placeholder="Dán mã 11 ký tự sau dấu v=")

    video_id = None
    if sound_choice == "Nhạc Lofi thư giãn":
        video_id = "DWcJYXZMstU"
    elif sound_choice == "Tiếng mưa rơi rào rào":
        video_id = "W9g84A1M2uE"
    elif sound_choice == "Tiếng ồn trắng (White Noise)":
        video_id = "q76bN0Gy6zo"
    elif sound_choice == "Nhạc tùy chỉnh (Custom ID)" and custom_id:
        video_id = custom_id.strip()

    if video_id:
        iframe_src = f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=0&loop=1&playlist={video_id}"
        st.markdown(
            f'<iframe width="100%" height="80" src="{iframe_src}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>', 
            unsafe_allow_html=True
        )
        
    st.markdown("---")
    st.caption("🚀 Phiên bản v5.5 đem đến trải nghiệm cá nhân hóa và bảo mật tối đa.")

tab_dashboard, tab_tasks, tab_ai, tab_archive, tab_system = st.tabs([
    "📊 Dashboard", 
    "📋 Nhiệm vụ", 
    "🧠 SoloMind AI", 
    "📦 Lưu trữ", 
    "⚙️ Hệ thống"
])

active_tasks = [t for t in user_tasks if not t.get("archived", False)]

# ==========================================
# TAB 1: DASHBOARD (TỔNG QUAN HIỆU SUẤT)
# ==========================================
with tab_dashboard:
    st.markdown(f"<h1 style='text-align: center; color: #3b82f6; margin-bottom: 10px;'>📊 Workspace: {current_user}</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color:#64748b; margin-bottom: 30px;'>Cá nhân hóa hiệu suất thông qua AI - Đập tan trì hoãn</p>", unsafe_allow_html=True)
    
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    total_active = len(active_tasks)
    pending_count = len([t for t in active_tasks if t["status"] == "Cần làm"])
    doing_count = len([t for t in active_tasks if t["status"] == "Đang làm"])
    done_count = len([t for t in active_tasks if t["status"] == "Đã xong"])
    
    with m_col1:
        st.markdown(f"""
        <div class="metric-glow">
            <h5 style="color:#64748b; margin:0;">Tổng việc hoạt động</h5>
            <h2 style="color:#f1f5f9; margin:10px 0 0 0; font-size:36px;">{total_active}</h2>
        </div>
        """, unsafe_allow_html=True)
        
    with m_col2:
        st.markdown(f"""
        <div class="metric-glow" style="border-left-color: #f59e0b;">
            <h5 style="color:#64748b; margin:0;">Cần thực hiện</h5>
            <h2 style="color:#f59e0b; margin:10px 0 0 0; font-size:36px;">{pending_count}</h2>
        </div>
        """, unsafe_allow_html=True)
        
    with m_col3:
        st.markdown(f"""
        <div class="metric-glow" style="border-left-color: #3b82f6;">
            <h5 style="color:#64748b; margin:0;">Đang xử lý</h5>
            <h2 style="color:#3b82f6; margin:10px 0 0 0; font-size:36px;">{doing_count}</h2>
        </div>
        """, unsafe_allow_html=True)
        
    with m_col4:
        st.markdown(f"""
        <div class="metric-glow" style="border-left-color: #10b981;">
            <h5 style="color:#64748b; margin:0;">Hoàn tất mục tiêu</h5>
            <h2 style="color:#10b981; margin:10px 0 0 0; font-size:36px;">{done_count}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h3 style='margin-top: 40px;'>🛡️ Chỉ số Lá chắn chống kiệt sức (Burnout Shield)</h3>", unsafe_allow_html=True)
    
    burnout_score = 0
    for t in active_tasks:
        if t["status"] != "Đã xong":
            prio = t.get("priority", "Trung bình")
            burnout_score += 3 if prio == "Cao" else (2 if prio == "Trung bình" else 1)
            
    if burnout_score == 0:
        shield_status = "An toàn tối đa 🟢"
        shield_color = "#10b981"
        shield_msg = "Lá chắn hoàn hảo! Bạn không chịu bất kỳ áp lực công việc quá tải nào. Hãy tập trung bắt tay thực thi mục tiêu mới."
    elif burnout_score <= 6:
        shield_status = "Tải trọng tối ưu 🟢"
        shield_color = "#10b981"
        shield_msg = "Mức độ công việc lý tưởng! Khối lượng công việc đang nằm trong tầm kiểm soát tuyệt vời của bạn."
    elif burnout_score <= 12:
        shield_status = "Cảnh báo quá tải nhẹ 🟡"
        shield_color = "#f59e0b"
        shield_msg = "Bạn đang gánh vác lượng công việc tương đối lớn. Hãy hạn chế nhận thêm việc mới và rã bớt các nhiệm vụ phức tạp."
    else:
        shield_status = "Nguy cơ kiệt sức cực độ 🔴"
        shield_color = "#ef4444"
        shield_msg = "🚨 BÁO ĐỘNG ĐỎ! Mức độ áp lực não bộ đang quá tải trầm trọng! Hãy lập tức hoãn/chia sẻ bớt việc hoặc nhờ AI hỗ trợ chia nhỏ các đầu việc này ngay."

    st.markdown(f"""
    <div class="glass-card" style="border-left: 6px solid {shield_color};">
        <h4 style="color:{shield_color}; margin: 0 0 10px 0;">Trạng thái: {shield_status} (Điểm áp lực hiện tại: {burnout_score})</h4>
        <p style="margin: 0; color: #cbd5e1; font-size: 14px; line-height: 1.6;">{shield_msg}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3>🎯 Tiến độ mục tiêu ngày hôm nay</h3>", unsafe_allow_html=True)
    if total_active > 0:
        progress_val = done_count / total_active
        st.markdown(f"**Tỉ lệ hoàn thành:** {int(progress_val*100)}%")
        st.progress(progress_val)
    else:
        st.info("Chào bạn mới! Hãy tạo lập mục tiêu đầu tiên tại tab 'Nhiệm vụ' để kiểm soát cuộc chơi nhé!")

# ==========================================
# TAB 2: NHIỆM VỤ (TASK MANAGEMENT)
# ==========================================
with tab_tasks:
    st.markdown("<h2 style='color:#3b82f6;'>📋 Trung tâm Quản trị Nhiệm vụ</h2>", unsafe_allow_html=True)
    
    st.markdown("### 🔍 Bộ lọc nâng cao")
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    
    with f_col1:
        search_query = st.text_input("🔍 Tìm kiếm theo tên hoặc ghi chú:", placeholder="Gõ từ khóa...")
    with f_col2:
        proj_list = list(set([t.get("project", "Mặc định") for t in user_tasks]))
        filter_project = st.selectbox("📂 Lọc theo Dự án:", ["Tất cả"] + proj_list)
    with f_col3:
        filter_priority = st.selectbox("🔴 Lọc theo Độ ưu tiên:", ["Tất cả", "Cao", "Trung bình", "Thấp"])
    with f_col4:
        filter_status = st.selectbox("🎯 Lọc theo Trạng thái:", ["Tất cả", "Cần làm", "Đang làm", "Đã xong"])

    sort_by = st.selectbox("⚙️ Sắp xếp danh sách theo:", ["Mặc định", "Hạn chót (Gần nhất)", "Độ ưu tiên (Cao -> Thấp)"])
    
    st.markdown("---")

    col_add1, col_add2 = st.columns([1, 1])
    
    with col_add1:
        st.markdown("### ➕ Thêm mục tiêu thủ công")
        with st.form("add_task_form", clear_on_submit=True):
            new_title = st.text_input("Tên mục tiêu cần làm (*):")
            new_project = st.text_input("Tên dự án:", value="Mặc định")
            new_priority = st.selectbox("Độ ưu tiên:", ["Cao", "Trung bình", "Thấp"], index=1)
            new_due = st.date_input("Hạn chót hoàn thành:", value=date.today())
            new_notes = st.text_area("Ghi chú chi tiết cách làm:")
            
            submitted = st.form_submit_button("Lưu mục tiêu vào hệ thống")
            if submitted:
                if not new_title.strip():
                    st.error("Tên mục tiêu không được để trống!")
                else:
                    new_id = random.randint(10000, 99999)
                    while any(t["id"] == new_id for t in all_tasks):
                        new_id = random.randint(10000, 99999)
                        
                    new_t = {
                        "id": new_id,
                        "title": new_title.strip(),
                        "project": new_project.strip() if new_project.strip() else "Mặc định",
                        "status": "Cần làm",
                        "priority": new_priority,
                        "due_date": str(new_due),
                        "notes": new_notes.strip(),
                        "archived": False,
                        "owner": current_user
                    }
                    all_tasks.append(new_t)
                    save_tasks(all_tasks)
                    
                    st.session_state.user_xp += 10
                    all_users[current_user]["xp"] = st.session_state.user_xp
                    save_users(all_users)
                    
                    st.success(f"🎉 Đã thêm mục tiêu thành công! Bạn nhận được +10 XP.")
                    st.rerun()

    with col_add2:
        st.markdown("### 🧠 AI Task Splitter - Tự động rã việc")
        st.write("Nhập mục tiêu lớn phức tạp, SoloMind AI sẽ tự phân tích và phân rã thành các hành động con nhỏ lập tức.")
        
        if HAS_AI and api_key_input:
            with st.container():
                ai_goal = st.text_area("Mục tiêu lớn cần rã việc:", placeholder="Ví dụ: Thiết lập kế hoạch marketing ra mắt sản phẩm giày chạy bộ mới")
                ai_proj_name = st.text_input("Gán cho Dự án:", placeholder="Ví dụ: Marketing")
                
                if st.button("🚀 Thực hiện rã việc bằng AI", use_container_width=True):
                    if not ai_goal.strip():
                        st.error("Vui lòng nhập mục tiêu lớn trước!")
                    else:
                        with st.spinner("SoloMind AI đang phân rã và thiết kế lộ trình tối ưu cho bạn..."):
                            system_instr = (
                                "Bạn là SoloMind AI, một chuyên gia phân tách mục tiêu công việc. "
                                "Nhiệm vụ của bạn là nhận vào một mục tiêu lớn và trả về chính xác "
                                "một danh sách gồm các nhiệm vụ con khả thi có thể hành động được ngay lập tức. "
                                "BẮT BUỘC phản hồi dưới dạng chuỗi JSON nguyên bản, không bao gồm giải thích thừa bên ngoài định dạng JSON này. "
                                "Định dạng mẫu:\n"
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
                                        while any(t["id"] == new_id for t in all_tasks):
                                            new_id = random.randint(10000, 99999)
                                        
                                        new_t = {
                                            "id": new_id,
                                            "title": stask.get("title", "Việc con không tên").strip(),
                                            "project": ai_proj_name.strip() if ai_proj_name.strip() != "" else "Dự án AI",
                                            "status": "Cần làm",
                                            "priority": stask.get("priority", "Trung bình"),
                                            "due_date": str(date.today()),
                                            "notes": stask.get("notes", "").strip(),
                                            "archived": False,
                                            "owner": current_user
                                        }
                                        all_tasks.append(new_t)
                                        added_count += 1
                                    save_tasks(all_tasks)
                                    st.success(f"🎉 Đã rã thành công và tự động thêm {added_count} task vào dự án '{ai_proj_name}'!")
                                    st.rerun()
                                else:
                                    st.error("AI không phản hồi đúng định dạng danh sách công việc. Hãy thử lại!")
                            except Exception as e:
                                st.error(f"Lỗi phân tích cú pháp AI: {e}")
                                with st.expander("Xem chi tiết lỗi"):
                                    st.code(ai_response)
        else:
            st.warning("⚠️ Vui lòng cài đặt thư viện AI và nhập API Key ở thanh bên để kích hoạt tính năng rã việc tự động!")

    st.markdown("---")
    st.subheader("📋 Danh sách công việc đang thực hiện")
    
    display_tasks = [t for t in user_tasks if not t.get("archived", False)]
    if search_query:
        display_tasks = [t for t in display_tasks if search_query.lower() in t["title"].lower() or search_query.lower() in t.get("notes", "").lower()]
    if filter_project != "Tất cả":
        display_tasks = [t for t in display_tasks if t.get("project", "Mặc định") == filter_project]
    if filter_priority != "Tất cả":
        display_tasks = [t for t in display_tasks if t["priority"] == filter_priority]
    if filter_status != "Tất cả":
        display_tasks = [t for t in display_tasks if t["status"] == filter_status]
        
    if sort_by == "Hạn chót (Gần nhất)":
        display_tasks = sorted(display_tasks, key=lambda x: x.get("due_date", "9999-12-31"))
    elif sort_by == "Độ ưu tiên (Cao -> Thấp)":
        p_map = {"Cao": 1, "Trung bình": 2, "Thấp": 3}
        display_tasks = sorted(display_tasks, key=lambda x: p_map.get(x["priority"], 99))

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
                            for t in all_tasks:
                                if t["id"] == task["id"] and t.get("owner") == current_user:
                                    t["status"] = next_s
                                    if next_s == "Đã xong":
                                        st.session_state.user_xp += 30
                                        all_users[current_user]["xp"] = st.session_state.user_xp
                                        save_users(all_users)
                                        st.toast("🔥 Bạn nhận được +30 XP vì đã hoàn thành mục tiêu!")
                                    break
                            save_tasks(all_tasks)
                            st.rerun()
                            
                    with col_b2:
                        if st.button("📦 Lưu trữ", key=f"archive_btn_{task['id']}_{idx}", use_container_width=True):
                            for t in all_tasks:
                                if t["id"] == task["id"] and t.get("owner") == current_user:
                                    t["archived"] = True
                                    break
                            save_tasks(all_tasks)
                            st.success("Đã chuyển vào kho lưu trữ!")
                            st.rerun()
                            
                    with col_b3:
                        if st.button("🗑️ Xóa bỏ", key=f"delete_btn_{task['id']}_{idx}", use_container_width=True):
                            all_tasks = [t for t in all_tasks if not (t["id"] == task["id"] and t.get("owner") == current_user)]
                            save_tasks(all_tasks)
                            st.success("Đã xóa vĩnh viễn!")
                            st.rerun()

# ==========================================
# TAB 3: TRỢ LÝ CHAT AI (SOLOMIND CHATBOT)
# ==========================================
with tab_ai:
    st.subheader("🧠 Trợ lý AI - SoloMind Chatbot")
    st.write("SoloMind sẽ đồng hành cùng bạn để lên ý tưởng, trả lời câu hỏi và giúp bạn quản trị dự án hiệu quả hơn.")
    
    if HAS_AI and api_key_input:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        col_chat_title, col_chat_clear = st.columns([4, 1])
        with col_chat_clear:
            if st.button("🗑️ Xóa lịch sử chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
                
        st.markdown("---")
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        if user_input := st.chat_input("Nhập câu hỏi tại đây... Ví dụ: Gợi ý cho tôi cách sắp xếp công việc"):
            with st.chat_message("user"):
                st.write(user_input)
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            context = f"Danh sách công việc của người dùng {current_user} hiện tại:\n"
            for t in active_tasks:
                context += f"- [{t['status']}] {t['title']} (Dự án: {t.get('project','Mặc định')}, Độ ưu tiên: {t['priority']})\n"
                
            system_instruction = (
                f"Bạn là SoloMind, trợ lý ảo thông minh tích hợp sẵn trong ứng dụng quản trị cá nhân SoloFlow OS v5.5. "
                f"Dưới đây là danh sách công việc hiện tại của người dùng {current_user}:\n{context}\n"
                f"Hãy trả lời người dùng một cách thân thiện, hài hước, truyền động lực mạnh mẽ và luôn sẵn sàng "
                f"đưa ra lời khuyên cụ thể dựa trên danh sách công việc của họ nếu được hỏi. Hãy nói tiếng Việt thật tự nhiên."
            )
            
            with st.chat_message("assistant"):
                with st.spinner("SoloMind đang suy nghĩ..."):
                    ai_reply = call_gemini(user_input, system_instruction=system_instruction)
                    st.write(ai_reply)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
    else:
        st.warning("⚠️ Vui lòng cài đặt thư viện AI và nhập API Key ở thanh bên để kích hoạt Trợ lý AI SoloMind!")

# ==========================================
# TAB 4: KHO LƯU TRỮ (ARCHIVE)
# ==========================================
with tab_archive:
    st.subheader("📦 Các công việc đã được lưu trữ (Archive)")
    archived_tasks = [t for t in user_tasks if t.get("archived", False)]
    
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
                            for t in all_tasks:
                                if t["id"] == task["id"] and t.get("owner") == current_user:
                                    t["archived"] = False
                                    break
                            save_tasks(all_tasks)
                            st.success("Đã khôi phục nhiệm vụ thành công!")
                            st.rerun()
                    with col_ab2:
                        if st.button("🗑️ Xóa hẳn", key=f"force_del_btn_{task['id']}_{idx}", use_container_width=True):
                            all_tasks = [t for t in all_tasks if not (t["id"] == task["id"] and t.get("owner") == current_user)]
                            save_tasks(all_tasks)
                            st.success("Đã xóa vĩnh viễn!")
                            st.rerun()

# ==========================================
# TAB 5: HỆ THỐNG & SAO LƯU
# ==========================================
with tab_system:
    st.subheader("⚙️ Quản lý Cơ sở Dữ liệu & Sao lưu dự phòng")
    st.markdown("---")
    col_sys1, col_sys2 = st.columns(2)
    
    with col_sys1:
        st.markdown("### 📥 Tải xuống Bản sao lưu cá nhân (Export Backup)")
        try:
            user_json_data = json.dumps(user_tasks, indent=4, ensure_ascii=False)
            st.download_button(
                label=f"💾 Tải về file tasks_{current_user}.json",
                data=user_json_data,
                file_name=f"tasks_{current_user}_backup.json",
                mime="application/json",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Không thể đọc tệp dữ liệu: {e}")
            
    with col_sys2:
        st.markdown("### 📤 Khôi phục từ Bản sao lưu (Import Backup)")
        uploaded_file = st.file_uploader("Chọn file backup (.json):", type=["json"])
        if uploaded_file is not None:
            try:
                uploaded_tasks = json.load(uploaded_file)
                if isinstance(uploaded_tasks, list):
                    if st.button("⚠️ Xác nhận khôi phục đè dữ liệu công việc", use_container_width=True, type="primary"):
                        filtered_global_tasks = [t for t in all_tasks if t.get("owner") != current_user]
                        for ut in uploaded_tasks:
                            ut["owner"] = current_user
                        filtered_global_tasks.extend(uploaded_tasks)
                        save_tasks(filtered_global_tasks)
                        st.success("Khôi phục thành công! Trang sẽ tải lại ngay.")
                        st.rerun()
                else:
                    st.error("File backup không đúng cấu trúc dữ liệu SoloFlow OS.")
            except Exception as e:
                st.error(f"Lỗi phân tích cú pháp file: {e}")