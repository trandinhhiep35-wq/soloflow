import streamlit as st
import time
import pandas as pd

# ==========================================
# CẤU HÌNH HỆ THỐNG TOÀN CỤC (soloflowOS v5.5)
# ==========================================
st.set_page_config(
    page_title="soloflowOS v5.5 - AI Task Decomposer", 
    page_icon="⚡", 
    layout="wide"
)

# Khởi tạo trạng thái bộ nhớ hệ thống (Session State)
if "tier" not in st.session_state:
    st.session_state.tier = "Free User"
if "tokens_left" not in st.session_state:
    st.session_state.tokens_left = 5
if "history_tasks" not in st.session_state:
    st.session_state.history_tasks = []

# --- SIDEBAR ĐIỀU HƯỚNG ---
st.sidebar.title("🚀 soloflowOS")
st.sidebar.subheader("Hệ Điều Hành Phân Rã Công Việc")

menu = st.sidebar.radio(
    "Trung tâm điều khiển:",
    [
        "📋 Rã Công Việc (AI)", 
        "👤 Hồ Sơ Cá Nhân (Profile)", 
        "⚙️ Cài Đặt Hệ Thống (Settings)", 
        "⚡ Sức Mạnh Bản PLUS", 
        "💳 Cổng Thanh Toán Plus"
    ]
)

st.sidebar.write("---")
# Hiển thị trạng thái tài khoản thời gian thực trên Sidebar
if st.session_state.tier == "PLUS Active":
    st.sidebar.success("👑 Tài khoản: PLUS PREMIUM")
else:
    st.sidebar.info(f"⚡ Tài khoản: Free User ({st.session_state.tokens_left} lượt còn lại)")

st.sidebar.caption(f"Phiên bản hiện tại: **v5.5**")
st.sidebar.caption("Phát triển bởi soloflow Team © 2026")

