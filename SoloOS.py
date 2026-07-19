import streamlit as st
import time

# 1. Cấu hình tiêu đề và bố cục trang web
st.set_page_config(
    page_title="AI Task Decomposer Pro", 
    page_icon="🔥", 
    layout="wide"
)

# 2. Khởi tạo State (Bộ nhớ tạm) để lưu trạng thái tài khoản người dùng
if "tier" not in st.session_state:
    st.session_state.tier = "Free User"
if "tokens_left" not in st.session_state:
    st.session_state.tokens_left = 5

# 3. Thanh điều hướng bên trái (Sidebar)
st.sidebar.title("🔥 DECOMPOSER AI")
menu = st.sidebar.radio(
    "Menu chức năng:",
    ["📋 Rã Công Việc", "👤 Hồ Sơ Cá Nhân", "⚙️ Cài Đặt Hệ Thống", "⚡ Nâng Cấp PLUS", "💳 Thanh Toán"]
)
st.sidebar.write("---")
st.sidebar.caption(f"Phiên bản: 1.0.0 | **{st.session_state.tier}**")

# ==========================================
# CHỨC NĂNG 1: RÃ CÔNG VIỆC
# ==========================================
if menu == "📋 Rã Công Việc":
    st.title("📋 Bảng Phân Rã Công Việc Bằng Trợ Lý AI")
    st.write("Nhập mục tiêu lớn của bạn, AI sẽ tự động bẻ gãy thành các lộ trình chi tiết.")
    
    # Ô nhập liệu công việc
    task_input = st.text_input(
        "Mục tiêu lớn cần rã nhỏ:", 
        value="Xây dựng website bán hàng chuẩn SEO bằng Django trong 1 tuần"
    )
    
    if st.button("🪄 Rã Việc Bằng AI", type="primary"):
        if not task_input.strip():
            st.warning("Vui lòng nhập nội dung công việc cần rã!")
        else:
            # Hiệu ứng loading chạy ngầm của Streamlit
            with st.spinner("AI đang phân tích và lên sơ đồ cấu trúc..."):
                time.sleep(2) # Giả lập AI xử lý
            st.success("Đã phân rã công việc thành công!")
            
            # Hiển thị cấu trúc cây bằng các khối Expander thả xuống
            with st.expander("🔹 Bước 1: Chuẩn bị kiến trúc & Thiết kế Database (Ngày 1-2) - Ưu tiên: Cao", expanded=True):
                st.checkbox("Thiết kế sơ đồ ERD (Thực thể - Mối quan hệ) [4 giờ]", value=False)
                st.checkbox("Khởi tạo cấu trúc thư mục Project Django & kết nối PostgreSQL [3 giờ]", value=False)
                
            with st.expander("🔹 Bước 2: Xây dựng các chức năng Core Backend (Ngày 3-5) - Ưu tiên: Cao", expanded=True):
                st.checkbox("Xây dựng App Product quản lý danh mục và sản phẩm [8 giờ]", value=False)
                st.checkbox("Tích hợp bộ lọc tìm kiếm và phân trang dữ liệu [5 giờ]", value=False)
                st.checkbox("Viết API xử lý giỏ hàng và đơn hàng [10 giờ]", value=False)
                
            with st.expander("🔹 Bước 3: Tối ưu SEO & Đóng gói Giao diện (Ngày 6-7) - Ưu tiên: Trung bình", expanded=True):
                st.checkbox("Render giao diện HTML/Tailwind CSS chuẩn Mobile [8 giờ]", value=False)
                st.checkbox("Cấu hình thẻ Meta, file Sitemap.xml và Robots.txt [4 giờ]", value=False)

# ==========================================
# CHỨC NĂNG 2: HỒ SƠ NGƯỜI DÙNG
# ==========================================
elif menu == "👤 Hồ Sơ Cá Nhân":
    st.title("👤 Hồ Sơ Tài Khoản")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Thông tin cá nhân")
        st.info(f"""
        - **Chủ tài khoản:** Nguyễn Văn A
        - **Email:** nguyenvana@gmail.com
        - **Gói hiện tại:** {st.session_state.tier}
        """)
        
    with col2:
        st.subheader("Tài nguyên AI trong ngày")
        if st.session_state.tier == "PLUS Active":
            st.success("🔥 Bạn đang sử dụng gói PLUS: Không giới hạn lượt rã việc!")
        else:
            st.write(f"Số lượt rã việc AI miễn phí còn lại: **{st.session_state.tokens_left}/5**")
            st.progress(st.session_state.tokens_left / 5)

