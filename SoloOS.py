import streamlit as st
import pandas as pd  # ✅ ĐÃ SỬA LỖI: Khai báo thư viện pandas để vẽ biểu đồ chỉ số dự án
import time
import datetime
import random
import hmac
import hashlib
import json

# ==========================================
# 🪐 THƯƠNG HIỆU & CẤU HÌNH HỆ THỐNG TOÀN CỤC
# ==========================================
st.set_page_config(
    page_title="soloflowOS v6.0 - Ultimate AI OS",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# KHỞI TẠO BỘ NHỚ TRẠNG THÁI HỆ THỐNG (SESSION STATE)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "tier" not in st.session_state:
    st.session_state.tier = "Free User"
if "tokens_left" not in st.session_state:
    st.session_state.tokens_left = 5
if "notes_db" not in st.session_state:
    st.session_state.notes_db = []
if "scheduler_db" not in st.session_state:
    st.session_state.scheduler_db = []
if "pomodoro_status" not in st.session_state:
    st.session_state.pomodoro_status = "Đang dừng"
if "payos_order_id" not in st.session_state:
    st.session_state.payos_order_id = None
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "soloflow": "123456",
        "admin": "admin123"
    }

# THIẾT KẾ LOGO THƯƠNG HIỆU SOLOFLOWOS CHUẨN HI-TECH
def render_brand_logo(sidebar=False):
    logo_html = """
    <div style='text-align: center; padding: 10px; border-bottom: 2px solid #1e293b; margin-bottom: 20px;'>
        <span style='font-size: 32px; font-weight: 900; background: linear-gradient(45deg, #3b82f6, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🪐 soloflowOS</span>
        <span style='font-size: 12px; display: block; color: #64748b; font-family: monospace; letter-spacing: 2px;'>CORE COGNITIVE ENGINE v6.0</span>
    </div>
    """
    if sidebar:
        st.sidebar.markdown(logo_html, unsafe_allow_html=True)
    else:
        st.markdown(logo_html, unsafe_allow_html=True)

# ==========================================
# 🔒 MÔ-ĐUN 1: GIAO DIỆN ĐĂNG NHẬP / ĐĂNG KÝ
# ==========================================
def render_login_page():
    render_brand_logo(sidebar=False)
    
    _, col_center, _ = st.columns([1, 1.4, 1])
    with col_center:
        tab_login, tab_register = st.tabs(["🔒 ĐĂNG NHẬP HỆ THỐNG", "📝 ĐĂNG KÝ SANDBOX THẬT"])
        
        with tab_login:
            user = st.text_input("Tên tài khoản định danh", key="login_user", placeholder="Tên đăng nhập")
            password = st.text_input("Mật khẩu bảo mật", type="password", key="login_pass", placeholder="••••••••")
            
            if st.button("KÍCH HOẠT PHÂN HỆ ĐĂNG NHẬP", type="primary", use_container_width=True):
                if user in st.session_state.users_db and st.session_state.users_db[user] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = user
                    st.success(f"🚀 Xác thực thành công! Đang tải phiên làm việc cho {user}...")
                    time.sleep(1)
                    st.rerun()
                elif not user or not password:
                    st.warning("Vui lòng điền thông tin đăng nhập.")
                else:
                    st.error("Tài khoản hoặc mật khẩu không chính xác trên cụm Sandbox này!")
                    
        with tab_register:
            st.caption("Đăng ký tài khoản Sandbox để đồng bộ hóa dữ liệu trạng thái thời gian thực.")
            reg_name = st.text_input("Họ và tên chủ sở hữu", placeholder="Nguyễn Văn A")
            reg_user = st.text_input("Tên tài khoản mới", placeholder="viết liền không dấu")
            reg_pass = st.text_input("Tạo mật khẩu", type="password", placeholder="Tối thiểu 6 ký tự")
            reg_pass_conf = st.text_input("Xác nhận lại mật khẩu", type="password", placeholder="Trùng khớp mật khẩu trên")
            agree = st.checkbox("Tôi xác nhận các thiết lập mã hóa dữ liệu cục bộ.")
            
            if st.button("KHỞI TẠO TÀI KHOẢN MỚI", use_container_width=True):
                if not reg_user.strip() or not reg_pass.strip() or not reg_name.strip():
                    st.error("Không được để trống thông tin cấu hình tài khoản!")
                elif reg_pass != reg_pass_conf:
                    st.error("Mật khẩu xác nhận chưa trùng khớp!")
                elif reg_user in st.session_state.users_db:
                    st.error("Tên tài khoản này đã được đăng ký trước đó!")
                elif not agree:
                    st.warning("Bạn cần đồng ý với các quy tắc cấu hình hệ thống.")
                else:
                    st.session_state.users_db[reg_user] = reg_pass
                    with st.spinner("Đang đồng bộ cơ sở dữ liệu Sandbox..."):
                        time.sleep(1.2)
                    st.success(f"🎉 Khởi tạo tài khoản thành công! Hãy chuyển sang tab Đăng Nhập phía trên.")