# ==========================================
# 1. GIAO DIỆN CHÍNH: RÃ CÔNG VIỆC & TÍNH NĂNG ĐẶC BIỆT
# ==========================================
if menu == "📋 Rã Công Việc (AI)":
    st.title("📋 Trung Tâm Phân Rã Công Việc Thông Minh")
    st.write("Giải pháp bẻ gãy các dự án phức tạp thành hành động thực tế bằng AI.")
    
    # Tạo Layout chia làm 2 cột: Cột trái nhập liệu & cấu hình nâng cao, Cột phải hiển thị kết quả
    col_input, col_output = st.columns([1, 2])
    
    with col_input:
        st.subheader("🛠️ Cấu hình bộ rã")
        task_input = st.text_area(
            "Nhập mục tiêu lớn hoặc dự án cần xử lý:", 
            value="Xây dựng website bán hàng chuẩn SEO bằng Django trong 1 tuần",
            height=100
        )
        
        # --- CÁC TÍNH NĂNG ĐẶC BIỆT VÀ CẦN THIẾT CHO NGƯỜI DÙNG ---
        ai_style = st.selectbox(
            "🎯 Phong cách phân tách của AI:",
            ["Chi tiết từng bước (Step-by-step)", "Tổng quan tối giản (Minimalist)", "Học thuật / Nghiên cứu chuyên sâu"]
        )
        
        depth_level = st.slider("🔍 Độ sâu phân rã (Lớp công việc con):", 1, 5, 2)
        
        col_date, col_priority = st.columns(2)
        with col_date:
            deadline = st.date_input("📅 Hạn chót dự án:")
        with col_priority:
            target_focus = st.selectbox("🔥 Trọng tâm tối ưu:", ["Tốc độ hoàn thành", "Chất lượng sản phẩm", "Tiết kiệm chi phí"])
            
        st.write("---")
        # Nút kích hoạt thuật toán rã việc
        btn_run = st.button("🪄 Bắt Đầu Phân Rã Ngay", type="primary", use_container_width=True)
        
    with col_output:
        st.subheader("📊 Sơ đồ lộ trình chi tiết từ soloflowOS")
        
        if btn_run:
            if not task_input.strip():
                st.warning("Vui lòng không để trống mục tiêu cần phân rã!")
            elif depth_level > 2 and st.session_state.tier == "Free User":
                st.error("❌ Giới hạn quyền hạn! Độ sâu phân rã từ tầng lớp cấp 3 trở lên yêu cầu nâng cấp lên phiên bản **PLUS**.")
                st.info("💡 Hãy chọn độ sâu <= 2 hoặc chuyển sang tab **Nâng Cấp PLUS** để mở khóa.")
            elif st.session_state.tier == "Free User" and st.session_state.tokens_left <= 0:
                st.error("❌ Bạn đã hết lượt dùng AI miễn phí trong ngày! Vui lòng nâng cấp bản PLUS để dùng vô hạn.")
            else:
                # Trừ token nếu là tài khoản free
                if st.session_state.tier == "Free User":
                    st.session_state.tokens_left -= 1
                    
                # Hiệu ứng Spinner của Streamlit
                with st.spinner(f"Trợ lý AI đang áp dụng thuật toán '{ai_style}' để xử lý dữ liệu..."):
                    time.sleep(2)
                st.success(f"Đã phân rã thành công dự án theo trọng tâm: {target_focus}!")
                
                # Render cây công việc chi tiết dựa theo cấu hình người dùng nhập
                with st.expander("📍 Giai đoạn 1: Khởi tạo & Thiết lập nền móng kiến trúc (Ngày 1-2)", expanded=True):
                    st.checkbox("Phân tích yêu cầu hệ thống và lập sơ đồ luồng dữ liệu (Dataflow Diagram)")
                    st.checkbox("Thiết lập môi trường ảo Python Virtualenv & Cài đặt Django/PostgreSQL")
                    if depth_level >= 2:
                        st.caption("↳ *Lớp con cấp 2:* Cấu hình các biến môi trường bảo mật `.env` và file `settings.py`")
                        
                with st.expander("📍 Giai đoạn 2: Xây dựng các tính năng Core & Logic Backend (Ngày 3-5)", expanded=True):
                    st.checkbox("Tạo Models cho Cơ sở dữ liệu Sản phẩm, Danh mục và Người dùng")
                    st.checkbox("Viết Views và APIs xử lý nghiệp vụ Giỏ hàng (Cart) và Đặt hàng (Checkout)")
                    st.checkbox("Tích hợp hệ thống quản trị admin-panel để quản lý kho hàng")
                    
                with st.expander("📍 Giai đoạn 3: Tối ưu SEO, Giao diện & Triển khai Đóng gói (Ngày 6-7)", expanded=True):
                    st.checkbox("Xây dựng giao diện Responsive tương thích mọi thiết bị di động")
                    st.checkbox("Tối ưu hóa các thẻ Heading, cấu hình file Sitemap.xml và Robots.txt chuẩn SEO")
                
                # Tính năng đặc biệt: Xuất dữ liệu
                st.write("")
                col_exp1, col_exp2 = st.columns(2)
                with col_exp1:
                    st.button("📥 Xuất lộ trình sang File Excel/CSV", use_container_width=True)
                with col_exp2:
                    if st.session_state.tier == "PLUS Active":
                        st.button("🗺️ Xuất sơ đồ tư duy Mindmap (XMind/PDF)", type="secondary", use_container_width=True)
                    else:
                        st.button("🗺️ Xuất Mindmap (Yêu cầu bản PLUS)", disabled=True, use_container_width=True)
        else:
            st.info("Chưa có dữ liệu xử lý. Vui lòng thiết lập cấu hình ở cột bên trái và bấm 'Bắt Đầu Phân Rã Ngay'.")

# ==========================================
# 2. GIAO DIỆN HỒ SƠ NGƯỜI DÙNG (PROFILE)
# ==========================================
elif menu == "👤 Hồ Sơ Cá Nhân (Profile)":
    st.title("👤 Trung Tâm Hồ Sơ Người Dùng")
    st.write("Quản lý thông tin cá nhân và xem các chỉ số hiệu suất làm việc của bạn.")
    
    # Thiết lập layout dạng thẻ (Cards) bằng hàng và cột
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.metric(label="Gói dịch vụ hiện tại", value=st.session_state.tier)
    with col_p2:
        if st.session_state.tier == "PLUS Active":
            st.metric(label="Lượt gọi trợ lý AI", value="Vô hạn (Unlimited)")
        else:
            st.metric(label="Lượt gọi AI miễn phí còn lại", value=f"{st.session_state.tokens_left} / 5")
    with col_p3:
        st.metric(label="Hiệu suất rã việc chính xác", value="98.4 %")
        
    st.write("---")
    st.subheader("Thông tin định danh tài khoản")
    
    col_form1, col_form2 = st.columns(2)
    with col_form1:
        st.text_input("Tên hiển thị:", value="Nguyễn Văn A")
        st.text_input("Địa chỉ Email đăng ký:", value="nguyenvana@gmail.com", disabled=True)
    with col_form2:
        st.text_input("Vai trò / Nghề nghiệp:", value="Nhà phát triển phần mềm độc lập (Solo Developer)")
        st.selectbox("Múi giờ hệ thống (Timezone):", ["UTC+07:00 (Băng Cốc, Hà Nội, Jakarta)", "UTC+00:00 (London)"])
        
    if st.button("💾 Cập nhật thông tin hồ sơ", type="primary"):
        st.success("Hệ thống soloflowOS đã đồng bộ dữ liệu hồ sơ mới thành công!")

