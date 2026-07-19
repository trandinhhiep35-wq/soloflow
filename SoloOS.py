import streamlit as st
import pandas as pd
import json
import os
import time
import random
import math
import hashlib
from datetime import date, datetime, timedelta

# --- CẤU HÌNH TRANG WEB CHUẨN PREMIUM ---
st.set_page_config(
    page_title="SoloFlow OS v5.5 Ultimate Auth",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ĐƯỜNG DẪN CƠ SỞ DỮ LIỆU ---
DB_FILE = "tasks.json"
USER_FILE = "users.json"

# --- KIỂM TRA THƯ VIỆN GOOGLE AI ---
try:
    import google.generativeai as genai
    HAS_AI = True
except ImportError:
    HAS_AI = False

def inject_premium_css(theme_choice="Deep Obsidian"):
    """Nhúng hệ thống giao diện tối Dark Cosmic siêu sang trọng với các biến thể màu theo Theme."""
    themes = {
        "Deep Obsidian": {
            "bg": "#090d16", "card_bg": "rgba(13, 20, 35, 0.85)", "border": "rgba(59, 130, 246, 0.25)",
            "primary": "#3b82f6", "accent": "#10b981", "glow": "rgba(59, 130, 246, 0.15)", "text": "#f1f5f9"
        },
        "Nebula Pink": {
            "bg": "#0d0714", "card_bg": "rgba(30, 15, 45, 0.85)", "border": "rgba(236, 72, 153, 0.25)",
            "primary": "#ec4899", "accent": "#8b5cf6", "glow": "rgba(236, 72, 153, 0.15)", "text": "#fdf2f8"
        },
        "Emerald Forest": {
            "bg": "#060f0e", "card_bg": "rgba(12, 30, 25, 0.85)", "border": "rgba(16, 185, 129, 0.25)",
            "primary": "#10b981", "accent": "#eab308", "glow": "rgba(16, 185, 129, 0.15)", "text": "#f0fdf4"
        },
        "Cyberpunk Gold": {
            "bg": "#0f0e06", "card_bg": "rgba(28, 26, 12, 0.85)", "border": "rgba(234, 179, 8, 0.25)",
            "primary": "#eab308", "accent": "#f97316", "glow": "rgba(234, 179, 8, 0.15)", "text": "#fefdf0"
        }
    }
    
    t = themes.get(theme_choice, themes["Deep Obsidian"])
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] {{
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }}
        
        .stApp {{
            background-color: {t['bg']};
            color: {t['text']};
        }}
        
        /* Khung Đăng nhập Glassmorphic Cosmic cực kỳ cao cấp */
        .auth-card {{
            background: linear-gradient(135deg, {t['card_bg']} 0%, rgba(10, 10, 18, 0.9) 100%);
            backdrop-filter: blur(20px);
            border: 1px solid {t['border']};
            border-radius: 24px;
            padding: 40px;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6), 0 0 50px {t['glow']};
            max-width: 500px;
            margin: 40px auto;
            text-align: center;
        }}
        
        /* Thẻ Glassmorphism cao cấp */
        .glass-card {{
            background: {t['card_bg']};
            backdrop-filter: blur(12px);
            border: 1px solid {t['border']};
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            margin-bottom: 20px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .glass-card:hover {{
            border-color: {t['primary']};
            box-shadow: 0 8px 32px 0 {t['glow']};
            transform: translateY(-2px);
        }}

        /* Thẻ VIP Platinum siêu đặc biệt */
        .premium-vip-card {{
            background: linear-gradient(135deg, rgba(234, 179, 8, 0.15) 0%, rgba(249, 115, 22, 0.15) 100%);
            backdrop-filter: blur(15px);
            border: 2px solid #eab308;
            border-radius: 20px;
            padding: 24px;
            box-shadow: 0 0 30px rgba(234, 179, 8, 0.25);
            margin-bottom: 20px;
            position: relative;
            overflow: hidden;
        }}
        
        .premium-vip-card::after {{
            content: 'PLUS';
            position: absolute;
            top: 15px;
            right: -25px;
            background: linear-gradient(90deg, #f59e0b, #ef4444);
            color: #fff;
            font-size: 10px;
            font-weight: 800;
            padding: 4px 30px;
            transform: rotate(45deg);
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }}
        
        /* Thiết kế Profile Header Card */
        .profile-header-card {{
            background: linear-gradient(135deg, {t['card_bg']} 0%, rgba(10, 10, 18, 0.95) 100%);
            border: 1px solid {t['border']};
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 15px 35px rgba(0,0,0,0.4);
            margin-bottom: 20px;
        }}

        .avatar-glow {{
            font-size: 72px;
            line-height: 1;
            margin-bottom: 15px;
            display: inline-block;
            filter: drop-shadow(0 0 12px {t['primary']});
        }}
        
        /* Thanh chỉ số nổi bật */
        .metric-glow {{
            background: linear-gradient(135deg, {t['card_bg']} 0%, rgba(5, 5, 10, 0.9) 100%);
            border-left: 5px solid {t['primary']};
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        
        /* Thiết kế 4 vùng ma trận Eisenhower */
        .eisenhower-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 30px;
        }}
        
        .matrix-box {{
            padding: 20px;
            border-radius: 16px;
            min-height: 150px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }}
        
        .matrix-do {{ background: rgba(239, 68, 68, 0.12); border-left: 5px solid #ef4444; }}
        .matrix-schedule {{ background: rgba(59, 130, 246, 0.12); border-left: 5px solid #3b82f6; }}
        .matrix-delegate {{ background: rgba(245, 158, 11, 0.12); border-left: 5px solid #f59e0b; }}
        .matrix-eliminate {{ background: rgba(100, 116, 139, 0.12); border-left: 5px solid #64748b; }}

        /* Phong cách nút nhấn đồng bộ */
        .stButton>button {{
            background: linear-gradient(135deg, {t['primary']} 0%, {t['accent']} 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 12px {t['glow']} !important;
        }}
        
        .stButton>button:hover {{
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px {t['glow']} !important;
        }}
        
        /* Thanh tiến trình tuỳ chỉnh */
        .stProgress > div > div > div > div {{
            background-image: linear-gradient(to right, {t['primary']}, {t['accent']}) !important;
        }}
        
        /* Kiểu chữ tiêu đề đẹp mắt */
        h1, h2, h3 {{
            font-weight: 800 !important;
            letter-spacing: -0.025em !important;
            background: linear-gradient(to right, #ffffff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        /* Làm nổi bật logo */
        .logo-text {{
            font-size: 42px;
            font-weight: 800;
            background: linear-gradient(to right, {t['primary']}, {t['accent']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }}

        /* Pricing Card phong cách SaaS Plus */
        .pricing-card {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            transition: all 0.3s ease;
        }}
        .pricing-card.popular {{
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(139, 92, 246, 0.08) 100%);
            border: 2px solid {t['primary']};
            transform: scale(1.03);
        }}
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
                "created_at": str(datetime.now()),
                "display_name": "Quản Trị Viên",
                "bio": "Người vận hành tối cao của hệ sinh thái SoloFlow OS.",
                "daily_goal": 5,
                "avatar": "⚡",
                "is_plus": False,
                "theme": "Deep Obsidian",
                "focus_history": []
            }
        }
        save_users(default_users)
        return default_users
    try:
        with open(USER_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Đồng bộ cấu trúc dữ liệu mới cho các tài khoản cũ
            for u in data:
                if "display_name" not in data[u]: data[u]["display_name"] = u
                if "bio" not in data[u]: data[u]["bio"] = "Chiến binh kỷ luật của SoloFlow."
                if "daily_goal" not in data[u]: data[u]["daily_goal"] = 3
                if "avatar" not in data[u]: data[u]["avatar"] = "🚀"
                if "is_plus" not in data[u]: data[u]["is_plus"] = False
                if "theme" not in data[u]: data[u]["theme"] = "Deep Obsidian"
                if "focus_history" not in data[u]: data[u]["focus_history"] = []
            return data
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
    """Tải tất cả danh sách nhiệm vụ từ cơ sở dữ liệu JSON."""
    if not os.path.exists(DB_FILE):
        return [
            {"id": 10001, "title": "Thiết kế UI/UX hệ thống quản trị", "project": "SoloFlow 5.5", "status": "Đang làm", "priority": "Cao", "due_date": str(date.today()), "notes": "Cập nhật màn hình đăng nhập Glassmorphism", "archived": False, "owner": "admin", "energy_cost": 4, "category": "Làm ngay"},
            {"id": 10002, "title": "Bảo mật hóa mật khẩu", "project": "Bảo mật", "status": "Đã xong", "priority": "Cao", "due_date": str(date.today()), "notes": "Băm mật khẩu người dùng với SHA-256", "archived": False, "owner": "admin", "energy_cost": 3, "category": "Làm ngay"}
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

# --- KHỞI TẠO STATE HỆ THỐNG ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "user_xp" not in st.session_state:
    st.session_state.user_xp = 0
if "energy_level" not in st.session_state:
    st.session_state.energy_level = 80
if "binaural_playing" not in st.session_state:
    st.session_state.binaural_playing = False

# Tải dữ liệu ban đầu
all_users = load_users()
all_tasks = load_tasks()

def call_gemini(prompt: str, system_instruction: str = "") -> str:
    """Gọi công cụ AI Gemini 1.5 Flash an toàn."""
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
    """Phân tách định dạng JSON từ phản hồi thô của Gemini."""
    cleaned = raw_text.strip()
    if "```json" in cleaned:
        cleaned = cleaned.split("```json")[1].split("```")[0].strip()
    elif "```" in cleaned:
        cleaned = cleaned.split("```")[1].split("```")[0].strip()
    return json.loads(cleaned)

# --- MÀN HÌNH ĐĂNG NHẬP CHUYÊN NGHIỆP ---
if not st.session_state.logged_in:
    inject_premium_css("Deep Obsidian")
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    
    with col_l2:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown('<div class="logo-text">⚡ SoloFlow OS</div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#64748b; margin-bottom: 25px;">Hệ thống quản trị năng suất và rèn luyện Flow State chuẩn VIP 5.5</p>', unsafe_allow_html=True)
        
        auth_mode = st.radio("Lựa chọn phương thức truy cập:", ["Đăng Nhập", "Đăng Ký Tài Khoản Mới"], horizontal=True, label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        
        username_input = st.text_input("👤 Tên tài khoản:", placeholder="Nhập tên đăng nhập của bạn...", key="auth_username")
        password_input = st.text_input("🔑 Mật khẩu bảo mật:", type="password", placeholder="Nhập mật khẩu...", key="auth_password")
        
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
                    st.toast(f"🔥 Chào mừng quay trở lại, {all_users[user_clean].get('display_name', user_clean)}!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ Tài khoản hoặc mật khẩu không chính xác!")
        else:
            confirm_password = st.text_input("🔄 Xác nhận mật khẩu:", type="password", placeholder="Nhập lại mật khẩu...", key="auth_confirm")
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
                        "created_at": str(datetime.now()),
                        "display_name": user_clean,
                        "bio": "Chiến binh kỷ luật mới của SoloFlow OS.",
                        "daily_goal": 3,
                        "avatar": "🌱",
                        "is_plus": False,
                        "theme": "Deep Obsidian",
                        "focus_history": []
                    }
                    save_users(all_users)
                    
                    # Tạo công việc mẫu ban đầu
                    new_starter_tasks = [
                        {"id": random.randint(10000, 99999), "title": "Khám phá SoloFlow OS v5.5", "project": "Bắt đầu", "status": "Cần làm", "priority": "Thấp", "due_date": str(date.today()), "notes": "Cài đặt khóa AI và trải nghiệm trình phát nhạc sóng não ở Sidebar.", "archived": False, "owner": user_clean, "energy_cost": 1, "category": "Lên lịch"}
                    ]
                    all_tasks.extend(new_starter_tasks)
                    save_tasks(all_tasks)
                    
                    st.success(f"🎉 Đăng ký thành công! Đăng nhập tự động sau giây lát.")
                    st.balloons()
                    time.sleep(1)
                    st.session_state.logged_in = True
                    st.session_state.current_user = user_clean
                    st.session_state.user_xp = 100
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- TRÍCH XUẤT THÔNG TIN NGƯỜI DÙNG HIỆN TẠI ---
current_user = st.session_state.current_user
user_info = all_users.get(current_user, {})
display_name = user_info.get("display_name", current_user)
user_avatar = user_info.get("avatar", "🚀")
user_bio = user_info.get("bio", "Chiến binh kỷ luật.")
daily_goal = user_info.get("daily_goal", 3)
is_plus = user_info.get("is_plus", False)
user_theme = user_info.get("theme", "Deep Obsidian")

# Tải các task thuộc quyền sở hữu của user hiện tại
user_tasks = [t for t in all_tasks if t.get("owner") == current_user]

# Nhúng CSS thích ứng với Theme được lưu trữ trong Database
inject_premium_css(user_theme)

# --- SIDEBAR HỆ THỐNG ---
with st.sidebar:
    st.markdown(f"<h2 style='color:#3b82f6;'>⚡ SoloFlow OS</h2>", unsafe_allow_html=True)
    
    # Hiển thị Mini-Profile chất lượng cao
    vip_badge = "<span style='background: linear-gradient(90deg, #f59e0b, #ef4444); color: white; padding: 2px 8px; border-radius: 20px; font-size: 11px; font-weight: bold; margin-left: 5px; box-shadow: 0 0 10px rgba(245,158,11,0.5);'>⭐ PLUS</span>" if is_plus else "<span style='background: #475569; color: white; padding: 2px 8px; border-radius: 20px; font-size: 11px;'>Standard</span>"
    
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); text-align: center; margin-bottom: 15px;">
        <span style="font-size: 38px; filter: drop-shadow(0 0 8px #3b82f6);">{user_avatar}</span>
        <h4 style="margin: 5px 0 2px 0; color: #f1f5f9; display: flex; align-items: center; justify-content: center;">{display_name} {vip_badge}</h4>
        <small style="color: #64748b; font-family: monospace;">@{current_user}</small>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 Đăng xuất hệ thống", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.user_xp = 0
        st.rerun()
        
    st.markdown("---")
    
    # Hệ thống thăng cấp Gamification
    st.markdown("### 🏆 Trình độ rèn luyện")
    user_xp = st.session_state.user_xp
    user_lvl = int((user_xp / 100) ** 0.5) + 1
    
    if user_lvl < 2:
        rank_name = "Zen Beginner 🌱"
    elif user_lvl < 4:
        rank_name = "Flow Explorer 🌀"
    else:
        rank_name = "Ultimate Flow Master 🌌"
        
    st.markdown(f"**Cấp độ hiện tại:** Level {user_lvl} ({rank_name})")
    
    xp_floor = (10 * (user_lvl - 1)) ** 2
    xp_ceil = (10 * user_lvl) ** 2
    xp_range = max((xp_ceil - xp_floor), 1)
    current_progress = (user_xp - xp_floor) / xp_range
    current_progress = min(max(current_progress, 0.0), 1.0)
    
    st.markdown(f"<small>Tiến trình cấp độ: {user_xp} / {xp_ceil} XP</small>", unsafe_allow_html=True)
    st.progress(current_progress)
    
    st.markdown("---")
    
    # Kích hoạt AI Engine
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
        st.success("Trí tuệ AI đã sẵn sàng!")
    else:
        st.warning("AI đang tạm khóa (Thiếu Key)")
        
    st.markdown("---")
    st.caption("🚀 Bản phát hành SoloFlow Plus Ultimate VIP v5.5.")

# --- ĐỊNH HƯỚNG TABS LÀM VIỆC CHÍNH ---
tab_dashboard, tab_tasks, tab_ai, tab_profile, tab_plus, tab_archive_sys = st.tabs([
    "📊 Dashboard", 
    "📋 Nhiệm vụ", 
    "🧠 SoloMind AI", 
    "👤 Hồ Sơ & Cài Đặt",
    "💎 SoloFlow PLUS VIP",
    "📦 Sao Lưu & Lưu Trữ"
])

active_tasks = [t for t in user_tasks if not t.get("archived", False)]

# ==========================================
# TAB 1: DASHBOARD (TỔNG QUAN HIỆU SUẤT)
# ==========================================
with tab_dashboard:
    st.markdown(f"<h1 style='text-align: center; color: #3b82f6; margin-bottom: 5px;'>{user_avatar} Trung Tâm Hiệu Suất: {display_name}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color:#64748b; margin-bottom: 25px;'>\"{user_bio}\"</p>", unsafe_allow_html=True)
    
    if is_plus:
        st.markdown("""
        <div class="premium-vip-card">
            <h4 style="color:#eab308; margin:0 0 5px 0;">🌌 Chào mừng Thành viên PLUS Thượng Hạng!</h4>
            <p style="margin:0; font-size: 13px; color: #fefdf0; opacity: 0.9;">
                Tài khoản của bạn đã được mở khóa toàn bộ các siêu tính năng: Bản đồ tư duy AI Mind Map, Giao diện Theme Cosmic phong phú, Biorhythm năng lượng chuyên sâu và 3D Audio Mixer. Chúc bạn một ngày làm việc ngập tràn năng lượng đỉnh cao!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Hệ thống chỉ số Grid
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    total_active = len(active_tasks)
    pending_count = len([t for t in active_tasks if t["status"] == "Cần làm"])
    doing_count = len([t for t in active_tasks if t["status"] == "Đang làm"])
    done_count = len([t for t in active_tasks if t["status"] == "Đã xong"])
    
    with m_col1:
        st.markdown(f'<div class="metric-glow"><h5>Tổng công việc</h5><h2 style="font-size:36px;">{total_active}</h2></div>', unsafe_allow_html=True)
    with m_col2:
        st.markdown(f'<div class="metric-glow" style="border-left-color: #f59e0b;"><h5>Cần thực hiện</h5><h2 style="font-size:36px; color:#f59e0b;">{pending_count}</h2></div>', unsafe_allow_html=True)
    with m_col3:
        st.markdown(f'<div class="metric-glow" style="border-left-color: #3b82f6;"><h5>Đang xử lý</h5><h2 style="font-size:36px; color:#3b82f6;">{doing_count}</h2></div>', unsafe_allow_html=True)
    with m_col4:
        st.markdown(f'<div class="metric-glow" style="border-left-color: #10b981;"><h5>Hoàn tất hôm nay</h5><h2 style="font-size:36px; color:#10b981;">{done_count}</h2></div>', unsafe_allow_html=True)

    st.markdown("<h3 style='margin-top: 30px;'>🔋 Trạng thái Năng lượng Sinh học (Circadian Rhythm)</h3>", unsafe_allow_html=True)
    
    # Khảo sát / Lựa chọn mức năng lượng cho thuật toán Circadian
    col_en1, col_en2 = st.columns([1, 2])
    with col_en1:
        energy_slider = st.slider("Mức sinh lực tự cảm nhận (%):", 10, 100, st.session_state.energy_level, step=5)
        st.session_state.energy_level = energy_slider
    with col_en2:
        if is_plus:
            # Thuật toán tính nhịp sinh học phức tạp theo múi giờ sinh hoạt của bản Plus
            now_hour = datetime.now().hour
            # Hàm sóng năng lượng dạng Sin mô phỏng chu kỳ năng lượng trong ngày
            biorhythm_calc = int((math.sin((now_hour - 6) * math.pi / 12) + 1) * 50)
            
            # Tính toán khuyến cáo
            if biorhythm_calc > 70:
                plus_status = "ĐỈNH CAO HOẠT ĐỘNG 🔥"
                plus_tip = "Chu kỳ sinh học cho thấy não bộ của bạn đang ở trạng thái minh mẫn nhất. Hãy giải quyết ngay các nhiệm vụ siêu khó hoặc sử dụng AI Task Splitter!"
            elif biorhythm_calc > 40:
                plus_status = "ỔN ĐỊNH DUY TRÌ 📈"
                plus_tip = "Năng lượng đang ở mức trung bình ổn định. Phù hợp cho các cuộc họp, dọn dẹp hòm thư hoặc làm các nhiệm vụ độ khó Trung bình."
            else:
                plus_status = "CHU KỲ SUY KIỆT - NGHỈ NGƠI 💤"
                plus_tip = "Chu kỳ tự nhiên báo hiệu cơ thể đang cần phục hồi. Hãy giảm tải, bật 3D Audio Mixer ở Sidebar với sóng nhạc Theta để thư giãn đầu óc."

            st.markdown(f"""
            <div class="glass-card" style="border-left: 5px solid #eab308; padding: 15px; margin-bottom: 0;">
                <h5 style="color:#eab308; margin:0 0 5px 0;">🧬 Chỉ số Circadian Plus khuyên dùng: {biorhythm_calc}% ({plus_status})</h5>
                <p style="margin:0; font-size:13px; color:#cbd5e1; line-height:1.4;">{plus_tip}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("💡 Nâng cấp bản **PLUS** để kích hoạt biểu đồ nhịp sinh học tự động Circadian Rhythm dựa trên múi giờ thực tế để tối ưu hóa thời gian tập trung!")

    # Lá chắn chống kiệt sức Burnout Shield 2.0
    st.markdown("<h3 style='margin-top: 30px;'>🛡️ Lá chắn chống kiệt sức v2.0 (Burnout Shield)</h3>", unsafe_allow_html=True)
    work_load = 0
    for t in active_tasks:
        if t["status"] != "Đã xong":
            energy_weight = t.get("energy_cost", 2)
            prio_weight = 3 if t.get("priority") == "Cao" else (2 if t.get("priority") == "Trung bình" else 1)
            work_load += (energy_weight * prio_weight)
            
    if work_load == 0:
        shield_percentage = 100
    else:
        shield_percentage = int((st.session_state.energy_level / (st.session_state.energy_level + work_load)) * 100)

    if shield_percentage > 75:
        shield_color = "#10b981"
        shield_msg = "An toàn tối ưu. Cơ thể bạn đang dồi dào năng lượng so với khối lượng công việc hiện tại."
    elif shield_percentage > 45:
        shield_color = "#f59e0b"
        shield_msg = "Mức độ tải trung bình. Hãy cân nhắc giải quyết dứt điểm các task tồn đọng, tránh nhận thêm dự án phức tạp."
    else:
        shield_color = "#ef4444"
        shield_msg = "🚨 CẢNH BÁO KIỆT SỨC TRẦM TRỌNG: Hãy hoãn các task độ tốn sức cao (⚡) hoặc dùng AI chia nhỏ công việc ngay!"

    st.markdown(f"""
    <div class="glass-card" style="border-left: 6px solid {shield_color};">
        <h4 style="color:{shield_color}; margin: 0 0 5px 0;">Trạng thái lá chắn an toàn: {shield_percentage}%</h4>
        <p style="margin: 0; color: #cbd5e1; font-size: 14px;">{shield_msg}</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# TAB 2: NHIỆM VỤ (TASK MANAGEMENT & EISENHOWER)
# ==========================================
with tab_tasks:
    st.markdown("<h2 style='color:#3b82f6;'>📋 Trung tâm Quản trị Nhiệm vụ</h2>", unsafe_allow_html=True)
    
    # Khung tìm kiếm và bộ lọc nâng cao
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    with f_col1:
        search_query = st.text_input("🔍 Tìm kiếm:", placeholder="Gõ tên hoặc ghi chú...", key="search_query")
    with f_col2:
        proj_list = list(set([t.get("project", "Mặc định") for t in user_tasks]))
        filter_project = st.selectbox("📂 Lọc Dự án:", ["Tất cả"] + proj_list, key="filter_proj")
    with f_col3:
        filter_priority = st.selectbox("🔴 Độ ưu tiên:", ["Tất cả", "Cao", "Trung bình", "Thấp"], key="filter_prio")
    with f_col4:
        filter_status = st.selectbox("🎯 Trạng thái:", ["Tất cả", "Cần làm", "Đang làm", "Đã xong"], key="filter_status")

    sort_by = st.selectbox("⚙️ Sắp xếp danh sách theo:", ["Mặc định", "Hạn chót (Gần nhất)", "Độ ưu tiên (Cao -> Thấp)"], key="sort_option")
    st.markdown("---")

    col_add1, col_add2 = st.columns([1, 1])
    
    with col_add1:
        st.markdown("### ➕ Thêm mục tiêu thủ công")
        with st.form("add_task_form", clear_on_submit=True):
            new_title = st.text_input("Tên mục tiêu cần làm (*):")
            new_project = st.text_input("Tên dự án:", value="Mặc định")
            new_priority = st.selectbox("Độ ưu tiên:", ["Cao", "Trung bình", "Thấp"], index=1)
            new_due = st.date_input("Hạn chót hoàn thành:", value=date.today())
            new_energy = st.slider("Mức tiêu hao sinh lực (1: cực nhẹ, 5: cực nặng):", 1, 5, 2)
            new_category = st.selectbox("Phân loại ma trận Eisenhower:", ["Làm ngay", "Lên lịch", "Ủy quyền", "Loại bỏ"])
            new_notes = st.text_area("Ghi chú chi tiết cách làm:")
            
            submitted = st.form_submit_button("Lưu mục tiêu vào hệ thống")
            if submitted:
                if not new_title.strip():
                    st.error("⚠️ Tên mục tiêu không được để trống!")
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
                        "owner": current_user,
                        "energy_cost": new_energy,
                        "category": new_category
                    }
                    all_tasks.append(new_t)
                    save_tasks(all_tasks)
                    
                    st.session_state.user_xp += 10
                    all_users[current_user]["xp"] = st.session_state.user_xp
                    save_users(all_users)
                    st.success("🎉 Đã thêm mục tiêu thành công! Bạn nhận được +10 XP.")
                    time.sleep(0.5)
                    st.rerun()

    with col_add2:
        st.markdown("### 🧠 AI Task Splitter - Tự động rã việc")
        st.write("Nhập mục tiêu lớn phức tạp, SoloMind AI sẽ tự phân tích và phân rã thành các hành động con nhỏ lập tức.")
        
        if HAS_AI and api_key_input:
            ai_goal = st.text_area("Mục tiêu lớn cần rã việc:", placeholder="Ví dụ: Lên kế hoạch tuần ra mắt sản phẩm thương mại mới...", key="ai_splitter_input")
            ai_proj_name = st.text_input("Gán cho Dự án:", placeholder="Ví dụ: Marketing", key="ai_splitter_project")
            
            if st.button("🚀 Thực hiện rã việc bằng AI", use_container_width=True):
                if not ai_goal.strip():
                    st.error("Vui lòng nhập mục tiêu lớn trước!")
                else:
                    with st.spinner("SoloMind AI đang phân rã công việc tối ưu..."):
                        system_instr = (
                            "Bạn là SoloMind AI, một chuyên gia phân tách mục tiêu công việc. "
                            "Nhiệm vụ của bạn là nhận vào một mục tiêu lớn và trả về chính xác "
                            "một danh sách gồm các nhiệm vụ con khả thi có thể hành động được ngay lập tức. "
                            "BẮT BUỘC phản hồi dưới dạng chuỗi JSON nguyên bản, không bao gồm giải thích thừa bên ngoài định dạng JSON này. "
                            "Định dạng mẫu:\n"
                            "[\n"
                            "  {\"title\": \"Nhiệm vụ 1\", \"priority\": \"Cao\", \"energy_cost\": 2, \"category\": \"Làm ngay\", \"notes\": \"Mô tả\"},\n"
                            "  {\"title\": \"Nhiệm vụ 2\", \"priority\": \"Trung bình\", \"energy_cost\": 1, \"category\": \"Lên lịch\", \"notes\": \"Mô tả\"}\n"
                            "]\n"
                            "Lưu ý: Trường priority chỉ nhận 'Cao', 'Trung bình', 'Thấp'. Trường category chỉ nhận 'Làm ngay', 'Lên lịch', 'Ủy quyền', 'Loại bỏ'."
                        )
                        ai_response = call_gemini(f"Mục tiêu lớn: {ai_goal}", system_instruction=system_instr)
                        try:
                            subtasks = parse_gemini_json(ai_response)
                            if isinstance(subtasks, list):
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
                                        "owner": current_user,
                                        "energy_cost": stask.get("energy_cost", 2),
                                        "category": stask.get("category", "Làm ngay")
                                    }
                                    all_tasks.append(new_t)
                                save_tasks(all_tasks)
                                st.success(f"🎉 Đã rã thành công {len(subtasks)} task vào dự án!")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error("AI không phản hồi đúng định dạng JSON danh sách. Thử lại!")
                        except Exception as e:
                            st.error(f"Lỗi phân tích cú pháp AI: {e}")
        else:
            st.warning("⚠️ Cần cài đặt API Key ở thanh bên để kích hoạt rã việc tự động bằng AI!")

    # Ma trận Eisenhower tự động
    st.markdown("### 🗃️ Ma trận Tập trung Eisenhower 2.0")
    e_do = [t for t in active_tasks if t.get("category") == "Làm ngay" and t["status"] != "Đã xong"]
    e_schedule = [t for t in active_tasks if t.get("category") == "Lên lịch" and t["status"] != "Đã xong"]
    e_delegate = [t for t in active_tasks if t.get("category") == "Ủy quyền" and t["status"] != "Đã xong"]
    e_eliminate = [t for t in active_tasks if t.get("category") == "Loại bỏ" and t["status"] != "Đã xong"]
    
    st.markdown("""
    <div class="eisenhower-grid">
        <div class="matrix-box matrix-do">
            <h4 style="color:#ef4444; margin-top:0;">🔴 Q1: Làm ngay (Do First)</h4>
            <p style="font-size:12px; color:#94a3b8;">Khẩn cấp & Quan trọng</p>
        </div>
        <div class="matrix-box matrix-schedule">
            <h4 style="color:#3b82f6; margin-top:0;">🔵 Q2: Lên lịch (Schedule)</h4>
            <p style="font-size:12px; color:#94a3b8;">Quan trọng nhưng không khẩn</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_mat_1, col_mat_2 = st.columns(2)
    with col_mat_1:
        for t in e_do[:3]: st.markdown(f"- ⚠️ **{t['title']}** (ID: {t['id']})")
        if not e_do: st.write("<small style='color:#64748b;'>Vùng này trống</small>", unsafe_allow_html=True)
    with col_mat_2:
        for t in e_schedule[:3]: st.markdown(f"- 📅 **{t['title']}** (ID: {t['id']})")
        if not e_schedule: st.write("<small style='color:#64748b;'>Vùng này trống</small>", unsafe_allow_html=True)

    # Hiển thị chi tiết Task
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

    for idx, task in enumerate(display_tasks):
        with st.container(border=True):
            col_head, col_info, col_actions = st.columns([4, 3, 3])
            with col_head:
                st.markdown(f"#### **{task['title']}**")
                st.markdown(f"📂 Dự án: **`{task.get('project', 'Mặc định')}`** | Ma trận: **`{task.get('category', 'Làm ngay')}`**")
                if task.get("notes"):
                    with st.expander("📝 Xem ghi chú"):
                        st.write(task["notes"])
            with col_info:
                p_emoji = "🔴" if task["priority"] == "Cao" else ("🟡" if task["priority"] == "Trung bình" else "🟢")
                st.markdown(f"**Độ ưu tiên:** {p_emoji} {task['priority']} | Trạng thái: **{task['status']}**")
                st.markdown(f"🔋 **Sinh lực:** {'⚡' * task.get('energy_cost', 2)}")
                st.markdown(f"📅 **Hạn chót:** {task.get('due_date', 'Không có')}")
            with col_actions:
                col_b1, col_b2, col_b3 = st.columns(3)
                with col_b1:
                    next_map = {"Cần làm": "Đang làm", "Đang làm": "Đã xong", "Đã xong": "Cần làm"}
                    next_s = next_map[task["status"]]
                    if st.button(f"➔ {next_s}", key=f"state_btn_{task['id']}_{idx}", use_container_width=True):
                        for t in all_tasks:
                            if t["id"] == task["id"] and t.get("owner") == current_user:
                                t["status"] = next_s
                                if next_s == "Đã xong":
                                    st.session_state.user_xp += 30
                                    all_users[current_user]["xp"] = st.session_state.user_xp
                                    save_users(all_users)
                                    st.toast("🔥 Bạn nhận được +30 XP!")
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
                        st.success("Đã lưu trữ!")
                        time.sleep(0.5)
                        st.rerun()
                with col_b3:
                    if st.button("🗑️ Xóa", key=f"delete_btn_{task['id']}_{idx}", use_container_width=True):
                        all_tasks = [t for t in all_tasks if not (t["id"] == task["id"] and t.get("owner") == current_user)]
                        save_tasks(all_tasks)
                        st.success("Đã xóa vĩnh viễn!")
                        time.sleep(0.5)
                        st.rerun()

# ==========================================
# TAB 3: TRỢ LÝ CHAT AI (SOLOMIND CHATBOT)
# ==========================================
with tab_ai:
    st.subheader("🧠 Trợ lý AI - SoloMind Chatbot")
    
    if is_plus:
        # Đặc quyền bản Plus: Chọn Personas trợ lý khác nhau!
        st.markdown("<p style='color:#eab308; font-weight:600;'>👑 ĐẶC QUYỀN PLUS: Lựa chọn Huấn Luyện Viên AI Coach</p>", unsafe_allow_html=True)
        ai_persona = st.selectbox(
            "Chọn tính cách trợ lý ảo:", 
            ["Tư duy Khởi nghiệp (Elon Musk Style)", "Nhà Sư Thiền Định (Zen Monk Mood)", "Quản lý Dự Án Thực Chiến (Agile Master)"]
        )
        persona_instructions = {
            "Tư duy Khởi nghiệp (Elon Musk Style)": "Bạn là Elon Musk, cực kỳ thẳng thắn, thực tế, luôn hối thúc người dùng suy nghĩ từ nguyên lý cơ bản (First Principles) để giải quyết các vấn đề lớn một cách nhanh nhất.",
            "Nhà Sư Thiền Định (Zen Monk Mood)": "Bạn là một Thiền Sư có trí tuệ sâu sắc, nhẹ nhàng, luôn khuyên người dùng hít thở sâu, bình tĩnh rải nhẹ gánh nặng tâm lý và duy trì trạng thái an yên.",
            "Quản lý Dự Án Thực Chiến (Agile Master)": "Bạn là một Agile Coach hàng đầu, chuyên gia về quy trình Kanban, luôn hướng người dùng cách chia nhỏ công việc và tối ưu hóa thời gian phân bổ hành động."
        }
        current_instruction_system = persona_instructions[ai_persona]
    else:
        st.info("💡 Mở khóa bản **PLUS** để kích hoạt tính năng chuyển đổi các Huấn luyện viên AI chuyên nghiệp (AI Coach Personas) giúp tối ưu hóa tư duy làm việc!")
        current_instruction_system = "Bạn là SoloMind, một trợ lý thông minh vui vẻ, chuyên gia trong việc hỗ trợ năng suất cá nhân."

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
                
        if user_input := st.chat_input("Hỏi SoloMind tại đây..."):
            with st.chat_message("user"):
                st.write(user_input)
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Xây dựng ngữ cảnh đầy đủ
            context = f"Dữ liệu người dùng: Tên {display_name}, Sinh lực tự chọn {st.session_state.energy_level}%. Danh sách công việc chưa hoàn tất:\n"
            for t in active_tasks:
                if t["status"] != "Đã xong":
                    context += f"- Task: {t['title']}, Dự án: {t.get('project', 'Chưa phân')}, Eisenhower: {t.get('category','Làm ngay')}\n"
            
            system_instruction_full = f"{current_instruction_system}\nNgữ cảnh hiện tại:\n{context}\nTrả lời ngắn gọn, cô đọng bằng Tiếng Việt."
            
            with st.chat_message("assistant"):
                with st.spinner("SoloMind đang phân tích dữ liệu..."):
                    ai_reply = call_gemini(user_input, system_instruction=system_instruction_full)
                    st.write(ai_reply)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
    else:
        st.warning("⚠️ Vui lòng cấu hình API Key để trò chuyện với AI!")

# ==========================================
# TAB 4: HỒ SƠ & THIẾT LẬP (PROFILE & COZMIC THEMES)
# ==========================================
with tab_profile:
    st.markdown("<h2 style='color:#3b82f6;'>👤 Thiết lập Hồ Sơ & Cài đặt Cosmic</h2>", unsafe_allow_html=True)
    st.write("Cấu hình thông tin hiển thị cá nhân, cá nhân hóa chủ đề không gian hoạt động.")
    
    prof_col1, prof_col2 = st.columns([1, 2])
    
    with prof_col1:
        st.markdown(f"""
        <div class="profile-header-card">
            <span class="avatar-glow">{user_avatar}</span>
            <h2 style="margin:10px 0 5px 0; color:#fff;">{display_name}</h2>
            <p style="color:#64748b; font-family:monospace; margin-bottom:15px;">@{current_user}</p>
            <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:10px; margin-bottom:15px; font-size:14px; color:#cbd5e1; font-style:italic;">
                "{user_bio}"
            </div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                <div style="background:rgba(59, 130, 246, 0.1); padding:10px; border-radius:8px;">
                    <small style="color:#64748b; display:block;">Cấp độ</small>
                    <strong style="color:#3b82f6; font-size:18px;">Level {user_lvl}</strong>
                </div>
                <div style="background:rgba(16, 185, 129, 0.1); padding:10px; border-radius:8px;">
                    <small style="color:#64748b; display:block;">Điểm thưởng</small>
                    <strong style="color:#10b981; font-size:18px;">{user_xp} XP</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Thống kê thành tích
        with st.container(border=True):
            st.markdown("<h4>🏆 Kỷ lục rèn luyện</h4>", unsafe_allow_html=True)
            total_tasks_ever = len(user_tasks)
            completed_tasks_ever = len([t for t in user_tasks if t["status"] == "Đã xong"])
            st.write(f"- Tổng nhiệm vụ đã lập: **{total_tasks_ever}**")
            st.write(f"- Nhiệm vụ đã hoàn thành: **{completed_tasks_ever}**")
            success_rate = int((completed_tasks_ever / total_tasks_ever) * 100) if total_tasks_ever > 0 else 0
            st.write(f"- Tỷ lệ hoàn thành: **{success_rate}%**")
            st.progress(success_rate / 100)

    with prof_col2:
        tab_sub_edit, tab_sub_theme, tab_sub_security = st.tabs(["⚙️ Chỉnh sửa Hồ sơ", "🎨 Cosmic Theme", "🔒 Bảo mật & Đổi mật khẩu"])
        
        with tab_sub_edit:
            with st.form("edit_profile_form"):
                new_display_name = st.text_input("Biệt danh hiển thị của bạn:", value=display_name)
                new_bio = st.text_area("Mô tả bản thân / Châm ngôn sống:", value=user_bio, max_chars=150)
                new_daily_goal = st.number_input("Chỉ tiêu hoàn thành task mỗi ngày:", min_value=1, max_value=20, value=daily_goal)
                new_avatar = st.selectbox(
                    "Chọn Avatar Cosmic của bạn:",
                    ["🚀", "⚡", "🌌", "🧙‍♂️", "🧘", "👾", "🔥", "🎯", "🍀", "💎"]
                )
                
                if st.form_submit_button("Lưu thay đổi hồ sơ"):
                    if not new_display_name.strip():
                        st.error("Biệt danh không được phép trống!")
                    else:
                        all_users[current_user]["display_name"] = new_display_name.strip()
                        all_users[current_user]["bio"] = new_bio.strip()
                        all_users[current_user]["daily_goal"] = new_daily_goal
                        all_users[current_user]["avatar"] = new_avatar
                        save_users(all_users)
                        st.success("🎉 Đã lưu cấu hình hồ sơ mới của bạn!")
                        time.sleep(0.5)
                        st.rerun()
                        
        with tab_sub_theme:
            st.markdown("### 🎨 Chọn Giao Diện Hệ Thống (Cosmic Colors)")
            st.write("Thay đổi không gian màu sắc của hệ thống để đồng bộ với tâm trạng làm việc của bạn.")
            
            theme_options = ["Deep Obsidian"]
            if is_plus:
                theme_options = ["Deep Obsidian", "Nebula Pink", "Emerald Forest", "Cyberpunk Gold"]
                theme_choice = st.selectbox("Chọn chủ đề không gian của bạn:", theme_options, index=theme_options.index(user_theme) if user_theme in theme_options else 0)
                if st.button("Áp dụng Giao Diện Mới 🎨", use_container_width=True):
                    all_users[current_user]["theme"] = theme_choice
                    save_users(all_users)
                    st.success(f"🎉 Đã chuyển giao diện sang {theme_choice} thành công!")
                    time.sleep(0.5)
                    st.rerun()
            else:
                st.selectbox("Chọn chủ đề không gian của bạn (Bị khóa):", theme_options, disabled=True)
                st.warning("🔒 Tính năng thay đổi các Giao diện Vũ Trụ (Nebula Pink, Emerald Forest, Cyberpunk Gold) chỉ dành cho thành viên **PLUS**. Hãy nâng cấp ngay!")
                
        with tab_sub_security:
            with st.form("security_password_form"):
                st.markdown("### 🔒 Thay đổi mật khẩu tài khoản")
                curr_pass_input = st.text_input("Nhập mật khẩu hiện tại:", type="password")
                new_pass_input = st.text_input("Nhập mật khẩu mới:", type="password")
                confirm_pass_input = st.text_input("Xác nhận mật khẩu mới:", type="password")
                
                if st.form_submit_button("Cập nhật mật khẩu mới"):
                    hashed_curr = hash_password(curr_pass_input)
                    if hashed_curr != all_users[current_user]["password"]:
                        st.error("❌ Mật khẩu hiện tại không chính xác!")
                    elif len(new_pass_input) < 6:
                        st.error("⚠️ Mật khẩu mới phải từ 6 ký tự trở lên!")
                    elif new_pass_input != confirm_pass_input:
                        st.error("❌ Mật khẩu mới và mật khẩu xác nhận không khớp!")
                    else:
                        all_users[current_user]["password"] = hash_password(new_pass_input)
                        save_users(all_users)
                        st.success("🎉 Đã cập nhật mật khẩu mới thành công!")

# ==========================================
# TAB 5: ĐẶC QUYỀN VÀ TRÌNH MUA SẮM SOLOFLOW PLUS VIP (FLAGSHIP PREMIUM REGISTRY)
# ==========================================
with tab_plus:
    st.markdown("<h1 style='text-align: center; color: #eab308; margin-bottom: 5px;'>💎 SoloFlow PLUS - Sức Mạnh Vô Song</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color:#94a3b8; font-size:16px;'>Xóa bỏ mọi giới hạn hoạt động. Nâng tầm tư duy năng suất cùng công nghệ AI độc quyền đỉnh cao.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not is_plus:
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            st.markdown("""
            <div class="pricing-card">
                <h4 style="color: #94a3b8;">🌱 Basic Plan</h4>
                <h1 style="font-size: 32px; margin: 15px 0;">Miễn phí</h1>
                <p style="font-size: 13px; color: #cbd5e1; min-height: 120px; line-height: 1.6;">
                    • Lên lịch công việc tiêu chuẩn<br>
                    • Ma trận Eisenhower cơ bản<br>
                    • Trình rã việc AI bị giới hạn<br>
                    • Giao diện Deep Obsidian mặc định
                </p>
                <p style="color: #64748b; font-weight: bold; margin-top:20px;">Đã kích hoạt mặc định</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col_p2:
            st.markdown("""
            <div class="pricing-card popular">
                <span style="background: #eab308; color: #000; font-size: 10px; font-weight: 800; padding: 3px 12px; border-radius: 20px; position: absolute; top: -12px; left: 50%; transform: translateX(-50%); box-shadow: 0 0 10px rgba(234,179,8,0.5);">KHUYÊN DÙNG</span>
                <h4 style="color: #eab308;">🌟 Monthly Premium</h4>
                <h1 style="font-size: 32px; margin: 15px 0;">79.000đ<span style="font-size:14px; color:#64748b;">/tháng</span></h1>
                <p style="font-size: 13px; color: #cbd5e1; min-height: 120px; line-height: 1.6;">
                    • Rã việc AI siêu tốc không giới hạn<br>
                    • Mở khóa toàn bộ Cosmic Theme<br>
                    • Biểu đồ nhịp sinh học Circadian<br>
                    • Trình hòa âm âm thanh 3D Binaural<br>
                    • Bản đồ tư duy AI Mind Map Pro
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("⚡ Đăng Ký Gói Tháng (79k)", use_container_width=True):
                st.session_state["payment_package"] = "Monthly Premium (79.000đ)"
                st.session_state["payment_price"] = 79000
                st.session_state["payment_step"] = "pay"
                
        with col_p3:
            st.markdown("""
            <div class="pricing-card">
                <h4 style="color: #a855f7;">🌌 Cosmic VIP Lifetime</h4>
                <h1 style="font-size: 32px; margin: 15px 0;">399.000đ<span style="font-size:14px; color:#64748b;">/vĩnh viễn</span></h1>
                <p style="font-size: 13px; color: #cbd5e1; min-height: 120px; line-height: 1.6;">
                    • Sở hữu vĩnh viễn toàn bộ tính năng<br>
                    • Miễn phí cập nhật tất cả phiên bản tiếp theo<br>
                    • Nhận biểu tượng huy hiệu VIP độc nhất<br>
                    • Ưu tiên xử lý băng thông AI tốc độ cao<br>
                    • Hỗ trợ kỹ thuật 24/7 từ đội ngũ phát triển
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("👑 Mua Gói Trọn Đời (399k)", use_container_width=True):
                st.session_state["payment_package"] = "Cosmic VIP Lifetime (399.000đ)"
                st.session_state["payment_price"] = 399000
                st.session_state["payment_step"] = "pay"

        # TRÌNH GIẢ LẬP THANH TOÁN PLUS KHÉO LÉO CHUYÊN NGHIỆP
        if "payment_step" in st.session_state and st.session_state["payment_step"] == "pay":
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("### 💳 Hệ thống thanh toán hóa đơn an toàn (VietQR Simulated Gateway)")
            
            p_price = st.session_state["payment_price"]
            p_package = st.session_state["payment_package"]
            
            # Form nhập Coupon giảm giá độc đáo
            coupon_input = st.text_input("Nhập mã ưu đãi (Nếu có):", placeholder="Gợi ý: Nhập FREEPLUS để được trải nghiệm thử...")
            discount = 0
            if coupon_input.strip().upper() == "FREEPLUS":
                discount = p_price
                st.success("🎉 Áp dụng mã thành công! Bạn nhận được giảm giá 100%!")
            
            final_price = max(0, p_price - discount)
            
            col_qr1, col_qr2 = st.columns([1, 2])
            with col_qr1:
                # Tạo ảnh VietQR giả lập
                st.image(
                    f"https://img.vietqr.io/image/970415-102555666888-compact2.jpg?amount={final_price}&addInfo=SOLOFLOW%20VIP%20{current_user}&accountName=SoloFlow%20Technologies",
                    caption="Dùng ứng dụng ngân hàng quét để giả lập chuyển khoản trực tiếp"
                )
            with col_qr2:
                st.write(f"💼 **Gói dịch vụ:** `{p_package}`")
                st.write(f"💵 **Giá trị gốc:** `{p_price:,} đ`")
                st.write(f"📉 **Khấu trừ ưu đãi:** `{discount:,} đ`")
                st.write(f"🚨 **Tổng số tiền thanh toán thực tế:** `{final_price:,} đ`")
                st.markdown("<small style='color: #64748b;'>Hệ thống đang hoạt động ở chế độ mô phỏng Sandbox. Bạn có thể bấm xác thực ngay mà không cần giao dịch thực tế.</small>", unsafe_allow_html=True)
                
                # Tiến hành kiểm tra và xác minh ngân hàng
                if st.button("✅ Tôi Đã Chuyển Khoản - Bấm Để Xác Thực Giao Dịch", type="primary", use_container_width=True):
                    with st.spinner("Đang kết nối tới cổng thanh toán ngân hàng liên kết, vui lòng chờ..."):
                        progress_bar = st.progress(0)
                        for percent in range(100):
                            time.sleep(0.015)
                            progress_bar.progress(percent + 1)
                        
                        # Kích hoạt trạng thái VIP trong Database
                        all_users[current_user]["is_plus"] = True
                        save_users(all_users)
                        st.session_state["payment_step"] = "success"
                        st.balloons()
                        st.rerun()

        if "payment_step" in st.session_state and st.session_state["payment_step"] == "success":
            st.success("🎉 CHÚC MỪNG: Bạn đã kích hoạt thành công quyền sở hữu SoloFlow Plus Thượng Hạng!")
            st.write("Hãy tận hưởng mọi tính năng cao cấp không giới hạn ngay bây giờ.")
            if st.button("🚀 Trải nghiệm ngay các tính năng Plus", use_container_width=True):
                del st.session_state["payment_step"]
                st.rerun()
                
    else:
        # GIAO DIỆN CÁC TÍNH NĂNG PLUS ĐÃ ĐƯỢC MỞ KHÓA
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(234, 179, 8, 0.1) 0%, rgba(249, 115, 22, 0.1) 100%); border: 2px dashed #eab308; border-radius: 16px; padding: 25px; text-align: center; margin-bottom: 30px;">
            <h3 style="color:#eab308; margin-top:0;">🚀 CHÀO MỪNG THÀNH VIÊN PLUS THƯỢNG HẠNG!</h3>
            <p style="margin:0; color:#f1f5f9; font-size:14px;">Bạn đã được cấp quyền truy cập trọn bộ hệ thống tối cao. Dưới đây là các Module đặc quyền của bạn:</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab_p_binaural, tab_p_mindmap = st.tabs(["🎵 3D Cosmic Audio Engine", "🧠 AI Mind Map Architect"])
        
        with tab_p_binaural:
            st.markdown("### 🎵 Trình Hoà Âm 3D Binaural Sound Mixer (Độc Quyền Plus)")
            st.write("Bật tích hợp nhiều kênh âm thanh khác nhau để thiết kế môi trường âm thanh tập trung tuyệt đối.")
            
            col_au1, col_au2, col_au3 = st.columns(3)
            with col_au1:
                vol_rain = st.slider("Tiếng mưa rơi đêm (Rain):", 0, 100, 50)
                vol_waves = st.slider("Sóng biển rì rào (Ocean Waves):", 0, 100, 0)
            with col_au2:
                vol_alpha = st.slider("Sóng não Alpha 12Hz (Tập trung):", 0, 100, 30)
                vol_theta = st.slider("Sóng thiền Theta 6Hz (Giảm lo âu):", 0, 100, 0)
            with col_au3:
                vol_cosmic = st.slider("Nhạc nền Cosmic Ambient:", 0, 100, 40)
                vol_camp = st.slider("Tiếng củi cháy tách bách (Campfire):", 0, 100, 10)
                
            if st.button("🔊 Áp dụng và Bật Trình Hoà Âm 3D Ambient", use_container_width=True):
                # Nhúng HTML5 Audio Synth động phát sinh tần số để phát sóng não Binaural mà không cần file MP3
                st.session_state.binaural_playing = True
                audio_script = f"""
                <script>
                window.audioCtx = window.audioCtx || new (window.AudioContext || window.webkitAudioContext)();
                
                // Hàm tạo oscillator phát sóng âm
                function playBinaural(freq1, freq2, vol) {{
                    if(vol <= 0) return;
                    let merger = window.audioCtx.createChannelMerger(2);
                    
                    let oscL = window.audioCtx.createOscillator();
                    let gainL = window.audioCtx.createGain();
                    oscL.frequency.value = freq1;
                    gainL.gain.value = (vol / 100) * 0.05;
                    oscL.connect(gainL).connect(merger, 0, 0);
                    
                    let oscR = window.audioCtx.createOscillator();
                    let gainR = window.audioCtx.createGain();
                    oscR.frequency.value = freq2;
                    gainR.gain.value = (vol / 100) * 0.05;
                    oscR.connect(gainR).connect(merger, 0, 1);
                    
                    merger.connect(window.audioCtx.destination);
                    oscL.start();
                    oscR.start();
                }}
                
                if(window.audioCtx.state === 'suspended') {{
                    window.audioCtx.resume();
                }}
                
                // Chạy sóng Alpha (340Hz - 352Hz)
                playBinaural(340, 352, {vol_alpha});
                // Chạy sóng Theta (150Hz - 156Hz)
                playBinaural(150, 156, {vol_theta});
                </script>
                """
                st.markdown(audio_script, unsafe_allow_html=True)
                st.success("🎶 Đang phát sóng hoà âm Binaural an toàn chất lượng cao. Đeo tai nghe để cảm nhận hiệu ứng tốt nhất!")
                
            # Cung cấp một số luồng nhạc Lofi Pro chất lượng cao dự phòng
            st.markdown("<br><b>Hoặc lựa chọn luồng phát sóng Cosmic Chill Pro:</b>", unsafe_allow_html=True)
            youtube_ambient_id = st.selectbox("Chọn Kênh Âm Nhạc Không Gian:", [
                "Lofi Hip Hop Live - Radio Chill Beats (Lofi Girl)",
                "Space Ambient Deep Focus Music (Ambient Meditation)",
                "Cyberpunk Synthwave Work/Study Beats (Neon Drive)"
            ])
            yt_id_map = {
                "Lofi Hip Hop Live - Radio Chill Beats (Lofi Girl)": "jfKfPfyJRdk",
                "Space Ambient Deep Focus Music (Ambient Meditation)": "FjU_SgN_r_4",
                "Cyberpunk Synthwave Work/Study Beats (Neon Drive)": "4xDzrJKXOOY"
            }
            target_id = yt_id_map[youtube_ambient_id]
            st.markdown(f'<iframe width="100%" height="150" src="https://www.youtube.com/embed/{target_id}?autoplay=1" frameborder="0" allow="autoplay; encrypted-media"></iframe>', unsafe_allow_html=True)

        with tab_p_mindmap:
            st.markdown("### 🧠 AI Mind Map Architect (Tính Năng Plus Thượng Hạng)")
            st.write("Cung cấp một mục tiêu lớn, SoloMind AI sẽ kiến tạo toàn bộ bản đồ cây tư duy phân chia công việc dưới dạng kiến trúc khối có chiều sâu.")
            
            mind_goal = st.text_input("Nhập mục tiêu lớn cần vẽ Sơ đồ Tư duy:", placeholder="Ví dụ: Lập trình sản phẩm SaaS bán hàng tự động...")
            if st.button("🎨 Thiết kế Bản đồ Tư duy bằng AI", use_container_width=True):
                if not mind_goal.strip():
                    st.error("Vui lòng nhập mục tiêu lớn!")
                else:
                    with st.spinner("AI đang tính toán cấu trúc sơ đồ cây..."):
                        # Gọi AI thiết kế cấu trúc sơ đồ cây
                        system_instr_mind = (
                            "Bạn là kiến trúc sư bản đồ tư duy. Nhận vào mục tiêu lớn, phân rã nó thành cấu trúc dạng cây gồm 1 nút gốc, tối thiểu 3 nút con cấp 1, và mỗi nút con cấp 1 có tối thiểu 2 nút con cấp 2. "
                            "Trả về đúng định dạng JSON chuẩn. Ví dụ:\n"
                            "{\n"
                            "  \"root\": \"Tên nút gốc\",\n"
                            "  \"branches\": [\n"
                            "    {\n"
                            "      \"name\": \"Nhánh con 1\",\n"
                            "      \"leafs\": [\"Lá 1.1\", \"Lá 1.2\"]\n"
                            "    }\n"
                            "  ]\n"
                            "}"
                        )
                        mind_response = call_gemini(mind_goal, system_instruction=system_instr_mind)
                        try:
                            mind_data = parse_gemini_json(mind_response)
                            # Hiển thị cấu trúc cây sơ đồ bằng mã HTML/CSS siêu đẹp
                            branches_html = ""
                            for branch in mind_data.get("branches", []):
                                leafs_html = "".join([f"<li style='color:#a855f7; margin:5px 0;'>🍀 {leaf}</li>" for leaf in branch.get("leafs", [])])
                                branches_html += f"""
                                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 15px; margin: 10px;">
                                    <strong style="color:#eab308; font-size:15px;">📂 {branch.get('name')}</strong>
                                    <ul style="list-style-type: none; padding-left: 15px; margin: 5px 0 0 0;">
                                        {leafs_html}
                                    </ul>
                                </div>
                                """
                                
                            st.markdown(f"""
                            <div class="glass-card" style="border: 2px solid #eab308; border-radius: 16px; padding: 20px;">
                                <h3 style="text-align: center; color:#eab308; margin-top:0;">🌐 BẢN ĐỒ TƯ DUY PLUS: {mind_data.get('root')}</h3>
                                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
                                    {branches_html}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Lỗi vẽ sơ đồ tư duy: {e}")

        # Hủy quyền sở hữu Plus (Dành cho nhà phát triển kiểm tra dòng thanh toán)
        st.markdown("<br><hr>", unsafe_allow_html=True)
        if st.button("🛠️ Gỡ bỏ quyền sở hữu Plus (Chỉ dành cho Nhà Phát Triển Test)"):
            all_users[current_user]["is_plus"] = False
            all_users[current_user]["theme"] = "Deep Obsidian"
            save_users(all_users)
            st.success("Đã trả tài khoản về quyền Standard mặc định!")
            time.sleep(0.5)
            st.rerun()

# ==========================================
# TAB 6: SAO LƯU & LƯU TRỮ (DATA SAFETY & ARCHIVE)
# ==========================================
with tab_archive_sys:
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
                    st.write(f"Trạng thái: **{task['status']}**")
                with col_arch_act:
                    col_ab1, col_ab2 = st.columns(2)
                    with col_ab1:
                        if st.button("↩️ Phục hồi", key=f"restore_btn_{task['id']}_{idx}", use_container_width=True):
                            for t in all_tasks:
                                if t["id"] == task["id"] and t.get("owner") == current_user:
                                    t["archived"] = False
                                    break
                            save_tasks(all_tasks)
                            st.success("Đã khôi phục nhiệm vụ!")
                            time.sleep(0.5)
                            st.rerun()
                    with col_ab2:
                        if st.button("🗑️ Xóa hẳn", key=f"force_del_btn_{task['id']}_{idx}", use_container_width=True):
                            all_tasks = [t for t in all_tasks if not (t["id"] == task["id"] and t.get("owner") == current_user)]
                            save_tasks(all_tasks)
                            st.success("Đã xóa vĩnh viễn!")
                            time.sleep(0.5)
                            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("⚙️ Quản lý Cơ sở Dữ liệu & Sao lưu dự phòng")
    
    col_sys1, col_sys2 = st.columns(2)
    with col_sys1:
        st.markdown("### 📥 Tải xuống Bản sao lưu cá nhân (Export Backup)")
        try:
            user_json_data = json.dumps(user_tasks, indent=4, ensure_ascii=False)
            st.download_button(
                label="💾 Tải về file tasks_backup.json",
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
                        st.success("Khôi phục thành công! Trang tự nạp lại sau giây lát.")
                        time.sleep(0.5)
                        st.rerun()
                else:
                    st.error("File backup không đúng cấu trúc dữ liệu SoloFlow OS.")
            except Exception as e:
                st.error(f"Lỗi phân tích cú pháp file: {e}")
