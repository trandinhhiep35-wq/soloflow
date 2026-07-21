
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import re
import os
from supabase import create_client, Client
import google.generativeai as genai

# ==========================================
# 1. CẤU HÌNH TRANG
# ==========================================
st.set_page_config(
    page_title="SoloFlow OS - AI Productivity Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CSS THEME OBSIDIAN / COSMIC
# ==========================================
CSS_STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #0b0f19;
    color: #f3f4f6;
}

.profile-card {
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
}

.plan-card {
    background: rgba(17, 24, 39, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 28px 22px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.3s ease, border-color 0.3s ease;
}

.plan-card:hover {
    transform: translateY(-5px);
}

.plan-featured {
    background: linear-gradient(180deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 2px solid #3b82f6 !important;
    box-shadow: 0 0 25px rgba(59, 130, 246, 0.25);
}

.plan-cosmic {
    background: linear-gradient(180deg, rgba(49, 16, 82, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 2px solid #a855f7 !important;
    box-shadow: 0 0 25px rgba(168, 85, 247, 0.25);
}

.feature-list {
    padding-left: 18px;
    margin: 20px 0;
    font-size: 0.9rem;
    color: #d1d5db;
    line-height: 1.8;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background-color: rgba(17, 24, 39, 0.6);
    padding: 8px 12px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.stTabs [data-baseweb="tab"] {
    height: 42px;
    border-radius: 8px;
    color: #9ca3af;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background-color: #1e293b !important;
    color: #3b82f6 !important;
    border-bottom: 2px solid #3b82f6 !important;
}
</style>
"""
st.markdown(CSS_STYLE, unsafe_allow_html=True)

# ==========================================
# 3. KHỎI TẠO SESSION STATE & KEYS
# ==========================================
aq_key_secret = (
    st.secrets.get("AQ") or 
    st.secrets.get("AQ_KEY") or 
    st.secrets.get("GEMINI_API_KEY", os.getenv("AQ", ""))
)

if 'gemini_key' not in st.session_state:
    st.session_state['gemini_key'] = aq_key_secret if aq_key_secret else ""

if 'user_plan' not in st.session_state:
    st.session_state['user_plan'] = 'Basic'

if 'user_xp' not in st.session_state:
    st.session_state['user_xp'] = 190

if 'tasks' not in st.session_state:
    st.session_state['tasks'] = []

is_vip = st.session_state['user_plan'] != 'Basic'

# ==========================================
# 4. CƠ SỞ DỮ LIỆU & AI HELPER
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

def clean_json_str(text_data: str) -> str:
    clean = re.sub(r'\x60{3}(?:json)?', '', text_data)
    return clean.strip()

def call_gemini_wbs(prompt_text, category, is_vip_mode=False):
    api_key = st.session_state.get('gemini_key')
    
    fallback = [
        {"step": 1, "title": f"Khảo sát & Lập Kế Hoạch: {prompt_text[:25]}", "description": "Xác định mục tiêu chính và thiết lập môi trường.", "time": "2.0 giờ", "priority": "Cao"},
        {"step": 2, "title": "Xây dựng Mô-đun Cốt Lõi", "description": "Lập trình chức năng chính và cơ sở dữ liệu.", "time": "4.5 giờ", "priority": "Cao"},
        {"step": 3, "title": "Thiết kế Giao diện & Tích hợp AI", "description": "Tối ưu hóa trải nghiệm UI/UX và kết nối API.", "time": "3.0 giờ", "priority": "Trung bình"},
        {"step": 4, "title": "Kiểm thử & Đóng gói Nâng cao", "description": "Sửa lỗi, tối ưu hiệu năng và phát hành.", "time": "1.5 giờ", "priority": "Thấp"}
    ]

    if not api_key:
        return fallback

    try:
        genai.configure(api_key=api_key)
        model_name = "gemini-1.5-pro" if is_vip_mode else "gemini-1.5-flash"
        model = genai.GenerativeModel(model_name)
        
        sys_prompt = f"""
        Bạn là Chuyên gia Quản lý Dự án cấp cao. Hãy phân rã công việc sau thành WBS dạng JSON Array:
        Nhiệm vụ: "{prompt_text}" | Lĩnh vực: "{category}"
        
        BẮT BUỘC chỉ trả về duy nhất chuỗi JSON Array nguyên bản, không dùng markdown codeblock.
        Cấu trúc JSON từng phần tử:
        [
            {{"step": 1, "title": "Tên bước", "description": "Mô tả chi tiết", "time": "2 giờ", "priority": "Cao"}}
        ]
        Priority chỉ gồm: "Cao", "Trung bình", "Thấp".
        """
        
        res = model.generate_content(sys_prompt)
        clean_json = clean_json_str(res.text)
        return json.loads(clean_json)
    except Exception as e:
        st.error(f"Lỗi AI: {str(e)}")
        return fallback

# ==========================================
# 5. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='margin:0; font-size:1.4rem;'>⚡ SoloFlow <span style='color:#3b82f6;'>OS</span></h2>", unsafe_allow_html=True)
    st.caption("System v3.5 - Deep Obsidian")
    st.write("")

    st.markdown("""
    <div class="profile-card">
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="font-size: 2rem;">🚀</div>
            <div>
                <strong style="font-size: 1.05rem; color:#f3f4f6;">epcute20</strong> <span style="font-size:0.75rem; color:#9ca3af;">(Member)</span>
                <div style="font-size: 0.8rem; color: #6b7280;">@epcute20</div>
            </div>
        </div>
        <hr style="border-color: rgba(255,255,255,0.08); margin: 12px 0;"/>
        <div style="font-size:0.82rem; color:#9ca3af;">Hệ thống rèn luyện</div>
        <div style="font-size:0.88rem; font-weight:600; color:#f3f4f6; margin-top:2px;">
            Hiện tại: Level 2 <span style="color:#3b82f6;">(Flow Master)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    xp_val = st.session_state['user_xp']
    st.caption(f"Tích lũy XP: **{xp_val} / 400 XP**")
    st.progress(xp_val / 400)

    st.divider()

    st.markdown("### 🔑 Key AQ (Gemini AI)")
    aq_in = st.text_input("Nhập Key AQ:", value=st.session_state['gemini_key'], type="password", placeholder="AQxxxxxxxxxxxx...")
    if st.button("💾 Lưu Key AQ", use_container_width=True):
        st.session_state['gemini_key'] = aq_in
        st.success("Đã cập nhật Key AQ!")

    if st.session_state['gemini_key']:
        st.caption("🟢 AI Engine: **Sẵn sàng**")
    else:
        st.caption("🔴 AI Engine: **Chưa kích hoạt**")

# ==========================================
# 6. KHU VỰC TABS CHÍNH
# ==========================================
tab_dash, tab_tasks, tab_mind, tab_profile, tab_vip, tab_storage = st.tabs([
    "📊 Dashboard", 
    "📋 Nhiệm vụ", 
    "🧠 SoloMind AI", 
    "👤 Hồ Sơ & Cài Đặt", 
    "💎 SoloFlow PLUS VIP", 
    "💾 Sao Lưu & Lưu Trữ"
])

# ------------------------------------------
# TAB 1: DASHBOARD
# ------------------------------------------
with tab_dash:
    st.title("📊 Dashboard - Tổng Quan Năng Suất")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Nhiệm vụ hôm nay", "5", "+2")
    c2.metric("Chuỗi Streak", "7 ngày", "🔥")
    c3.metric("Tổng giờ tập trung", "14.5h", "+3.2h")
    c4.metric("Cấp độ Rèn luyện", "Lvl 2", "190 XP")

    st.divider()
    col_eisen, col_binaural = st.columns([2, 1])
    with col_eisen:
        st.subheader("🎯 Ma trận Eisenhower Cơ Bản")
        m1, m2 = st.columns(2)
        with m1:
            st.info("**🔴 Khẩn cấp & Quan trọng**\n- Sửa lỗi nộp bài tập AI\n- Họp team SoloFlow")
        with m2:
            st.success("**🔵 Không khẩn cấp nhưng Quan trọng**\n- Học tiếng Bắc giọng chuẩn\n- Lên lịch trình dự án mới")
    with col_binaural:
        st.subheader("🎧 Âm thanh 3D Binaural")
        st.selectbox("Chọn sóng não:", ["Alpha (Tập trung sâu)", "Beta (Sáng tạo)", "Theta (Thư giãn)"])
        st.button("▶️ Phát âm thanh", use_container_width=True)

# ------------------------------------------
# TAB 2: NHIỆM VỤ
# ------------------------------------------
with tab_tasks:
    st.title("📋 Trình Phân Rã Nhiệm Vụ AI")
    t_input = st.text_input("Nhập tên dự án / công việc lớn:", placeholder="Ví dụ: Lập trình ứng dụng SoloFlow OS bản hoàn chỉnh")
    t_cat = st.selectbox("Lĩnh vực:", ["Lập trình / Tech", "Marketing", "Kinh doanh", "Cá nhân"])
    
    if st.button("⚡ Kích Hoạt AI Rã Việc", type="primary"):
        if t_input:
            with st.spinner("AI đang phân tích..."):
                res = call_gemini_wbs(t_input, t_cat, is_vip_mode=is_vip)
                st.session_state['tasks'] = res
                st.session_state['user_xp'] += 20
                st.success("Phân rã thành công! +20 XP")
                st.rerun()

    if st.session_state['tasks']:
        st.divider()
        st.subheader("📋 Checklist Chi Tiết WBS")
        for sub in st.session_state['tasks']:
            st.checkbox(f"**Bước {sub['step']}: {sub['title']}** ({sub['time']}) - *Độ ưu tiên: {sub['priority']}*")
            st.caption(sub['description'])

# ------------------------------------------
# TAB 3: SOLOMIND AI
# ------------------------------------------
with tab_mind:
    st.title("🧠 SoloMind AI - Bản Đồ Tư Duy Mind Map Pro")
    st.caption("Tự động hệ thống hóa ý tưởng dự án dưới dạng sơ đồ trực quan.")
    
    df_mind = pd.DataFrame([
        {"From": "Dự án SoloFlow", "To": "Giao diện UI/UX"},
        {"From": "Dự án SoloFlow", "To": "Xử lý AI Gemini"},
        {"From": "Giao diện UI/UX", "To": "Theme Obsidian"},
        {"From": "Giao diện UI/UX", "To": "Gói cước VIP"},
        {"From": "Xử lý AI Gemini", "To": "Key AQ Integration"}
    ])
    fig = px.sunburst(df_mind, path=['From', 'To'], title="Sơ Đồ Phân Nhánh Ý Tưởng")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------
# TAB 4: HỒ SƠ & CÀI ĐẶT
# ------------------------------------------
with tab_profile:
    st.title("👤 Hồ Sơ & Cài Đặt Hệ Thống")
    st.text_input("Tên hiển thị:", value="epcute20")
    st.text_input("Username:", value="@epcute20")
    st.selectbox("Giao diện mặc định:", ["Deep Obsidian (Tối)", "Cosmic Cyberpunk (VIP)", "Light Minimal"])
    st.toggle("Bật thông báo Circadian Nhịp sinh học", value=True)

# ------------------------------------------
# TAB 5: SOLOFLOW PLUS VIP
# ------------------------------------------
with tab_vip:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="font-size: 2.3rem; margin-bottom: 8px;">💎 SoloFlow PLUS - Sức Mạnh Vô Song</h1>
        <p style="color: #9ca3af; font-size: 1.05rem;">
            Xóa bỏ mọi giới hạn hoạt động. Nâng tầm tư duy năng suất cùng công nghệ AI đặc quyền đỉnh cao.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_basic, col_monthly, col_cosmic = st.columns(3)

    with col_basic:
        st.markdown("""
        <div class="plan-card">
            <div>
                <h3>🌱 Basic Plan</h3>
                <h2 style="font-size: 1.8rem; margin: 15px 0;">Miễn phí</h2>
                <ul class="feature-list">
                    <li>Lên lịch công việc tiêu chuẩn</li>
                    <li>Ma trận Eisenhower cơ bản</li>
                    <li>Trình rã việc AI bị giới hạn</li>
                    <li>Giao diện Deep Obsidian mặc định</li>
                </ul>
            </div>
            <div style="text-align: center; color: #6b7280; padding: 10px; font-weight: 600;">
                Đã kích hoạt mặc định
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_monthly:
        st.markdown("""
        <div class="plan-card plan-featured">
            <div>
                <span style="background:#3b82f6; color:white; font-size:0.75rem; padding:3px 10px; border-radius:10px; font-weight:bold;">POPULAR</span>
                <h3 style="margin-top:8px;">👑 Monthly Premium</h3>
                <h2 style="font-size: 1.8rem; margin: 15px 0; color:#60a5fa;">79.000đ<span style="font-size:0.9rem; color:#9ca3af;">/tháng</span></h2>
                <ul class="feature-list">
                    <li>Rã việc AI siêu tốc không giới hạn</li>
                    <li>Mở khóa toàn bộ Cosmic Theme</li>
                    <li>Điều chỉnh nhịp sinh học Circadian</li>
                    <li>Định hòa âm âm thanh 3D Binaural</li>
                    <li>Bản đồ tư duy AI Mind Map Pro</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚡ Đăng Ký Gói Tháng", type="primary", key="btn_month", use_container_width=True):
            st.session_state['user_plan'] = 'Monthly Premium'
            st.success("Đã kích hoạt Gói Tháng thành công!")
            st.rerun()

    with col_cosmic:
        st.markdown("""
        <div class="plan-card plan-cosmic">
            <div>
                <span style="background:#a855f7; color:white; font-size:0.75rem; padding:3px 10px; border-radius:10px; font-weight:bold;">BEST VALUE</span>
                <h3 style="margin-top:8px;">🎆 Cosmic VIP Lifetime</h3>
                <h2 style="font-size: 1.8rem; margin: 15px 0; color:#c084fc;">399.000đ<span style="font-size:0.9rem; color:#9ca3af;">/trọn đời</span></h2>
                <ul class="feature-list">
                    <li>Sở hữu vĩnh viễn toàn bộ tính năng</li>
                    <li>Miễn phí cập nhật tất cả phiên bản tiếp theo</li>
                    <li>Nhiều biểu tượng huy hiệu VIP đặc biệt</li>
                    <li>Ưu tiên xử lý bằng hệ thống AI tốc độ cao</li>
                    <li>Hỗ trợ kỹ thuật 24/7 từ đội ngũ phát triển</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔮 Mua Trọn Đời", key="btn_life", use_container_width=True):
            st.session_state['user_plan'] = 'Cosmic VIP Lifetime'
            st.success("Đã kích hoạt Gói VIP Trọn Đời!")
            st.rerun()

# ------------------------------------------
# TAB 6: SAO LƯU & LƯU TRỮ
# ------------------------------------------
with tab_storage:
    st.title("💾 Sao Lưu & Đồng Bộ Dữ Liệu")
    if supabase:
        st.success("🟢 Cơ sở dữ liệu Supabase Cloud: Đã kết nối")
    else:
        st.info("🔵 Chế độ lưu trữ: Bộ nhớ tạm thời Streamlit Session")
    
    col_ex, col_im = st.columns(2)
    with col_ex:
        st.subheader("Xuất dữ liệu")
        json_str = json.dumps(st.session_state['tasks'], ensure_ascii=False, indent=2)
        st.download_button("📥 Tải về file Backup (.json)", data=json_str, file_name="soloflow_backup.json", mime="application/json")
    with col_im:
        st.subheader("Nhập dữ liệu")
        st.file_uploader("📤 Tải lên file backup", type=["json"])