# ==========================================
# 3. GIAO DIỆN CÀI ĐẶT HỆ THỐNG (SETTINGS)
# ==========================================
elif menu == "⚙️ Cài Đặt Hệ Thống (Settings)":
    st.title("⚙️ Tùy Chỉnh Cấu Hình Hệ Thống")
    st.write("Cấu hình sâu các thông số hoạt động của lõi phần mềm soloflowOS v5.5.")
    
    # Sử dụng Tabs để phân tách các khu vực cài đặt chuyên nghiệp
    tab_ai, tab_ui, tab_security = st.tabs(["🤖 Cấu Hình Lõi AI", "🎨 Giao Diện & Trải Nghiệm", "🔒 Bảo Mật & Kết Nối"])
    
    with tab_ai:
        st.subheader("AI Engine Linker")
        selected_model = st.selectbox(
            "Lựa chọn siêu mô hình LLM để kết nối:",
            ["soloflow-Core-Engine v1 (Mặc định)", "GPT-4o Advanced Reasoning (PLUS)", "Claude 3.5 Sonnet Vision (PLUS)"]
        )
        if "PLUS" in selected_model and st.session_state.tier == "Free User":
            st.error("⚠️ Mô hình cao cấp này đã bị khóa. Vui lòng nâng cấp tài khoản lên gói PLUS để liên kết.")
            
        st.slider("Độ sáng tạo của AI (Temperature):", 0.0, 1.0, 0.3, step=0.1)
        st.caption("Mức thấp (0.1 - 0.3) giúp AI rã việc logic, thực tế. Mức cao (> 0.7) kích thích ý tưởng đột phá.")
        
    with tab_ui:
        st.subheader("Tùy biến UI/UX")
        st.checkbox("Tự động cuộn trang khi AI sinh văn bản", value=True)
        st.checkbox("Gửi thông báo âm thanh khi hoàn thành rã việc lớn", value=False)
        st.write("💡 *Mẹo thay đổi Dark/Light Mode:* Bản v5.5 tương thích trực tiếp với cài đặt của Streamlit. Bạn chỉ cần nhấn vào biểu tượng 3 chấm ở góc trên cùng bên phải -> Chọn **Settings** -> Điều chỉnh mục **Theme** theo sở thích cá nhân.")
        
    with tab_security:
        st.subheader("Quản lý khóa API liên kết")
        st.text_input("Nhập OpenAI API Key cá nhân của bạn (Nếu có):", type="password", placeholder="sk-proj-........................")
        st.caption("Lưu ý: Khóa API cá nhân sẽ được lưu mã hóa ngay tại bộ nhớ trình duyệt (Local Storage) của bạn, đảm bảo an toàn tuyệt đối.")

# ==========================================
# 4. GIAO DIỆN SỨC MẠNH BẢN PLUS NÂNG CẤP
# ==========================================
elif menu == "⚡ Sức MẠNH Bản PLUS":
    st.title("⚡ soloflowOS v5.5 PLUS - Giải Phóng Sức Mạnh Trợ Lý AI")
    st.write("Khám phá sự khác biệt vượt trội về hiệu năng và công nghệ xử lý dữ liệu.")
    
    # So sánh chi tiết dưới dạng bảng cấu trúc Markdown
    st.markdown("""
    ### 📊 Bảng so sánh năng lực xử lý giữa các phiên bản
    
    | Tiêu chí kỹ thuật và tính năng | Phiên bản MIỄN PHÍ | Phiên bản soloflowOS PLUS |
    | :--- | :---: | :---: |
    | **Tốc độ xử lý & phản hồi của AI** | Tiêu chuẩn (1x) | 🔥 **Băng thông ưu tiên (Gấp 3x lần)** |
    | **Giới hạn số lần rã việc** | Tối đa 5 lần / ngày | ♾️ **VÔ HẠN KHÔNG GIỚI HẠN** |
    | **Độ sâu phân lớp sơ đồ cây** | Bị giới hạn ở 2 tầng | 🚀 **Phân rã sâu vô hạn (Deep layers)** |
    | **Siêu mô hình trí tuệ nhân tạo** | Lõi Free-Model | 🧠 **Tích hợp trực tiếp GPT-4o & Claude 3.5** |
    | **Cửa sổ ngữ cảnh xử lý (Context)** | 4.000 Tokens | 📊 **128.000 Tokens (Đọc tài liệu dày 300 trang)** |
    | **Xuất sơ đồ Mindmap / Tiến độ** | Không hỗ trợ | ✅ **Hỗ trợ xuất 1-Click (XMind, Excel, PDF)** |
    """)
    
    st.write("")
    st.info("💡 **Hệ thống trợ lý AI trên bản PLUS** sử dụng thuật toán suy luận thông minh mới, tự động phát hiện các điểm nghẽn (Bottlenecks) trong kế hoạch dự án của bạn và tự đề xuất phương án giải quyết tối ưu nhất.")

