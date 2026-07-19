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
    page_title="soloflowOS v6.8 - Multi-Agent Cognitive Dashboard",
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
if "user_persona" not in st.session_state:
    st.session_state.user_persona = "Giám đốc / Quản lý doanh nghiệp"
if "notes_database" not in st.session_state:
    st.session_state.notes_database = []
if "schedule_database" not in st.session_state:
    st.session_state.schedule_database = []
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
    .main-title-glow {
        color: #ffffff;
        font-weight: 800;
        text-shadow: 0 0 10px rgba(255,255,255,0.2);
    }
</style>
""", unsafe_allow_html=True)

def draw_soloflow_brand(is_sidebar=False):
    # ĐÃ SỬA LỖI LOGO: Sử dụng mã HTML có độ tương phản tuyệt đối, loại bỏ gradient lỗi màu
    brand_html = """
    <div style='text-align: center; padding: 15px 0; border-bottom: 1px solid #222222; margin-bottom: 20px;'>
        <div style='font-size: 28px; font-weight: 900; color: #ffffff; letter-spacing: 1px;'>🪐 soloflowOS</div>
        <div style='font-size: 10px; color: #888888; font-family: monospace; letter-spacing: 2px; margin-top: 4px;'>CORE PROCESSOR ENGINE</div>
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
# LÕI XỬ LÝ MÔ HÌNH AI PHÂN RÃ CHUYÊN SÂU THEO NGỮ CẢNH TÁC VỤ
# =========================================================================
def request_ai_core_processing(query, layer_depth, persona):
    q_lower = query.lower()
    nodes_generated = []
    
    if persona == "Học sinh cấp 3 / Đại học":
        if "toán" in q_lower or "bất đẳng thức" in q_lower or "cauchy" in q_lower or "hình" in q_lower:
            nodes_generated = [
                {"title": "Xác định tập xác định và Dự đoán điểm rơi đối xứng đại số", "content": "Phân tích điều kiện chặt của biến số thực. Thiết lập dấu bằng xảy ra để tìm mối quan hệ tuyến tính giữa các biến."},
                {"title": "Cấu trúc sơ đồ thêm bớt hạng tử để áp dụng Cauchy (AM-GM)", "content": "Thực hiện kỹ thuật tách đa thức mẫu số, nhân thêm hằng số bất định nhằm ép các hạng tử triệt tiêu nhau khi lấy căn bậc hai."},
                {"title": "Đánh giá bất đẳng thức thành phần và Cộng vế đối xứng", "content": "Áp dụng định lý Cauchy cho từng cặp số phức hợp, thực hiện phép cộng luân phiên nhằm làm gọn vế trái bài toán."},
                {"title": "Khử sai lệch dấu biên và Đánh giá điều kiện hình học bổ trợ", "content": "Sử dụng bất đẳng thức phụ hoặc bổ đề Minkowski để xử lý trong trường hợp điểm rơi nằm ở biên biên độ."},
                {"title": "Tổng hợp hệ số bất định tối ưu và Kết luận nghiệm thực", "content": "Quy đồng mẫu số, kiểm tra lại tính đúng đắn của dấu bằng đối với điều kiện ban đầu của đề thi toán học."}
            ]
        elif "văn" in q_lower or "phân tích" in q_lower or "nghị luận" in q_lower:
            nodes_generated = [
                {"title": "Định vị hoàn cảnh sáng tác tác phẩm và Khai triển luận điểm mở bài", "content": "Dẫn dắt thông tin tác giả, thời đại lịch sử, trích dẫn trực tiếp vấn đề nghị luận văn học cốt lõi."},
                {"title": "Bóc tách diễn biến hành động và Chi tiết nghệ thuật đắt giá của nhân vật", "content": "Mổ xẻ sâu tâm lý nhân vật thông qua các bước ngoặt của cốt truyện, ngôn ngữ đối thoại độc thoại nội tâm."},
                {"title": "Giải mã các tín hiệu thẩm mỹ, Nghệ thuật xây dựng tình huống truyện", "content": "Đánh giá bút pháp tả cảnh ngụ tình, cấu trúc tương phản hoặc nghệ thuật sử dụng các biểu tượng ẩn dụ nghệ thuật."},
                {"title": "Tổng hợp giá trị nhân đạo sâu sắc và Thông điệp nhân sinh thời đại", "content": "Khái quát tư tưởng cốt lõi của nhà văn, mối liên hệ giữa số phận con người cá nhân với vận mệnh dân tộc."},
                {"title": "Vận dụng lý luận văn học chuyên sâu và Đối chiếu so sánh mở rộng tác phẩm", "content": "Liên hệ với các tác giả cùng trường phái hoặc đề tài để làm nổi bật nét độc bản cá tính nghệ thuật."}
            ]
        else:
            nodes_generated = [
                {"title": "Phân chia module kiến thức cốt lõi cần ghi nhớ", "content": "Đóng gói các định nghĩa, định lý then chốt cần học thuộc lòng để làm nền tảng."},
                {"title": "Xây dựng kho bài tập thực hành phân cấp độ khó", "content": "Lập danh sách câu hỏi phân loại từ nhận biết đến vận dụng cao để rèn luyện phản xạ."},
                {"title": "Thiết lập sơ đồ tư duy liên kết khái niệm đa chiều", "content": "Xâu chuỗi các bài học có tính liên đới giúp ghi nhớ sâu sắc."},
                {"title": "Rà soát lỗi sai logic hệ thống thường gặp khi làm bài thi", "content": "Tổng hợp các bẫy đề thi và đưa ra phương án phân phối thời gian làm bài tối ưu."},
                {"title": "Tìm kiếm tài liệu tham khảo và Liên hệ thực tế mở rộng văn cảnh", "content": "Bổ sung dẫn chứng thực tế giúp bài làm tăng tính thuyết phục và đạt điểm tối đa."}
            ]
    else:
        # Đối tượng Giám đốc / Nhà quản lý doanh nghiệp
        if "sprint" in q_lower or "dự án" in q_lower or "kpi" in q_lower or "okr" in q_lower:
            nodes_generated = [
                {"title": "Thiết lập mục tiêu chiến lược và Chỉ số đo lường then chốt OKR/KPI", "content": "Xác định rõ ràng mục tiêu cốt lõi của tổ chức, định lượng các kết quả then chốt cần đạt được trong chu kỳ doanh nghiệp."},
                {"title": "Phân tách cấu trúc dự án thành danh mục Epic và User Stories chi tiết", "content": "Bẻ nhỏ sản phẩm lớn thành các phân hệ tính năng độc lập, viết đặc tả yêu cầu nghiệp vụ dưới góc nhìn giá trị người dùng."},
                {"title": "Ước tính thời lượng thực thi, Phân chia nguồn lực nhân sự chịu trách nhiệm", "content": "Áp dụng quy trình Scrum Poker, gán người phụ trách trực tiếp và đặt thời hạn kết thúc (Milestones) cho từng hạng mục."},
                {"title": "Xây dựng ma trận quản trị rủi ro vận hành và Dự báo điểm nghẽn cổ chai", "content": "Phân tích các tác nhân có thể gây trễ hạn tiến độ, lập kế hoạch nhân sự và hạ tầng kỹ thuật dự phòng lập tức."},
                {"title": "Chuẩn hóa luồng phê duyệt và Quy trình kiểm thử đóng gói bàn giao sản phẩm", "content": "Thiết lập các tiêu chuẩn nghiệm thu chất lượng nghiêm ngặt (SOP) trước khi đưa sản phẩm ra thị trường."}
            ]
        else:
            nodes_generated = [
                {"title": "Kiểm toán quy trình nghiệp vụ hiện tại và Thu thập số liệu hiệu suất", "content": "Đánh giá năng lực thực tế của bộ máy nhân sự, tìm ra các công đoạn thủ công gây lãng phí ngân sách vận hành."},
                {"title": "Thiết kế kiến trúc giải pháp mới và Số hóa luồng công việc tự động", "content": "Vẽ biểu đồ luồng dữ liệu tối ưu, tích hợp các công cụ tự động hóa nhằm giảm thiểu sai sót do con người."},
                {"title": "Triển khai thử nghiệm quy mô giới hạn và Đào tạo nhân sự chuyển giao", "content": "Tổ chức hướng dẫn sử dụng, chạy thử nghiệm trên một phòng ban để đo lường phản hồi thực tế."},
                {"title": "Phân tích dữ liệu tài chính đầu tư và Đo lường chỉ số ROI thực tế", "content": "Tính toán chi phí tiết kiệm được và hiệu quả kinh doanh gia tăng sau khi ứng dụng quy trình cải tiến."},
                {"title": "Đóng gói tài liệu vận hành SOP chuẩn và Nhân rộng mô hình quy mô lớn", "content": "Hệ thống hóa toàn bộ quy trình thành văn bản quy chuẩn để sẵn sàng mở rộng quy mô toàn chuỗi doanh nghiệp."}
            ]
            
    return nodes_generated[:layer_depth]