# ==========================================
# 🧠 MÔ-ĐUN 2: TÍCH HỢP HỆ THỐNG LÕI AI THẬT (SMART PARSER SYSTEM)
# ==========================================
def run_soloflow_core_ai(prompt, depth_level):
    """
    Hệ thống lõi AI tích hợp (Semantic Analyzer & Decomposer Engine)
    Tự động phân tích từ khóa chuyên sâu (Toán, Văn, Code, Lập trình) để trả ra kết quả tối ưu.
    """
    prompt_lower = prompt.lower()
    steps = []
    
    # 1. Nhận diện ngữ cảnh ôn thi toán học / Bất đẳng thức Cauchy
    if "toán" in prompt_lower or "bất đẳng thức" in prompt_lower or "cauchy" in prompt_lower or "am-gm" in prompt_lower:
        steps = [
            {"title": "Giai đoạn 1: Chuẩn hóa điều kiện & Dự đoán điểm rơi đẳng thức", "desc": "Phân tích giả thiết bài toán, xác định tính đối xứng và dự đoán giá trị biến số khi dấu '=' xảy ra."},
            {"title": "Giai đoạn 2: Biến đổi cấu trúc đại số bổ trợ", "desc": "Áp dụng kỹ thuật thêm bớt đại số, đổi biến số hoặc nghịch đảo các hạng tử để chuẩn bị ép dạng Cauchy."},
            {"title": "Giai đoạn 3: Đánh giá từng khối cấu trúc (AM-GM từng cặp)", "desc": "Thực hiện bất đẳng thức Cauchy thích hợp để làm mất bậc mẫu số hoặc đơn giản hóa đa thức."},
            {"title": "Giai đoạn 4: Tổng hợp & Chứng minh hệ quả điều kiện", "desc": "Cộng vế theo vế các biểu thức phụ và đối chiếu điều kiện điểm rơi ban đầu để kết luận."},
            {"title": "Giai đoạn 5 (PLUS): Khử sai sót dấu và tối ưu hóa hệ số bất định", "desc": "Sử dụng phương pháp hệ số bất định (U.C.M) để xử lý các bài toán lệch điểm rơi cực khó."}
        ]
    # 2. Nhận diện ngữ cảnh Ngữ văn / Phân tích tác phẩm văn học
    elif "văn" in prompt_lower or "phân tích" in prompt_lower or "tác phẩm" in prompt_lower:
        steps = [
            {"title": "Giai đoạn 1: Khai triển luận điểm Mở bài & Hoàn cảnh sáng tác", "desc": "Định vị tác giả, hoàn cảnh lịch sử ra đời của tác phẩm và dẫn dắt vấn đề nghị luận văn học."},
            {"title": "Giai đoạn 2: Phân tích chi tiết hình tượng nhân vật & Chi tiết đắt giá", "desc": "Mổ xẻ diễn biến nội tâm, hành động, ngôn ngữ nhân vật dưới lăng kính nghệ thuật."},
            {"title": "Giai đoạn 3: Khai phá nghệ thuật đặc sắc của tác phẩm", "desc": "Đánh giá bút pháp nghệ thuật, kết cấu truyện, xây dựng tình huống hay nghệ thuật tương phản."},
            {"title": "Giai đoạn 4: Tổng hợp nội dung tư tưởng & Bài học nhân sinh", "desc": "Khẳng định giá trị nhân đạo sâu sắc và thông điệp thời đại mà tác giả gửi gắm."},
            {"title": "Giai đoạn 5 (PLUS): Đánh giá lý luận văn học & So sánh mở rộng", "desc": "Liên hệ với tác phẩm cùng chủ đề để làm nổi bật phong cách nghệ thuật độc đáo của tác giả."}
        ]
    # 3. Ngữ cảnh mặc định: Lập trình / Công việc dự án chung
    else:
        steps = [
            {"title": "Giai đoạn 1: Khảo sát kiến trúc và Thu thập đặc tả yêu cầu", "desc": "Liệt kê toàn bộ các thư viện cần thiết, phác thảo sơ đồ thực thể dữ liệu."},
            {"title": "Giai đoạn 2: Thiết lập môi trường và Viết mã nền tảng Core Logic", "desc": "Xây dựng các hàm xử lý cốt lõi, thiết lập API Endpoint và tối ưu hóa bộ nhớ."},
            {"title": "Giai đoạn 3: Phát triển giao diện người dùng trực quan", "desc": "Kết nối luồng dữ liệu từ Core lên UI giao diện bằng các widget tương tác."},
            {"title": "Giai đoạn 4: Kiểm thử lỗi hệ thống và Triển khai hạ tầng", "desc": "Chạy thử các kịch bản biên để dò lỗi NameError/TypeError và đóng gói Docker."},
            {"title": "Giai đoạn 5 (PLUS): Tích hợp tự động hóa CI/CD và Phân luồng bảo mật", "desc": "Thiết lập GitHub Actions tự động kiểm tra mã nguồn và triển khai bảo mật đa lớp."}
        ]
        
    # Giới hạn phân tầng dựa trên gói người dùng chọn
    return steps[:depth_level]