# ==========================================
# 5. GIAO DIỆN MUA BẢN PLUS & CỔNG THANH TOÁN
# ==========================================
elif menu == "💳 Cổng Thanh Toán Plus":
    st.title("💳 Trung Tâm Thanh Toán Hóa Đơn Dịch Vụ")
    
    col_invoice, col_gateway = st.columns([1, 1])
    
    with col_invoice:
        st.subheader("🧾 Chi tiết hóa đơn điện tử")
        st.write("---")
        st.write("**Gói dịch vụ:** Nâng cấp Bản quyền soloflowOS v5.5 PLUS")
        st.write("**Thời hạn:** Bản quyền vĩnh viễn theo tài khoản (Gia hạn chu kỳ 30 ngày)")
        st.write("**Đơn giá niêm yết:** ~~199.000đ / tháng~~")
        st.markdown("**Giá ưu đãi chiến dịch phần mềm:** :red[99.000đ / tháng] *(Tiết kiệm 50% / Đã áp mã giảm giá)*")
        st.write("---")
        st.caption("🔒 Giao dịch được mã hóa đầu cuối bằng chuẩn bảo mật SSL 256-bit, bảo vệ quyền lợi người dùng tuyệt đối.")
        
    with col_gateway:
        st.subheader("🛡️ Lựa chọn cổng thanh toán an toàn")
        pay_option = st.radio(
            "Chọn cổng kết nối trực tiếp vào hệ thống xử lý ngân hàng:",
            ["Cổng VietQR - Quét mã Chuyển khoản nhanh tự động", "Cổng Thẻ Quốc Tế - Visa / Mastercard / JCB"]
        )
        
        st.write("---")
        if pay_option == "Cổng VietQR - Quét mã Chuyển khoản nhanh tự động":
            # Hiển thị mockup cổng mã QR
            st.code(
                "┌──────────────────────────────────┐\n"
                "│                                  │\n"
                "│       [ MÃ QR VIETQR MOCKUP ]    │\n"
                "│      soloflowOS v5.5 Premium     │\n"
                "│                                  │\n"
                "└──────────────────────────────────┘", 
                language="text"
            )
            st.caption("Hãy mở ứng dụng Ngân hàng di động (Banking App) bất kỳ của bạn để thực hiện quét mã QR tự động.")
            
            if st.button("🔄 Tôi Đã Chuyển Khoản - Kiểm Tra Ngay", type="primary", use_container_width=True):
                with st.spinner("Hệ thống đang quét xác thực tín hiệu Webhook tài khoản ngân hàng..."):
                    time.sleep(2.5)
                st.session_state.tier = "PLUS Active"
                st.success("🎉 Hệ thống xác nhận thành công! soloflowOS v5.5 của bạn đã được nâng cấp lên bản PLUS.")
                
        else:
            # Giao diện nhập liệu thẻ tín dụng
            st.text_input("Số thẻ tín dụng của bạn:", value="4321 0987 6543 2100")
            c_sub1, c_sub2 = st.columns(2)
            with c_sub1:
                st.text_input("Hạn dùng thẻ (MM/YY):", value="12/29")
            with c_sub2:
                st.text_input("Mã bảo mật (CVC/CVV):", value="***", type="password")
                
            if st.button("💳 Xác Nhận Thanh Toán Ký Số Qua Thẻ", type="primary", use_container_width=True):
                with st.spinner("Đang kết nối trung tâm thanh toán thẻ quốc tế bảo mật..."):
                    time.sleep(2.5)
                st.session_state.tier = "PLUS Active"
                st.success("🎉 Giao dịch thành công! Xin chào đón bạn đến với thế giới sức mạnh của soloflowOS PLUS.")