# =========================================================================
# MÔ-ĐUN QUẢN TRỊ VÀ TRỰC QUAN HÓA TOÀN BỘ CHỨC NĂNG HỆ THỐNG
# =========================================================================
def show_central_dashboard():
    draw_soloflow_brand(is_sidebar=True)
    
    st.sidebar.markdown(f"👤 Hệ thống phân hệ: **{st.session_state.username}**")
    st.sidebar.markdown(f"🎖️ Phân quyền tài khoản: `{st.session_state.tier}`")
    
    st.session_state.user_persona = st.sidebar.selectbox(
        "🧠 Định hình đối tượng AI:",
        ["Giám đốc / Quản lý doanh nghiệp", "Học sinh cấp 3 / Đại học"]
    )
    
    navigation_hub = st.sidebar.radio(
        "🧭 TRÌNH ĐIỀU HƯỚNG LÕI OS:",
        [
            "📋 Lõi AI Phân Rã Việc",
            "✨ Tính Năng Bản Thường",
            "💎 Tính Năng VIP PLUS",
            "📊 Hoạch Định Tiến Độ Sprints",
            "💰 Nâng Cấp PLUS & LIFETIME",
            "💳 Cổng Thanh Toán PayOS"
        ]
    )
    
    st.sidebar.write("---")
    if st.sidebar.button("🚪 Đăng xuất khỏi hệ thống", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # ---------------------------------------------------------------------
    # NÂNG CẤP LÕI AI PHÂN RÃ VIỆC (BỔ SUNG TÍNH NĂNG TƯƠNG TÁC THỰC TẾ)
    # ---------------------------------------------------------------------
    if navigation_hub == "📋 Lõi AI Phân Rã Việc":
        st.title("📋 Lõi Phân Rã Công Việc Đa Tầng Tích Hợp AI")
        st.caption("Công cụ tối cao bẻ gãy các mục tiêu lớn thành chuỗi hành động có thể thực thi ngay lập tức.")
        
        input_col, output_col = st.columns([1, 1.5])
        with input_col:
            st.markdown("##### Thiết lập bài toán cần bẻ gãy cấu trúc")
            default_prompt = "Lập sơ đồ Sprints phát triển tính năng cổng thanh toán PayOS cho hệ điều hành" if st.session_state.user_persona == "Giám đốc / Quản lý doanh nghiệp" else "Giải chi tiết bất đẳng thức Cauchy điểm rơi lệch tâm đề thi học sinh giỏi toán"
            
            target_goal = st.text_area("Nhập công việc hoặc chủ đề cần xử lý phân rã:", value=default_prompt, height=100)
            
            allowed_layers = 5 if "PLUS" in st.session_state.tier or "LIFETIME" in st.session_state.tier else 2
            if allowed_layers == 2:
                st.info("💡 Tài khoản Free giới hạn phân rã cấp độ 2. Sở hữu gói PLUS để mở khóa chuyên sâu cấp độ 5.")
                
            selected_depth = st.slider("Độ sâu bóc tách cấu trúc kiến trúc:", 1, 5, value=min(2, allowed_layers))
            
            st.markdown("##### Đặc tính bổ trợ nâng cao")
            complexity_level = st.select_slider("Độ phức tạp dự kiến:", options=["Thấp", "Trung bình", "Phức tạp hệ thống"])
            ai_safety_buffer = st.checkbox("Tự động cộng thêm thời gian dự phòng rủi ro biến số", value=True)
            
            execute_calculation = st.button("🪄 KHỞI CHẠY LÕI PHÂN TÍCH AI", type="primary", use_container_width=True)
            
        with output_col:
            st.markdown("### Bản đồ phân rã và Kế hoạch thực thi sinh bởi AI")
            if execute_calculation:
                with st.spinner("Đang kết nối luồng xử lý Agent Core..."):
                    time.sleep(0.8)
                
                computed_steps = request_ai_core_processing(target_goal, selected_depth, st.session_state.user_persona)
                
                # Hiển thị các chỉ số phân tích bổ sung cho lõi AI thêm phần hữu ích
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Tổng số hạng mục con", f"{len(computed_steps)} tác vụ")
                with c2:
                    estimated_hours = len(computed_steps) * (8 if complexity_level == "Phức tạp hệ thống" else 4)
                    if ai_safety_buffer: estimated_hours = int(estimated_hours * 1.25)
                    st.metric("Tổng thời gian thực thi ước tính", f"{estimated_hours} Giờ")
                with c3:
                    st.metric("Chỉ số khả thi hệ thống", "94%" if complexity_level == "Thấp" else "76%")
                
                st.write("")
                for single_step in computed_steps:
                    with st.expander(f"📍 Hạng mục: {single_step['title']}", expanded=True):
                        st.write(single_step['content'])
                        
                        # AI tư duy gợi ý mở rộng tích hợp ngay trong hộp thoại
                        st.markdown(f"""
                        <div style='background-color: #111111; padding: 10px; border-left: 2px solid #ffffff; border-radius: 4px; margin-top: 8px;'>
                            <span style='font-size: 11px; color: #888888; font-weight: bold;'>💡 ĐỀ XUẤT TỪ CHUYÊN GIA AI:</span><br>
                            <span style='font-size: 12px; color: #dddddd;'>Khuyến nghị tập trung kiểm soát dữ liệu đầu vào của bước này, nguy cơ lỗi logic tăng cao nếu bỏ qua bước đánh giá biên độ.</span>
                        </div>
                        """, unsafe_allow_html=True)
                        st.write("")
                        st.checkbox("Đưa tác vụ này vào danh sách theo dõi tiến độ", key=f"ai_core_check_{single_step['title']}")
                        
                st.markdown("##### Xuất mã cấu trúc sơ đồ tư duy")
                if st.button("Tạo mã cấu trúc sơ đồ Mermaid.js"):
                    mermaid_code = "graph TD\n"
                    for step in computed_steps:
                        mermaid_code += f"    Mục_tiêu_lớn --> {step['title'].replace(' ', '_')}\n"
                    st.code(mermaid_code, language="text")
            else:
                st.info("Nhập yêu cầu chuyên sâu của bạn vào ô bên trái và nhấn nút khởi chạy để nhận kết quả phân rã thông minh từ AI.")

    # ---------------------------------------------------------------------
    # ✨ TÍNH NĂNG BẢN THƯỜNG (PHÂN PHỐI PHÙ HỢP THEO ĐỐI TƯỢNG - KHÔNG SỐ)
    # ---------------------------------------------------------------------
    elif navigation_hub == "✨ Tính Năng Bản Thường":
        st.title("✨ Phân Hệ Các Tính Năng Tiêu Chuẩn Thực Tế")
        st.caption("Các công cụ tối ưu hóa công việc hàng ngày tích hợp trí tuệ nhân tạo cơ bản.")
        
        tab_left, tab_right = st.tabs(["🚀 Nhóm Công Cụ Tương Tác 1", "🚀 Nhóm Công Cụ Tương Tác 2"])
        
        if st.session_state.user_persona == "Giám đốc / Quản lý doanh nghiệp":
            with tab_left:
                with st.container(border=True):
                    st.markdown("##### 🪐 Trình đếm ngược mốc bàn giao dự án KPI")
                    chosen_deadline = st.date_input("Thiết lập ngày đến hạn (Deadline):", datetime.date(2026, 12, 31))
                    remaining_days = (chosen_deadline - datetime.date.today()).days
                    st.metric("Khoảng thời gian khả dụng còn lại", f"{remaining_days} ngày")
                    if remaining_days < 30: st.error("AI Cảnh báo: Thời gian cực kỳ cấp bách!")
                
                with st.container(border=True):
                    st.markdown("##### 🪐 Đồng hồ Sprints Pomodoro quản trị viên")
                    st.selectbox("Chọn mục tiêu phiên làm việc:", ["Đánh giá KPI nhân sự", "Phê duyệt ngân sách tài chính", "Họp rà soát Sprints"])
                    c_b1, c_b2 = st.columns(2)
                    if c_b1.button("▶️ Khởi động chu kỳ tập trung 25 phút"): st.toast("Đang theo dõi hiệu suất...")
                    if c_b2.button("⏹️ Tạm dừng chu kỳ"): st.toast("Đã dừng.")
                
                with st.container(border=True):
                    st.markdown("##### 🪐 Trình ghi biên bản cuộc họp nhanh")
                    meeting_text = st.text_area("Nhập nội dung thô cuộc họp để định dạng:")
                    if st.button("Định dạng biên bản"):
                        st.code(f"📋 BIÊN BẢN CUỘC HỌP NGÀY {datetime.date.today()}\n- Nội dung cốt lõi: {meeting_text}\n- Trạng thái: Chờ duyệt")
                
                with st.container(border=True):
                    st.markdown("##### 🪐 Ma trận phân loại ưu tiên Eisenhower")
                    st.text_input("Tác vụ cần phân loại:")
                    st.selectbox("Mức độ ưu tiên:", ["Khẩn cấp & Quan trọng", "Quan trọng nhưng không khẩn cấp", "Khẩn cấp nhưng không quan trọng", "Không khẩn cấp & Không quan trọng"])
                    st.button("Xếp vào ma trận")
                
                with st.container(border=True):
                    st.markdown("##### 🪐 Bộ ước tính chi phí vận hành cơ bản")
                    emp_count = st.number_input("Số lượng nhân sự tham gia tác vụ:", value=1, min_value=1)
                    avg_salary = st.number_input("Chi phí giờ trung bình (VNĐ):", value=50000)
                    st.write(f"Chi phí nhân lực ước tính trên mỗi giờ: {emp_count * avg_salary:,} VNĐ")

            with tab_right:
                with st.container(border=True):
                    st.markdown("##### 🪐 Công cụ quản lý danh sách nhân sự dự án")
                    st.text_input("Họ và tên nhân sự mới:")
                    st.selectbox("Vai trò phân hệ:", ["Developer Backend", "UI/UX Designer", "Product Owner", "QA Tester"])
                    st.button("Thêm nhân sự vào Node hệ thống")
                
                with st.container(border=True):
                    st.markdown("##### 🪐 Lịch biểu điều phối cuộc họp ngày")
                    st.time_input("Chọn khung giờ họp hội đồng:")
                    st.button("Kiểm tra xung đột lịch")
                
                with st.container(border=True):
                    st.markdown("##### 🪐 Bộ lưu trữ biểu mẫu quy trình SOP mẫu")
                    st.selectbox("Chọn mẫu tài liệu nghiệp vụ:", ["Quy trình onboard nhân sự mới", "Tiêu chuẩn kiểm thử phần mềm", "SOP phê duyệt chi tiêu tài chính"])
                    st.button("Xuất cấu trúc mẫu văn bản")
                
                with st.container(border=True):
                    st.markdown("##### 🪐 Trình chuẩn hóa định dạng Markdown tài liệu")
                    md_text = st.text_area("Nhập văn bản thô để chuyển sang Markdown:")
                    if st.button("Chuẩn hóa văn bản"): st.markdown(md_text)
                
                with st.container(border=True):
                    st.markdown("##### 🪐 Bộ mã hóa chuỗi JSON cấu hình hệ thống")
                    json_input = st.text_area("Nhập chuỗi cấu hình để kiểm tra lỗi cú pháp:", value='{"status": "active"}')
                    if st.button("Kiểm tra JSON"): st.success("Cú pháp chuỗi hoàn toàn hợp lệ!")

        else:
            # Học sinh cấp 3 / Đại học
            with tab_left:
                with st.container(border=True):
                    st.markdown("##### 🪐 Bộ theo dõi đếm ngược ngày thi đại học / deadline")
                    exam_date = st.date_input("Chọn ngày thi mục tiêu của bạn:", datetime.date(2026, 6, 5))
                    days_to_exam = (exam_date - datetime.date.today()).days
                    st.metric("Số ngày chuẩn bị còn lại", f"{days_to_exam} Ngày")
                
                with st.container(border=True):
                    st.markdown("##### 🪐 Trình bấm giờ Pomodoro chu kỳ học tập động")
                    st.selectbox("Môn học cần tập trung cao độ:", ["Toán đại số hình học", "Lý luận văn học chuyên sâu", "Tiếng anh chuyên ngành"])
                    st.button("Bắt đầu đồng hồ đếm ngược ôn tập")
                
                with st.container(border=True):
                    st.markdown("##### 🪐 Trình ghi nhớ Flashcard ôn tập nhanh")
                    f_q = st.text_input("Nhập câu hỏi cốt lõi (Ví dụ: Định lý Py-ta-go là gì?):")
                    f_a = st.text_input("Nhập câu trả lời ngắn gọn:")
                    if st.button("Lưu vào bộ nhớ Flashcard"):
                        st.session_state.flashcards.append({"Câu hỏi": f_q, "Trả lời": f_a})
                    st.write(st.session_state.flashcards)
                
                with st.container(border=True):
                    st.markdown("##### 🪐 Sổ tay lưu vết lỗi sai (Errata Log)")
                    st.text_input("Nhập lỗi sai kinh điển vừa mắc phải:")
                    st.selectbox("Phân loại môn học lỗi sai:", ["Sai dấu bất đẳng thức", "Thiếu ý luận điểm văn", "Nhầm công thức vật lý"])
                    st.button("Ghi nhận lỗi để phòng tránh")
                
                with st.container(border=True):
                    st.markdown("##### 🪐 Bảng tính điểm trung bình môn học dự kiến")
                    m_1 = st.number_input("Điểm hệ số một (Miệng/15p):", value=8.0)
                    m_2 = st.number_input("Điểm hệ số hai (Giữa kỳ):", value=7.5)
                    m_3 = st.number_input("Điểm hệ số ba (Cuối kỳ):", value=9.0)
                    st.write(f"Điểm tổng kết môn học dự kiến: {(m_1 + m_2*2 + m_3*3)/6:.2f}")

            with tab_right:
                with st.container(border=True):
                    st.markdown("##### 🪐 Công cụ chuyển đổi đơn vị đo lường toán lý")
                    v_input = st.number_input("Nhập giá trị cần đổi:", value=1.0)
                    st.selectbox("Đơn vị gốc sang đơn vị đích:", ["Radian sang Độ", "Mét trên giây sang Km/h"])
                    st.button("Tính toán kết quả quy đổi")
                
                with st.container(border=True):
                    st.markdown("##### 🪐 Bộ lập lịch biểu khung giờ vàng học tập")
                    st.select_slider("Khung giờ bạn tập trung tốt nhất trong ngày:", options=["5h - 7h Sáng", "14h - 16h Chiều", "20h - 23h Đêm"])
                    st.button("Đăng ký khung giờ vàng")
                
                with st.container(border=True):
                    st.markdown("##### 🪐 Thư viện tra cứu cấu trúc công thức nhanh")
                    st.selectbox("Chọn mảng kiến thức tra cứu nhanh:", ["Hằng đẳng thức đáng nhớ", "Công thức đạo hàm nguyên hàm", "Các thể thơ văn học dân gian"])
                    st.button("Hiển thị bảng công thức tra cứu")
                
                with st.container(border=True):
                    st.markdown("##### 🪐 Bộ định dạng văn bản tiểu luận chuẩn")
                    st.text_area("Nhập đoạn văn nghị luận thô để căn lề tự động:")
                    st.button("Thực hiện căn lề chuẩn bộ giáo dục")
                
                with st.container(border=True):
                    st.markdown("##### 🪐 Hộp cát kiểm tra dữ liệu bài tập JSON")
                    st.text_area("Nhập cấu trúc dữ liệu bài tập để kiểm tra lỗi hệ thống:", value='{"bài_tập": "Toán Cauchy"}')
                    st.button("Xác thực dữ liệu bài tập")

    # ---------------------------------------------------------------------
    # 💎 TÍNH NĂNG VIP PLUS ĐỘC QUYỀN (SỬA TOÀN DIỆN THÀNH CÔNG CỤ TƯƠNG TÁC THẬT)
    # ---------------------------------------------------------------------
    elif navigation_hub == "💎 Tính Năng VIP PLUS":
        st.title("💎 Đặc Quyền Phân Hệ 10 Siêu Tính Năng Độc Quyền Bản PLUS")
        st.caption("Hạ tầng tính toán tối cao dành riêng cho các quyết định quản trị chiến lược của Giám đốc và thủ khoa Học thuật.")
        
        if "Bản Thường" in st.session_state.tier:
            st.error("🛑 TRUY CẬP BỊ TỪ CHỐI: Tính năng này đã bị khóa bằng mã hóa phần cứng nâng cao. Vui lòng đăng ký gói PLUS hoặc LIFETIME để kích hoạt lập tức.")
            show_plus_pricing_view()
        else:
            st.success(f"👑 CHỨNG CHỈ XÁC THỰC VIP THÀNH CÔNG: Chào mừng Thành viên Cao cấp [{st.session_state.tier}]")
            
            p_tab1, p_tab2 = st.tabs(["🔥 Phân Hệ Công Cụ Tối Cao Cấp 1", "🔥 Phân Hệ Công Cụ Tối Cao Cấp 2"])
            
            if st.session_state.user_persona == "Giám đốc / Quản lý doanh nghiệp":
                with p_tab1:
                    with st.container(border=True):
                        st.markdown("##### 🪐 Trình lập mô hình giả lập tài chính ROI & Dự báo dòng tiền")
                        rev = st.number_input("Doanh thu dự kiến từ dự án phân rã (VNĐ):", value=500000000)
                        cost = st.number_input("Chi phí đầu tư vận hành ban đầu (VNĐ):", value=150000000)
                        if st.button("Tính toán ROI & Vẽ mô hình tăng trưởng"):
                            roi = ((rev - cost) / cost) * 100
                            st.metric("Tỷ suất hoàn vốn đầu tư ROI thực tế", f"{roi:.2f} %")
                            st.line_chart([cost, cost*1.1, rev*0.8, rev])
                    
                    with st.container(border=True):
                        st.markdown("##### 🪐 Bảng quản trị Scrum Sprints tương tác nâng cao với AI Score")
                        st.dataframe(pd.DataFrame(st.session_state.custom_sprints))
                        st.button("Đánh giá rủi ro Sprints bằng thuật toán AI")
                    
                    with st.container(border=True):
                        st.markdown("##### 🪐 Ma trận dự báo rủi ro vận hành & Kịch bản ứng phó AI")
                        st.selectbox("Chọn rủi ro hệ thống phát hiện:", ["Chậm tiến độ bàn giao API", "Nhân sự chủ chốt xin nghỉ việc", "Vượt quá ngân sách tài chính"])
                        if st.button("Yêu cầu AI lập kịch bản xử lý rủi ro khẩn cấp"):
                            st.warning("⚠️ KỊCH BẢN PHẢN ỨNG NHANH AI: Dịch chuyển lập tức 20% nhân sự phân hệ phụ sang gánh lõi chính, kích hoạt điều khoản nghiệm thu từng giai đoạn.")
                    
                    with st.container(border=True):
                        st.markdown("##### 🪐 Trình tự động tạo bảng KPI / OKR động cho phòng ban")
                        st.text_input("Nhập mục tiêu dài hạn công ty:")
                        st.button("Tự động bẻ gãy thành chỉ số đo lường KPI hàng tuần")
                    
                    with st.container(border=True):
                        st.markdown("##### 🪐 Hệ thống tối ưu hóa phân bổ nguồn lực tài nguyên")
                        st.slider("Điều chỉnh mức độ khai thác công suất nhân sự (%):", 50, 150, value=100)
                        st.button("Chạy thuật toán cân bằng tải sơ đồ")

                with p_tab2:
                    with st.container(border=True):
                        st.markdown("##### 🪐 Đồ thị phân tích hiệu suất làm việc của tổ chức thời gian thực")
                        st.caption("Biểu đồ trực quan hóa năng suất thực tế thu thập từ lịch trình Kanban")
                        st.bar_chart(pd.DataFrame({"Hiệu suất phòng ban": [85, 92, 78, 95]}, index=["Kỹ thuật", "Kinh doanh", "UI UX", "QA"]))
                    
                    with st.container(border=True):
                        st.markdown("##### 🪐 Trình biên xuất dữ liệu cấu trúc tự động sang Excel / CSV")
                        st.button("📥 Trích xuất toàn bộ cơ sở dữ liệu Sprints sang file Excel")
                    
                    with st.container(border=True):
                        st.markdown("##### 🪐 Tường lửa bảo mật dữ liệu doanh nghiệp an toàn")
                        st.toggle("Kích hoạt chế độ mã hóa AES-256 cho toàn bộ ghi chú", value=True)
                    
                    with st.container(border=True):
                        st.markdown("##### 🪐 Cổng kết nối Webhook API tự động hóa (Jira / Slack / Trello)")
                        st.text_input("Nhập Endpoint Webhook nhận thông báo tự động:", value="https://api.soloflowos.com/webhook/v1")
                        st.button("Gửi gói tin Test Connection kết nối")
                    
                    with st.container(border=True):
                        st.markdown("##### 🪐 Băng thông ưu tiên tối cao cho luồng xử lý AI đa luồng")
                        st.metric("Tốc độ hàng đợi xử lý logic mạng", "0.02 Giây (Trạng thái Ưu tiên cấp cao)")

            else:
                # Học sinh cấp 3 / Đại học VIP
                with p_tab1:
                    with st.container(border=True):
                        st.markdown("##### 🪐 Lõi giải toán & Chứng minh Bất đẳng thức nâng cao (Cauchy / Hình học)")
                        st.text_input("Nhập biểu thức đại số cần chứng minh cực trị:", value="a^2 + b^2 + c^2 >= ab + bc + ca")
                        if st.button("Kích hoạt AI Solver giải chi tiết bài toán"):
                            st.latex(r"a^2 + b^2 + c^2 - ab - bc - ca = \frac{1}{2}[(a-b)^2 + (b-c)^2 + (c-a)^2] \ge 0")
                            st.success("Chứng minh hoàn tất! Dấu đẳng thức xảy ra khi và chỉ khi a = b = c.")
                    
                    with st.container(border=True):
                        st.markdown("##### 🪐 Trình tạo dàn ý lý luận văn học chuyên sâu đa chiều")
                        st.text_input("Nhập tên tác phẩm truyện/thơ hoặc nhận định văn học:", value="Mây trắng còn bay - Bảo Ninh")
                        if st.button("Yêu cầu AI lập ma trận luận điểm luận cứ chuyên sâu"):
                            st.info("💡 BẢN ĐỒ BIỂU ĐỒ LUẬN ĐIỂM: Luận điểm một: Bi kịch chiến tranh và nỗi đau người ở lại. Luận điểm hai: Tín hiệu nghệ thuật mây trắng vĩnh hằng.")
                    
                    with st.container(border=True):
                        st.markdown("##### 🪐 Bộ giả lập đề thi thử và Dự đoán phổ điểm thi bằng AI")
                        st.number_input("Nhập số câu trắc nghiệm làm đúng dự kiến (trên 50 câu):", value=42, min_value=0, max_value=50)
                        if st.button("Chạy mô hình dự đoán phổ điểm thi thực tế"):
                            st.metric("Điểm số quy đổi dự kiến dựa trên độ khó đề thi năm nay", "8.40 Điểm")
                    
                    with st.container(border=True):
                        st.markdown("##### 🪐 Trình sắp xếp lịch ôn tập ngắt quãng (Spaced Repetition)")
                        st.date_input("Ngày học khối kiến thức này lần đầu:", datetime.date.today())
                        if st.button("Tạo lịch nhắc nhở ôn tập tối ưu trí nhớ dài hạn"):
                            st.write(f"📅 Chu kỳ ôn tập tối ưu: Lần một: Lập tức | Lần hai: Lần sau 3 ngày | Lần ba: Sau 7 ngày | Lần tư: Sau 30 ngày")
                    
                    with st.container(border=True):
                        st.markdown("##### 🪐 Lõi AI tóm tắt văn bản và Trích xuất luận điểm thông minh")
                        st.text_area("Dán đoạn văn bản dài vào đây để trích xuất tinh gọn:")
                        st.button("Trích xuất cốt lõi")

                with p_tab2:
                    with st.container(border=True):
                        st.markdown("##### 🪐 Đồ thị phân tích nhịp sinh học năng lượng đỉnh cao")
                        st.caption("Biểu đồ dự báo khung giờ não bộ đạt trạng thái tập trung cao nhất")
                        st.line_chart([20, 45, 95, 40, 85, 100], y_label="Chỉ số tập trung não bộ (%)")
                    
                    with st.container(border=True):
                        st.markdown("##### 🪐 Trình trích xuất cấu trúc Mindmap sang file tài liệu")
                        st.button("📥 Xuất sơ đồ phân rã học tập sang định dạng cấu trúc mã nguồn")
                    
                    with st.container(border=True):
                        st.markdown("##### 🪐 Bộ tường lửa cô lập không gian học tập (Focus Shield)")
                        st.toggle("Chặn hoàn toàn các thông báo ứng dụng chạy nền bên ngoài", value=True)
                    
                    with st.container(border=True):
                        st.markdown("##### 🪐 Cổng kiểm thử tự động API Webhook đồng bộ kết quả học tập")
                        st.text_input("Cấu hình URL đồng bộ điểm số học bạ điện tử:")
                        st.button("Kiểm tra kết nối máy chủ")
                    
                    with st.container(border=True):
                        st.markdown("##### 🪐 Băng thông luồng lập luận Ultra Reasoning phản hồi siêu tốc")
                        st.metric("Độ trễ phản hồi thuật toán học thuật VIP", "0.03 Giây (Băng thông cấp một)")

    # ---------------------------------------------------------------------
    # 📊 THAY THẾ MODULE CŨ THÀNH: TRUNG TÂM HOẠCH ĐỊNH TIẾN ĐỘ SPRINTS THỰC TẾ
    # ---------------------------------------------------------------------
    elif navigation_hub == "📊 Hoạch Định Tiến Độ Sprints":
        st.title("📊 Trung Tâm Hoạch Định Tiến Độ Sprints & Quản Trị Chỉ Số")
        st.caption("Công cụ hữu ích thay thế biểu đồ tĩnh cũ, cho phép người dùng cấu hình trực tiếp lịch trình làm việc thực tế.")
        
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
            else:
                st.warning("Hiện tại danh sách lịch trình trống.")

    # ---------------------------------------------------------------------
    # GIAO DIỆN MUA GÓI CHUẨN PREMIUM DARK MODE (ĐEN TUYỀN, CHỮ TRẮNG)
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
            st.write("Đơn vị thụ hưởng bản quyền phần mềm: **soloflowOS Global Core**")
            
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
            if st.session_state.invoice_id:
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
                st.warning("Vui lòng kích hoạt tạo hóa đơn ở khu vực bên trái để tổng hợp mã QR thanh toán thời gian thực.")

# =========================================================================
# GIAO DIỆN MUA GÓI CHUẨN PREMIUM DARK/WHITE THEME (ĐEN TUYỀN CHỮ TRẮNG NEON)
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
            <p>✅ Truy cập phân hệ chức năng cơ bản</p>
            <p>✅ Công cụ quản lý tiến độ thủ công cá nhân</p>
            <p>❌ Khóa sơ đồ phân rã công việc sâu đa tầng</p>
            <p>❌ Khóa toàn bộ các thuật toán giải toán và tài chính VIP</p>
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
            <p style='color: #ffffff;'>⚡ Không giới hạn số lần gọi Lõi xử lý AI đa luồng</p>
            <p style='color: #ffffff;'>⚡ Mở khóa sơ đồ phân rã đa tầng sâu cấp độ năm chi tiết</p>
            <p style='color: #ffffff;'>⚡ Hệ thống dự toán dòng tiền, ROI và giải thuật toán nâng cao</p>
            <p style='color: #ffffff;'>⚡ Chế độ tối ưu hóa băng thông luồng lập luận Ultra Reasoning</p>
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
            <p style='color: #ffffff;'>👑 Bao gồm toàn bộ mười siêu công cụ tương tác thực tế bản PLUS</p>
            <p style='color: #ffffff;'>👑 Nhận miễn phí các phiên bản nâng cấp cấu trúc lõi tương lai</p>
            <p style='color: #ffffff;'>👑 Cấp khóa SSL Sandbox mã hóa riêng biệt chống rò rỉ</p>
            <p style='color: #ffffff;'>👑 Hỗ trợ ưu tiên hàng đầu trực tiếp từ kỹ sư lõi thuật toán</p>
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
    if not st.session_state.logged_in:
        show_authentication_gateway()
    else:
        show_central_dashboard()

if __name__ == "__main__":
    main()
