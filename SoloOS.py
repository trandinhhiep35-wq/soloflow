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
# 1. CẤU HÌNH TRANG & GIAO DIỆN HYBRID
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

if 'task_history' not in st.session_state:
    st.session_state['task_history'] = []

is_plus = (st.session_state['user_plan'] != 'Basic')

# CSS Theme Dynamic (Basic vs PLUS VIP Cyberpunk)
plus_css = """
    .stApp { background-color: #030712; }
    .glass-card {
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.8) 0%, rgba(31, 41, 55, 0.6) 100%);
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.15) !important;
    }
    .vip-badge-active {
        background: linear-gradient(90deg, #ec4899, #8b5cf6, #3b82f6);
        color: #ffffff; padding: 6px 14px; border-radius: 20px;
        font-weight: 800; font-size: 0.85rem; text-align: center;
        box-shadow: 0 0 10px rgba(139, 92, 246, 0.5);
    }
    .stat-box {
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 10px; padding: 12px; text-align: center;
    }
""" if is_plus else """
    .stApp { background-color: #0f172a; }
    .glass-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .stat-box {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px; padding: 12px; text-align: center;
    }
"""

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
    .glass-card {{
        border-radius: 12px; padding: 20px; margin-bottom: 15px;
        backdrop-filter: blur(12px);
    }}
    .p-high {{ color: #f87171; background: rgba(248, 113, 113, 0.15); padding: 4px 10px; border-radius: 6px; font-size: 0.78rem; font-weight:700; }}
    .p-med {{ color: #fbbf24; background: rgba(251, 191, 36, 0.15); padding: 4px 10px; border-radius: 6px; font-size: 0.78rem; font-weight:700; }}
    .p-low {{ color: #34d399; background: rgba(52, 211, 153, 0.15); padding: 4px 10px; border-radius: 6px; font-size: 0.78rem; font-weight:700; }}
    {plus_css}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. KHỞI TẠO SUPABASE & CÔNG CỤ XỬ LÝ AN TOÀN
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

def clean_json_response(raw_text: str) -> str:
    """Hàm bóc tách JSON siêu an toàn, chống triệt để lỗi SyntaxError"""
    text = raw_text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text

def call_gemini_ai_wbs(prompt_text, category, depth_str, is_vip=False):
    api_key = st.session_state.get('gemini_key')
    
    # Dữ liệu mẫu cực chuẩn nếu chưa cài Key AQ
    fallback_data = [
        {"step": 1, "title": f"Khảo sát & Lập kiến trúc: {prompt_text[:30]}", "description": "Phân tích yêu cầu kĩ thuật, lựa chọn công cụ và thiết lập môi trường.", "time": "2.0 giờ", "priority": "Cao", "risk": "Thấp"},
        {"step": 2, "title": "Xây dựng sơ đồ dữ liệu & API Core", "description": "Thiết kế CSDL, tạo endpoints và cấu hình chính sách bảo mật.", "time": "4.0 giờ", "priority": "Cao", "risk": "Trung bình"},
        {"step": 3, "title": "Phát triển giao diện & Tích hợp AI", "description": "Lập trình UI/UX, kết nối API Gemini và xử lý logic luồng công việc.", "time": "5.5 giờ", "priority": "Trung bình", "risk": "Cao"},
        {"step": 4, "title": "Kiểm thử, Tối ưu & Nghiệm thu", "description": "Sửa lỗi crash, tối ưu hiệu năng và đóng gói phiên bản chính thức.", "time": "2.0 giờ", "priority": "Thấp", "risk": "Thấp"}
    ]

    if not api_key:
        return fallback_data

    try:
        genai.configure(api_key=api_key)
        model_name = "gemini-1.5-pro" if is_vip else "gemini-1.5-flash"
        model = genai.GenerativeModel(model_name)
        
        vip_prompt_addon = "Đánh giá thêm yếu tố rủi ro ('risk': 'Cao'/'Trung bình'/'Thấp') cho từng bước và đề xuất giải pháp sâu sắc." if is_vip else ""

        sys_prompt = f"""
        Bạn là Chuyên gia Quản lý Dự án (Senior Project Manager). Hãy rã công việc sau thành danh sách WBS thực thi:
        - Công việc: "{prompt_text}"
        - Lĩnh vực: "{category}"
        - Mức độ chi tiết: "{depth_str}"
        {vip_prompt_addon}

        BẮT BUỘC trả về duy nhất 1 mảng JSON Array (không kèm văn bản dẫn dắt).
        Mẫu JSON:
        [
            {{
                "step": 1,
                "title": "Tên bước thực hiện ngắn gọn",
                "description": "Mô tả chi tiết hành động",
                "time": "2.5 giờ",
                "priority": "Cao",
                "risk": "Trung bình"
            }}
        ]
        Chỉ dùng giá trị priority và risk gồm: "Cao", "Trung bình", "Thấp".
        """

        response = model.generate_content(sys_prompt)
        cleaned_str = clean_json_response(response.text)
        return json.loads(cleaned_str)
    except Exception as e:
        st.error(f"⚠️ Thông báo kết nối Key AQ: {str(e)}. Hệ thống chuyển sang chế độ dữ liệu thông minh dự phòng.")
        return fallback_data

def save_to_supabase(title, category, subtasks):
    if supabase:
        try:
            m_res = supabase.table("main_tasks").insert({"title": title, "category": category, "progress": 0}).execute()
            if m_res.data:
                m_id = m_res.data[0]['id']
                payload = [{
                    "main_task_id": m_id,
                    "step_number": s["step"],
                    "title": s["title"],
                    "description": s.get("description", ""),
                    "time_estimate": s["time"],
                    "priority": s["priority"],
                    "is_completed": False
                } for s in subtasks]
                supabase.table("subtasks").insert(payload).execute()
                return True, "Đã đồng bộ dữ liệu trực tiếp lên Supabase Cloud!"
        except Exception as e:
            return False, f"Lỗi Supabase: {str(e)}"
    return True, "Đã lưu vào bộ nhớ tạm ứng dụng."

# ==========================================
# 3. THANH MENU SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='margin:0;'>⚡ SoloFlow <span style='color:#3b82f6;'>OS</span></h2>", unsafe_allow_html=True)
    st.caption("Hệ Thống Phân Rã & Quản Lý Công Việc AI")
    st.divider()

    # Trạng thái Bản quyền
    if is_plus:
        st.markdown('<div class="vip-badge-active">💎 BẢN PLUS VIP ĐÃ KÍCH HOẠT</div>', unsafe_allow_html=True)
        st.caption("✨ AI Core: Gemini 1.5 Pro Deep Reasoning")
    else:
        st.markdown('<b>Gói hiện tại: Basic</b>', unsafe_allow_html=True)
        if st.button("🚀 Kích Hoạt Bản PLUS VIP", use_container_width=True):
            st.session_state['user_plan'] = 'SoloFlow PLUS'
            st.rerun()

    st.divider()

    # Cấu hình Key AQ
    st.markdown("### 🔑 Cấu Hình Key AQ")
    input_aq = st.text_input(
        "Nhập Key AQ (Gemini API):",
        value=st.session_state.get('gemini_key', ''),
        type="password",
        placeholder="AQxxxxxxxxxxxx...",
        help="Nhập Key định dạng AQ hoặc lưu vào Streamlit Secrets với tên 'AQ'"
    )

    if st.button("💾 Lưu Key AQ", use_container_width=True):
        st.session_state['gemini_key'] = input_aq
        st.success("Đã cập nhật Key AQ thành công!")
        st.rerun()

    if st.session_state.get('gemini_key'):
        st.caption("🟢 Key AQ: **Đã kết nối AI thành công**")
    else:
        st.caption("🔴 Chưa có Key AQ (Chạy dữ liệu mô phỏng)")

    st.divider()

    # Công tắc thử nghiệm VIP
    dev_mode = st.toggle("🧪 Trải nghiệm Giao diện & AI PLUS VIP", value=is_plus)
    if dev_mode != is_plus:
        st.session_state['user_plan'] = 'SoloFlow PLUS' if dev_mode else 'Basic'
        st.rerun()

# ==========================================
# 4. TRANG CHÍNH (MAIN APP)
# ==========================================
st.title("⚡ SoloFlow OS - AI Phân Rã Công Việc Dũng Mãnh")
st.caption("Giải quyết đúng trọng tâm - Tự động thiết lập lộ trình & đồng bộ hóa dữ liệu.")

# Khung Thống kê Nhanh
sc1, sc2, sc3 = st.columns(3)
with sc1:
    st.markdown(f'<div class="stat-box"><b>Mô Hình AI</b><br/><span style="color:#3b82f6; font-size:1.1rem; font-weight:bold;">{"Gemini Pro" if is_plus else "Gemini Flash"}</span></div>', unsafe_allow_html=True)
with sc2:
    st.markdown(f'<div class="stat-box"><b>Kết Nối CSDL</b><br/><span style="color:#34d399; font-size:1.1rem; font-weight:bold;">{"Supabase Ready" if supabase else "Bộ Nhớ Tạm"}</span></div>', unsafe_allow_html=True)
with sc3:
    st.markdown(f'<div class="stat-box"><b>Chế Độ Hệ Thống</b><br/><span style="color:#c084fc; font-size:1.1rem; font-weight:bold;">{"PLUS VIP" if is_plus else "BASIC"}</span></div>', unsafe_allow_html=True)

st.write("")

# Form Nhập Công Việc
c_in1, c_in2 = st.columns([3, 1])
with c_in1:
    task_title_input = st.text_input("Tên dự án hoặc công việc lớn cần rã:", placeholder="Ví dụ: Thiết lập phần mềm AI quốc tế tích hợp cổng thanh toán")
with c_in2:
    task_cat_input = st.selectbox("Lĩnh vực:", ["Lập trình / Technology", "Marketing / Branding", "Kinh doanh / Startups", "Cá nhân / Productivity"])

c_opt1, c_opt2, c_opt3 = st.columns(3)
with c_opt1:
    depth_choice = st.select_slider("Mức độ chia nhỏ (Depth):", options=["Cơ bản (3-4 bước)", "Tiêu chuẩn (5-7 bước)", "Chuyên sâu (8-12 bước)"])
with c_opt2:
    st.checkbox("Tính toán giờ làm ước tính", value=True)
with c_opt3:
    st.checkbox("Đồng bộ trực tiếp lên Supabase", value=True if supabase else False, disabled=not supabase)

if is_plus:
    st.markdown("""
    <div style="background: rgba(139, 92, 246, 0.12); border: 1px solid rgba(139, 92, 246, 0.4); padding: 12px 16px; border-radius: 10px; margin-top: 10px;">
        <span style="color: #c084fc; font-weight: bold;">💎 PLUS VIP ACTIVE:</span> 
        Đang bật mô hình Gemini Pro Suy Luận Sâu + Tự động vẽ Sơ đồ Visual WBS & Xuất Developer Prompt.
    </div>
    """, unsafe_allow_html=True)

st.write("")
if st.button("🚀 Kích Hoạt AI Rã Công Việc", type="primary", use_container_width=True):
    if not task_title_input.strip():
        st.warning("Vui lòng nhập tên công việc cần rã!")
    else:
        status_msg = "💎 Gemini Pro đang thực hiện suy luận sâu & phân rã công việc..." if is_plus else "⚡ AI Gemini đang phân tích và rã công việc..."
        with st.spinner(status_msg):
            subtasks_result = call_gemini_ai_wbs(task_title_input, task_cat_input, depth_choice, is_vip=is_plus)
            ok, msg = save_to_supabase(task_title_input, task_cat_input, subtasks_result)
            
            st.session_state['last_result'] = subtasks_result
            st.session_state['last_title'] = task_title_input
            if ok:
                st.success(f"✅ {msg}")

# ==========================================
# 5. HIỂN THỊ KẾT QUẢ KHI CÓ DỮ LIỆU
# ==========================================
if 'last_result' in st.session_state:
    res = st.session_state['last_result']
    title = st.session_state['last_title']

    st.divider()
    st.markdown(f"### 📋 Danh Sách Phân Rã Cho: **{title}**")

    if is_plus:
        v_tab1, v_tab2, v_tab3, v_tab4 = st.tabs(["📌 Checklist Thực Thi", "🧠 Mindmap Visual (WBS)", "💻 Developer Prompt Export", "⚠️ Ma Trận Rủi Ro"])

        with v_tab1:
            for sub in res:
                p_cls = "p-high" if sub['priority'] == "Cao" else ("p-med" if sub['priority'] == "Trung bình" else "p-low")
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="background: #3b82f6; color: white; padding: 3px 10px; border-radius: 6px; font-weight: bold; font-size: 0.8rem;">Bước {sub['step']}</span>
                            <strong style="font-size: 1.05rem; margin-left: 10px; color: #f8fafc;">{sub['title']}</strong>
                            <div style="color: #94a3b8; font-size: 0.88rem; margin-top: 6px;">{sub['description']}</div>
                        </div>
                        <div style="text-align: right; min-width: 110px;">
                            <span class="{p_cls}">{sub['priority']}</span>
                            <div style="color: #64748b; font-size: 0.8rem; margin-top: 8px;">⏱️ {sub['time']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with v_tab2:
            st.markdown("##### 🗺️ Sơ Đồ Cây Tiến Độ WBS (Visual Graph)")
            df_node = pd.DataFrame(res)
            fig_tree = px.bar(
                df_node,
                x='time',
                y='title',
                orientation='h',
                color='priority',
                color_discrete_map={'Cao': '#f87171', 'Trung bình': '#fbbf24', 'Thấp': '#34d399'},
                title="Ước Tính Thời Gian & Mức Độ Ưu Tiên Từng Bước"
            )
            fig_tree.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis={'autorange': 'reversed'}
            )
            st.plotly_chart(fig_tree, use_container_width=True)

        with v_tab3:
            st.markdown("##### 💻 Prompt Tự Động Cho Lập Trình Viên / Project Manager")
            dev_prompt = f"Tôi đang triển khai dự án: '{title}'. Hãy viết mã nguồn chi tiết và kịch bản thực thi cho danh sách các bước sau:\n\n"
            for idx, item in enumerate(res, 1):
                dev_prompt += f"Bước {idx}: {item['title']}\n- Mô tả: {item['description']}\n- Ước tính: {item['time']} | Độ ưu tiên: {item['priority']}\n\n"
            st.code(dev_prompt, language="markdown")

        with v_tab4:
            st.markdown("##### ⚠️ Mức Độ Rủi Ro Tiềm Ấn (VIP Deep Analysis)")
            df_risk = pd.DataFrame(res)
            if 'risk' in df_risk.columns:
                st.dataframe(df_risk[['step', 'title', 'priority', 'risk', 'time']], use_container_width=True)
            else:
                st.info("Kích hoạt lại với Key AQ để AI tính toán ma trận rủi ro chuyên sâu.")

    else:
        for sub in res:
            p_cls = "p-high" if sub['priority'] == "Cao" else ("p-med" if sub['priority'] == "Trung bình" else "p-low")
            st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="background: #3b82f6; color: white; padding: 3px 10px; border-radius: 6px; font-weight: bold; font-size: 0.8rem;">Bước {sub['step']}</span>
                        <strong style="font-size: 1.05rem; margin-left: 10px; color: #f8fafc;">{sub['title']}</strong>
                        <div style="color: #94a3b8; font-size: 0.88rem; margin-top: 6px;">{sub['description']}</div>
                    </div>
                    <div style="text-align: right; min-width: 110px;">
                        <span class="{p_cls}">{sub['priority']}</span>
                        <div style="color: #64748b; font-size: 0.8rem; margin-top: 8px;">⏱️ {sub['time']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.info("💡 Mẹo: Bật công tắc 'Trải nghiệm Giao diện & AI PLUS VIP' ở menu bên trái để mở khóa Sơ đồ Mindmap Visual WBS và Gemini suy luận sâu!")
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
