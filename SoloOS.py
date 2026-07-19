import streamlit as st
import pandas as pd
import time
import datetime
import random
import json

# =========================================================================
# CẤU HÌNH HỆ THỐNG TOÀN CỤC & BRANDING THƯƠNG HIỆU SOLOFLOWOS
# =========================================================================
st.set_page_config(
    page_title="soloflowOS v7.5 - Next-Gen AI Workspace",
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

# Bộ nhớ Trợ lý AI Chatbot
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Lưu trữ thông tin Profile cá nhân
if "profile_fullname" not in st.session_state:
    st.session_state.profile_fullname = "Trần Đình Hiệp"
if "profile_role" not in st.session_state:
    st.session_state.profile_role = "Core Developer / Product Manager"
if "profile_bio" not in st.session_state:
    st.session_state.profile_bio = "Đang tối ưu hóa các phân hệ AI đa luồng song song."

# Lưu trữ các tùy chỉnh Settings hệ thống
if "settings_ai_temp" not in st.session_state:
    st.session_state.settings_ai_temp = 0.7
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

# PHỦ CSS PREMIUM MINIMALIST DARK MODE (NỀN ĐEN TUYỀN, CHỮ TRẮNG, VIỀN SÁNG COGNITIVE)
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #ffffff; }
    div[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #222222; }
    .plus-card-premium {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        padding: 30px;
        border-radius: 14px;
        box-shadow: 0px 4px 25px rgba(255, 255, 255, 0.1);
    }
    .profile-badge {
        background-color: #111111;
        border: 1px solid #333333;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .chat-bubble-user {
        background-color: #222222; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 3px solid #ffffff;
    }
    .chat-bubble-ai {
        background-color: #111111; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 3px solid #888888;
    }
</style>
""", unsafe_allow_html=True)

def draw_soloflow_brand(is_sidebar=False):
    brand_html = """
    <div style='text-align: center; padding: 15px 0; border-bottom: 1px solid #222222; margin-bottom: 20px;'>
        <div style='font-size: 28px; font-weight: 900; color: #ffffff; letter-spacing: 1px;'>🪐 soloflowOS</div>
        <div style='font-size: 10px; color: #888888; font-family: monospace; letter-spacing: 2px; margin-top: 4px;'>NEXT-GEN AI WORKSPACE</div>
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
    _, central_panel, _ = st.columns([1, 1.4, 1])
    with central_panel:
        st.markdown("<h3 style='text-align: center; color: white;'>Hệ Thống Phân Tách Tác Vụ Song Song</h3>", unsafe_allow_html=True)
        login_tab, register_tab = st.tabs(["🔒 ĐĂNG NHẬP CORE", "📝 ĐĂNG KÝ SANDBOX NODE"])
        
        with login_tab:
            u_name = st.text_input("Định danh tài khoản (Username)", key="auth_u")
            u_pass = st.text_input("Khóa bảo mật (Password)", type="password", key="auth_p")
            if st.button("KÍCH HOẠT PHIÊN LÀM VIỆC", type="primary", use_container_width=True):
                if u_name and u_pass:
                    st.session_state.logged_in = True
                    st.session_state.username = u_name
                    st.success("Xác thực chứng chỉ thành công. Đang tải hạ tầng lưu trữ...")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Vui lòng điền đầy đủ thông tin xác thực tài khoản.")
                    
        with register_tab:
            st.caption("Khởi tạo một Node dữ liệu mới cục bộ để phân tách tác vụ đa nhiệm.")
            st.text_input("Họ và tên người sử dụng")
            st.text_input("Định danh Node mới")
            st.text_input("Tạo mã khóa bảo mật mới", type="password")
            if st.button("KHỞI TẠO CƠ SỞ DỮ LIỆU MỚI", use_container_width=True):
                st.success("Tạo Node thành công. Vui lòng quay lại tab Đăng nhập để kích hoạt.")

# =========================================================================
# LÕI XỬ LÝ MÔ HÌNH AI PHÂN RÃ THEO DANH MỤC CÔNG VIỆC DYNAMIC
# =========================================================================
def request_ai_core_processing(query, layer_depth, category, split_mode="Xần tuần tự (Sequential)"):
    q_lower = query.lower()
    nodes_generated = []
    
    # Giả lập bóc tách dựa theo danh mục công việc được chọn
    if "Quản lý" in category:
        nodes_generated = [
            {"title": "Thiết lập mục tiêu chiến lược và Chỉ số đo lường then chốt OKR/KPI", "content": "Xác định rõ ràng mục tiêu cốt lõi của tổ chức, định lượng các kết quả then chốt cần đạt được trong chu kỳ doanh nghiệp.", "type": "Tác vụ nền tảng", "risk": "Thấp"},
            {"title": "Phân tách cấu trúc dự án thành danh mục Epic và User Stories chi tiết", "content": "Bẻ nhỏ sản phẩm lớn thành các phân hệ tính năng độc lập, viết đặc tả yêu cầu nghiệp vụ dưới góc nhìn giá trị người dùng.", "type": "Luồng độc lập", "risk": "Trung bình"},
            {"title": "Ước tính thời lượng thực thi và phân bổ Sprints lập tiến độ", "content": "Áp dụng quy trình Scrum Poker, gán người phụ trách trực tiếp và đặt thời hạn kết thúc (Milestones) cho từng hạng mục.", "type": "Luồng song song", "risk": "Cao"},
            {"title": "Xây dựng ma trận quản trị rủi ro vận hành và Dự báo điểm nghẽn cổ chai", "content": "Phân tích các tác nhân có thể gây trễ hạn tiến độ, lập kế hoạch nhân sự và hạ tầng kỹ thuật dự phòng lập tức.", "type": "Luồng giám sát", "risk": "Trung bình"},
            {"title": "Chuẩn hóa luồng phê duyệt và Quy trình kiểm thử đóng gói bàn giao sản phẩm", "content": "Thiết lập các tiêu chuẩn nghiệm thu chất lượng nghiêm ngặt (SOP) trước khi đưa sản phẩm ra thị trường.", "type": "Hậu kỳ khóa đuôi", "risk": "Thấp"}
        ]
    elif "Học tập" in category:
        if "toán" in q_lower or "bất đẳng thức" in q_lower or "cauchy" in q_lower:
            nodes_generated = [
                {"title": "Xác định tập xác định và Dự đoán điểm rơi đối xứng đại số", "content": "Phân tích điều kiện chặt của biến số thực. Thiết lập dấu bằng xảy ra để tìm mối quan hệ tuyến tính giữa các biến.", "type": "Tác vụ nền tảng", "risk": "Thấp"},
                {"title": "Cấu trúc sơ đồ thêm bớt hạng tử để áp dụng Cauchy (AM-GM)", "content": "Thực hiện kỹ thuật tách đa thức mẫu số, nhân thêm hằng số bất định nhằm ép các hạng tử triệt tiêu nhau khi lấy căn bậc hai.", "type": "Luồng song song", "risk": "Cao"},
                {"title": "Đánh giá bất đẳng thức thành phần và Cộng vế đối xứng", "content": "Áp dụng định lý Cauchy cho từng cặp số phức hợp, thực hiện phép cộng luân phiên nhằm làm gọn vế trái bài toán.", "type": "Hậu kỳ khóa đuôi", "risk": "Trung bình"}
            ]
        else:
            nodes_generated = [
                {"title": "Định vị hoàn cảnh sáng tác tác phẩm và Khai triển luận điểm mở bài", "content": "Dẫn dắt thông tin tác giả, thời đại lịch sử, trích dẫn trực tiếp vấn đề nghị luận văn học cốt lõi.", "type": "Tác vụ nền tảng", "risk": "Thấp"},
                {"title": "Bóc tách diễn biến hành động và Chi tiết nghệ thuật đắt giá của nhân vật", "content": "Mổ xẻ sâu tâm lý nhân vật thông qua các bước ngoặt của cốt truyện, ngôn ngữ đối thoại đối thoại nội tâm.", "type": "Luồng độc lập", "risk": "Trung bình"},
                {"title": "Giải mã các tín hiệu thẩm mỹ, Nghệ thuật xây dựng tình huống truyện", "content": "Đánh giá bút pháp tả cảnh ngụ tình, cấu trúc tương phản hoặc nghệ thuật sử dụng các biểu tượng ẩn dụ nghệ thuật.", "type": "Hậu kỳ khóa đuôi", "risk": "Thấp"}
            ]
    elif "Lập trình" in category:
        nodes_generated = [
            {"title": "Phân tích kiến trúc hệ thống và Thiết kế cơ sở dữ liệu (Database Schema)", "content": "Xác định cấu trúc các bảng dữ liệu, thiết lập mối quan hệ và tối ưu hóa các chỉ mục index để truy vấn tăng tốc.", "type": "Tác vụ nền tảng", "risk": "Cao"},
            {"title": "Xây dựng các Module API Core và Xử lý logic nghiệp vụ luồng xử lý", "content": "Viết mã nguồn xử lý các luồng dữ liệu chính, tích hợp cơ chế bắt lỗi ngoại lệ và kiểm soát log hệ thống.", "type": "Luồng song song", "risk": "Trung bình"},
            {"title": "Kiểm thử tự động (Unit Test / Integration Test) và Tối ưu hóa hiệu năng", "content": "Chạy các kịch bản kiểm thử tự động để phát hiện lỗi logic biên, thực hiện tối ưu hóa cấu trúc vòng lặp và bộ nhớ đệm cache.", "type": "Hậu kỳ khóa đuôi", "risk": "Thấp"}
        ]
    else: # Sáng tạo & Thiết kế
        nodes_generated = [
            {"title": "Nghiên cứu thị hiếu khán giả và Phát triển ý tưởng chủ đạo (Concept)", "content": "Phân tích dữ liệu xu hướng hiện hành, định vị phong cách nghệ thuật độc bản và thiết lập thông điệp cốt lõi.", "type": "Tác vụ nền tảng", "risk": "Thấp"},
            {"title": "Xây dựng kịch bản phân cảnh chi tiết và Phác thảo bố cục (Storyboard)", "content": "Bẻ nhỏ cấu trúc nội dung thành từng phân đoạn, thiết kế sơ đồ phân bổ nhịp điệu hình ảnh.", "type": "Luồng độc lập", "risk": "Trung bình"},
            {"title": "Sản xuất chất liệu mỹ thuật nghệ thuật và Tinh chỉnh hậu kỳ tối ưu", "content": "Thiết kế chi tiết đồ họa, chỉnh sửa màu sắc đồng bộ, đồng nhất nhận diện thương hiệu trên mọi kênh truyền tải.", "type": "Hậu kỳ khóa đuôi", "risk": "Cao"}
        ]
            
    # Nếu chọn luồng song song, AI sắp xếp lại nhãn loại tác vụ tối ưu
    if "Mô phỏng Đa luồng" in split_mode:
        for node in nodes_generated:
            if node["type"] == "Luồng độc lập":
                node["type"] = "Luồng song song Async"
                
    return nodes_generated[:layer_depth]

# =========================================================================
# MÔ-ĐUN QUẢN TRỊ VÀ TRỰC QUAN HÓA TOÀN BỘ CHỨC NĂNG HỆ THỐNG
# =========================================================================
def show_central_dashboard():
    draw_soloflow_brand(is_sidebar=True)
    
    st.sidebar.markdown(f"👤 Tài khoản: **{st.session_state.username}**")
    st.sidebar.markdown(f"🎖️ Phân quyền: `{st.session_state.tier}`")
    
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
        "🧭 TRÌNH ĐIỀU HƯỚNG LÕI OS:",
        [
            "📋 Lõi AI Phân Rã Việc",
            "💬 Trợ lý AI Đa Nhiệm",
            "✨ Phân Hệ Tính Năng Dynamic",
            "📊 Hoạch Định Tiến Độ Sprints",
            "⚙️ Hồ Sơ & Cài Đặt Hệ Thống",
            "💰 Nâng Cấp PLUS & LIFETIME",
            "💳 Cổng Thanh Toán PayOS"
        ]
    )
    
    st.sidebar.write("---")
    if st.sidebar.button("🚪 Đăng xuất khỏi hệ thống", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.chat_history = []
        st.rerun()

    # ---------------------------------------------------------------------
    # 📋 LÕI AI PHÂN RÃ VIỆC (ĐÃ ĐỘT PHÁ TÍNH NĂNG)
    # ---------------------------------------------------------------------
    if navigation_hub == "📋 Lõi AI Phân Rã Việc":
        st.title("📋 Lõi Phân Rã Công Việc Đa Tầng Tích Hợp AI (Bản Cập Nhật Nâng Cao)")
        st.caption(f"Đang hoạt động trên phân hệ dữ liệu: **{st.session_state.work_category}**")
        
        input_col, output_col = st.columns([1, 1.4])
        with input_col:
            st.markdown("##### Thiết lập bài toán cần bẻ gãy cấu trúc")
            
            if "Quản lý" in st.session_state.work_category:
                default_prompt = "Lập sơ đồ Sprints phát triển tính năng cổng thanh toán PayOS cho hệ điều hành"
            elif "Học tập" in st.session_state.work_category:
                default_prompt = "Giải chi tiết bất đẳng thức Cauchy điểm rơi lệch tâm đề thi học sinh giỏi toán"
            elif "Lập trình" in st.session_state.work_category:
                default_prompt = "Thiết kế kiến trúc hệ thống Microservices cho ứng dụng thương mại điện tử phân tán"
            else:
                default_prompt = "Xây dựng kế hoạch sản xuất chuỗi video ngắn Viral Content trên các nền tảng số"
                
            target_goal = st.text_area("Nhập công việc cần xử lý phân rã:", value=default_prompt, height=100)
            
            allowed_layers = 5 if "PLUS" in st.session_state.tier or "LIFETIME" in st.session_state.tier else 2
            if allowed_layers == 2:
                st.info("💡 Gói Free giới hạn phân rã cấp độ 2. Lên gói PLUS để mở khóa chuyên sâu cấp độ 5.")
                
            selected_depth = st.slider("Độ sâu bóc tách cấu trúc kiến trúc:", 1, 5, value=min(2, allowed_layers))
            
            st.markdown("##### Tùy chọn cấu hình lõi phân toán sâu")
            execution_mode = st.radio("Chế độ phân phối tác vụ con:", ["Tuần tự tuyến tính (Sequential)", "Mô phỏng Đa luồng song song (Asynchronous Parallel)"])
            complexity_level = st.select_slider("Độ phức tạp hệ thống:", options=["Thấp", "Trung bình", "Phức tạp hệ thống"])
            
            st.markdown("##### Bộ lọc phân tích rủi ro đột phá")
            enable_risk_tag = st.checkbox("Tự động gán thẻ chỉ số rủi ro (Risk Matrix Tag)", value=True)
            ai_safety_buffer = st.checkbox("Tự động cộng thêm thời gian dự phòng rủi ro biến số", value=True)
            
            execute_calculation = st.button("🪄 KHỞI CHẠY LÕI PHÂN TÍCH AI V7.5", type="primary", use_container_width=True)
            
        with output_col:
            st.markdown("### Bản đồ cấu trúc & Khung điều phối tiến độ")
            if execute_calculation:
                with st.spinner("Đang kích hoạt ma trận xử lý thuật toán song song..."):
                    time.sleep(0.6)
                
                computed_steps = request_ai_core_processing(target_goal, selected_depth, st.session_state.work_category, execution_mode)
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Tổng số hạng mục con", f"{len(computed_steps)} tác vụ")
                with c2:
                    estimated_hours = len(computed_steps) * (8 if complexity_level == "Phức tạp hệ thống" else 4)
                    if ai_safety_buffer: estimated_hours = int(estimated_hours * 1.25)
                    st.metric("Thời gian thực thi tối ưu", f"{estimated_hours} Giờ")
                with c3:
                    st.metric("Cấu hình điều phối", "Đa luồng" if "Mô phỏng" in execution_mode else "Tuyến tự")
                
                st.write("")
                # Hiển thị kết quả kèm tính năng nâng cao
                for idx, single_step in enumerate(computed_steps):
                    with st.container(border=True):
                        st.markdown(f"##### 📍 Hạng mục {idx+1}: {single_step['title']}")
                        st.write(single_step['content'])
                        
                        sub_c1, sub_c2 = st.columns(2)
                        with sub_c1:
                            st.markdown(f"Phân loại luồng: `{single_step['type']}`")
                        with sub_c2:
                            if enable_risk_tag:
                                color_map = {"Thấp": "green", "Trung bình": "orange", "Cao": "red"}
                                st.markdown(f"Mức độ rủi ro: : {color_map.get(single_step['risk'], 'white')}[{single_step['risk']}]")
                
                # Tính năng xuất khẩu dữ liệu đột phá mới bổ sung
                st.write("---")
                st.markdown("##### 📥 Xuất cấu trúc tài liệu phân rã")
                export_format = st.selectbox("Định dạng xuất:", ["Markdown Document (.md)", "JSON Data Flow (.json)"])
                if export_format == "Markdown Document (.md)":
                    md_output = f"# Bản đồ Phân Rã: {target_goal}\n\n"
                    for s in computed_steps:
                        md_output += f"## {s['title']}\n- Luồng: {s['type']}\n- Rủi ro: {s['risk']}\n- Nội dung: {s['content']}\n\n"
                    st.download_button("Tải xuống tệp tin Markdown", md_output, file_name="soloflow_decomp.md", use_container_width=True)
                else:
                    st.download_button("Tải xuống tệp tin JSON Schema", json.dumps(computed_steps, ensure_ascii=False, indent=4), file_name="soloflow_schema.json", use_container_width=True)
            else:
                st.info("Hạ tầng phân rã AI đã sẵn sàng. Hãy nhập mục tiêu và nhấn nút để xem luồng bóc tách dữ liệu nâng cao.")

    # ---------------------------------------------------------------------
    # 💬 TRỢ LÝ AI ĐA NHIỆM (TÍNH NĂNG MỚI BỔ SUNG ĐỘT PHÁ)
    # ---------------------------------------------------------------------
    elif navigation_hub == "💬 Trợ lý AI Đa Nhiệm":
        # Xác định Persona dựa trên danh mục công việc được lựa chọn bên ngoài Sidebar
        if "💼 Quản lý" in st.session_state.work_category:
            persona_title = "Cố Vấn Quản Trị Chiến Lược & Vận Hành Doanh Nghiệp"
            persona_desc = "Tôi sẽ giúp bạn giải quyết các bài toán về tối ưu hóa mô hình OKR, quản lý rủi ro dự án Sprints, lập mô hình tài chính và tối ưu hiệu suất nhân sự."
            placeholder_text = "Hỏi về cách tối ưu chi phí vận hành hoặc xây dựng KPI..."
        elif "🎓 Học tập" in st.session_state.work_category:
            persona_title = "Chuyên Gia Học Thuật & Trợ Lý Giải Thuật Cao Cấp"
            persona_desc = "Chuyên gia bóc tách các bài toán Bất đẳng thức phức tạp (AM-GM/Cauchy), phân tích cấu trúc sơ đồ luận điểm Ngữ Văn lớp 9 thi vào lớp 10 ôn luyện chuyên sâu."
            placeholder_text = "Hỏi về phương pháp chứng minh điểm rơi bất đẳng thức hoặc lập dàn ý văn học..."
        elif "💻 Lập trình" in st.session_state.work_category:
            persona_title = "Kiến Trúc Sư Hệ Thống & Tech Lead Công Nghệ AI"
            persona_desc = "Hỗ trợ bạn gỡ lỗi cấu trúc mã nguồn, thiết kế sơ đồ cơ sở dữ liệu quan hệ, tối ưu luồng Webhook và xây dựng mô hình tự động hóa nâng cao."
            placeholder_text = "Hỏi về cách thiết kế Database, sửa lỗi JSON hoặc tạo luồng API..."
        else:
            persona_title = "Giám Đốc Sáng Tạo & Chuyên Gia Tối Ưu Chiến Dịch Viral"
            persona_desc = "Chuyên gia tư vấn xây dựng cấu trúc kịch bản phân cảnh video ngắn, phân tích bảng phối màu HEX và lên ý tưởng tiêu đề thu hút giữ chân người xem."
            placeholder_text = "Hỏi về cách viết hook giữ chân khán giả hoặc cách lên bảng màu layout..."

        st.title("💬 Trợ Lý AI Đa Nhiệm Tích Hợp Sâu (AI Co-Pilot)")
        st.caption(f"Hệ thống tự động điều chỉnh vai trò chuyên gia: **{persona_title}**")
        
        with st.container(border=True):
            st.markdown(f"**🤖 Định hình Persona hiện tại:** {persona_desc}")
        
        # Hiển thị lịch sử hội thoại dạng Bong bóng chat tối giản
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.markdown(f'<div class="chat-bubble-user"><b>👤 Bạn:</b><br>{chat["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bubble-ai"><b>🪐 Trợ lý AI ({st.session_state.work_category.split()[-1]}):</b><br>{chat["content"]}</div>', unsafe_allow_html=True)
                
        # Khung nhập tin nhắn
        user_msg = st.chat_input(placeholder_text)
        if user_msg:
            # Ghi nhận tin nhắn người dùng
            st.session_state.chat_history.append({"role": "user", "content": user_msg})
            
            # Giả lập phản hồi thông minh dựa trên danh mục
            with st.spinner("AI đang phân tích ngữ cảnh câu hỏi..."):
                time.sleep(0.5)
                
            ai_reply = ""
            msg_lower = user_msg.lower()
            if "💼 Quản lý" in st.session_state.work_category:
                ai_reply = f"Đối với vấn đề '{user_msg}' trong doanh nghiệp, chiến lược cốt lõi là bẻ nhỏ thành các Key Results đo lường được. Bạn nên áp dụng sơ đồ Sprints 2 tuần để kiểm tra tính khả thi và đo lường trực tiếp điểm nghẽn về dòng tiền hoặc nhân sự."
            elif "🎓 Học tập" in st.session_state.work_category:
                if "cauchy" in msg_lower or "bất đẳng thức" in msg_lower:
                    ai_reply = "Để giải bài toán bất đẳng thức này, bước đầu tiên cực kỳ quan trọng là dự đoán 'Điểm rơi hình học hoặc đại số'. Nếu các biến đối xứng, hãy thử đặt chúng bằng nhau. Nếu lệch tâm, ta dùng kỹ thuật nhân hằng số bất định để triệt tiêu bậc cao khi áp dụng định lý AM-GM."
                else:
                    ai_reply = "Một bài văn nghị luận xuất sắc cần có cấu trúc 3 phần chặt chẽ. Ở luận điểm này, em nên bóc tách diễn biến nội tâm nhân vật qua các chi tiết nghệ thuật đắt giá, kết hợp các từ nối tư duy logic để làm nổi bật thông điệp của tác giả."
            elif "💻 Lập trình" in st.session_state.work_category:
                ai_reply = f"Luồng logic cho hệ thống xử lý tác vụ '{user_msg}' nên được cấu trúc tách biệt giữa API xử lý và Worker xử lý ngầm (Asynchronous Background Task). Sử dụng mã hóa cấu trúc đầu ra chuẩn JSON để đảm bảo tính mở mở rộng luồng."
            else:
                ai_reply = "Để tối ưu ý tưởng sáng tạo này, hãy áp dụng quy tắc 3 giây đầu tiên (The Hook) đánh thẳng vào nỗi đau hoặc sự tò mò của người xem. Bố cục hình ảnh nên đi theo bảng phối màu tương phản cao (như Minimalist Dark kết hợp Neon Accent) để giữ chân mắt người dùng."
                
            st.session_state.chat_history.append({"role": "ai", "content": ai_reply})
            st.rerun()

    # ---------------------------------------------------------------------
    # ✨ PHÂN HỆ TÍNH NĂNG DYNAMIC (ĐÃ ĐỘT PHÁ TĂNG CƯỜNG CHỨC NĂNG)
    # ---------------------------------------------------------------------
    elif navigation_hub == "✨ Phân Hệ Tính Năng Dynamic":
        st.title("✨ Phân Hệ Các Tính Năng Tương Tác Chuyên Biệt V7.5")
        st.caption(f"Hệ thống tự động kích hoạt bộ công cụ phù hợp nhất cho danh mục: **{st.session_state.work_category}**")
        
        is_vip = "Bản Thường" not in st.session_state.tier
        
        # 💼 DANH MỤC: QUẢN LÝ & DOANH NGHIỆP
        if "💼 Quản lý" in st.session_state.work_category:
            tab_free, tab_plus = st.tabs(["🚀 Công Cụ Tiêu Chuẩn (Free)", "💎 Siêu Chức Năng Quản Trị (PLUS VIP)"])
            with tab_free:
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    with st.container(border=True):
                        st.markdown("##### 🪐 Trình đếm ngược mốc bàn giao dự án KPI")
                        chosen_deadline = st.date_input("Thiết lập ngày đến hạn (Deadline):", datetime.date(2026, 12, 31))
                        st.metric("Thời gian khả dụng còn lại", f"{(chosen_deadline - datetime.date.today()).days} ngày")
                with col_f2:
                    with st.container(border=True):
                        st.markdown("##### 🪐 Ma trận phân loại ưu tiên Eisenhower")
                        st.text_input("Tác vụ cần phân loại doanh nghiệp:", value="Đánh giá lại hợp đồng máy chủ")
                        st.selectbox("Mức độ ưu tiên:", ["Khẩn cấp & Quan trọng", "Quan trọng nhưng không khẩn cấp", "Khẩn cấp nhưng không quan trọng"])
                        st.button("Xếp vào ma trận quản trị", use_container_width=True)
            with tab_plus:
                if not is_vip:
                    st.warning("Tính năng thuộc phân hệ PLUS. Vui lòng nâng cấp cấp quyền tài khoản.")
                else:
                    with st.container(border=True):
                        st.markdown("##### 🪐 [ĐỘT PHÁ] Trình giả lập tài chính ROI & Dự báo đường băng tiền mặt (Runway)")
                        c_r1, c_r2, c_r3 = st.columns(3)
                        with c_r1: rev = st.number_input("Doanh thu dự kiến tháng (VNĐ):", value=120000000)
                        with c_r2: cost = st.number_input("Chi phí cố định tháng (VNĐ):", value=45000000)
                        with c_r3: cash_pool = st.number_input("Quỹ tiền mặt dự trữ hiện tại (VNĐ):", value=300000000)
                        
                        if st.button("Kích hoạt tính toán kịch bản dòng tiền", type="primary", use_container_width=True):
                            net_burn = cost - rev
                            if net_burn <= 0:
                                st.success("Dòng tiền dương ổn định! Doanh nghiệp an toàn tuyệt đối.")
                            else:
                                runway = cash_pool / net_burn
                                st.error(f"Cảnh báo: Tốc độ đốt tiền ròng đang diễn ra. Đường băng tài chính chỉ còn: {runway:.1f} Tháng!")
                            st.line_chart([cash_pool, cash_pool + (rev-cost), cash_pool + (rev-cost)*2, cash_pool + (rev-cost)*3])

        # 🎓 DANH MỤC: HỌC TẬP & NGHIÊN CỨU
        elif "🎓 Học tập" in st.session_state.work_category:
            tab_free, tab_plus = st.tabs(["🚀 Công Cụ Ôn Tập (Free)", "💎 Lõi Học Thuật Cao Cấp (PLUS VIP)"])
            with tab_free:
                col_h1, col_h2 = st.columns(2)
                with col_h1:
                    with st.container(border=True):
                        st.markdown("##### 🪐 Bộ đếm ngược kỳ thi & Đồng hồ Pomodoro tập trung")
                        exam_date = st.date_input("Chọn ngày thi mục tiêu:", datetime.date(2026, 6, 5))
                        st.metric("Số ngày chuẩn bị còn lại", f"{(exam_date - datetime.date.today()).days} Ngày")
                with col_h2:
                    with st.container(border=True):
                        st.markdown("##### 🪐 Trình ghi nhớ Flashcard ôn tập nhanh")
                        f_q = st.text_input("Nhập câu hỏi cốt lõi ôn tập:")
                        f_a = st.text_input("Nhập câu trả lời ngắn gọn:")
                        if st.button("Lưu vào bộ nhớ Flashcard", use_container_width=True):
                            st.session_state.flashcards.append({"Câu hỏi": f_q, "Trả lời": f_a})
                        st.write(st.session_state.flashcards)
            with tab_plus:
                if not is_vip:
                    st.warning("Tính năng thuộc phân hệ PLUS. Vui lòng nâng cấp cấp quyền tài khoản.")
                else:
                    col_hp1, col_hp2 = st.columns(2)
                    with col_hp1:
                        with st.container(border=True):
                            st.markdown("##### 🪐 Lõi giải toán & Chứng minh Bất đẳng thức nâng cao (Cauchy / AM-GM)")
                            st.text_input("Biểu thức cần chứng minh cực trị:", value="a^2 + b^2 + c^2 >= ab + bc + ca")
                            if st.button("Kích hoạt AI Solver giải chi tiết", type="primary", use_container_width=True):
                                st.latex(r"a^2 + b^2 + c^2 - ab - bc - ca = \frac{1}{2}[(a-b)^2 + (b-c)^2 + (c-a)^2] \ge 0")
                                st.success("Chứng minh hoàn tất! Dấu đẳng thức xảy ra khi và chỉ khi a = b = c.")
                    with col_hp2:
                        with st.container(border=True):
                            st.markdown("##### 🪐 [ĐỘT PHÁ] Khung cấu trúc lập luận văn học lý luận chuyên sâu")
                            lit_work = st.text_input("Tên tác phẩm văn học cần phân tích cấu trúc tâm lý:", value="Mây trắng còn bay - Bảo Ninh")
                            if st.button("Xuất ma trận hệ thống luận điểm", use_container_width=True):
                                st.markdown("""
                                - **Luận điểm 1:** Hoàn cảnh trớ trêu trên chuyến bay thương mại thời bình (Không gian va chạm quá khứ - hiện tại).
                                - **Luận điểm 2:** Chi tiết nghệ thuật 'bức ảnh thờ' và hành động thầm lặng của bà cụ (Biểu tượng của nỗi đau âm thầm sau chiến tranh).
                                - **Luận điểm 3:** Sự thức tỉnh lương tri của các nhân vật xung quanh (Tính nhân văn sâu sắc bừng sáng).
                                """)

        # 💻 DANH MỤC: LẬP TRÌNH & KỸ THUẬT
        elif "💻 Lập trình" in st.session_state.work_category:
            tab_free, tab_plus = st.tabs(["🚀 Tiện Ích Code Tiêu Chuẩn (Free)", "💎 Công Cụ Kiến Trúc Hệ Thống (PLUS VIP)"])
            with tab_free:
                with st.container(border=True):
                    st.markdown("##### 🪐 Bộ xác thực mã hóa chuỗi cấu hình JSON")
                    json_input = st.text_area("Nhập chuỗi JSON cấu hình kiểm tra:", value='{"status": "active", "node": 1, "features": ["auth", "ai_core"]}')
                    if st.button("Kiểm tra lỗi cú pháp chuỗi biên", use_container_width=True):
                        try:
                            json.loads(json_input)
                            st.success("Cú pháp chuỗi JSON hoàn toàn hợp lệ, cấu trúc không có lỗi biên!")
                        except Exception as e:
                            st.error(f"Lỗi cú pháp: {e}")
            with tab_plus:
                if not is_vip:
                    st.warning("Tính năng thuộc phân hệ PLUS. Vui lòng nâng cấp cấp quyền tài khoản.")
                else:
                    col_cp1, col_cp2 = st.columns(2)
                    with col_cp1:
                        with st.container(border=True):
                            st.markdown("##### 🪐 [ĐỘT PHÁ] Bộ phân tích độ phức tạp thuật toán (Big O Complexity)")
                            code_snippet = st.text_area("Dán đoạn mã nguồn vòng lặp cần phân tích:", value="for i in range(n):\n  for j in range(n):\n    print(i, j)")
                            if st.button("Phân tích cấu trúc thời gian chạy", type="primary", use_container_width=True):
                                st.markdown("Độ phức tạp thời gian dự kiến: **O(n²)**")
                                st.warning("Khuyên dùng: Hãy tối ưu bằng cách dùng cấu trúc bảng băm (Hash Map) để giảm độ phức tạp xuống O(n).")
                    with col_cp2:
                        with st.container(border=True):
                            st.markdown("##### 🪐 Trình tạo sơ đồ kiến trúc luồng dữ liệu Mermaid.js tự động")
                            st.text_area("Mô tả luồng hệ thống logic cần vẽ sơ đồ:")
                            if st.button("Tạo mã cấu trúc Mermaid.js", use_container_width=True):
                                st.code("graph LR\n  A[Client Web/App] --> B[API Gateway Core]\n  B --> C[Microservice Auth]\n  B --> D[AI Processing Node]", language="text")

        # 🎨 DANH MỤC: SÁNG TẠO & THIẾT KẾ
        else:
            tab_free, tab_plus = st.tabs(["🚀 Hỗ Trợ Content Ý Tưởng (Free)", "💎 Tối Ưu Hóa Chiến Dịch Viral (PLUS VIP)"])
            with tab_free:
                with st.container(border=True):
                    st.markdown("##### 🪐 Trình phối màu nghệ thuật thông minh dựa trên mã màu HEX")
                    palette_style = st.selectbox("Chọn tông màu chủ đạo mong muốn:", ["Minimalist Dark", "Neon Futuristic", "Retro Vintage"])
                    if st.button("Xuất mã bảng màu chuẩn HEX", use_container_width=True):
                        if palette_style == "Minimalist Dark":
                            st.code("#000000 | #111111 | #FFFFFF | #888888", language="text")
                        elif palette_style == "Neon Futuristic":
                            st.code("#0A0A23 | #00FFCC | #FF007F | #330066", language="text")
                        else:
                            st.code("#F4EAE1 | #D9B48F | #A66E4E | #4C3A31", language="text")
            with tab_plus:
                if not is_vip:
                    st.warning("Tính năng thuộc phân hệ PLUS. Vui lòng nâng cấp cấp quyền tài khoản.")
                else:
                    with st.container(border=True):
                        st.markdown("##### 🪐 [ĐỘT PHÁ] Trình tự động tạo kịch bản phân cảnh phân đoạn (Storyboard) thời gian thực")
                        st.text_input("Chủ đề cốt lõi của chiến dịch nội dung ngắn:", value="Bẻ khóa tính năng hệ điều hành AI")
                        if st.button("Xây dựng sơ đồ phân cảnh 60 giây", type="primary", use_container_width=True):
                            st.markdown("""
                            - **00:00 - 00:03 (Mở màn giật gân):** Cảnh quay cận màn hình mã nguồn chạy ma trận. Câu thoại kích thích tò mò.
                            - **00:03 - 00:25 (Nêu vấn đề):** Show ra sự bất tiện khi hệ thống cứng nhắc không thay đổi được danh mục ngành nghề.
                            - **00:25 - 00:50 (Giải pháp đột phá):** Thao tác chọn danh mục, toàn bộ các nút tính năng cao cấp tự động hiển thị ra.
                            - **00:50 - 01:00 (Call to Action):** Kêu gọi đăng ký dùng thử phiên bản hệ điều hành cục bộ mới.
                            """)

    # ---------------------------------------------------------------------
    # 📊 TRUNG TÂM HOẠCH ĐỊNH TIẾN ĐỘ SPRINTS
    # ---------------------------------------------------------------------
    elif navigation_hub == "📊 Hoạch Định Tiến Độ Sprints":
        st.title("📊 Trung Tâm Hoạch Định Tiến Độ Sprints & Quản Trị Chỉ Số")
        st.caption("Cho phép người dùng thiết lập và cấu hình trực tiếp lịch trình làm việc thực tế.")
        
        c_add, c_view = st.columns([1, 1.4])
        with c_add:
            st.markdown("##### Thêm hạng mục công việc vào biểu đồ tiến độ")
            new_item_name = st.text_input("Tên hạng mục hành động:")
            new_item_hours = st.number_input("Số giờ đầu tư dự kiến:", value=10, min_value=1)
            new_item_comp = st.selectbox("Mức độ phức tạp tác vụ:", ["Thấp", "Trung bình", "Cao"])
            if st.button("Cập nhật vào hệ thống đồ thị", use_container_width=True):
                if new_item_name:
                    st.session_state.custom_sprints.append({"Hạng mục": new_item_name, "Thời gian (Giờ)": new_item_hours, "Độ phức tạp": new_item_comp})
                    st.toast("Đã đồng bộ dữ liệu đồ thị tiến độ mới!")
                    
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
        st.title("⚙️ Trung Tâm Quản Trị Hồ Sơ & Tùy Chỉnh Hệ Thống")
        st.caption("Quản lý thông tin định danh nút dữ liệu cá nhân và cấu hình các biến số hoạt động của lõi điều hành.")
        
        prof_col, sett_col = st.columns(2)
        
        with prof_col:
            st.markdown("### 👤 Hồ Sơ Tài Khoản Cục Bộ")
            with st.container(border=True):
                st.markdown(f"""
                <div class="profile-badge">
                    <span style='font-size: 12px; color: #888888; font-family: monospace;'>WORKSPACE ACCOUNT NODE</span>
                    <h2 style='margin: 5px 0 0 0; color: #ffffff;'>{st.session_state.profile_fullname}</h2>
                    <p style='margin: 2px 0 10px 0; color: #aaaaaa; font-style: italic;'>{st.session_state.profile_role}</p>
                    <span style='background-color: #ffffff; color: #000000; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;'>{st.session_state.tier.upper()}</span>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("##### Tinh chỉnh thông tin hồ sơ")
                new_fn = st.text_input("Họ và tên người sử dụng:", value=st.session_state.profile_fullname)
                new_rl = st.text_input("Định danh vị trí / Chức vụ hiện tại:", value=st.session_state.profile_role)
                new_bio = st.text_area("Tiểu sử công việc tóm tắt:", value=st.session_state.profile_bio)
                
                if st.button("💾 CẬP NHẬT THÔNG TIN HỒ SƠ", use_container_width=True):
                    st.session_state.profile_fullname = new_fn
                    st.session_state.profile_role = new_rl
                    st.session_state.profile_bio = new_bio
                    st.toast("Đã ghi nhận thay đổi thông tin cấu trúc hồ sơ cá nhân!")
                    st.rerun()

        with sett_col:
            st.markdown("### ⚙️ Cài Đặt Cấu Hình Lõi")
            with st.container(border=True):
                st.markdown("##### Tham số Mô hình Trí tuệ Nhân tạo")
                st.session_state.settings_ai_temp = st.slider(
                    "Độ sáng tạo chuyên sâu của AI (AI Temperature):",
                    0.0, 1.0, value=st.session_state.settings_ai_temp, step=0.1
                )
                st.caption("Giá trị thấp giúp câu trả lời chính xác, mang tính logic cao; giá trị cao tăng tính đột phá sáng tạo ý tưởng.")
                st.write("")
                
                st.markdown("##### Tùy chọn Hạ tầng An toàn Bảo mật")
                st.session_state.settings_secure_mode = st.toggle(
                    "Kích hoạt chế độ cô lập Sandboxed & Mã hóa dữ liệu AES-256",
                    value=st.session_state.settings_secure_mode
                )
                
                st.markdown("##### Giao diện Tông nền Hệ điều hành")
                st.session_state.settings_theme = st.selectbox(
                    "Chọn kiến trúc bảng phối màu chủ đạo giao diện:",
                    ["Đen tuyền Premium (Jet Black)", "Xám sâu không gian (Space Gray)", "Trắng phòng thí nghiệm (Laboratory White)"]
                )
                
                st.write("---")
                if st.button("⚙️ CÀI LẠI TOÀN BỘ CẤU HÌNH GỐC", use_container_width=True):
                    st.session_state.settings_ai_temp = 0.7
                    st.session_state.settings_secure_mode = True
                    st.session_state.settings_theme = "Đen tuyền Premium (Jet Black)"
                    st.toast("Cấu hình hệ thống đã được thiết lập lại về trạng thái mặc định ban đầu.")
                    st.rerun()

    # ---------------------------------------------------------------------
    # GIAO DIỆN MUA GÓI CHUẨN PREMIUM DARK MODE
    # ---------------------------------------------------------------------
    elif navigation_hub == "💰 Nâng Cấp PLUS & LIFETIME":
        show_plus_pricing_view()

    # ---------------------------------------------------------------------
    # CỔNG THANH TOÁN PAYOS
    # ---------------------------------------------------------------------
    elif navigation_hub == "💳 Cổng Thanh Toán PayOS":
        st.title("💳 Trung Tâm Xác Thực Hóa Đơn Tự Động Qua Cổng PayOS")
        
        left_invoice, right_qrcode = st.columns([1, 1.1])
        with left_invoice:
            st.subheader("🧾 Chi tiết hóa đơn khởi tạo")
            st.write("Đơn vị thụ hưởng: **soloflowOS Global Core**")
            
            billing_amount = 99000
            billing_title = "Giấy phép Gói Tháng PLUS Premium"
            
            if "payos_target" in st.session_state and st.session_state.payos_target == "LIFETIME":
                billing_amount = 499000
                billing_title = "Giấy phép Sở hữu TRỌN ĐỜI (Lifetime) VIP"
                
            st.markdown(f"Sản phẩm đăng ký hệ thống: **{billing_title}**")
            st.write("---")
            st.markdown(f"### Tổng chi phí thanh toán: <span style='color: #ffffff; text-decoration: underline;'>{billing_amount:,} VNĐ</span>", unsafe_allow_html=True)
            
            if st.button("🔗 Khởi tạo Link liên kết hóa đơn PayOS", type="primary", use_container_width=True):
                st.session_state.invoice_id = str(random.randint(111111, 999999))
                st.success(f"Khởi tạo hóa đơn thành công đơn hàng: #{st.session_state.invoice_id}")
                
        with right_qrcode:
            st.subheader("📲 Quét mã mã hóa VietQR PayOS")
            if "invoice_id" in st.session_state and st.session_state.invoice_id:
                st.markdown(f"""
                <div style='border: 2px solid #ffffff; padding: 25px; border-radius: 12px; text-align: center; background-color: #000000; color: #ffffff;'>
                    <p style='font-weight: bold; letter-spacing: 1px;'>ĐỐI TÁC THANH TOÁN PAYOS CHÍNH THỨC</p>
                    <div style='background-color: #ffffff; width: 220px; height: 220px; margin: 20px auto; padding: 15px; display: flex; align-items: center; justify-content: center;'>
                        <p style='color: #000000; font-size: 11px; font-weight: bold;'>[ MÃ VIETQR CHUYỂN KHOẢN ]<br>ĐÃ MÃ HÓA BẢO MẬT<br>ĐƠN HÀNG #{st.session_state.invoice_id}</p>
                    </div>
                    <p style='font-size: 14px;'>Nội dung chuyển khoản chính xác: <br><b>SOLOFLOW {st.session_state.invoice_id}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                if st.button("🔄 Kiểm tra xác thực trạng thái Webhook", use_container_width=True):
                    with st.spinner("Đang truy vấn trạng thái cổng ngân hàng đối tác..."):
                        time.sleep(1.0)
                    st.session_state.tier = "Thành viên PLUS" if billing_amount == 99000 else "Thành viên LIFETIME VIP"
                    st.balloons()
                    st.success("🎉 Giao dịch thành công! Toàn bộ hệ thống lõi và các siêu tính năng VIP độc quyền đã được mở khóa.")
            else:
                st.warning("Vui lòng kích hoạt tạo hóa đơn ở khu vực bên trái để tổng hợp mã QR thanh toán.")

# =========================================================================
# GIAO DIỆN MUA GÓI CHUẨN PREMIUM
# =========================================================================
def show_plus_pricing_view():
    st.write("---")
    col_free, col_plus, col_lifetime = st.columns(3)
    
    with col_free:
        st.markdown("""
        <div style='background-color: #050505; color: #888888; border: 1px solid #222222; padding: 30px; border-radius: 14px; height: 100%;'>
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
        <div class="plus-card-premium" style="border: 2px solid #ffffff !important; box-shadow: 0px 0px 20px rgba(255,255,255,0.15) !important;">
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