# ==========================================
# CHỨC NĂNG 3: CÀI ĐẶT HỆ THỐNG
# ==========================================
elif menu == "⚙️ Cài Đặt Hệ Thống":
    st.title("⚙️ Cài Đặt Hệ Thống")
    
    st.subheader("Mô hình trí tuệ nhân tạo (AI Engine)")
    model = st.selectbox(
        "Lựa chọn bộ não LLM xử lý logic:",
        ["Decomposer Free-Model v1", "Claude 3.5 Sonnet (Gói PLUS)", "GPT-4o Reasoning (Gói PLUS)"]
    )
    
    if "PLUS" in model and st.session_state.tier == "Free User":
        st.error("❌ Quyền truy cập bị từ chối! Bạn cần nâng cấp lên bản quyền PLUS để dùng mô hình này.")
        
    st.subheader("Tùy biến giao diện")
    st.write("💡 *Mẹo:* Để chuyển đổi giao diện **Sáng / Tối (Dark Mode)**, bạn chỉ cần bấm vào biểu tượng 3 dấu chấm ở góc trên cùng bên phải màn hình web -> Chọn **Settings** -> Thay đổi mục **Theme** nhé!")

# ==========================================
# CHỨC NĂNG 4: GIỚI THIỆU BẢN PLUS
# ==========================================
elif menu == "⚡ Nâng Cấp PLUS":
    st.title("⚡ Nâng Cấp Phiên Bản PLUS Cao Cấp")
    st.write("Giải phóng 100% sức mạnh công nghệ đột phá, bẻ gãy mọi dự án siêu lớn thành các mục tiêu siêu nhỏ.")
    
    # Tạo bảng so sánh tính năng bằng Markdown
    st.markdown("""
    | Tính năng cốt lõi | Bản MIỄN PHÍ | Bản PLUS CAO CẤP |
    | :--- | :---: | :---: |
    | **Giới hạn rã việc hàng ngày** | 5 lần / ngày | **VÔ HẠN KHÔNG GIỚI HẠN** |
    | **Độ sâu phân tầng cây mục tiêu** | Tối đa 2 tầng con | **Phân rã vô hạn lớp (Deep layers)** |
    | **Mô hình AI xử lý chuyên sâu** | Free Custom Model | **GPT-4o & Claude 3.5 Sonnet** |
    | **Xuất dữ liệu Excel/Mindmap** | Không hỗ trợ | **Hỗ trợ xuất 1-Click** |
    | **Tốc độ phản hồi của AI** | Tiêu chuẩn | **Ưu tiên băng thông cao (Gấp 3 lần)** |
    """)
    
    st.write("")
    st.success("💰 Ưu đãi đặc biệt: Chỉ **99.000đ / tháng** (Tiết kiệm 50% so với giá gốc).")

# ==========================================
# CHỨC NĂNG 5: CỔNG THANH TOÁN
# ==========================================
elif menu == "💳 Thanh Toán":
    st.title("💳 Cổng Thanh Toán Hóa Đơn Dịch Vụ")
    
    col_bill, col_pay = st.columns([1, 1])
    
    with col_bill:
        st.subheader("Đơn hàng của bạn")
        st.write("---")
        st.write("**Sản phẩm:** Gia hạn Premium AI Plus")
        st.write("**Thời hạn sử dụng:** 30 Ngày")
        st.write("**Giá tiền niêm yết:** ~~199.000đ~~")
        st.markdown("**Số tiền cần thanh toán:** :red[99.000đ] *(Đã áp mã giảm giá)*")
        
    with col_pay:
        st.subheader("Phương thức thanh toán")
        pay_method = st.radio(
            "Chọn cổng kết nối trực tiếp:",
            ["Quét mã QR Chuyển khoản (VietQR)", "Thẻ tín dụng Quốc tế (Visa/Mastercard)"]
        )
        
        st.write("---")
        if pay_method == "Quét mã QR Chuyển khoản (VietQR)":
            # Tạo một khung giả lập mã QR bằng Markdown phối màu
            st.code("┌───────────────────────────┐\n│                           │\n│     [ MÃ QR VIETQR ]      │\n│    Nạp tiền tự động       │\n│                           │\n└───────────────────────────┘", language="text")
            st.caption("Dùng ứng dụng Ngân hàng (Banking) quét mã để thanh toán.")
            
            if st.button("🔄 Tôi Đã Chuyển Khoản - Kiểm Tra Ngay", type="primary"):
                with st.spinner("Đang quét tín hiệu Webhook tài khoản ngân hàng..."):
                    time.sleep(2.5)
                st.session_state.tier = "PLUS Active"
                st.success("🎉 Kích hoạt thành công! Tài khoản của bạn đã được nâng cấp lên gói PLUS.")
                
        else:
            card_num = st.text_input("Số thẻ tín dụng:", value="4321 0987 6543 2100")
            col_sub1, col_sub2 = st.columns(2)
            with col_sub1:
                st.text_input("Hạn dùng (MM/YY):", value="12/29")
            with col_sub2:
                st.text_input("Mã bảo mật CVC:", value="***", type="password")
                
            if st.button("💳 Xác Nhận Thanh Toán Ký Số", type="primary"):
                with st.spinner("Đang kết nối cổng thanh toán Visa/Mastercard quốc tế..."):
                    time.sleep(2.5)
                st.session_state.tier = "PLUS Active"
                st.success("🎉 Kích hoạt thành công! Tài khoản của bạn đã được nâng cấp lên gói PLUS.")
