import streamlit as st
import time
import json

# ==========================================
# 1. CẤU HÌNH TRANG & THEME
# ==========================================
st.set_page_config(
    page_title="SoloFlow OS",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS giao diện Deep Obsidian & VIP Cards giống ảnh 100%
st.markdown("""
<style>
    /* Nền tổng thể */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Custom Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* User Profile Card ở Sidebar */
    .user-profile-card {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .user-badge {
        background: #2563eb;
        color: white;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    
    /* VIP Pricing Cards Styling */
    .vip-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 24px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.2s, border-color 0.2s;
    }
    .vip-card:hover {
        border-color: #58a6ff;
        transform: translateY(-2px);
    }
    .vip-card-featured {
        background: linear-gradient(180deg, #1c2333 0%, #0d1117 100%);
        border: 2px solid #3b82f6;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.2);
    }
    .vip-price {
        font-size: 1.8rem;
        font-weight: 800;
        color: #ffffff;
        margin: 15px 0;
    }
    .vip-feature-list {
        list-style: none;
        padding: 0;
        margin: 15px 0;
    }
    .vip-feature-list li {
        margin-bottom: 10px;
        color: #8b949e;
        font-size: 0.9rem;
    }
    .vip-feature-list li::before {
        content: "• ";
        color: #3b82f6;
        font-weight: bold;
    }
    
    /* Tiêu đề SoloFlow Plus VIP */
    .vip-header {
        text-align: center;
        margin-bottom: 30px;
    }
    .vip-title {
        font-size: 2.2rem;
        font-weight: 900;
        color: #ffffff;
    }
    .vip-subtitle {
        color: #8b949e;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Khởi tạo Session State cho trạng thái tài khoản
if 'user_plan' not in st.session_state:
    st.session_state['user_plan'] = 'Basic'  # Basic, Premium, Lifetime

# ==========================================
# 2. SIDEBAR - USER PROFILE & AI ENGINE
# ==========================================
with st.sidebar:
    st.title("🚀 SoloFlow OS")
    
    # User Profile Box
    plan_display = f"<span class='user-badge'>{st.session_state['user_plan']}</span>" if st.session_state['user_plan'] != 'Basic' else "<span class='user-badge' style='background:#4b5563;'>Basic</span>"
    st.markdown(f"""
    <div class="user-profile-card">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="font-size: 2rem;">👤</div>
            <div>
                <strong style="color: white; font-size: 1.1rem;">Nepcutu20</strong> {plan_display}<br>
                <span style="color: #6e7681; font-size: 0.85rem;">@nepcutu20</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🏋️ Trình độ rèn luyện")
    st.caption("Cấp độ hiện tại: Level 2 (Flow Explorer)")
    st.progress(180 / 400)
    st.caption("Tiến trình cấp độ: 180 / 400 XP")
    
    st.divider()
    
    st.subheader("🤖 Cấu hình AI Engine")
    ai_model = st.selectbox("Mô hình AI active", ["SoloMind-v2 Fast", "SoloMind Pro (Bản Plus)", "GPT-4o Integration"])
    temp = st.slider("Độ sáng tạo AI", 0.0, 1.0, 0.7)

# ==========================================
# 3. THANH ĐIỀU HƯỚNG TABS
# ==========================================
tab_dashboard, tab_tasks, tab_ai, tab_settings, tab_plus, tab_backup = st.tabs([
    "📊 Dashboard", 
    "📋 Nhiệm vụ", 
    "🧠 SoloMind AI", 
    "⚙️ Hồ Sơ & Cài Đặt", 
    "💎 SoloFlow PLUS VIP", 
    "💾 Sao Lưu & Lưu Trữ"
])

# ==========================================
# TAB 1: DASHBOARD
# ==========================================
with tab_dashboard:
    st.header("Tổng quan năng suất")
    col1, col2, col3 = st.columns(3)
    col1.metric("Nhiệm vụ hoàn thành", "12/15", "+2 hôm nay")
    col2.metric("Thời gian Flow State", "4.5 giờ", "85% mục tiêu")
    col3.metric("Gói hiện tại", st.session_state['user_plan'])
    
    st.info("💡 Mẹo: Sử dụng tab 'Nhiệm vụ' để rã các công việc phức tạp thành checklist chi tiết.")

# ==========================================
# TAB 2: TÍNH NĂNG RÃ CÔNG VIỆC (TASK DECOMPOSITION)
# ==========================================
with tab_tasks:
    st.header("📋 Công cụ Rã Công Việc AI")
    st.write("Nhập mục tiêu hoặc dự án lớn của bạn, AI sẽ tự động phân tách thành các bước nhỏ dễ thực hiện.")
    
    main_task = st.text_input("Nhập tên công việc lớn cần rã:", placeholder="Ví dụ: Lập kế hoạch ra mắt phần mềm SaaS trong 30 ngày")
    detail_level = st.select_slider("Mức độ chi tiết:", options=["Cơ bản (3-5 bước)", "Chi tiết (5-8 bước)", "Sâu sắc (8-12 bước)"])
    
    if st.button("🚀 AI Rã Công Việc", type="primary"):
        if not main_task:
            st.warning("Vui lòng nhập nội dung công việc!")
        else:
            with st.spinner("SoloMind AI đang phân tích và rã nhỏ công việc..."):
                time.sleep(1.5) # Giả lập gian xử lý AI
                
                st.success("Đã rã công việc thành công!")
                
                # Kết quả mẫu được phân rã
                subtasks = [
                    {"step": "Bước 1", "title": "Nghiên cứu thị trường & đối thủ", "time": "2 giờ", "priority": "Cao"},
                    {"step": "Bước 2", "title": "Xác định tính năng cốt lõi (MVP)", "time": "1.5 giờ", "priority": "Cao"},
                    {"step": "Bước 3", "title": "Thiết kế UI/UX Wireframe", "time": "4 giờ", "priority": "Trung bình"},
                    {"step": "Bước 4", "title": "Lập trình Backend & Database", "time": "8 giờ", "priority": "Cao"},
                    {"step": "Bước 5", "title": "Tích hợp cổng thanh toán VietQR", "time": "3 giờ", "priority": "Trung bình"},
                    {"step": "Bước 6", "title": "Kiểm thử (Testing) & Sửa lỗi", "time": "3 giờ", "priority": "Thấp"},
                ]
                
                st.subheader(f"📌 Kế hoạch chi tiết cho: {main_task}")
                for task in subtasks:
                    with st.expander(f"{task['step']}: {task['title']}"):
                        st.write(f"- **Thời gian ước tính:** {task['time']}")
                        st.write(f"- **Độ ưu tiên:** {task['priority']}")
                        st.checkbox("Đánh dấu đã hoàn thành", key=task['step'])

# ==========================================
# TAB 3: SOLOMIND AI
# ==========================================
with tab_ai:
    st.header("🧠 Trợ lý SoloMind AI")
    if st.session_state['user_plan'] == 'Basic':
        st.warning("⚡ Bạn đang dùng bản Basic. Nâng cấp lên bản PLUS để không giới hạn token AI.")
    
    chat_input = st.text_input("Hỏi SoloMind AI bất kỳ điều gì về tiến độ làm việc...")
    if chat_input:
        st.write(f"🤖 **SoloMind AI:** Tôi đã ghi nhận yêu cầu: *'{chat_input}'*. Hãy tập trung hoàn thành các bước trong tab Nhiệm vụ!")

# ==========================================
# TAB 4: HỒ SƠ & CÀI ĐẶT
# ==========================================
with tab_settings:
    st.header("⚙️ Cài đặt hệ thống")
    st.text_input("Tên hiển thị", value="Nepcutu20")
    st.text_input("Email nhận thông báo", value="nepcutu20@soloflow.io")
    st.toggle("Bật thông báo nhịp sinh học Circadian", value=True)

# ==========================================
# TAB 5: SOLOFLOW PLUS VIP (GIAO DIỆN GIỐNG HÌNH ÁNH 100%)
# ==========================================
with tab_plus:
    st.markdown("""
    <div class="vip-header">
        <div class="vip-title">💎 SoloFlow PLUS - Sức Mạnh Vô Song</div>
        <div class="vip-subtitle">Xóa bỏ mọi giới hạn hoạt động. Nâng tầm tư duy năng suất cùng công nghệ AI đặc quyền đỉnh cao.</div>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    # CARD 1: Basic Plan
    with c1:
        st.markdown("""
        <div class="vip-card">
            <div>
                <h3>⏳ Basic Plan</h3>
                <div class="vip-price">Miễn phí</div>
                <ul class="vip-feature-list">
                    <li>Rã công việc tối thiểu</li>
                    <li>Hạ tầng FlowViewer cơ bản</li>
                    <li>Trình tư vấn AI bị giới hạn</li>
                    <li>Giao diện Deep Obsidian mặc định</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button("Đã kích hoạt mặc định", disabled=True, key="btn_basic", use_container_width=True)

    # CARD 2: Monthly Premium (Nổi bật)
    with c2:
        st.markdown("""
        <div class="vip-card vip-card-featured">
            <div>
                <span style="background: #f59e0b; color: black; font-weight: bold; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;">POPULAR</span>
                <h3 style="margin-top: 5px;">🌟 Monthly Premium</h3>
                <div class="vip-price">79.000đ<span style="font-size:1rem; font-weight:normal;">/tháng</span></div>
                <ul class="vip-feature-list">
                    <li>Rã công việc siêu tốc không giới hạn</li>
                    <li>Mở khóa toàn bộ Cosmic Theme</li>
                    <li>Điều độ nhịp sinh học Circadian</li>
                    <li>Trình hạ âm Âm thanh 3D Binaural</li>
                    <li>Bản đồ tư duy AI Mind Map Pro</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚡ Đăng ký ngay (79k)", type="primary", key="btn_monthly", use_container_width=True):
            st.session_state['pay_type'] = "Monthly Premium"
            st.session_state['pay_amount'] = 79000

    # CARD 3: Cosmic VIP Lifetime
    with c3:
        st.markdown("""
        <div class="vip-card">
            <div>
                <h3>🌌 Cosmic VIP Lifetime</h3>
                <div class="vip-price">399.000đ<span style="font-size:1rem; font-weight:normal;">/vĩnh viễn</span></div>
                <ul class="vip-feature-list">
                    <li>Sở hữu vĩnh viễn toàn bộ tính năng</li>
                    <li>Miễn phí cập nhật tất cả phiên bản tiếp theo</li>
                    <li>Nhận biểu tượng huy hiệu VIP đặc biệt</li>
                    <li>Ưu tiên xử lý hệ thống AI tốc độ cao</li>
                    <li>Hỗ trợ kỹ thuật 24/7 từ đội ngũ phát triển</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💎 Mua gói Lifetime (399k)", key="btn_lifetime", use_container_width=True):
            st.session_state['pay_type'] = "Cosmic VIP Lifetime"
            st.session_state['pay_amount'] = 399000

    # HỘP THOẠI THANH TOÁN VIETQR KHI KHÁCH HÀNG BẤM MUA
    if 'pay_type' in st.session_state:
        st.divider()
        st.subheader(f"💳 Cổng thanh toán VietQR - {st.session_state['pay_type']}")
        
        col_qr, col_info = st.columns([1, 2])
        
        # Cấu hình tài khoản nhận tiền của bạn tại đây
        bank_id = "MB" # Ngân hàng MBBank (hoặc ICB, VCB, ACB...)
        account_no = "0333333333" # Điền STK ngân hàng của bạn vào đây
        account_name = "SOLOFLOW OS VIP"
        amount = st.session_state['pay_amount']
        add_info = f"SOLOFLOW {st.session_state['pay_type'].replace(' ', '')}"
        
        # Tạo URL VietQR chuẩn hóa
        vietqr_url = f"https://img.vietqr.io/image/{bank_id}-{account_no}-compact2.png?amount={amount}&addInfo={add_info}&accountName={account_name}"
        
        with col_qr:
            st.image(vietqr_url, caption="Quét mã QR qua app ngân hàng để kích hoạt tự động", width=250)
            
        with col_info:
            st.write(f"- **Số tiền:** `{amount:,} VNĐ`")
            st.write(f"- **Nội dung chuyển khoản:** `{add_info}`")
            st.write(f"- **Ngân hàng:** `{bank_id}` - STK: `{account_no}`")
            st.write(f"- **Chủ tài khoản:** `{account_name}`")
            
            if st.button("✅ Tôi đã chuyển khoản thành công"):
                st.session_state['user_plan'] = st.session_state['pay_type']
                del st.session_state['pay_type']
                st.success("Xác nhận thanh toán thành công! Tài khoản của bạn đã được nâng cấp lên bản PLUS VIP.")
                time.sleep(1)
                st.rerun()

# ==========================================
# TAB 6: SAO LƯU & LƯU TRỮ
# ==========================================
with tab_backup:
    st.header("💾 Sao lưu & Lưu trữ dữ liệu")
    st.write("Xuất toàn bộ cấu hình công việc và lịch sử rã task ra file JSON.")
    
    sample_data = {"user": "Nepcutu20", "level": 2, "xp": 180, "plan": st.session_state['user_plan']}
    st.download_button(
        label="📥 Tải về dữ liệu (.json)",
        data=json.dumps(sample_data, indent=4),
        file_name="soloflow_backup.json",
        mime="application/json"
    )