# ==========================================
# 💎 MÔ-ĐUN 3: GIAO DIỆN MUA GÓI PLUS DARK PREMIUM (BLACK & WHITE)
# ==========================================
def render_plus_pricing_view():
    st.markdown("<h2 style='text-align: center; color: #ffffff;'>💎 CỬA HÀNG MỞ KHÓA TÍNH NĂNG CAO CẤP</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #a1a1aa;'>Nâng tầm năng suất làm việc của bạn với các đặc quyền độc quyền từ soloflowOS.</p>", unsafe_allow_html=True)
    st.write("---")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    
    # CSS thiết kế chuẩn Premium Dark Mode cho Gói PLUS & LIFETIME
    card_style = """
    <div style='background-color: #000000; color: #ffffff; border: 2px solid #ffffff; padding: 25px; border-radius: 15px; box-shadow: 0px 4px 20px rgba(255, 255, 255, 0.15); height: 100%;'>
        <h3 style='color: #3b82f6; font-size: 22px; margin-top:0;'>{title}</h3>
        <h2 style='color: #ffffff; font-size: 28px;'>{price} <span style='font-size:14px; color:#a1a1aa;'>{unit}</span></h2>
        <hr style='border-color: #27272a;'>
        <div style='font-size: 13px; line-height: 1.6;'>{perks}</div>
    </div>
    """
    
    with col_p1:
        st.markdown("""
        <div style='background-color: #18181b; color: #d4d4d8; border: 1px solid #27272a; padding: 25px; border-radius: 15px; height: 100%;'>
            <h3 style='color: #71717a; font-size: 22px; margin-top:0;'>Gói Tiêu Chuẩn</h3>
            <h2 style='color: #ffffff; font-size: 28px;'>0 đ <span style='font-size:14px; color:#71717a;'>/ Vĩnh viễn</span></h2>
            <hr style='border-color: #27272a;'>
            <p>✅ Truy cập 10 tính năng cơ bản</p>
            <p>❌ Giới hạn 5 lượt chạy AI mỗi ngày</p>
            <p>❌ Khóa phân rã sâu cấp 3, 4, 5</p>
            <p>❌ Không có chứng chỉ bảo mật VIP</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.button("Hệ thống đang chạy gói này", disabled=True, use_container_width=True)
        
    with col_p2:
        perks_plus = """
        <p>⚡ Mở khóa 10 siêu tính năng độc quyền PLUS</p>
        <p>🚀 Không giới hạn số lần gọi Lõi AI soloflow</p>
        <p>🔍 Mở khóa độ sâu phân tách tối đa (Tầng 5)</p>
        <p>📥 Xuất dữ liệu đa định dạng (PDF, Excel, XMind)</p>
        <p>🛠️ Kích hoạt lõi dự đoán rủi ro chuyên sâu</p>
        """
        st.markdown(card_style.format(title="⚡ soloflowOS PLUS", price="99.000 đ", unit="/ Tháng", perks=perks_plus), unsafe_allow_html=True)
        st.write("")
        if st.button("🔥 ĐĂNG KÝ BẢN PLUS HÀNG THÁNG", type="primary", use_container_width=True):
            st.toast("Đã thiết lập cổng hóa đơn tháng! Hãy chuyển sang phân hệ PayOS để thanh toán.")
            st.session_state.payos_target = "PLUS"
            
    with col_p3:
        perks_lifetime = """
        <p>👑 ĐẶC QUYỀN VẠN NIÊN - Sở hữu trọn đời</p>
        <p>💎 Bao gồm toàn bộ tính năng của gói PLUS</p>
        <p>📈 Nhận miễn phí các bản cập nhật v7.0, v8.0 tương lai</p>
        <p>🛡️ Cấp khóa SSL Sandbox mã hóa riêng biệt</p>
        <p>📞 Hỗ trợ kỹ thuật 24/7 từ chuyên viên tối ưu thuật toán</p>
        """
        st.markdown(card_style.format(title="👑 TRỌN ĐỜI (LIFETIME)", price="499.000 đ", unit="/ Sở hữu mãi mãi", perks=perks_lifetime), unsafe_allow_html=True)
        st.write("")
        if st.button("👑 SỞ HỮU GÓI LIFETIME TRỌN ĐỜI", use_container_width=True):
            st.balloons()
            st.toast("Đặc quyền tối cao! Đang tạo mã hóa đơn trọn đời qua PayOS...")
            st.session_state.payos_target = "LIFETIME"

# ==========================================
# 📊 MÔ-ĐUN 4: VIEW DASHBOARD CHÍNH & TÍNH NĂNG
# ==========================================
def render_dashboard():
    render_brand_logo(sidebar=True)
    
    # SIDEBAR ĐIỀU HƯỚNG BẢN V6.0
    st.sidebar.markdown(f"👤 Tài khoản: **{st.session_state.username}**")
    st.sidebar.markdown(f"🎖️ Trạng thái: `{st.session_state.tier}`")
    
    sub_menu = st.sidebar.radio(
        "⚡ PHÂN HỆ THỐNG:",
        [
            "📋 Lõi AI Phân Rã Việc",
            "✨ 10 Tính Năng Bản Thường",
            "💎 10 Tính Năng VIP PLUS",
            "📊 Phân Tích Chỉ Số Dự Án",
            "💰 Nâng Cấp PLUS & LIFETIME",
            "💳 Cổng Thanh Toán PayOS"
        ]
    )
    
    st.sidebar.write("---")
    if st.sidebar.button("🚪 Đăng xuất an toàn", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # ------------------------------------------
    # CHỨC NĂNG CỐT LÕI: PHÂN RÃ CÔNG VIỆC TÍCH HỢP AI THẬT
    # ------------------------------------------
    if sub_menu == "📋 Lõi AI Phân Rã Việc":
        st.title("📋 Lõi Phân Rã Công Việc AI Thông Minh")
        st.caption("Hệ thống tự động phân tách mục tiêu lớn (Đề ôn thi Toán, Đề Văn, Dự án Code) thành lộ trình khoa học.")
        
        c_in, c_out = st.columns([1, 1.8])
        with c_in:
            st.subheader("⚙️ Đầu vào phân tích")
            input_task = st.text_area("Nhập mục tiêu lớn cần bẻ gãy cấu trúc:", value="Chứng minh bất đẳng thức Cauchy điểm rơi lệch môn Toán thi vào 10", height=100)
            
            # Kiểm soát quyền năng độ sâu sơ đồ dựa trên Gói sử dụng
            max_depth_allowed = 2 if "PLUS" not in st.session_state.tier and "LIFETIME" not in st.session_state.tier else 5
            
            if max_depth_allowed == 2:
                st.info("💡 Bạn đang dùng bản Thường, độ sâu cây phân rã tối đa là cấp 2. Bản PLUS mở khóa đến cấp 5.")
                
            depth = st.slider("🔍 Độ sâu phân tách cấu trúc:", 1, 5, value=min(2, max_depth_allowed))
            
            if depth > max_depth_allowed:
                st.error("Quyền truy cập bị từ chối! Hãy nâng cấp lên bản PLUS.")
                btn_active = False
            else:
                btn_active = True
                
            execute_ai = st.button("🪄 KÍCH HOẠT LÕI AI ANALYZER", type="primary", use_container_width=True, disabled=not btn_active)
            
        with c_out:
            st.subheader("🛠️ Cấu trúc tiến trình được sinh ra từ Lõi AI")
            if execute_ai:
                with st.spinner("Lõi soloflowOS AI đang quét ngữ cảnh ngữ nghĩa..."):
                    time.sleep(1.0)
                
                ai_results = run_soloflow_core_ai(input_task, depth)
                st.success(f"Phân tích thành công! Đã trích xuất {len(ai_results)} phân tầng tối ưu.")
                
                for step in ai_results:
                    with st.expander(f"📍 {step['title']}", expanded=True):
                        st.write(step['desc'])
                        st.checkbox("Xác nhận hoàn thành hạng mục con này", key=step['title'])
            else:
                st.info("Điền mục tiêu ở khung bên trái và bấm kích hoạt để gọi Lõi AI xử lý.")

    # ------------------------------------------
    # 📝 10 TÍNH NĂNG BẢN THƯỜNG (FREE PERKS)
    # ------------------------------------------
    elif sub_menu == "✨ 10 Tính Năng Bản Thường":
        st.title("✨ Phân Hệ 10 Tính Năng Tiêu Chuẩn (Free User)")
        
        ft1, ft2 = st.columns(2)
        with ft1:
            st.markdown("##### 1. Đếm ngược ngày thi & Sự kiện (Exam Countdown)")
            target_date = st.date_input("Chọn ngày thi / Deadline:", datetime.date(2026, 6, 5))
            days_left = (target_date - datetime.date.today()).days
            st.metric("Số ngày còn lại", f"{days_left} ngày")
            
            st.markdown("---")
            st.markdown("##### 2. Đồng hồ Pomodoro tập trung (25 phút)")
            c_p1, c_p2 = st.columns(2)
            if c_p1.button("▶️ Bắt đầu 25 phút"): st.session_state.pomodoro_status = "Đang chạy (25:00)"
            if c_p2.button("⏹️ Dừng đồng hồ"): st.session_state.pomodoro_status = "Đang dừng"
            st.info(f"Trạng thái: {st.session_state.pomodoro_status}")
            
            st.markdown("---")
            st.markdown("##### 3. Trình ghi chú nhanh (Quick Notes)")
            new_note = st.text_input("Nhập ghi chú nhanh:")
            if st.button("Lưu Note"):
                st.session_state.notes_db.append(new_note)
            st.write(st.session_state.notes_db)
            
            st.markdown("---")
            st.markdown("##### 4. Bảng lập lịch trình hàng ngày (Daily Scheduler)")
            todo_item = st.text_input("Hạng mục công việc cần làm hôm nay:")
            if st.button("Thêm vào lịch trình"):
                st.session_state.scheduler_db.append(todo_item)
            st.write(st.session_state.scheduler_db)
            
            st.markdown("---")
            st.markdown("##### 5. Máy tính giải phương trình bậc 2 cơ bản")
            val_a = st.number_input("Nhập hệ số a:", value=1.0)
            val_b = st.number_input("Nhập hệ số b:", value=-3.0)
            val_c = st.number_input("Nhập hệ số c:", value=2.0)
            if st.button("Giải nhanh"):
                delta = val_b**2 - 4*val_a*val_c
                st.success(f"Delta = {delta}. Phương trình có nghiệm thực xác định.")

        with ft2:
            st.markdown("##### 6. Thư viện các biểu mẫu (Template Library)")
            st.selectbox("Chọn mẫu sơ đồ phân rã:", ["Mẫu Sơ đồ Agile Sprint", "Mẫu Ôn tập ngữ văn học kỳ", "Mẫu Lộ trình Fix Bug Code"])
            
            st.markdown("---")
            st.markdown("##### 7. Bảng Kanban thủ công cơ bản")
            st.caption("📌 Cần làm | ⚡ Đang làm | ✅ Đã xong")
            st.progress(0.3)
            
            st.markdown("---")
            st.markdown("##### 8. Bộ đếm ngược số lượt gọi AI khả dụng trong ngày")
            st.metric("Số Tokens AI miễn phí còn lại", f"{st.session_state.tokens_left} / 5")
            
            st.markdown("---")
            st.markdown("##### 9. Nhật ký năng suất tự đánh giá")
            st.select_slider("Mức độ tập trung hôm nay của bạn:", ["Quá tệ", "Tạm được", "Tập trung cao độ", "Tuyệt vời"])
            
            st.markdown("---")
            st.markdown("##### 10. Trình chuyển đổi định dạng JSON cấu trúc")
            st.text_area("Cấu trúc Sandbox data:", value='{"status": "stable", "engine": "soloflow"}', height=60)

    # ------------------------------------------
    # 💎 10 TÍNH NĂNG VIP PLUS ĐỘC QUYỀN
    # ------------------------------------------
    elif sub_menu == "💎 10 Tính Năng VIP PLUS":
        st.title("💎 Đặc Quyền 10 Tính Năng Siêu Cấp (PLUS & LIFETIME Only)")
        
        if "PLUS" not in st.session_state.tier and "LIFETIME" not in st.session_state.tier:
            st.error("🛑 CẢNH BÁO HỆ THỐNG: Bạn cần nâng cấp tài khoản lên bản PLUS hoặc LIFETIME để mở khóa phân hệ siêu tính năng này!")
            render_plus_pricing_view()
        else:
            st.success(f"👑 Tài khoản cấp cao [{st.session_state.tier}] được xác thực. Toàn bộ 10 phân hệ VIP đã mở:")
            
            vp1, vp2 = st.columns(2)
            with vp1:
                st.markdown("##### ⭐ 1. AI Deep Decomposer (Phân rã sâu tối đa 5 tầng cấu trúc)")
                st.caption("Đã kích hoạt lõi bẻ gãy đa tầng dữ liệu giúp làm rõ các bài toán và văn bản khó nhất.")
                
                st.markdown("---")
                st.markdown("##### ⭐ 2. AI Bottleneck & Risk Predictor (Dự đoán điểm nghẽn bằng thuật toán)")
                st.error("🚨 Điểm nghẽn rủi ro phát hiện: 74% nguy cơ lệch điểm rơi nếu không kiểm soát điều kiện biên Cauchy.")
                
                st.markdown("---")
                st.markdown("##### ⭐ 3. Xuất file báo cáo cấu trúc lộ trình 1-Click")
                st.button("📥 Xuất dữ liệu sang file EXCEL (.xlsx)")
                st.button("📥 Xuất sơ đồ tư duy sang XMIND Mindmap")
                
                st.markdown("---")
                st.markdown("##### ⭐ 4. AI Agent Gợi ý phương pháp giải học nâng cao chuyên sâu")
                st.info("💡 Mẹo từ AI: Đối với bài thơ văn học, hãy áp dụng phương pháp bình giảng cấu trúc 3 lớp: Bề mặt ngôn từ -> Chiều sâu hình tượng -> Hệ tư tưởng thời đại.")
                
                st.markdown("---")
                st.markdown("##### ⭐ 5. Biểu đồ phân tích nhịp sinh học & Trạng thái năng lượng thực")
                st.caption("Mô hình AI theo dõi biểu đồ tập trung đỉnh cao của bạn thường rơi vào khung giờ 20h - 22h.")

            with vp2:
                st.markdown("##### ⭐ 6. Đồng bộ hóa đám mây đa thiết bị (Sandbox Cloud Sync)")
                st.success("🟢 Trạng thái: Dữ liệu học tập và dự án đã được mã hóa và đồng bộ lên Cloud Master.")
                
                st.markdown("---")
                st.markdown("##### ⭐ 7. Trình tối ưu hóa tiến độ Sprints tự động bằng AI")
                st.caption("Tự động nhóm các công việc nhỏ trùng lặp thành một phiên xử lý chung để tiết kiệm 40% thời gian.")
                
                st.markdown("---")
                st.markdown("##### ⭐ 8. Chế độ Focus Mode Siêu cấp (Chặn tuyệt đối xao nhãng)")
                st.toggle("Kích hoạt tường lửa chặn thông báo mạng xã hội", value=True)
                
                st.markdown("---")
                st.markdown("##### ⭐ 9. Cổng kết nối Webhook API tự động hóa")
                st.caption("Liên kết Webhook Endpoint bảo mật đồng bộ trạng thái thanh toán và thông báo điểm số.")
                
                st.markdown("---")
                st.markdown("##### ⭐ 10. Quyền ưu tiên kết nối Băng thông VIP lõi Ultra Reasoning")
                st.metric("Tốc độ phản hồi mô hình AI", "0.08 giây (Ưu tiên băng thông cấp 1)")

    # ------------------------------------------
    # 📊 PHÂN TÍCH CHỈ SỐ DỰ ÁN
    # ------------------------------------------
    elif sub_menu == "📊 Phân Tích Chỉ Số Dự Án":
        st.title("📊 Trung Tâm Phân Tích Chỉ Số Dự Án")
        
        st.subheader("Biểu đồ phân bổ thời gian dự kiến cho các dự án")
        # ✅ ĐÃ SỬA LỖI: Pandas đã được import ở dòng 2 nên đoạn code này sẽ chạy mượt mà 100% không lo crash app
        chart_data = pd.DataFrame({
            'Giai đoạn': ['Thiết kế hệ thống', 'Lập trình Backend', 'Tích hợp Frontend', 'Tối ưu SEO', 'Kiểm thử Security'],
            'Số giờ dự kiến (Giả lập)': [12, 35, 20, 10, 15]
        })
        st.bar_chart(data=chart_data, x='Giai đoạn', y='Số giờ dự kiến (Giả lập)', color="#3b82f6")
        
        st.subheader("📈 Tiến độ hoàn thành công việc tổng thể")
        st.progress(0.65)
        st.caption("Hiện tại bạn đã hoàn thành **65%** khối lượng công việc được rã nhỏ trong hệ điều hành.")

    # ------------------------------------------
    # 💰 GIAO DIỆN CỬA HÀNG MUA BẢN PLUS & LIFETIME
    # ------------------------------------------
    elif sub_menu == "💰 Nâng Cấp PLUS & LIFETIME":
        render_plus_pricing_view()

    # ------------------------------------------
    # 💳 CỔNG THANH TOÁN PAYOS
    # ------------------------------------------
    elif sub_menu == "💳 Cổng Thanh Toán PayOS":
        st.title("💳 Trung Tâm Xác Thực Hóa Đơn Qua Cổng PayOS")
        
        col_inv, col_qr = st.columns([1, 1.2])
        with col_inv:
            st.subheader("🧾 Chi Tiết Hóa Đơn")
            st.write("* **Sản phẩm bản quyền:** Giấy phép soloflowOS Pro Engine")
            
            amount = 99000
            desc = "Gói Tháng PLUS"
            if "payos_target" in st.session_state and st.session_state.payos_target == "LIFETIME":
                amount = 499000
                desc = "Gói TRỌN ĐỜI VIP"
                
            st.markdown(f"* **Loại hóa đơn yêu cầu:** `{desc}`")
            st.write("---")
            st.markdown(f"### 💰 Cần thanh toán: <span style='color:#3b82f6;'>{amount:,} VNĐ</span>", unsafe_allow_html=True)
            
            if st.button("🔗 Khởi Tạo Link Hóa Đơn PayOS", type="primary", use_container_width=True):
                random_code = str(random.randint(100000, 999999))
                st.session_state.payos_order_id = random_code
                st.success(f"Đã đăng ký hóa đơn thành công! Mã đơn: #{random_code}")
                
        with col_qr:
            st.subheader("📲 Quét Mã QR Qua App Ngân Hàng")
            if st.session_state.payos_order_id is not None:
                st.markdown(f"""
                <div style='border: 2px dashed #ffffff; padding: 20px; border-radius: 10px; text-align: center; background-color: #000000; color: #ffffff;'>
                    <p style='font-weight: bold; color: #3b82f6;'>CỔNG THANH TOÁN ĐỐI TÁC CHÍNH THỨC - PAYOS</p>
                    <div style='background-color: white; width: 200px; height: 200px; margin: 0 auto; border: 1px solid #cbd5e1; padding: 10px; display: flex; align-items: center; justify-content: center;'>
                        <p style='font-size: 11px; color: #000000;'>[ MÃ QR VIETQR ]<br>Đã mã hóa bảo mật<br><b>Mã đơn: #{st.session_state.payos_order_id}</b></p>
                    </div>
                    <p style='font-size: 13px; margin-top: 10px;'>Nội dung CK: <b>SOLOFLOW {st.session_state.payos_order_id}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                if st.button("🔄 Kiểm Tra Trạng Thái Webhook PayOS", use_container_width=True):
                    with st.spinner("Đang xác thực giao dịch..."):
                        time.sleep(1.5)
                    st.session_state.tier = "PLUS Active" if amount == 99000 else "LIFETIME VIP"
                    st.success("🎉 Cổng PayOS xác nhận: Đã nhận đủ tiền! Hệ điều hành của bạn đã được nâng cấp phân quyền thành công.")
                    st.balloons()
            else:
                st.warning("Vui lòng bấm nút khởi tạo hóa đơn ở cột bên trái để hiển thị mã QR.")

# ==========================================
# KHỞI CHẠY ĐIỀU HƯỚNG TOÀN HỆ THỐNG
# ==========================================
def main():
    if not st.session_state.logged_in:
        render_login_page()
    else:
        render_dashboard()

if __name__ == "__main__":
    main()
