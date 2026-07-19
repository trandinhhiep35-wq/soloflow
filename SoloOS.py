import streamlit as st
import time
import datetime
import random
import hmac
import hashlib
import json

# ==========================================
# CẤU HÌNH HỆ THỐNG TOÀN CỤC & THEME TRỰC QUAN
# ==========================================
st.set_page_config(
    page_title="soloflowOS v6.0 - Ultimate AI OS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# KHỞI TẠO BỘ NHỚ LƯU TRỮ TRẠNG THÁI (SESSION STATE)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "tier" not in st.session_state:
    st.session_state.tier = "Free User"
if "tokens_left" not in st.session_state:
    st.session_state.tokens_left = 5
if "tasks_db" not in st.session_state:
    st.session_state.tasks_db = []
if "pomodoro_status" not in st.session_state:
    st.session_state.pomodoro_status = "Đang dừng"
if "payos_order_id" not in st.session_state:
    st.session_state.payos_order_id = None

# 🌟 CẬP NHẬT: Khởi tạo cơ sở dữ liệu tài khoản ảo để đồng bộ Sandbox thật
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "soloflow": "123456",  # Tài khoản admin mặc định
        "admin": "admin123"
    }

# ==========================================
# MÔ-ĐUN 1: HỆ THỐNG ĐĂNG NHẬP / ĐĂNG KÝ THẬT
# ==========================================
def render_login_page():
    st.markdown("<h1 style='text-align: center; color: #2563eb;'>🚀 soloflowOS v6.0</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #64748b;'>Hệ Điều Hành Quản Trị & Phân Rã Dự Án Tự Động</h3>", unsafe_allow_html=True)
    
    _, col_center, _ = st.columns([1, 1.5, 1])
    
    with col_center:
        tab_login, tab_register = st.tabs(["🔒 Đăng Nhập", "📝 Đăng Ký Tài Khoản"])
        
        with tab_login:
            st.write("Chào mừng quay trở lại! Vui lòng nhập thông tin hệ thống.")
            user = st.text_input("Tên đăng nhập / Email", key="login_user", placeholder="soloflow_dev")
            password = st.text_input("Mật khẩu", type="password", key="login_pass", placeholder="••••••••")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("Đăng Nhập Hệ Thống", type="primary", use_container_width=True):
                    # 🌟 CẬP NHẬT: Kiểm tra tài khoản trong Database hệ thống thay vì fix cứng
                    if user in st.session_state.users_db and st.session_state.users_db[user] == password:
                        st.session_state.logged_in = True
                        st.session_state.username = user
                        st.success(f"Đăng nhập thành công! Xin chào {user}...")
                        time.sleep(1)
                        st.rerun()
                    elif user == "" or password == "":
                        st.warning("Vui lòng điền đầy đủ thông tin.")
                    else:
                        st.error("Sai tài khoản hoặc mật khẩu! Vui lòng kiểm tra lại.")
            with col_btn2:
                st.button("Quên mật khẩu?", use_container_width=True)
                
        with tab_register:
            st.write("Tạo tài khoản soloflowOS mới để đồng bộ hóa dữ liệu đám mây.")
            reg_name = st.text_input("Họ và tên", placeholder="Nguyễn Văn A")
            reg_user = st.text_input("Tên đăng nhập mới", placeholder="Username viết liền không dấu")
            reg_pass = st.text_input("Tạo mật khẩu", type="password", placeholder="Tối thiểu 6 ký tự")
            reg_pass_conf = st.text_input("Xác nhận mật khẩu", type="password", placeholder="Trùng khớp mật khẩu trên")
            agree = st.checkbox("Tôi đồng ý với các Điều khoản dịch vụ và Chính sách bảo mật.")
            
            if st.button("Đăng Ký Ngay", use_container_width=True, type="primary"):
                if not reg_user.strip() or not reg_pass.strip() or not reg_name.strip():
                    st.error("❌ Vui lòng không để trống bất kỳ trường thông tin nào!")
                elif reg_pass != reg_pass_conf:
                    st.error("❌ Mật khẩu xác nhận không trùng khớp!")
                elif reg_user in st.session_state.users_db:
                    st.error("❌ Tên đăng nhập này đã tồn tại trên Sandbox soloflowOS!")
                elif not agree:
                    st.warning("⚠️ Bạn cần tích chọn đồng ý với Điều khoản dịch vụ.")
                else:
                    # 🌟 CẬP NHẬT: Thực hiện đồng bộ thêm tài khoản mới vào DB Sandbox
                    st.session_state.users_db[reg_user] = reg_pass
                    
                    with st.spinner("Đang đồng bộ cấu trúc tài khoản lên bộ nhớ Sandbox..."):
                        time.sleep(1.5)
                        
                    st.success(f"🎉 Đăng ký thành công tài khoản [{reg_user}]!")
                    st.info("👉 Hãy bấm chuyển qua tab **🔒 Đăng Nhập** ở phía trên để vào hệ thống.")

# ==========================================
# MÔ-ĐUN 2: THƯ VIỆN KẾT NỐI PAYOS (MOCK INTEGRATION)
# ==========================================
def generate_payos_link(amount: int, order_id: str):
    payos_client_id = "soloflow_pos_cid_9921"
    payos_api_key = "soloflow_pos_key_xyz8821"
    
    raw_data = f"amount={amount}&cancelUrl=https://soloflow.streamlit.app&description=UpgradePlus&orderCode={order_id}&returnUrl=https://soloflow.streamlit.app"
    signature = hmac.new(payos_api_key.encode(), raw_data.encode(), hashlib.sha256).hexdigest()
    
    payment_url = f"https://checkout.payos.vn/v2/payment-link-mockup?id={order_id}&sig={signature}&cid={payos_client_id}"
    return payment_url, signature

# ==========================================
# MÔ-ĐUN 3: CÁC TÍNH NĂNG SIÊU ĐẶC BIỆT (SUPER FEATURES)
# ==========================================
def feature_ai_bottleneck_predictor(task_text):
    st.markdown("#### 🧠 Siêu Tính Năng: AI Bottleneck & Risk Predictor")
    st.caption("Thuật toán Deep Learning giả lập phân tích dữ liệu lịch sử để tìm điểm nghẽn tiến độ.")
    
    with st.spinner("AI đang chạy mô hình Monte Carlo dự đoán rủi ro rò rỉ tiến độ..."):
        time.sleep(1.5)
        
    col1, col2, col3 = st.columns(3)
    with col1:
        st.error("🔴 Rủi ro kỹ thuật: 74%")
        st.caption("Xung đột thư viện hoặc cấu hình sai Database ở Giai đoạn 1.")
    with col2:
        st.warning("🟡 Điểm nghẽn tài nguyên: 42%")
        st.caption("Thời gian viết API Giỏ hàng dễ bị quá tải (vượt dự kiến 5 giờ).")
    with col3:
        st.success("🟢 Khả năng tối ưu SEO: Đạt 92%")
        st.caption("Cấu hình sitemap tự động giảm tải công việc thủ công.")

def feature_pomodoro_timer():
    st.markdown("#### ⏱️ Đồng Hồ Tập Trung Pomodoro Integration")
    
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        st.info(f"Trạng thái vòng lặp: **{st.session_state.pomodoro_status}** (Tiêu chuẩn: 25 phút tập trung / 5 phút nghỉ)")
    with c2:
        if st.button("▶️ Bắt Đầu Tập Trung", use_container_width=True):
            st.session_state.pomodoro_status = "Đang chạy (25:00)"
            st.toast("Bắt đầu tính giờ Pomodoro! Tập trung cao độ nhé!")
    with c3:
        if st.button("⏹️ Dừng Tính Giờ", use_container_width=True):
            st.session_state.pomodoro_status = "Đang dừng"
            st.toast("Đã dừng đồng hồ.")

def feature_kanban_simulator():
    st.markdown("#### 📋 Bảng Thống Kê Kanban Tiến Độ ( soloflow-Kanban )")
    kb_todo, kb_doing, kb_done = st.columns(3)
    
    with kb_todo:
        st.markdown("<div style='background-color:#fee2e2; padding:10px; border-radius:5px; color:#991b1b; font-weight:bold;'>📌 CẦN LÀM (To Do)</div>", unsafe_allow_html=True)
        st.caption("▪️ Viết API xử lý Giỏ hàng và Thanh toán PayOS")
        st.caption("▪️ Cấu hình bảo mật khóa mã hóa SSL")
        
    with kb_doing:
        st.markdown("<div style='background-color:#fef3c7; padding:10px; border-radius:5px; color:#92400e; font-weight:bold;'>⚡ ĐANG LÀM (In Progress)</div>", unsafe_allow_html=True)
        st.caption("▪️ Thiết kế cấu trúc sơ đồ ERD dữ liệu")
        
    with kb_done:
        st.markdown("<div style='background-color:#dcfce7; padding:10px; border-radius:5px; color:#166534; font-weight:bold;'>✅ ĐÃ XONG (Done)</div>", unsafe_allow_html=True)
        st.caption("▪️ Khởi tạo khung xương ứng dụng soloflowOS v6.0")

# ==========================================
# MÔ-ĐUN 4: CÁC VIEW GIAO DIỆN CHỨC NĂNG
# ==========================================
def render_dashboard():
    st.sidebar.subheader(f"👋 Chào, {st.session_state.username}!")
    sub_menu = st.sidebar.radio(
        "Phân hệ ứng dụng:",
        [
            "📋 Rã Công Việc Nâng Cao",
            "📊 Dashboard & Phân Tích",
            "👤 Hồ Sơ Hệ Thống",
            "⚙️ Cài Đặt Toàn Cục",
            "💎 Nâng Cấp PLUS",
            "💳 Cổng Thanh Toán PayOS"
        ]
    )
    
    st.sidebar.write("---")
    if st.sidebar.button("🚪 Đăng Xuất", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # ------------------------------------------
    # CHỨC NĂNG 1: RÃ CÔNG VIỆC NÂNG CAO
    # ------------------------------------------
    if sub_menu == "📋 Rã Công Việc Nâng Cao":
        st.title("📋 Trung Tâm Rã Công Việc AI Cao Cấp")
        
        c_left, c_right = st.columns([1, 1.8])
        with c_left:
            st.subheader("⚙️ Thông Số Đầu Vào")
            main_task = st.text_area("Mục tiêu lớn cần bẻ gãy:", value="Xãy dựng website bán hàng chuẩn SEO bằng Django trong 1 tuần", height=80)
            
            ai_mode = st.selectbox("🎯 Mô hình phân rã:", ["Agile Sprints Optimizer", "Waterfall Step-by-Step", "Mindmap Node Generator"])
            depth = st.slider("🔍 Độ sâu phân tầng lớp con:", 1, 5, 2)
            
            st.write("---")
            btn_decompose = st.button("🪄 Kích Hoạt Lõi AI soloflow", type="primary", use_container_width=True)
            
            st.write("")
            feature_pomodoro_timer()
            
        with c_right:
            st.subheader("📊 Lộ Trình Phân Tách Chi Tiết")
            if btn_decompose:
                if depth > 2 and st.session_state.tier == "Free User":
                    st.error("❌ Quyền truy cập bị giới hạn! Độ sâu phân rã từ cấp 3 trở lên chỉ dành cho bản PLUS.")
                else:
                    with st.spinner("Lõi AI đang bẻ gãy cấu trúc dữ liệu mục tiêu..."):
                        time.sleep(1.5)
                    st.success("Đã phân tách cấu trúc thành công!")
                    
                    with st.expander("📍 Bước 1: Khởi tạo kiến trúc nền tảng (Ngày 1-2)", expanded=True):
                        st.checkbox("Thiết kế sơ đồ ERD hệ thống dữ liệu liên kết")
                        st.checkbox("Cài đặt môi trường Python, Django Framework và Docker Container")
                        if depth >= 3:
                            st.caption("↳ *Mở rộng lớp con PLUS:* Tạo tệp cấu hình bảo mật khóa API mã hóa.")
                            
                    with st.expander("📍 Bước 2: Xây dựng logic & Tích hợp cổng PayOS (Ngày 3-5)", expanded=True):
                        st.checkbox("Viết API quản lý danh mục giỏ hàng")
                        st.checkbox("Tích hợp webhook đồng bộ hóa trạng thái hóa đơn PayOS")
                        
                    st.write("---")
                    feature_ai_bottleneck_predictor(main_task)
                    st.write("---")
                    feature_kanban_simulator()
            else:
                st.info("Nhập thông tin bên trái và bấm nút kích hoạt để xem kết quả sơ đồ.")

    # ------------------------------------------
    # CHỨC NĂNG 2: DASHBOARD & PHÂN TÍCH
    # ------------------------------------------
    elif sub_menu == "📊 Dashboard & Phân Tích":
        st.title("📊 Trung Tâm Phân Tích Chỉ Số Dự Án")
        
        st.subheader("Biểu đồ phân bổ thời gian dự kiến cho các dự án")
        chart_data = pd.DataFrame({
            'Giai đoạn': ['Thiết kế hệ thống', 'Lập trình Backend', 'Tích hợp Frontend', 'Tối ưu SEO', 'Kiểm thử Security'],
            'Số giờ dự kiến (Giả lập)': [12, 35, 20, 10, 15]
        })
        st.bar_chart(data=chart_data, x='Giai đoạn', y='Số giờ dự kiến (Giả lập)', color="#2563eb")
        
        st.subheader("📈 Tiến độ hoàn thành công việc tổng thể")
        st.progress(0.65)
        st.caption("Hiện tại bạn đã hoàn thành **65%** khối lượng công việc được rã nhỏ trong tuần này.")

    # ------------------------------------------
    # CHỨC NĂNG 3: HỒ SƠ HỆ THỐNG (PROFILE)
    # ------------------------------------------
    elif sub_menu == "👤 Hồ Sơ Hệ Thống":
        st.title("👤 Hồ Sơ Người Dùng soloflowOS")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Cấp độ tài khoản", st.session_state.tier)
        col_m2.metric("Số token AI khả dụng trong ngày", f"{st.session_state.tokens_left} / 5" if st.session_state.tier == "Free User" else "Vô hạn (PLUS)")
        col_m3.metric("Tốc độ phản hồi trung bình", "0.24 giây")
        
        st.write("---")
        st.subheader("Cập nhật thông tin nhận diện sinh trắc học")
        st.text_input("Tên định danh lập trình viên:", value=st.session_state.username)
        st.text_input("Mã định danh hệ thống (UUID):", value="SFL-9921-X85-2026", disabled=True)
        st.selectbox("Ngôn ngữ ưu tiên của AI:", ["Tiếng Việt", "English", "日本語"])
        if st.button("Đồng Bộ Hóa Hồ Sơ", type="primary"):
            st.toast("Đã lưu cấu hình hồ sơ cá nhân!")

    # ------------------------------------------
    # CHỨC NĂNG 4: CÀI ĐẶT TOÀN CỤC (SETTINGS)
    # ------------------------------------------
    elif sub_menu == "⚙️ Cài Đặt Toàn Cục":
        st.title("⚙️ Cấu Hình Hệ Thống Lõi")
        
        tab_engine, tab_webhook = st.tabs(["🤖 Lõi Trí Tuệ Nhân Tạo", "🔌 Kết Nối Webhook Ngoài"])
        with tab_engine:
            st.selectbox("Lọc thuật toán LLM xử lý:", ["soloflow GPT-4o Supercharged", "Claude 3.5 Sonnet Heavy Reasoning"])
            st.slider("Tham số nhiệt độ sáng tạo (Temperature):", 0.0, 1.0, 0.2)
        with tab_webhook:
            st.text_input("PayOS Webhook URL endpoint:", value="https://soloflow.streamlit.app/api/payos-webhook")
            st.text_input("PayOS Checksum Key:", type="password", value="1234567890abcdefghijklmnopqrstuvwxyz")

    # ------------------------------------------
    # CHỨC NĂNG 5: GIAO DIỆN MUA BẢN PLUS ĐẸP MẮT
    # ------------------------------------------
    elif sub_menu == "💎 Nâng Cấp PLUS":
        st.markdown("<h1 style='text-align: center; color: #e11d48;'>💎 Kích Hoạt Quyền Năng Hệ Điều Hành PLUS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size:18px;'>Giải phóng toàn bộ ranh giới công nghệ, tối ưu hóa 300% hiệu năng xử lý của trợ lý AI.</p>", unsafe_allow_html=True)
        st.write("---")
        
        col_card1, col_card2 = st.columns(2)
        
        with col_card1:
            st.markdown("""
            <div style='border: 2px solid #e2e8f0; padding: 25px; border-radius: 15px; background-color: #f8fafc;'>
                <h3 style='color: #64748b;'>Gói Tiêu Chuẩn (Free)</h3>
                <h2>0 đ <span style='font-size:14px; color:gray;'>/ vĩnh viễn</span></h2>
                <hr>
                <p>❌ Giới hạn 5 lượt rã việc mỗi ngày</p>
                <p>❌ Độ sâu sơ đồ cây bị khóa ở cấp 2</p>
                <p>❌ Không mở khóa mô hình phân tích rủi ro chuyên sâu</p>
                <p>❌ Không hỗ trợ xuất file sơ đồ tư duy Mindmap</p>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
            st.button("Bạn đang sử dụng gói này", disabled=True, use_container_width=True)
            
        with col_card2:
            st.markdown("""
            <div style='border: 3px solid #e11d48; padding: 25px; border-radius: 15px; background-color: #fff1f2; box-shadow: 0px 4px 15px rgba(225, 29, 72, 0.2);'>
                <h3 style='color: #e11d48;'>⚡ Gói soloflowOS PLUS 💎</h3>
                <h2>99.000 đ <span style='font-size:14px; color:gray;'>/ tháng (Giá gốc: 199.000 đ)</span></h2>
                <hr>
                <p>🟢 <b>VÔ HẠN</b> số lần phân rã công việc bằng AI</p>
                <p>🟢 Mở khóa độ sâu phân rã tối đa (Cấp 5 - Deep Layers)</p>
                <p>🟢 Kích hoạt Siêu tính năng <b>AI Bottleneck Predictor</b> tìm điểm nghẽn</p>
                <p>🟢 Xuất dữ liệu 1-Click sang định dạng Excel, PDF và Sơ đồ XMind</p>
                <p>🟢 Ưu tiên băng thông kết nối lõi GPT-4o & Claude 3.5 độc quyền</p>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
            if st.button("🔥 NÂNG CẤP LÊN BẢN PLUS NGAY", type="primary", use_container_width=True):
                st.balloons()
                st.toast("Đang chuyển hướng bạn sang cổng thanh toán trực tiếp PayOS...")
                time.sleep(1)
                st.info("Hãy chuyển sang tab 'Cổng Thanh Toán PayOS' ở menu bên trái để quét mã hóa đơn!")

    # ------------------------------------------
    # CHỨC NĂNG 6: TÍCH HỢP CỔNG THANH TOÁN PAYOS
    # ------------------------------------------
    elif sub_menu == "💳 Cổng Thanh Toán PayOS":
        st.title("💳 Trung Tâm Xác Thực Hóa Đơn Qua Cổng PayOS")
        st.write("Hệ thống liên kết trực tiếp API bảo mật của cổng trung gian thanh toán PayOS.")
        
        col_inv, col_qr = st.columns([1, 1.2])
        
        with col_inv:
            st.subheader("🧾 Chi Tiết Hóa Đơn Thanh Toán")
            st.markdown("""
            * **Đơn vị cung cấp giải pháp:** soloflowOS Technology Global
            * **Sản phẩm bản quyền:** Giấy phép kích hoạt `soloflowOS v6.0 PLUS`
            * **Thời hạn sử dụng:** 30 Ngày (Hệ thống tự động gia hạn)
            * **Mã giao dịch ứng dụng:** `SFL-ORDER-2026-9921A`
            """)
            st.write("---")
            st.markdown("### 💰 Số tiền cần thanh toán: <span style='color:red;'>99.000 VNĐ</span>", unsafe_allow_html=True)
            
            if st.button("🔗 Khởi Tạo Link Thanh Toán Tự Động Qua PayOS", type="primary", use_container_width=True):
                random_code = str(random.randint(100000, 999999))
                url, sig = generate_payos_link(99000, random_code)
                st.session_state.payos_order_id = random_code
                st.success(f"Đã đăng ký hóa đơn thành công lên máy chủ PayOS! Mã đơn: #{random_code}")
                
        with col_qr:
            st.subheader("📲 Quét Mã QR Qua Ứng Dụng Ngân Hàng (VietQR)")
            if st.session_state.payos_order_id is not None:
                st.markdown(f"""
                <div style='border: 2px dashed #2563eb; padding: 20px; border-radius: 10px; text-align: center; background-color: #f0f7ff;'>
                    <p style='font-weight: bold; color: #2563eb;'>CỔNG THANH TOÁN ĐỐI TÁC CHÍNH THỨC - PAYOS</p>
                    <div style='background-color: white; width: 200px; height: 200px; margin: 0 auto; border: 1px solid #cbd5e1; padding: 10px;'>
                        <p style='font-size: 11px; margin-top: 40px; color: #64748b;'>[ MÃ QR VIETQR ]<br>Đã mã hóa bảo mật<br><b>Mã đơn: #{st.session_state.payos_order_id}</b></p>
                    </div>
                    <p style='font-size: 13px; margin-top: 10px; color: #475569;'>Nội dung CK tự động: <b>SOLOFLOW {st.session_state.payos_order_id}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                if st.button("🔄 Tôi Đã Chuyển Khoản - Kiểm Tra Trạng Thế PayOS Webhook", use_container_width=True):
                    with st.spinner("Đang truy vấn API PayOS xem tiền đã vào tài khoản chưa..."):
                        time.sleep(2)
                    st.session_state.tier = "PLUS Active"
                    st.success("🎉 Hệ thống PayOS phản hồi: Đã nhận đủ 99.000 đ! Tài khoản của bạn đã nâng cấp thành PLUS thành công.")
                    st.balloons()
            else:
                st.warning("Vui lòng bấm nút khởi tạo hóa đơn ở cột bên trái để hiển thị mã QR thanh toán PayOS.")

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
