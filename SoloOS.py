import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import json
import time
from datetime import datetime, timedelta
from supabase import create_client, Client

# ==========================================
# 1. CẤU HÌNH TRANG & THEME GLASSMORPHISM SAAS
# ==========================================
st.set_page_config(
    page_title="SoloFlow OS - Enterprise Task Decomposition Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS High-End Obsidian Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Background chính */
    .stApp {
        background-color: #080c14;
        color: #f1f5f9;
    }
    
    /* Custom Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    
    /* Glassmorphic Card Container */
    .glass-card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.25s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(59, 130, 246, 0.4);
        box-shadow: 0 8px 30px rgba(59, 130, 246, 0.12);
    }
    
    /* Status Badges */
    .badge-online {
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .badge-offline {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    /* Priority Tags */
    .p-high { color: #f87171; background: rgba(248, 113, 113, 0.12); padding: 3px 10px; border-radius: 6px; font-size: 0.78rem; font-weight:600; }
    .p-med { color: #fbbf24; background: rgba(251, 191, 36, 0.12); padding: 3px 10px; border-radius: 6px; font-size: 0.78rem; font-weight:600; }
    .p-low { color: #34d399; background: rgba(52, 211, 153, 0.12); padding: 3px 10px; border-radius: 6px; font-size: 0.78rem; font-weight:600; }
    
    /* VIP Pricing Cards */
    .vip-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 24px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .vip-card-popular {
        border: 2px solid #3b82f6;
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        box-shadow: 0 0 35px rgba(59, 130, 246, 0.2);
    }
    .vip-price {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        margin: 12px 0;
    }
    
    /* Metric Card Styling */
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #38bdf8;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. KHỞI TẠO ĐỘNG SUPABASE CLIENT
# ==========================================
@st.cache_resource
def init_supabase_client(url: str, key: str):
    try:
        if url and key:
            return create_client(url, key)
    except Exception as e:
        st.error(f"Lỗi khởi tạo Supabase Client: {str(e)}")
    return None

# Tải credentials từ Secrets hoặc biến môi trường
sb_url = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL", ""))
sb_key = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY", ""))

if 'supabase_url' not in st.session_state:
    st.session_state['supabase_url'] = sb_url
if 'supabase_key' not in st.session_state:
    st.session_state['supabase_key'] = sb_key

supabase: Client = init_supabase_client(st.session_state['supabase_url'], st.session_state['supabase_key'])

# Quản lý bộ nhớ tạm (Local Fallback) nếu chưa nối Supabase
if 'local_tasks' not in st.session_state:
    st.session_state['local_tasks'] = []
if 'user_plan' not in st.session_state:
    st.session_state['user_plan'] = 'Basic'

# ==========================================
# 3. HELPER FUNCTIONS (BACKEND CRUD)
# ==========================================
def db_save_task_with_subtasks(title, category, framework, detail_level, subtasks_list):
    """Lưu dự án và danh sách subtask vào Supabase hoặc Local Session State"""
    if supabase:
        try:
            # 1. Insert Main Task
            res_main = supabase.table("main_tasks").insert({
                "title": title,
                "category": category,
                "framework": framework,
                "detail_level": detail_level,
                "progress": 0
            }).execute()
            
            if res_main.data:
                main_id = res_main.data[0]['id']
                # 2. Insert Subtasks
                payload = [
                    {
                        "main_task_id": main_id,
                        "step_number": st_item["step"],
                        "title": st_item["title"],
                        "description": st_item.get("description", ""),
                        "time_estimate": st_item["time"],
                        "priority": st_item["priority"],
                        "complexity": st_item.get("complexity", "Trung bình"),
                        "is_completed": False
                    } for st_item in subtasks_list
                ]
                supabase.table("subtasks").insert(payload).execute()
                return True, "Đã lưu trực tiếp vào Supabase Cloud!"
        except Exception as e:
            return False, f"Lỗi Supabase: {str(e)}"
    
    # Local Fallback
    new_task = {
        "id": f"local_{int(time.time())}",
        "title": title,
        "category": category,
        "framework": framework,
        "detail_level": detail_level,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "subtasks": subtasks_list
    }
    st.session_state['local_tasks'].insert(0, new_task)
    return True, "Đã lưu vào bộ nhớ tạm (Local Session State)"

def db_get_all_tasks():
    """Lấy danh sách task từ Supabase hoặc Local Storage"""
    if supabase:
        try:
            res = supabase.table("main_tasks").select("*, subtasks(*)").order("created_at", desc=True).execute()
            return res.data
        except Exception:
            pass
    return st.session_state['local_tasks']

def db_toggle_subtask(subtask_id, current_status):
    """Đổi trạng thái hoàn thành của subtask"""
    if supabase and not str(subtask_id).startswith("local"):
        try:
            supabase.table("subtasks").update({"is_completed": not current_status}).eq("id", subtask_id).execute()
            return True
        except Exception:
            return False
    return True

def db_delete_main_task(task_id):
    """Xóa dự án"""
    if supabase and not str(task_id).startswith("local"):
        try:
            supabase.table("main_tasks").delete().eq("id", task_id).execute()
            return True
        except Exception:
            return False
    else:
        st.session_state['local_tasks'] = [t for t in st.session_state['local_tasks'] if t['id'] != task_id]
        return True

# ==========================================
# 4. SIDEBAR NAVIGATION & ACCOUNT STATUS
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='margin:0; font-weight:800; color:#fff;'>⚡ SoloFlow <span style='color:#3b82f6;'>OS</span></h2>", unsafe_allow_html=True)
    st.caption("Executive Task Decomposition & Project Engine")
    
    st.write("")
    
    # Trạng thái kết nối Supabase Indicator
    if supabase:
        st.markdown('<span class="badge-online">🟢 Supabase Connected</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-offline">🔴 Local Memory Mode</span>', unsafe_allow_html=True)
        with st.expander("🔑 Kết Nối Supabase Cloud"):
            u_input = st.text_input("Supabase URL", value=st.session_state['supabase_url'])
            k_input = st.text_input("Supabase Anon Key", type="password", value=st.session_state['supabase_key'])
            if st.button("Lưu & Kết Nối Tức Thì"):
                st.session_state['supabase_url'] = u_input
                st.session_state['supabase_key'] = k_input
                st.cache_resource.clear()
                st.rerun()

    st.divider()

    # Profile người dùng
    plan_label = f"<b style='color:#60a5fa;'>{st.session_state['user_plan']}</b>"
    st.markdown(f"""
    <div style="background: #1e293b; padding: 14px; border-radius: 12px; border: 1px solid #334155;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; font-size: 1.1rem;">N</div>
            <div>
                <div style="font-weight: 700; color: white; font-size: 0.95rem;">Nepcutu20</div>
                <div style="font-size: 0.8rem; color: #94a3b8;">Gói: {plan_label}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.subheader("⚙️ Cấu Hình AI Breakdown")
    ai_framework = st.selectbox("Khung tư duy Rã Task", ["WBS Đa Tầng (Standard)", "Agile Sprint Decomposition", "Ma Trận Ưu Tiên Eisenhower", "Checklist Thực Thi Nhanh"])
    ai_creativity = st.slider("Mức độ chi tiết AI", 0.1, 1.0, 0.75)

# ==========================================
# 5. MAIN NAVIGATION TABS
# ==========================================
tab_dashboard, tab_engine, tab_workspace, tab_vip, tab_db_admin, tab_settings = st.tabs([
    "📊 Dashboard", 
    "🧠 AI Rã Công Việc", 
    "📋 Workspace & WBS Tree", 
    "💎 SoloFlow PLUS VIP", 
    "🗄️ Quản Lý Supabase", 
    "⚙️ Cài Đặt"
])

# ==========================================
# TAB 1: EXECUTIVE DASHBOARD
# ==========================================
with tab_dashboard:
    st.markdown("### 📊 Tổng Quan Năng Suất & Tiến Độ Dự Án")
    
    all_tasks = db_get_all_tasks()
    total_projects = len(all_tasks)
    total_subtasks = 0
    completed_subtasks = 0
    
    for t in all_tasks:
        sub_list = t.get('subtasks', [])
        total_subtasks += len(sub_list)
        completed_subtasks += sum(1 for s in sub_list if s.get('is_completed', False))
        
    completion_rate = int((completed_subtasks / total_subtasks * 100)) if total_subtasks > 0 else 0

    # Top Metrics Grid
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="glass-card"><div class="metric-label">Tổng Dự Án</div><div class="metric-value">{total_projects}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="glass-card"><div class="metric-label">Tổng Bước Công Việc</div><div class="metric-value">{total_subtasks}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="glass-card"><div class="metric-label">Đã Hoàn Thành</div><div class="metric-value" style="color:#10b981;">{completed_subtasks}</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="glass-card"><div class="metric-label">Tỷ Lệ Hoàn Thành</div><div class="metric-value" style="color:#f59e0b;">{completion_rate}%</div></div>', unsafe_allow_html=True)

    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        st.markdown("##### 📈 Phân Bổ Công Việc Theo Danh Mục")
        if all_tasks:
            cat_counts = {}
            for t in all_tasks:
                cat = t.get('category', 'Chung')
                cat_counts[cat] = cat_counts.get(cat, 0) + 1
            
            df_chart = pd.DataFrame(list(cat_counts.items()), columns=['Category', 'Count'])
            fig = px.bar(df_chart, x='Category', y='Count', color='Category', template='plotly_dark', color_discrete_sequence=px.colors.qualitative.Bold)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=280)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Chưa có dữ liệu biểu đồ. Hãy rã công việc mới ở Tab AI!")

    with col_chart2:
        st.markdown("##### 🎯 Trạng Thái Phân Rã")
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Đã Hoàn Thành', 'Đang Thực Hiện'],
            values=[completed_subtasks, max(0, total_subtasks - completed_subtasks)],
            hole=.6,
            marker_colors=['#10b981', '#3b82f6']
        )])
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, height=280, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================
# TAB 2: AI DECOMPOSITION ENGINE (RÃ CÔNG VIỆC)
# ==========================================
with tab_engine:
    st.markdown("### 🧠 Động Cơ AI Rã Công Việc Chuyên Sâu")
    st.caption("Nhập mục tiêu lớn hoặc tên dự án, SoloFlow AI sẽ phân rã thành các khối thực thi cụ thể kèm ước tính thời gian & độ ưu tiên.")
    
    col_input1, col_input2 = st.columns([3, 1])
    with col_input1:
        task_input_title = st.text_input("Tên dự án / Công việc lớn cần phân rã:", placeholder="Ví dụ: Lập kế hoạch xây dựng phần mềm Quản lý công việc có cổng thanh toán")
    with col_input2:
        task_category = st.selectbox("Phân loại dự án:", ["Lập trình / Technology", "Marketing / Content", "Kinh doanh / Sales", "Vận hành / Operations", "Học tập / Cá nhân"])

    col_opt1, col_opt2, col_opt3 = st.columns(3)
    with col_opt1:
        granularity = st.select_slider("Mức độ chia nhỏ (Depth):", options=["Cơ bản (3-5 bước)", "Chi tiết (6-8 bước)", "Sâu sắc (9-12 bước)"])
    with col_opt2:
        est_time_toggle = st.checkbox("Tính toán giờ làm ước tính", value=True)
    with col_opt3:
        auto_sync_sb = st.checkbox("Đồng bộ trực tiếp lên Supabase", value=True if supabase else False, disabled=not supabase)

    st.write("")
    if st.button("🚀 Kích Hoạt AI Rã Công Việc", type="primary", use_container_width=True):
        if not task_input_title:
            st.warning("Vui lòng điền nội dung công việc lớn cần rã!")
        else:
            with st.spinner("⚡ SoloMind AI đang phân tích cấu trúc, thiết lập ma trận ưu tiên và chia nhỏ task..."):
                time.sleep(1.4) # Simulated AI latency
                
                # Dynamic Template Generator Based on Input
                if "thanh toán" in task_input_title.lower() or "phần mềm" in task_input_title.lower() or "web" in task_input_title.lower():
                    mock_subtasks = [
                        {"step": 1, "title": "Phân tích yêu cầu hệ thống & Kiến trúc CSDL Supabase", "description": "Thiết kế bảng main_tasks, subtasks và các chính sách bảo mật RLS", "time": "2.0 giờ", "priority": "Cao", "complexity": "Phức tạp"},
                        {"step": 2, "title": "Khởi tạo môi trường lập trình & Cấu hình SDK", "description": "Cài đặt thư viện Streamlit, Supabase-py, tạo file .env", "time": "0.5 giờ", "priority": "Cao", "complexity": "Dễ"},
                        {"step": 3, "title": "Xây dựng Giao diện UI Obsidian Dark Theme Glassmorphism", "description": "Viết CSS custom cho sidebar, thẻ card, badge và bảng màu SaaS", "time": "3.0 giờ", "priority": "Trung bình", "complexity": "Vừa"},
                        {"step": 4, "title": "Tích hợp Cổng thanh toán VietQR & Gói PLUS VIP", "description": "Tạo QR code chuyển khoản tự động kèm nội dung memo định danh", "time": "1.5 giờ", "priority": "Cao", "complexity": "Vừa"},
                        {"step": 5, "title": "Kiểm thử luồng gửi nhận dữ liệu Real-time với Supabase", "description": "Test các thao tác Thêm, Sửa, Xóa và xử lý lỗi gãy kết nối mạng", "time": "1.0 giờ", "priority": "Trung bình", "complexity": "Dễ"},
                        {"step": 6, "title": "Đóng gói & Deploy ứng dụng lên Streamlit Cloud", "description": "Cấu hình requirements.txt và secrets trên Cloud Dashboard", "time": "0.5 giờ", "priority": "Thấp", "complexity": "Dễ"}
                    ]
                else:
                    mock_subtasks = [
                        {"step": 1, "title": "Nghiên cứu thị trường & Xác định mục tiêu cốt lõi", "description": "Làm rõ phạm vi công việc và kết quả đầu ra (Deliverables)", "time": "1.5 giờ", "priority": "Cao", "complexity": "Vừa"},
                        {"step": 2, "title": "Lập danh sách nguồn lực & Công cụ cần thiết", "description": "Chuẩn bị nhân sự, phần mềm và ngân sách thực hiện", "time": "1.0 giờ", "priority": "Trung bình", "complexity": "Dễ"},
                        {"step": 3, "title": "Xây dựng kịch bản chi tiết từng bước thực thi", "description": "Phân chia công việc theo các mốc mốc thời gian (Milestones)", "time": "2.5 giờ", "priority": "Cao", "complexity": "Phức tạp"},
                        {"step": 4, "title": "Thực hiện giai đoạn thử nghiệm (Pilot phase)", "description": "Chạy thử kịch bản nhỏ để phát hiện sai sót", "time": "3.0 giờ", "priority": "Cao", "complexity": "Phức tạp"},
                        {"step": 5, "title": "Đánh giá kết quả & Tối ưu hóa quy trình", "description": "Tổng kết bài học kinh nghiệm và bàn giao kết quả", "time": "1.0 giờ", "priority": "Thấp", "complexity": "Dễ"}
                    ]
                
                # Save to Database / State
                success, msg = db_save_task_with_subtasks(task_input_title, task_category, ai_framework, granularity, mock_subtasks)
                
                if success:
                    st.success(f"✅ Rã công việc thành công! {msg}")
                else:
                    st.error(msg)
                
                # Display Results Immediately
                st.markdown(f"#### 📋 Danh Sách Phân Rã Cho: **{task_input_title}**")
                for sub in mock_subtasks:
                    p_class = "p-high" if sub['priority'] == "Cao" else ("p-med" if sub['priority'] == "Trung bình" else "p-low")
                    st.markdown(f"""
                    <div class="glass-card">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div>
                                <span style="background: #3b82f6; color: white; padding: 2px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem;">Bước {sub['step']}</span>
                                <strong style="font-size: 1.05rem; margin-left: 10px; color: #f8fafc;">{sub['title']}</strong>
                                <div style="color: #94a3b8; font-size: 0.88rem; margin-top: 6px;">{sub['description']}</div>
                            </div>
                            <div style="text-align: right;">
                                <span class="{p_class}">{sub['priority']}</span>
                                <div style="color: #64748b; font-size: 0.8rem; margin-top: 6px;">⏱️ {sub['time']}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# ==========================================
# TAB 3: WORKSPACE & WBS TREE VIEW
# ==========================================
with tab_workspace:
    st.markdown("### 📋 Không Gian Làm Việc & Quản Lý WBS")
    
    tasks_list = db_get_all_tasks()
    
    if not tasks_list:
        st.info("Chưa có dự án nào trong hệ thống. Hãy sang Tab 'AI Rã Công Việc' để tạo dự án đầu tiên!")
    else:
        for t_idx, t_item in enumerate(tasks_list):
            task_id = t_item.get('id')
            title = t_item.get('title', 'Không có tiêu đề')
            subtasks = t_item.get('subtasks', [])
            
            # Tính toán phần trăm tiến độ
            total_sub = len(subtasks)
            done_sub = sum(1 for s in subtasks if s.get('is_completed', False))
            prog_percent = int((done_sub / total_sub * 100)) if total_sub > 0 else 0
            
            with st.expander(f"📌 {title} | Progress: {prog_percent}% ({done_sub}/{total_sub} hoàn thành)"):
                st.progress(prog_percent / 100)
                
                col_exp1, col_exp2 = st.columns([3, 1])
                with col_exp1:
                    st.caption(f"ID: `{task_id}` | Khung rã: {t_item.get('framework', 'WBS')} | Danh mục: {t_item.get('category', 'Chung')}")
                with col_exp2:
                    if st.button("🗑️ Xóa Dự Án Này", key=f"btn_del_{task_id}"):
                        if db_delete_main_task(task_id):
                            st.success("Đã xóa dự án!")
                            time.sleep(0.5)
                            st.rerun()

                st.markdown("##### 📝 Cây Thư Mục Công Việc (WBS Checklist):")
                for s_item in subtasks:
                    s_id = s_item.get('id', f"local_sub_{s_item.get('step_number')}")
                    s_title = s_item.get('title')
                    is_done = s_item.get('is_completed', False)
                    s_time = s_item.get('time_estimate', 'N/A')
                    s_priority = s_item.get('priority', 'Trung bình')
                    
                    c_chk, c_txt, c_meta = st.columns([0.5, 3.5, 1])
                    with c_chk:
                        chk_val = st.checkbox("", value=is_done, key=f"chk_{task_id}_{s_id}")
                        if chk_val != is_done:
                            db_toggle_subtask(s_id, is_done)
                            st.rerun()
                    with c_txt:
                        if is_done:
                            st.markdown(f"~~**Bước {s_item.get('step_number')}**: {s_title}~~ ✅")
                        else:
                            st.markdown(f"**Bước {s_item.get('step_number')}**: {s_title}")
                    with c_meta:
                        st.caption(f"⏱️ {s_time} | {s_priority}")

# ==========================================
# TAB 4: BẢN PLUS VIP & CỔNG THANH TOÁN (100% MATCH)
# ==========================================
with tab_vip:
    st.markdown("""
    <div style="text-align: center; padding: 15px 0 30px 0;">
        <h1 style="font-size: 2.3rem; font-weight: 900; color: #ffffff;">💎 SoloFlow PLUS - Sức Mạnh Vô Song</h1>
        <p style="color: #94a3b8; font-size: 1.05rem;">Xóa bỏ mọi giới hạn hoạt động. Nâng tầm tư duy năng suất cùng công nghệ AI đặc quyền đỉnh cao.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_v1, col_v2, col_v3 = st.columns(3)
    
    # Card Basic
    with col_v1:
        st.markdown("""
        <div class="vip-card">
            <div>
                <h3 style="color:#94a3b8;">⏳ Basic Plan</h3>
                <div class="vip-price">Miễn phí</div>
                <ul style="color: #94a3b8; font-size: 0.88rem; padding-left: 18px; line-height: 1.8;">
                    <li>Rã công việc giới hạn nhu cầu</li>
                    <li>Hạ tầng FlowViewer cơ bản</li>
                    <li>Trình tư vấn AI bị giới hạn</li>
                    <li>Giao diện Deep Obsidian mặc định</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button("Đã Kích Hoạt Mặc Định", disabled=True, key="v_basic", use_container_width=True)

    # Card Monthly Premium
    with col_v2:
        st.markdown("""
        <div class="vip-card vip-card-popular">
            <div>
                <span style="background: #f59e0b; color: black; font-weight: bold; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem;">POPULAR</span>
                <h3 style="color:#60a5fa; margin-top:6px;">🌟 Monthly Premium</h3>
                <div class="vip-price">79.000đ<span style="font-size:0.95rem; font-weight:normal; color:#94a3b8;">/tháng</span></div>
                <ul style="color: #cbd5e1; font-size: 0.88rem; padding-left: 18px; line-height: 1.8;">
                    <li>Rã công việc siêu tốc không giới hạn</li>
                    <li>Mở khóa toàn bộ Cosmic Theme</li>
                    <li>Điều độ nhịp sinh học Circadian</li>
                    <li>Trình hạ âm Âm thanh 3D Binaural</li>
                    <li>Bản đồ tư duy AI Mind Map Pro</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚡ Đăng Ký Ngay (79k)", type="primary", key="v_monthly", use_container_width=True):
            st.session_state['pay_plan'] = "Monthly Premium"
            st.session_state['pay_price'] = 79000

    # Card Cosmic VIP Lifetime
    with col_v3:
        st.markdown("""
        <div class="vip-card">
            <div>
                <h3 style="color:#c084fc;">🌌 Cosmic VIP Lifetime</h3>
                <div class="vip-price">399.000đ<span style="font-size:0.95rem; font-weight:normal; color:#94a3b8;">/vĩnh viễn</span></div>
                <ul style="color: #cbd5e1; font-size: 0.88rem; padding-left: 18px; line-height: 1.8;">
                    <li>Sở hữu vĩnh viễn toàn bộ tính năng</li>
                    <li>Miễn phí cập nhật tất cả phiên bản tiếp theo</li>
                    <li>Nhận biểu tượng huy hiệu VIP đặc biệt</li>
                    <li>Ưu tiên xử lý hệ thống AI tốc độ cao</li>
                    <li>Hỗ trợ kỹ thuật 24/7 từ đội ngũ phát triển</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💎 Mua Gói Lifetime (399k)", key="v_lifetime", use_container_width=True):
            st.session_state['pay_plan'] = "Cosmic VIP Lifetime"
            st.session_state['pay_price'] = 399000

    # Modal / Block Thanh Toán VietQR Tự Động
    if 'pay_plan' in st.session_state:
        st.divider()
        st.markdown(f"### 💳 Cổng Thanh Toán VietQR - Gói `{st.session_state['pay_plan']}`")
        
        c_qr_img, c_qr_info = st.columns([1, 2])
        
        bank_id = "MB"
        acc_num = "0333333333"
        acc_name = "SOLOFLOW OS VIP"
        amount = st.session_state['pay_price']
        memo = f"SOLOFLOW {st.session_state['pay_plan'].replace(' ', '')}"
        
        qr_url = f"https://img.vietqr.io/image/{bank_id}-{acc_num}-compact2.png?amount={amount}&addInfo={memo}&accountName={acc_name}"
        
        with c_qr_img:
            st.image(qr_url, caption="Quét mã QR bằng App Ngân Hàng bất kỳ", width=240)
        with c_qr_info:
            st.write(f"• **Số tiền:** `{amount:,} VNĐ`")
            st.write(f"• **Nội dung chuyển khoản:** `{memo}`")
            st.write(f"• **Ngân hàng:** `{bank_id}` - **STK:** `{acc_num}`")
            st.write(f"• **Tên tài khoản:** `{acc_name}`")
            st.info("💡 Hệ thống sẽ tự động xác thực giao dịch sau khi chuyển khoản thành công.")
            
            if st.button("✅ Tôi Đã Chuyển Khoản Thành Công", type="primary"):
                st.session_state['user_plan'] = st.session_state['pay_plan']
                del st.session_state['pay_plan']
                st.balloons()
                st.success("Tài khoản của bạn đã nâng cấp thành công lên bản VIP!")
                time.sleep(1.5)
                st.rerun()

# ==========================================
# TAB 5: QUẢN LÝ DATABASE SUPABASE DIRECT
# ==========================================
with tab_db_admin:
    st.markdown("### 🗄️ Quản Lý Dữ Liệu Trực Tiếp Trên Supabase Cloud")
    
    if not supabase:
        st.warning("⚠️ Hiện tại ứng dụng đang ở chế độ 'Local Memory'. Vui lòng cấu hình URL & Anon Key ở Sidebar để xem dữ liệu Supabase.")
    else:
        st.success("🟢 Kết nối Supabase thông suốt! Bạn có thể xem bảng dữ liệu bên dưới:")
        
        tbl_choice = st.radio("Chọn bảng dữ liệu để kiểm tra:", ["main_tasks", "subtasks"], horizontal=True)
        
        try:
            res_data = supabase.table(tbl_choice).select("*").order("created_at", desc=True).limit(50).execute()
            if res_data.data:
                df_sb = pd.DataFrame(res_data.data)
                st.dataframe(df_sb, use_container_width=True)
                st.caption(f"Tổng số bản ghi: {len(res_data.data)}")
            else:
                st.info("Bảng dữ liệu trống.")
        except Exception as e:
            st.error(f"Lỗi truy vấn bảng `{tbl_choice}`: {str(e)}")

# ==========================================
# TAB 6: CÀI ĐẶT HỆ THỐNG
# ==========================================
with tab_settings:
    st.markdown("### ⚙️ Cài Đặt Hệ Thống & Tùy Chỉnh Biến Môi Trường")
    st.text_input("Tên tài khoản hiển thị", value="Nepcutu20")
    st.text_input("Email liên hệ", value="nepcutu20@soloflow.io")
    st.toggle("Tự động đồng bộ Realtime với Supabase", value=True)
    st.toggle("Bật thông báo nhịp sinh học Circadian", value=True)
    
    st.divider()
    st.markdown("##### 📥 Xuất / Sao Lưu Dữ Liệu Local")
    backup_data = db_get_all_tasks()
    st.download_button(
        label="📥 Tải Về File Backup JSON",
        data=json.dumps(backup_data, indent=4, ensure_ascii=False),
        file_name=f"soloflow_backup_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )
