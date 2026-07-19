import streamlit as st
import pandas as pd
import time
import datetime
import random
import json

# =========================================================================
# CẤU HÌNH HỆ THỐNG TOÀN CỤC V9.0 QUANTUM CORE
# =========================================================================
st.set_page_config(
    page_title="soloflowOS v9.0 - Quantum AI Workspace",
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
    st.session_state.tier = "Bản Thường (Free)"
if "work_category" not in st.session_state:
    st.session_state.work_category = "💼 Quản lý & Doanh nghiệp"

# Lịch sử Chatbot nâng cao
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Cấu hình Profile
if "profile_fullname" not in st.session_state:
    st.session_state.profile_fullname = "Trần Đình Hiệp"
if "profile_role" not in st.session_state:
    st.session_state.profile_role = "Core Developer / Product Manager"
if "profile_bio" not in st.session_state:
    st.session_state.profile_bio = "Đang tối ưu hóa cấu trúc rã việc đa luồng chống trì hoãn."

# Cài đặt hệ thống
if "settings_ai_temp" not in st.session_state:
    st.session_state.settings_ai_temp = 0.6
if "settings_secure_mode" not in st.session_state:
    st.session_state.settings_secure_mode = True
if "settings_theme" not in st.session_state:
    st.session_state.settings_theme = "Đen tuyền Premium (Jet Black)"

if "custom_sprints" not in st.session_state:
    st.session_state.custom_sprints = [
        {"Hạng mục": "Khảo sát và Lập chiến lược sơ đồ", "Thời gian (Giờ)": 12, "Độ phức tạp": "Cao"},
        {"Hạng mục": "Xây dựng cấu trúc dữ liệu nền tảng", "Thời gian (Giờ)": 24, "Độ phức tạp": "Trung bình"}
    ]
if "flashcards" not in st.session_state:
    st.session_state.flashcards = [{"Câu hỏi": "Bất đẳng thức Cauchy dạng tổng quát cho n số?", "Trả lời": "Trung bình cộng luôn lớn hơn hoặc bằng trung bình nhân"}]

# PHỦ CSS PREMIUM MINIMALIST DARK MODE (NỀN ĐEN TUYỀN, VIỀN SÁNG COGNITIVE)
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #ffffff; }
    div[data-testid="stSidebar"] { background-color: #040404 !important; border-right: 1px solid #1a1a1a; }
    .plus-card-premium {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        padding: 30px;
        border-radius: 14px;
        box-shadow: 0px 4px 30px rgba(255, 255, 255, 0.15);
    }
    .psychology-box {
        background-color: #080808;
        border: 1px dashed #333333;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
    }
    .chat-bubble-user {
        background-color: #161616; padding: 14px; border-radius: 10px; margin-bottom: 12px; border-left: 4px solid #ffffff;
    }
    .chat-bubble-ai {
        background-color: #0a0a0a; padding: 14px; border-radius: 10px; margin-bottom: 12px; border-left: 4px solid #555555; border: 1px solid #222222;
    }
</style>
""", unsafe_allow_html=True)

def draw_soloflow_brand(is_sidebar=False):
    brand_html = """
    <div style='text-align: center; padding: 15px 0; border-bottom: 1px solid #1a1a1a; margin-bottom: 20px;'>
        <div style='font-size: 30px; font-weight: 900; color: #ffffff; letter-spacing: -0.5px;'>🪐 soloflowOS <span style='font-size: 12px; vertical-align: super; color: #888888;'>v9.0</span></div>
        <div style='font-size: 9px; color: #666666; font-family: monospace; letter-spacing: 3px; margin-top: 2px;'>QUANTUM COGNITIVE WORKSPACE</div>
    </div>
    """
    if is_sidebar:
        st.sidebar.markdown(brand_html, unsafe_allow_html=True)
    else:
        st.markdown(brand_html, unsafe_allow_html=True)

# =========================================================================
# CỔNG ĐĂNG NHẬP / XÁC THỰC AN TOÀN
# =========================================================================
def show_authentication_gateway():
    draw_soloflow_brand(is_sidebar=False)
    _, central_panel, _ = st.columns([1, 1.3, 1])
    with central_panel:
        st.markdown("<h3 style='text-align: center; color: white; font-weight: 700;'>Hạ Tầng Phân Rã Hệ Thống Thần Kinh AI</h3>", unsafe_allow_html=True)
        login_tab, register_tab = st.tabs(["🔒 ĐĂNG NHẬP NODE", "📝 KHỞI TẠO SANDBOX"])
        
        with login_tab:
            u_name = st.text_input("Định danh tài khoản (Username)", key="auth_u")
            u_pass = st.text_input("Khóa bảo mật (Password)", type="password", key="auth_p")
            if st.button("KÍCH HOẠT PHIÊN LÀM VIỆC QUANTUM", type="primary", use_container_width=True):
                if u_name and u_pass:
                    st.session_state.logged_in = True
                    st.session_state.username = u_name
                    st.success("Xác thực thành công. Đang đồng bộ hóa bộ nhớ cache...")
                    time.sleep(0.4)
                    st.rerun()
                else:
                    st.error("Vui lòng nhập đầy đủ thông tin để giải mã dữ liệu Node.")
                    
        with register_tab:
            st.caption("Khởi tạo không gian sandbox cục bộ cách ly hoàn toàn với internet.")
            st.text_input("Họ và tên người điều hành")
            st.text_input("Tên Node định danh mới")
            st.text_input("Khóa bảo mật master", type="password")
            if st.button("KHỞI TẠO CORE DATABASE", use_container_width=True):
                st.success("Khởi tạo cấu trúc Node thành công!")

# =========================================================================
# LÕI AI PHÂN RÃ HỌC LỎM TỪ CÁC SIÊU ỨNG DỤNG THẾ GIỚI (GOBLIN / LINEAR)
# =========================================================================
def request_ai_core_processing(query, layer_depth, category, split_mode, cognitive_load):
    q_lower = query.lower()
    steps = []
    
    # Xử lý mức độ chia nhỏ dựa trên tâm lý người dùng (Cognitive Load - Mượn ý tưởng từ Goblin.tools)
    is_micro = "Siêu nhỏ (Micro-steps)" in cognitive_load
    
    if "Quản lý" in category:
        if is_micro:
            steps = [
                {"title": "Mở file spreadsheet hoặc Notion mẫu", "content": "Chuẩn bị một không gian trống, chưa cần ghi gì phức tạp. Viết ra đúng 3 đầu mục lớn nhất trong đầu.", "dep": "Không có", "risk": "Thấp"},
                {"title": "Ghi ra tiêu chuẩn hoàn thành (DoD) cho tính năng PayOS", "content": "Định nghĩa rõ thế nào là hoàn thành: Ví dụ, quét được mã QR và nhận webhook thành công.", "dep": "Mở file mẫu", "risk": "Thấp"},
                {"title": "Tách sơ đồ luồng thành 2 phần: Khách chuyển tiền và Hệ thống nhận", "content": "Vẽ nháp ra giấy luồng đi của dòng tiền để tránh thiết kế sai kiến trúc.", "dep": "Ghi ra tiêu chuẩn hoàn thành", "risk": "Trung bình"},
                {"title": "Tạo task con trên Jira/Linear và gán tag Khẩn cấp", "content": "Đưa các đầu việc này lên bảng quản trị chung để đội ngũ nhìn thấy tiến độ.", "dep": "Tách sơ đồ luồng", "risk": "Thấp"}
            ]
        else:
            steps = [
                {"title": "Thiết lập kiến trúc vận hành & Mục tiêu OKR cốt lõi", "content": "Xác định rõ ràng mục tiêu kinh doanh, các chỉ số kết quả then chốt cần đạt được trong chu kỳ.", "dep": "Không có", "risk": "Thấp"},
                {"title": "Phân bẻ cấu trúc Epic lớn thành các User Stories trên Linear", "content": "Viết đặc tả yêu cầu nghiệp vụ dưới dạng giá trị cung cấp cho người dùng cuối.", "dep": "Thiết lập kiến trúc vận hành", "risk": "Trung bình"},
                {"title": "Ước tính ma trận điểm thắt nút cổ chai (Bottleneck Prediction)", "content": "Phân tích các rủi ro chậm trễ do hạ tầng bên thứ ba hoặc xung đột nhân sự.", "dep": "Phân bẻ cấu trúc Epic", "risk": "Cao"}
            ]
            
    elif "Học tập" in category:
        if "toán" in q_lower or "bất đẳng thức" in q_lower or "cauchy" in q_lower:
            if is_micro:
                steps = [
                    {"title": "Viết lại biểu thức gốc ra nháp bằng bút đỏ", "content": "Nhìn kỹ cấu trúc đối xứng hoặc lệch tâm của các biến số thực để kích hoạt vùng tư duy trực giác.", "dep": "Không có", "risk": "Thấp"},
                    {"title": "Thử thế các giá trị biên bằng nhau (a = b = c)", "content": "Kiểm tra xem dấu bằng xảy ra tại đâu. Đây gọi là kỹ thuật xác định điểm rơi đại số.", "dep": "Viết lại biểu thức gốc", "risk": "Thấp"},
                    {"title": "Tách riêng từng hạng tử có chứa mẫu số", "content": "Chuẩn bị nhân thêm hằng số thích hợp để khi áp dụng Cauchy, mẫu số sẽ bị triệt tiêu hoàn toàn.", "dep": "Thử thế các giá trị biên", "risk": "Cao"}
                ]
            else:
                steps = [
                    {"title": "Phân tích tập xác định và Xác lập điểm rơi đối xứng hình học", "content": "Dự đoán chính xác dấu bằng của bất đẳng thức để chọn điểm rơi thích hợp.", "dep": "Không có", "risk": "Thấp"},
                    {"title": "Áp dụng kỹ thuật tách nhóm hạng tử bất định (AM-GM)", "content": "Thêm bớt các đại lượng thích hợp nhằm ép các biến triệt tiêu khi lấy căn thức.", "dep": "Phân tích tập xác định", "risk": "Cao"}
                ]
        else: # Ngữ văn / Lý luận
            if is_micro:
                steps = [
                    {"title": "Ghi lại tên tác giả, năm sáng tác và hoàn cảnh lịch sử", "content": "Ví dụ: 'Mây trắng còn bay' của Bảo Ninh sáng tác trong thời kỳ đổi mới, nhìn nhận chiến tranh từ góc độ nhân văn sâu sắc.", "dep": "Không có", "risk": "Thấp"},
                    {"title": "Gạch dưới 2 chi tiết nghệ thuật đắt giá nhất", "content": "Tập trung phân tích hình ảnh bức ảnh thờ trên máy bay và thái độ của nhân vật bà cụ.", "dep": "Ghi lại tên tác giả", "risk": "Thấp"}
                ]
            else:
                steps = [
                    {"title": "Xây dựng luận điểm tổng quan và Hoàn cảnh lịch sử tác phẩm", "content": "Dẫn dắt mạch tư duy, liên kết bối cảnh thời đại với thông điệp cốt lõi của tác giả.", "dep": "Không có", "risk": "Thấp"},
                    {"title": "Bóc tách diễn biến tâm lý nhân vật & Giải mã tín hiệu thẩm mỹ", "content": "Đi sâu vào các phân đoạn bước ngoặt để làm nổi bật chiều sâu nghệ thuật của tác phẩm văn học.", "dep": "Xây dựng luận điểm tổng quan", "risk": "Trung bình"}
                ]
                
    elif "Lập trình" in category:
        if is_micro:
            steps = [
                {"title": "Tạo file main.py và thiết lập môi trường ảo venv", "content": "Đảm bảo môi trường cô lập, cài đặt các thư viện lõi ban đầu sạch sẽ.", "dep": "Không có", "risk": "Thấp"},
                {"title": "Viết cấu trúc class hoặc hàm mẫu (Mock Data)", "content": "Chưa viết logic phức tạp, chỉ định nghĩa đầu vào đầu ra dạng JSON để test luồng.", "dep": "Tạo file main.py", "risk": "Thấp"},
                {"title": "Viết hàm bắt lỗi try-except cho cổng API kết nối", "content": "Bảo vệ hệ thống không bị crash đột ngột khi dữ liệu trả về bị lỗi cú pháp.", "dep": "Viết cấu trúc class", "risk": "Trung bình"}
            ]
        else:
            steps = [
                {"title": "Thiết kế sơ đồ kiến trúc dữ liệu và Thực thể quan hệ (ERD)", "content": "Tối ưu các chỉ mục truy vấn, phân tách các bảng dữ liệu để tránh deadlock khi chạy đa luồng.", "dep": "Không có", "risk": "Cao"},
                {"title": "Xây dựng trục logic nghiệp vụ API Core Async", "content": "Triển khai mã nguồn xử lý song song bất đồng bộ, tối ưu hóa bộ nhớ đệm cache.", "dep": "Thiết kế sơ đồ kiến trúc dữ liệu", "risk": "Trung bình"}
            ]
    else: # Thiết kế & Sáng tạo
        if is_micro:
            steps = [
                {"title": "Mở Pinterest hoặc Behance tìm 5 ảnh thuộc tông Minimalist Dark", "content": "Lấy cảm hứng về bố cục, cách đi tuyến chữ và tỷ lệ tương phản sáng tối.", "dep": "Không có", "risk": "Thấp"},
                {"title": "Viết câu tiêu đề giật gân (Hook) dài dưới 10 từ", "content": "Tập trung đánh thẳng vào sự tò mò hoặc một hiểu lầm phổ biến của người xem.", "dep": "Mở Pinterest tìm ảnh", "risk": "Thấp"}
            ]
        else:
            steps = [
                {"title": "Định vị Concept chủ đạo & Nghiên cứu hành vi đối tượng", "content": "Phát triển ý tưởng nghệ thuật độc bản dựa trên số liệu phân tích xu hướng.", "dep": "Không có", "risk": "Thấp"},
                {"title": "Phác thảo kịch bản phân cảnh chi tiết (Storyboard đa luồng)", "content": "Bẻ nhỏ cấu trúc thời gian của video thành từng giây, gán âm thanh và nhịp hình ảnh tương ứng.", "dep": "Định vị Concept chủ đạo", "risk": "Trung bình"}
            ]
            
    return steps[:layer_depth]

# =========================================================================
# GIAO DIỆN ĐIỀU HÀNH TRUNG TÂM SOLOFLOWOS V9.0
# =========================================================================
def show_central_dashboard():
    draw_soloflow_brand(is_sidebar=True)
    
    st.sidebar.markdown(f"👤 Node Người dùng: **{st.session_state.username}**")
    st.sidebar.markdown(f"⚙️ Quyền truy cập: `{st.session_state.tier}`")
    
    # DANH MỤC CÔNG VIỆC DYNAMIC - THAY ĐỔI TOÀN BỘ TÍNH NĂNG KHI CHỌN
    st.session_state.work_category = st.sidebar.selectbox(
        "🧠 Cấu hình Danh mục Công việc:",
        [
            "💼 Quản lý & Doanh nghiệp",
            "🎓 Học tập & Nghiên cứu",
            "💻 Lập trình & Kỹ thuật",
            "🎨 Sáng tạo & Thiết kế"
        ]
    )
    
    navigation_hub = st.sidebar.radio(
        "🧭 TRÌNH ĐIỀU HƯỚNG QUANTUM CORE:",
        [
            "📋 Lõi AI Phân Rã Việc 9.0",
            "💬 Trợ lý AI Chuyên Gia (Co-Pilot)",
            "✨ Siêu Phân Hệ Tâm Lý Học",
            "📊 Hoạch Định Tiến Độ Sprints",
            "⚙️ Hồ Sơ & Cài Đặt Hệ Thống",
            "💰 Nâng Cấp PLUS & LIFETIME",
            "💳 Cổng Thanh Toán PayOS"
        ]
    )
    
    st.sidebar.write("---")
    if st.sidebar.button("🚪 Đăng xuất an toàn", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.chat_history = []
        st.rerun()

    # ---------------------------------------------------------------------
    # 📋 LÕI AI PHÂN RÃ VIỆC 9.0 (HỌC LỎM LINEAR & GOBLIN.TOOLS)
    # ---------------------------------------------------------------------
    if navigation_hub == "📋 Lõi AI Phân Rã Việc 9.0":
        st.title("📋 Lõi Phân Rã Công Việc Đa Tầng Cấp Cao v9.0")
        st.caption(f"Hệ thống đang phân tích ngữ cảnh cho: **{st.session_state.work_category}**")
        
        input_col, output_col = st.columns([1, 1.4])
        with input_col:
            st.markdown("##### 🧩 Thiết lập bài toán cần bẻ gãy cấu trúc")
            
            if "Quản lý" in st.session_state.work_category:
                default_prompt = "Lập sơ đồ triển khai cổng thanh toán PayOS tự động hóa cho hệ thống"
            elif "Học tập" in st.session_state.work_category:
                default_prompt = "Giải chi tiết bài toán chứng minh bất đẳng thức Cauchy điểm rơi lệch tâm"
            elif "Lập trình" in st.session_state.work_category:
                default_prompt = "Xây dựng script Python tự động hóa đồng bộ dữ liệu API ngầm"
            else:
                default_prompt = "Xây dựng cấu trúc kịch bản video ngắn giữ chân người xem trong 3 giây đầu"
                
            target_goal = st.text_area("Nhập mục tiêu lớn của bạn:", value=default_prompt, height=90)
            
            st.markdown("##### 🧠 Bộ điều chỉnh tâm lý nhận thức (Cognitive Load Slider)")
            cognitive_load = st.select_slider(
                "Mức độ chi tiết mong muốn (Goblin Mode):",
                options=["Tổng quan dự án (Macro-milestones)", "Cấu trúc tiêu chuẩn (Standard Steps)", "Siêu nhỏ chống trì hoãn (Micro-steps)"]
            )
            st.caption("Nếu bạn đang thấy mệt mỏi hoặc lười, hãy chọn 'Siêu nhỏ' để AI chia việc cực kỳ dễ làm.")
            
            allowed_layers = 5 if "Free" not in st.session_state.tier else 3
            if allowed_layers == 3:
                st.info("💡 Tài khoản Free giới hạn rã 3 cấp độ. Lên gói PLUS để mở khóa chuyên sâu 5 tầng.")
            selected_depth = st.slider("Độ sâu bóc tách cấu trúc:", 1, 5, value=min(3, allowed_layers))
            
            st.markdown("##### ⚙️ Thiết lập điều phối luồng")
            execution_mode = st.radio("Cơ chế sắp xếp tác vụ:", ["Tuần tự có phụ thuộc (Linear Pipeline)", "Song song bất đồng bộ (Async Parallel)"])
            
            execute_calculation = st.button("🚀 KÍCH HOẠT LÕI QUANTUM DECOMPOSE", type="primary", use_container_width=True)
            
        with output_col:
            st.markdown("### 🗺️ Bản đồ tác vụ & Sơ đồ phụ thuộc (Dependency Map)")
            if execute_calculation:
                with st.spinner("Hệ thống đang bóc tách luồng tư duy..."):
                    time.sleep(0.5)
                
                computed_steps = request_ai_core_processing(target_goal, selected_depth, st.session_state.work_category, execution_mode, cognitive_load)
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Tổng số hạng mục con", f"{len(computed_steps)} việc cần làm")
                with c2:
                    base_hours = len(computed_steps) * (2 if "Siêu nhỏ" in cognitive_load else 6)
                    st.metric("Ước tính thời gian tối ưu", f"{base_hours} Giờ")
                with c3:
                    st.metric("Trạng thái nhận thức", "🛡️ Êm dịu" if "Siêu nhỏ" in cognitive_load else "⚡ Thử thách")
                
                st.write("")
                for idx, single_step in enumerate(computed_steps):
                    with st.container(border=True):
                        st.markdown(f"##### 📍 Bước {idx+1}: {single_step['title']}")
                        st.write(single_step['content'])
                        
                        sub_c1, sub_c2 = st.columns(2)
                        with sub_c1:
                            st.markdown(f"🔗 Tác vụ tiền đề: `{single_step['dep']}`")
                        with sub_c2:
                            color_map = {"Thấp": "green", "Trung bình": "orange", "Cao": "red"}
                            st.markdown(f"Mức độ rủi ro thắt nút: :{color_map.get(single_step['risk'], 'white')}[{single_step['risk']}]")
                
                st.write("---")
                st.markdown("##### 📥 Xuất dữ liệu cấu trúc")
                export_format = st.selectbox("Định dạng xuất file:", ["Markdown Document (.md)", "JSON Schema Flow (.json)"])
                if export_format == "Markdown Document (.md)":
                    md_output = f"# Bản đồ rã việc soloflowOS v9.0\nMục tiêu: {target_goal}\nMức độ nhận thức: {cognitive_load}\n\n"
                    for s in computed_steps:
                        md_output += f"## {s['title']}\n- Tiền đề: {s['dep']}\n- Nội dung: {s['content']}\n\n"
                    st.download_button("Tải tệp tin Markdown (.md)", md_output, file_name="soloflow_v9.md", use_container_width=True)
                else:
                    st.download_button("Tải tệp tin JSON (.json)", json.dumps(computed_steps, ensure_ascii=False, indent=4), file_name="soloflow_v9.json", use_container_width=True)
            else:
                st.info("Hạ tầng rã việc thông minh đã sẵn sàng. Hãy điền mục tiêu lớn bên trái để trải nghiệm lõi tư duy Linear kết hợp Goblin.")

    # ---------------------------------------------------------------------
    # 💬 TRỢ LÝ AI CHUYÊN GIA - CO-PILOT (TỰ ĐỘNG CHUYỂN PERSONA CHUYÊN SÂU)
    # ---------------------------------------------------------------------
    elif navigation_hub == "💬 Trợ lý AI Chuyên Gia (Co-Pilot)":
        if "💼 Quản lý" in st.session_state.work_category:
            persona_title = "Cố Vấn Tối Ưu Quy Trình Doanh Nghiệp (Linear Expert)"
            persona_desc = "Tôi giúp bạn tối ưu hóa dòng tiền, giảm thiểu các cuộc họp thừa thãi, thiết lập quy trình kiểm thử SOP và xây dựng chỉ số OKR thực chiến."
            placeholder_text = "Hỏi về cách xử lý thắt nút tiến độ hoặc quản trị dòng tiền..."
        elif "🎓 Học tập" in st.session_state.work_category:
            persona_title = "Trợ Lý Học Thuật Cấp Cao (Math & Literature Master)"
            persona_desc = "Tôi chuyên xử lý các bài toán Bất đẳng thức Cauchy điểm rơi nâng cao, bóc tách cấu trúc nghị luận văn học lớp 9 sâu sắc để đạt điểm tuyệt đối."
            placeholder_text = "Hỏi về phương pháp đổi biến bất đẳng thức hoặc hệ thống luận điểm văn học..."
        elif "💻 Lập trình" in st.session_state.work_category:
            persona_title = "Tech Lead Hệ Thống & Trợ Lý Kiến Trúc Phần Mềm"
            persona_desc = "Tôi hỗ trợ kiểm tra lỗi biên logic, tối ưu hóa các vòng lặp phức tạp, cấu trúc file JSON và làm sạch mã nguồn theo chuẩn Clean Code."
            placeholder_text = "Hỏi cách gỡ lỗi cấu trúc dữ liệu hoặc tối ưu hóa thuật toán..."
        else:
            persona_title = "Giám Đốc Nghệ Thuật & Chuyên Gia Tâm Lý Giữ Chân Khán Giả"
            persona_desc = "Tôi giúp bạn bẻ gãy cấu trúc kịch bản nội dung ngắn, phối bảng màu tương phản cao để đánh mạnh vào thị giác và kích hoạt tâm lý tò mò của người xem."
            placeholder_text = "Hỏi cách viết kịch bản chuyển đổi cao hoặc chọn tông màu layout..."

        st.title("💬 Trợ Lý AI Chuyên Gia Đa Nhiệm (AI Co-Pilot)")
        st.caption(f"Vai trò chuyên biệt hiện tại: **{persona_title}**")
        
        with st.container(border=True):
            st.markdown(f"**🤖 Định hình tư duy AI:** {persona_desc}")
        
        # Hiển thị bong bóng chat
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.markdown(f'<div class="chat-bubble-user"><b>👤 Bạn:</b><br>{chat["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bubble-ai"><b>🪐 AI Co-Pilot:</b><br>{chat["content"]}</div>', unsafe_allow_html=True)
                
        user_msg = st.chat_input(placeholder_text)
        if user_msg:
            st.session_state.chat_history.append({"role": "user", "content": user_msg})
            
            with st.spinner("AI đang xử lý thông tin ngầm..."):
                time.sleep(0.4)
                
            msg_lower = user_msg.lower()
            if "💼 Quản lý" in st.session_state.work_category:
                ai_reply = f"Giải quyết vấn đề '{user_msg}' đòi hỏi bạn phải xác định rõ 'Đâu là tác vụ chặn luồng (Blocker)'. Hãy dọn sạch điểm thắt nút đó trước, sau đó chia nhỏ công việc thành chu kỳ Sprints 2 tuần để đo lường hiệu suất thực tế của đội ngũ."
            elif "🎓 Học tập" in st.session_state.work_category:
                if "cauchy" in msg_lower or "bất đẳng thức" in msg_lower:
                    ai_reply = "Chào em, đối với bài toán bất đẳng thức Cauchy nâng cao, tư duy mấu chốt là xác định 'Điểm rơi'. Nếu các biến số thực lệch tâm, em hãy dùng phương pháp hằng số bất định, nhân thêm một hệ số thích hợp vào trước hạng tử để khi lấy căn bậc hai, chúng triệt tiêu hoàn toàn với mẫu số. Hãy viết nháp biểu thức đối xứng trước nhé!"
                else:
                    ai_reply = "Một mạch văn lập luận xuất sắc cần đi từ tổng quan hoàn cảnh sáng tác đến chi tiết tín hiệu thẩm mỹ. Ví dụ với truyện ngắn, em hãy mổ xẻ chiều sâu diễn biến tâm lý nhân vật qua các bước ngoặt tình huống truyện, sử dụng các từ nối logic để bài làm đạt điểm tối đa."
            elif "💻 Lập trình" in st.session_state.work_category:
                ai_reply = f"Để xử lý tác vụ logic '{user_msg}', kiến trúc tốt nhất là tách biệt hoàn toàn luồng nhận request từ client và luồng xử lý dữ liệu ngầm (Asynchronous Worker). Hãy xuất dữ liệu đầu ra dưới dạng JSON chuẩn hóa để dễ mở rộng mô hình sau này."
            else:
                ai_reply = "Trong sáng tạo nội dung, tâm lý giữ chân khán giả quyết định 90% thành công. Hãy đặt câu Hook dài dưới 3 giây đầu tiên đánh thẳng vào nỗi sợ bỏ lỡ thông tin (FOMO) của người xem, phối hợp cùng tông nền tối và chữ neon để tăng kích thích thị giác."
                
            st.session_state.chat_history.append({"role": "ai", "content": ai_reply})
            st.rerun()

    # ---------------------------------------------------------------------
    # ✨ SIÊU PHÂN HỆ TÂM LÝ HỌC ĐỘT PHÁ V9.0 (TÙY BIẾN THEO DANH MỤC)
    # ---------------------------------------------------------------------
    elif navigation_hub == "✨ Siêu Phân Hệ Tâm Lý Học":
        st.title("✨ Siêu Phân Hệ Tâm Lý Học & Công Cụ Chuyên Biệt v9.0")
        st.caption("Kích hoạt các bộ công cụ giải tỏa áp lực tâm lý và thúc đẩy hành động thực tế.")
        
        is_vip = "Bản Thường" not in st.session_state.tier
        
        # 💼 DANH MỤC: QUẢN LÝ & DOANH NGHIỆP
        if "💼 Quản lý" in st.session_state.work_category:
            st.markdown("### 🚨 Bộ Lọc Chống Kiệt Sức Dự Án (Burnout Risk Alert)")
            with st.container(border=True):
                st.markdown("##### 📊 Đo lường mức độ quá tải của đội ngũ vận hành")
                tasks_count = st.number_input("Số lượng tác vụ khẩn cấp đang tồn đọng:", value=5)
                meetings_count = st.number_input("Số giờ họp hành trung bình mỗi tuần (Giờ):", value=15)
                
                if st.button("Phân tích nguy cơ kiệt sức", type="primary", use_container_width=True):
                    if meetings_count > 12 or tasks_count > 7:
                        st.error("🚨 CẢNH BÁO: Đội ngũ đang rơi vào vùng kiệt sức nhận thức! Hãy cắt bỏ ít nhất 30% cuộc họp không cần thiết và chuyển bớt việc sang luồng song song.")
                    else:
                        st.success("🟢 Trạng thái an toàn. Năng lượng làm việc của đội ngũ đang được tối ưu.")
                        
            if is_vip:
                st.markdown("##### 💎 [Mở khóa VIP] Trình mô phỏng đường băng tài chính & Dự báo dòng tiền ròng")
                c1, c2 = st.columns(2)
                with c1: rev = st.number_input("Doanh thu tháng (VNĐ):", value=150000000)
                with c2: cost = st.number_input("Chi phí cố định (VNĐ):", value=60000000)
                st.info(f"Dòng tiền ròng hàng tháng: +{(rev - cost):,} VNĐ. Hệ thống tài chính vận hành an toàn.")
            else:
                st.warning("Nâng cấp gói PLUS để mở khóa Trình mô phỏng giả lập Runway dòng tiền doanh nghiệp.")

        # 🎓 DANH MỤC: HỌC TẬP & NGHIÊN CỨU
        elif "🎓 Học tập" in st.session_state.work_category:
            st.markdown("### 🧠 Bộ Kích Hoạt Phá Vỡ Trì Hoãn (Mental Block Breaker)")
            with st.container(border=True):
                st.markdown("##### 🛑 Bạn đang bị kẹt ý tưởng hoặc sợ bài toán quá khó?")
                subject_block = st.selectbox("Chọn trạng thái bạn đang gặp phải:", ["Sợ chứng minh điểm rơi bất đẳng thức", "Bị bí ý tưởng viết đoạn mở bài Ngữ Văn", "Sợ bài tập tiếng Anh chia động từ phức tạp"])
                
                if st.button("Kích hoạt phác thảo tư duy cấp tốc", type="primary", use_container_width=True):
                    if "bất đẳng thức" in subject_block.lower():
                        st.markdown("<div class='psychology-box'><b>💡 Mẹo tâm lý:</b> Đừng cố giải cả bài! Hãy viết đúng 3 dòng: Điều kiện xác định, biểu thức khi các biến bằng nhau, và viết lại vế trái dưới dạng phân số. Chỉ cần đặt bút viết 3 dòng này, não bạn sẽ tự động giải phóng nỗi sợ bài khó.</div>", unsafe_allow_html=True)
                        st.latex(r"\text{Điểm rơi đối xứng: } a = b = c \implies a^2 + b^2 + c^2 \ge ab + bc + ca")
                    else:
                        st.markdown("<div class='psychology-box'><b>💡 Mẹo tâm lý:</b> Hãy dùng phương pháp 'Viết tự do vô tri'. Viết ra bất kỳ câu nào xuất hiện trong đầu về tác phẩm mà không cần quan tâm hay dở trong 2 phút. Sau đó AI sẽ giúp bạn cấu trúc lại mạch lập luận chuẩn chỉnh.</div>", unsafe_allow_html=True)
                        
            if is_vip:
                st.markdown("##### 💎 [Mở khóa VIP] Lõi cấu trúc sơ đồ tư duy chuyên sâu")
                st.success("Mở khóa thành công bộ ngân hàng đề thi học sinh giỏi và cấu trúc luận điểm văn học lý luận chuyên sâu cấp độ 5.")
            else:
                st.warning("Nâng cấp gói PLUS để mở khóa Ma trận giải toán hình học và cấu trúc văn học nâng cao.")

        # 💻 DANH MỤC: LẬP TRÌNH & KỸ THUẬT
        elif "💻 Lập trình" in st.session_state.work_category:
            st.markdown("### 🦆 Trợ Lý Giải Thuật Vịt Cao Su (Rubber Duck Debugger)")
            with st.container(border=True):
                st.markdown("##### 🛠️ Hãy giải thích đoạn mã nguồn lỗi của bạn cho chú vịt AI")
                bug_desc = st.text_area("Đoạn code của bạn đang bị chạy sai logic như thế nào?", value="Vòng lặp for chạy qua danh sách nhưng bị bỏ sót phần tử cuối cùng...")
                
                if st.button("Hỏi Vịt Cao Su AI", use_container_width=True):
                    st.markdown("<div class='psychology-box'><b>🦆 Vịt AI nói:</b> Cậu đã kiểm tra lại điều kiện biên `range(len(arr))` hay `range(len(arr) - 1)` chưa? Việc giải thích lỗi ra thành lời chính là cách tốt nhất để cậu tự tìm ra câu trả lời đấy! Thử sửa lại điều kiện xem sao nhé.</div>", unsafe_allow_html=True)

        # 🎨 DANH MỤC: SÁNG TẠO & THIẾT KẾ
        else:
            st.markdown("### 🎯 Bộ Tiêu Diệt Áp Lực Sáng Tạo (Imposter Syndrome Killer)")
            with st.container(border=True):
                st.markdown("##### 📈 Đo lường tỷ lệ giữ chân người xem (Hook Rate Predictor)")
                hook_text = st.text_input("Nhập câu tiêu đề mở đầu video của bạn:", value="Bí mật mà không một lập trình viên nào muốn cho bạn biết...")
                
                if st.button("Dự đoán điểm thu hút thị giác", type="primary", use_container_width=True):
                    st.markdown("🔥 Điểm giữ chân dự kiến: **88% (Rất Cao)**")
                    st.markdown("<div class='psychology-box'><b>🎨 Lời khuyên layout:</b> Hãy dùng chữ màu Neon Xanh lục trên nền Đen tuyền chớp tắt để kích hoạt vùng chú ý của võng mạc người xem trong 3 giây đầu tiên!</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------------------
    # 📊 TRUNG TÂM HOẠCH ĐỊNH TIẾN ĐỘ SPRINTS
    # ---------------------------------------------------------------------
    elif navigation_hub == "📊 Hoạch Định Tiến Độ Sprints":
        st.title("📊 Trung Tâm Hoạch Định Tiến Độ Sprints & Biểu Đồ Chỉ Số")
        st.caption("Đồng bộ hóa trực tiếp lịch trình công việc thực tế của bạn lên hệ thống đồ thị trực quan.")
        
        c_add, c_view = st.columns([1, 1.4])
        with c_add:
            st.markdown("##### Thêm tác vụ hành động mới")
            new_item_name = st.text_input("Tên tác vụ:")
            new_item_hours = st.number_input("Số giờ đầu tư thực tế:", value=8, min_value=1)
            new_item_comp = st.selectbox("Độ phức tạp toán học/hệ thống:", ["Thấp", "Trung bình", "Cao"])
            if st.button("Đồng bộ lên đồ thị tiến độ", use_container_width=True):
                if new_item_name:
                    st.session_state.custom_sprints.append({"Hạng mục": new_item_name, "Thời gian (Giờ)": new_item_hours, "Độ phức tạp": new_item_comp})
                    st.toast("Đã đồng bộ thành công!")
                    
        with c_view:
            st.markdown("##### Biểu đồ phân bổ thời gian thực tế giữa các hạng mục Sprints")
            df_sprints = pd.DataFrame(st.session_state.custom_sprints)
            if not df_sprints.empty:
                st.bar_chart(data=df_sprints, x="Hạng mục", y="Thời gian (Giờ)", color="#ffffff")
                st.dataframe(df_sprints, use_container_width=True)

    # ---------------------------------------------------------------------
    # ⚙️ HỆ THỐNG PROFILE & SETTINGS
    # ---------------------------------------------------------------------
    elif navigation_hub == "⚙️ Hồ Sơ & Cài Đặt Hệ Thống":
        st.title("⚙️ Hồ Sơ Người Điều Hành & Tùy Chỉnh Hệ Thống")
        st.caption("Quản lý thông tin định danh nút dữ liệu cá nhân cục bộ.")
        
        prof_col, sett_col = st.columns(2)
        with prof_col:
            st.markdown("### 👤 Cấu Hình Node Cá Nhân")
            with st.container(border=True):
                st.markdown(f"""
                <div style='background-color: #0c0c0c; border: 1px solid #222222; padding: 20px; border-radius: 10px; margin-bottom: 15px;'>
                    <span style='font-size: 10px; color: #666666; font-family: monospace;'>LOCAL CORE NODE</span>
                    <h2 style='margin: 4px 0; color: #ffffff;'>{st.session_state.profile_fullname}</h2>
                    <p style='margin: 0 0 10px 0; color: #888888; font-style: italic; font-size: 14px;'>{st.session_state.profile_role}</p>
                    <span style='background-color: #ffffff; color: #000000; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: bold;'>{st.session_state.tier.upper()}</span>
                </div>
                """, unsafe_allow_html=True)
                
                new_fn = st.text_input("Họ và tên chủ tài khoản:", value=st.session_state.profile_fullname)
                new_rl = st.text_input("Vị trí đảm nhiệm hiện tại:", value=st.session_state.profile_role)
                new_bio = st.text_area("Tiểu sử ngắn gọn:", value=st.session_state.profile_bio)
                
                if st.button("保存 - LƯU THÔNG TIN HỒ SƠ", use_container_width=True):
                    st.session_state.profile_fullname = new_fn
                    st.session_state.profile_role = new_rl
                    st.session_state.profile_bio = new_bio
                    st.toast("Đã đồng bộ thông tin hồ sơ người dùng.")
                    st.rerun()

        with sett_col:
            st.markdown("### ⚙️ Cấu Hình Mô Hình Trí Tuệ")
            with st.container(border=True):
                st.session_state.settings_ai_temp = st.slider(
                    "Độ sáng tạo chuyên sâu của AI (AI Temperature):",
                    0.0, 1.0, value=st.session_state.settings_ai_temp, step=0.1
                )
                st.caption("Giá trị thấp giúp câu trả lời mang tính logic, chính xác cao; giá trị cao tăng tính đột phá sáng tạo ý tưởng.")
                
                st.session_state.settings_secure_mode = st.toggle(
                    "Kích hoạt chế độ mã hóa dữ liệu cục bộ AES-256",
                    value=st.session_state.settings_secure_mode
                )
                st.session_state.settings_theme = st.selectbox(
                    "Chọn kiến trúc bảng màu giao diện chủ đạo:",
                    ["Đen tuyền Premium (Jet Black)", "Xám sâu không gian (Space Gray)"]
                )

    # ---------------------------------------------------------------------
    # GIAO DIỆN NĂNG CẤP GÓI CHUẨN PREMIUM DARK MODE
    # ---------------------------------------------------------------------
    elif navigation_hub == "💰 Nâng Cấp PLUS & LIFETIME":
        show_plus_pricing_view()

    # ---------------------------------------------------------------------
    # CỔNG THANH TOÁN PAYOS TỰ ĐỘNG
    # ---------------------------------------------------------------------
    elif navigation_hub == "💳 Cổng Thanh Toán PayOS":
        st.title("💳 Xác Thực Hóa Đơn Tự Động Qua Cổng PayOS")
        
        left_invoice, right_qrcode = st.columns([1, 1.1])
        with left_invoice:
            st.subheader("🧾 Chi tiết hóa đơn khởi tạo")
            st.write("Đơn vị thụ hưởng: **soloflowOS Global Core**")
            
            billing_amount = 99000
            billing_title = "Giấy phép Gói Tháng PLUS Premium"
            
            if "payos_target" in st.session_state and st.session_state.payos_target == "LIFETIME":
                billing_amount = 499000
                billing_title = "Giấy phép Sở hữu TRỌN ĐỜI (Lifetime) VIP"
                
            st.markdown(f"Sản phẩm đăng ký: **{billing_title}**")
            st.write("---")
            st.markdown(f"### Tổng chi phí cần thanh toán: <span style='color: #ffffff; text-decoration: underline;'>{billing_amount:,} VNĐ</span>", unsafe_allow_html=True)
            
            if st.button("🔗 Khởi tạo Link liên kết hóa đơn PayOS", type="primary", use_container_width=True):
                st.session_state.invoice_id = str(random.randint(111111, 999999))
                st.success(f"Khởi tạo hóa đơn thành công đơn hàng: #{st.session_state.invoice_id}")
                
        with right_qrcode:
            st.subheader("📲 Quét mã VietQR PayOS mã hóa")
            if "invoice_id" in st.session_state and st.session_state.invoice_id:
                st.markdown(f"""
                <div style='border: 2px solid #ffffff; padding: 25px; border-radius: 12px; text-align: center; background-color: #000000;'>
                    <p style='font-weight: bold; letter-spacing: 1px;'>ĐỐI TÁC THANH TOÁN PAYOS CHÍNH THỨC</p>
                    <div style='background-color: #ffffff; width: 200px; height: 200px; margin: 20px auto; padding: 15px; display: flex; align-items: center; justify-content: center;'>
                        <p style='color: #000000; font-size: 11px; font-weight: bold;'>[ MÃ VIETQR CHUYỂN KHOẢN ]<br>ĐÃ MÃ HÓA BẢO MẬT<br>ĐƠN HÀNG #{st.session_state.invoice_id}</p>
                    </div>
                    <p style='font-size: 14px;'>Nội dung chuyển khoản chính xác: <br><b>SOLOFLOW {st.session_state.invoice_id}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                if st.button("🔄 Kiểm tra xác thực trạng thái Webhook", use_container_width=True):
                    with st.spinner("Đang kiểm tra kết nối cổng ngân hàng ngân hàng đối tác..."):
                        time.sleep(0.8)
                    st.session_state.tier = "Thành viên PLUS" if billing_amount == 99000 else "Thành viên LIFETIME VIP"
                    st.balloons()
                    st.success("🎉 Giao dịch thành công! Toàn bộ tính năng rã việc nâng cao cấp độ 5 đã được kích hoạt.")
            else:
                st.warning("Vui lòng kích hoạt tạo hóa đơn ở khu vực bên trái để tổng hợp mã QR.")

# =========================================================================
# GIAO DIỆN BẢNG GIÁ ĐĂNG KÝ MUA GÓI PREMUM
# =========================================================================
def show_plus_pricing_view():
    st.write("---")
    col_free, col_plus, col_lifetime = st.columns(3)
    
    with col_free:
        st.markdown("""
        <div style='background-color: #040404; color: #888888; border: 1px solid #1a1a1a; padding: 30px; border-radius: 14px; height: 100%;'>
            <h3 style='color: #555555; margin-top:0;'>Bản Tiêu Chuẩn</h3>
            <h2>0 đ <span style='font-size:14px; color:#444444;'>/ Vĩnh viễn</span></h2>
            <hr style='border-color: #222222;'>
            <p>✅ Truy cập phân hệ chức năng cơ bản theo danh mục</p>
            <p>✅ Công cụ quản lý tiến độ cá nhân</p>
            <p>❌ Khóa sơ đồ phân rã công việc sâu đa tầng cấp độ cao</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.button("Hệ điều hành hiện tại đang chạy gói này", disabled=True, use_container_width=True)
        
    with col_plus:
        st.markdown("""
        <div class="plus-card-premium">
            <h3 style='color: #ffffff; font-weight: 800; font-size: 24px; margin-top:0;'>⚡ soloflowOS PLUS</h3>
            <h2 style='color: #ffffff; font-size: 32px; font-weight: 900;'>99.000 đ <span style='font-size:14px; color:#888888;'>/ Tháng</span></h2>
            <hr style='border-color: #333333;'>
            <p style='color: #ffffff;'>⚡ Mở khóa toàn bộ các siêu công cụ tính toán tương tác thực tế</p>
            <p style='color: #ffffff;'>⚡ Mở khóa không giới hạn số lần gọi Lõi xử lý AI đa luồng</p>
            <p style='color: #ffffff;'>⚡ Mở khóa sơ đồ phân rã đa tầng sâu cấp độ năm chi tiết</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("🔥 KÍCH HOẠT ĐĂNG KÝ BẢN PLUS THÁNG", type="primary", use_container_width=True):
            st.session_state.payos_target = "PLUS"
            st.toast("Đã cấu hình hóa đơn sang Gói Tháng PLUS! Vui lòng vào mục Cổng Thanh Toán PayOS.")
            
    with col_lifetime:
        st.markdown("""
        <div class="plus-card-premium" style="border: 2px solid #ffffff !important; box-shadow: 0px 0px 25px rgba(255,255,255,0.2) !important;">
            <h3 style='color: #ffffff; font-weight: 800; font-size: 24px; margin-top:0;'>👑 VIP LIFETIME</h3>
            <h2 style='color: #ffffff; font-size: 32px; font-weight: 900;'>499.000 đ <span style='font-size:14px; color:#888888;'>/ Sở hữu trọn đời</span></h2>
            <hr style='border-color: #333333;'>
            <p style='color: #ffffff;'>👑 Thanh toán một lần duy nhất - Sở hữu vĩnh viễn</p>
            <p style='color: #ffffff;'>👑 Bao gồm toàn bộ các siêu công cụ tương tác thực tế bản PLUS</p>
            <p style='color: #ffffff;'>👑 Cấp khóa SSL Sandbox mã hóa riêng biệt bảo vệ dữ liệu</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("👑 SỞ HỮU TRỌN ĐỜI VĨNH VIỄN", use_container_width=True):
            st.session_state.payos_target = "LIFETIME"
            st.toast("Đã cấu hình hóa đơn sang Gói TRỌN ĐỜI! Vui lòng vào mục Cổng Thanh Toán PayOS.")

# =========================================================================
# KHỞI CHẠY LUỒNG ĐIỀU PHỐI CHÍNH CỦA ỨNG DỤNG
# =========================================================================
def main():
    if "invoice_id" not in st.session_state:
        st.session_state.invoice_id = None
        
    if not st.session_state.logged_in:
        show_authentication_gateway()
    else:
        show_central_dashboard()

if __name__ == "__main__":
    main()
