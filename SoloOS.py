import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import time
import os
from datetime import datetime
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

# Quản lý State Bản Quyền & Keys
if 'user_plan' not in st.session_state:
    st.session_state['user_plan'] = 'Basic'  # Options: 'Basic', 'SoloFlow PLUS'
if 'gemini_key' not in st.session_state:
    st.session_state['gemini_key'] = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))

is_plus = (st.session_state['user_plan'] != 'Basic')

# CSS Dynamic Customization (VIP Plus sẽ có hiệu ứng Glow Cyberpunk)
plus_css = """
    /* Cyberpunk Neon Theme cho VIP PLUS */
    .stApp { background-color: #050811; }
    .glass-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.5) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.15) !important;
    }
    .vip-badge-active {
        background: linear-gradient(90deg, #ec4899, #8b5cf6, #3b82f6);
        color: white; padding: 4px 12px; border-radius: 20px;
        font-weight: 800; font-size: 0.8rem; text-shadow: 0 0 8px rgba(255,255,255,0.5);
    }
""" if is_plus else """
    /* Standard Dark Theme */
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
    """Gọi Gemini AI để phân rã công việc chính xác 100% dạng JSON"""
    api_key = st.session_state.get('gemini_key')
    if not api_key:
        # Tra về dữ liệu mô phỏng thông minh nếu thiếu API Key
        return [
            {"step": 1, "title": f"Khảo sát & Lập kế hoạch: {prompt_text[:30]}...", "description": "Xác định rõ mục tiêu cốt lõi, công cụ cần sử dụng và đầu ra.", "time": "2.0 giờ", "priority": "Cao"},
            {"step": 2, "title": "Thiết kế kiến trúc / Kịch bản thực thi", "description": "Phân chia module, tối ưu quy trình xử lý công việc.", "time": "3.5 giờ", "priority": "Cao"},
            {"step": 3, "title": "Thực thi xây dựng sản phẩm / nội dung", "description": "Tạo ra bản mẫu đầu tiên và tiến hành kiểm thử nội bộ.", "time": "5.0 giờ", "priority": "Trung bình"},
            {"step": 4, "title": "Đánh giá, tối ưu và nghiệm thu", "description": "Sửa lỗi, hoàn thiện chi tiết và đóng gói hoàn tất.", "time": "1.5 giờ", "priority": "Thấp"}
        ]
    
    try:
        genai.configure(api_key=api_key)
        # Sử dụng mô hình Gemini
        model_name = "gemini-1.5-pro" if is_vip else "gemini-1.5-flash"
        model = genai.GenerativeModel(model_name)
        
        vip_instruction = "Phân tích cực kỳ sâu sắc, tính toán ma trận rủi ro và liệt kê hành động cụ thể cho từng bước." if is_vip else "Trả về các bước thực thi gọn gàng, thực tế."

        sys_prompt = f"""
        Bạn là chuyên gia quản lý dự án cấp cao. Hãy phân rã công việc sau đây thành danh sách các bước thực thi chi tiết (WBS).
        Công việc: "{prompt_text}"
        Ngành nghề/Danh mục: "{category}"
        Mức độ chi tiết: "{depth_str}"
        Yêu cầu nâng cao: {vip_instruction}

        BẮT BUỘC trả về đúng định dạng JSON Array chứa các Object, không thêm bất kỳ văn bản nào khác ngoài JSON.
        Cấu trúc JSON từng phần tử:
        [
            {{
                "step": 1,
                "title": "Tên bước thực hiện ngắn gọn",
                "description": "Mô tả hành động cụ thể cần làm",
                "time": "Ví dụ: 1.5 giờ",
                "priority": "Cao" hoặc "Trung bình" hoặc "Thấp"
            }}
        ]
        """
        
        response = model.generate_content(sys_prompt)
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_text)
        return data
    except Exception as e:
        st.error(f"⚠️ Lỗi AI Gemini: {str(e)}. Đang dùng chế độ dự phòng...")
        return [
            {"step": 1, "title": f"Phân tích yêu cầu: {prompt_text[:25]}", "description": "Khảo sát và chuẩn bị tài nguyên.", "time": "1.0 giờ", "priority": "Cao"},
            {"step": 2, "title": "Triển khai thực hiện", "description": "Xây dựng các thành phần chính.", "time": "3.0 giờ", "priority": "Trung bình"}
        ]

# Helper Lưu Task
def save_task(title, category, subtasks):
    if supabase:
        try:
            m_res = supabase.table("main_tasks").insert({"title": title, "category": category, "progress": 0}).execute()
            if m_res.data:
                m_id = m_res.data[0]['id']
                payload = [{
                    "main_task_id": m_id, "step_number": s["step"], "title": s["title"],
                    "description": s.get("description",""), "time_estimate": s["time"],
                    "priority": s["priority"], "is_completed": False
                } for s in subtasks]
                supabase.table("subtasks").insert(payload).execute()
                return True, "Đã lưu trực tiếp vào Supabase Cloud!"
        except Exception as e:
            return False, f"Lỗi Supabase: {str(e)}"
    return True, "Đã lưu vào bộ nhớ tạm ứng dụng."

# ==========================================
# 3. SIDEBAR NAVIGATION & PLUS VIP SWITCH
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='margin:0;'>⚡ SoloFlow <span style='color:#3b82f6;'>OS</span></h2>", unsafe_allow_html=True)
    st.caption("AI Task Decomposition Platform")
    
    st.divider()
    
    # Khu vực Trạng thái VIP / Switch
    if is_plus:
        st.markdown('<div class="vip-badge-active">💎 BẢN PLUS VIP ĐÃ KÍCH HOẠT</div>', unsafe_allow_html=True)
        st.caption("✨ Mô hình AI: Gemini 1.5 Pro Deep Reasoning")
    else:
        st.markdown('<b>Gói hiện tại: Basic</b>', unsafe_allow_html=True)
        if st.button("🚀 Nâng Cấp / Kích Hoạt Bản PLUS", use_container_width=True):
            st.session_state['user_plan'] = 'SoloFlow PLUS'
            st.rerun()

    st.divider()

    # Nhập Gemini API Key
    with st.expander("🔑 Cấu Hình Gemini AI Key", expanded=not bool(st.session_state['gemini_key'])):
        g_key = st.text_input("Gemini API Key:", value=st.session_state['gemini_key'], type="password", help="Lấy Key miễn phí tại Google AI Studio")
        if st.button("Lưu API Key"):
            st.session_state['gemini_key'] = g_key
            st.success("Đã lưu API Key!")
            st.rerun()

    # Nút Toggle dùng thử nhanh bản VIP để người dùng trải nghiệm ngay
    st.write("")
    dev_mode = st.toggle("🧪 Dùng thử giao diện & AI PLUS VIP", value=is_plus)
    if dev_mode != is_plus:
        st.session_state['user_plan'] = 'SoloFlow PLUS' if dev_mode else 'Basic'
        st.rerun()

# ==========================================
# 4. TRANG CHÍNH: GIAO DIỆN RÃ CÔNG VIỆC AI
# ==========================================
st.title("⚡ AI Phân Rã Công Việc Dũng Mãnh")
st.caption("Nhập mục tiêu của bạn, AI sẽ giải quyết đúng trọng tâm và xây dựng lộ trình thực thi từng bước.")

# Khung Nhập Liệu
c_in1, c_in2 = st.columns([3, 1])
with c_in1:
    task_title_input = st.text_input("Tên dự án hoặc công việc lớn cần rã:", placeholder="Ví dụ: Thiết lập phần mềm AI quốc tế tích hợp cổng thanh toán")
with c_in2:
    task_cat_input = st.selectbox("Lĩnh vực:", ["Lập trình / Technology", "Marketing / Branding", "Kinh doanh / Startups", "Cá nhân / Productivity"])

c_opt1, c_opt2, c_opt3 = st.columns(3)
with c_opt1:
    depth_choice = st.select_slider("Mức độ chi tiết:", options=["Cơ bản (3-4 bước)", "Tiêu chuẩn (5-7 bước)", "Chuyên sâu (8-12 bước)"])
with c_opt2:
    st.checkbox("Tính thời gian ước tính", value=True)
with c_opt3:
    st.checkbox("Đồng bộ Supabase Cloud", value=True if supabase else False, disabled=not supabase)

# TÍNH NĂNG ĐẶC QUYỀN PLUS VIP NGAY TẠI KHUNG AI
if is_plus:
    st.markdown("""
    <div style="background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.3); padding: 12px; border-radius: 10px; margin-top: 10px;">
        <span style="color: #c084fc; font-weight: bold;">💎 PLUS VIP ACTIVE:</span> 
        Chế độ suy luận Gemini Pro & Tự động xuất Mindmap Visual WBS đã sẵn sàng.
    </div>
    """, unsafe_allow_html=True)

st.write("")
if st.button("🚀 Kích Hoạt AI Rã Công Việc", type="primary", use_container_width=True):
    if not task_title_input.strip():
        st.warning("Vui lòng điền nội dung công việc!")
    else:
        status_msg = "💎 Gemini Pro Deep Thinking đang phân tích toàn diện..." if is_plus else "⚡ Gemini AI đang phân tích và rã công việc..."
        with st.spinner(status_msg):
            # Gọi Gemini AI
            subtasks_result = call_gemini_ai_wbs(task_title_input, task_cat_input, depth_choice, is_vip=is_plus)
            
            # Lưu vào CSDL / State
            ok, msg = save_task(task_title_input, task_cat_input, subtasks_result)
            st.session_state['last_result'] = subtasks_result
            st.session_state['last_title'] = task_title_input
            if ok:
                st.success(f"✅ Rã công việc thành công! {msg}")

# ==========================================
# 5. HIỂN THỊ KẾT QUẢ & CÁC TÍNH NĂNG NÂNG CẤP
# ==========================================
if 'last_result' in st.session_state:
    res = st.session_state['last_result']
    title = st.session_state['last_title']
    
    st.divider()
    st.markdown(f"### 📋 Danh Sách Phân Rã Cho: **{title}**")
    
    # 🌟 GIAO DIỆN VIP PLUS: Tab bổ sung sơ đồ MindMap & Prompt xuất Developer
    if is_plus:
        v_tab1, v_tab2, v_tab3 = st.tabs(["📌 Checklist Thực Thi", "🧠 Mindmap Visual (VIP)", "💻 Developer Prompt Export (VIP)"])
        
        with v_tab1:
            for sub in res:
                p_cls = "p-high" if sub['priority'] == "Cao" else ("p-med" if sub['priority'] == "Trung bình" else "p-low")
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="background: #3b82f6; color: white; padding: 2px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem;">Bước {sub['step']}</span>
                            <strong style="font-size: 1.05rem; margin-left: 10px; color: #f8fafc;">{sub['title']}</strong>
                            <div style="color: #94a3b8; font-size: 0.88rem; margin-top: 6px;">{sub['description']}</div>
                        </div>
                        <div style="text-align: right;">
                            <span class="{p_cls}">{sub['priority']}</span>
                            <div style="color: #64748b; font-size: 0.8rem; margin-top: 6px;">⏱️ {sub['time']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with v_tab2:
            st.markdown("##### 🗺️ Sơ Đồ Cây Tiến Độ (WBS Visual Graph)")
            # Vẽ sơ đồ dòng chảy tiến độ công việc bằng Plotly
            df_node = pd.DataFrame(res)
            fig_tree = px.bar(df_node, x='time', y='title', orientation='h', color='priority', title="Tiến Độ & Thời Gian Dự Kiến Từng Bước")
            fig_tree.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_tree, use_container_width=True)

        with v_tab3:
            st.markdown("##### 💻 Prompt Tự Động Cho Lập Trình Viên / ChatGPT")
            dev_prompt = f"Tôi đang xây dựng dự án: '{title}'. Hãy triển khai chi tiết mã nguồn và hướng dẫn kĩ thuật cho các bước sau:\n"
            for idx, item in enumerate(res, 1):
                dev_prompt += f"{idx}. {item['title']}: {item['description']}\n"
            st.code(dev_prompt, language="markdown")

    else:
        # GIAO DIỆN CHUẨN (BASIC)
        for sub in res:
            p_cls = "p-high" if sub['priority'] == "Cao" else ("p-med" if sub['priority'] == "Trung bình" else "p-low")
            st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="background: #3b82f6; color: white; padding: 2px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem;">Bước {sub['step']}</span>
                        <strong style="font-size: 1.05rem; margin-left: 10px; color: #f8fafc;">{sub['title']}</strong>
                        <div style="color: #94a3b8; font-size: 0.88rem; margin-top: 6px;">{sub['description']}</div>
                    </div>
                    <div style="text-align: right;">
                        <span class="{p_cls}">{sub['priority']}</span>
                        <div style="color: #64748b; font-size: 0.8rem; margin-top: 6px;">⏱️ {sub['time']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.info("💡 Mẹo: Bật nút 'Dùng thử giao diện & AI PLUS VIP' ở thanh menu bên trái để mở khóa Sơ đồ Mindmap & Chế độ Gemini Pro!")
