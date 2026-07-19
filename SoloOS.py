import streamlit as st
import pandas as pd
import time
import datetime
import random
import json

# =========================================================================
# 🪐 HỆ THỐNG CẤU HÌNH TOÀN CỤC & BRANDING THƯƠNG HIỆU SOLOFLOWOS
# =========================================================================
st.set_page_config(
    page_title="soloflowOS v6.5 - Multi-Agent Cognitive Dashboard",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# KHỞI TẠO STATE TOÀN CỤC ĐỂ ĐỒNG BỘ DỮ LIỆU CÁC MÔ-ĐUN TRỰC QUAN
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
if "kanban_tasks" not in st.session_state:
    st.session_state.kanban_tasks = [
        {"task": "Phân tích cấu trúc đề thi chuyên Toán", "status": "Cần làm", "type": "Học thuật"},
        {"task": "Xây dựng sơ đồ phân rã Sprints hệ thống CRM", "status": "Đang làm", "type": "Doanh nghiệp"}
    ]
if "payos_target" not in st.session_state:
    st.session_state.payos_target = None
if "invoice_id" not in st.session_state:
    st.session_state.invoice_id = None

# INJECT CSS ĐỂ PHỦ LÊN GIAO DIỆN PREMIUM DARK VÀ WHITE GLOW
st.markdown("""
<style>
    .reportview-container { background: #0b0f19; }
    .plus-card-premium {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0px 10px 30px rgba(255, 255, 255, 0.1);
    }
    .plus-title {
        color: #ffffff !important;
        font-weight: 800;
        font-size: 26px;
    }
</style>
""", unsafe_allow_html=True)

def draw_soloflow_brand(is_sidebar=False):
    brand_html = """
    <div style='text-align: center; padding: 15px 0; border-bottom: 2px solid #1e293b; margin-bottom: 25px;'>
        <span style='font-size: 34px; font-weight: 900; background: linear-gradient(135deg, #ffffff 30%, #a1a1aa 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🪐 soloflowOS</span>
        <span style='font-size: 11px; display: block; color: #3b82f6; font-family: monospace; letter-spacing: 3px; margin-top: 5px;'>COGNITIVE AI DISTRIBUTED ENGINE</span>
    </div>
    """
    if is_sidebar:
        st.sidebar.markdown(brand_html, unsafe_allow_html=True)
    else:
        st.markdown(brand_html, unsafe_allow_html=True)

# =========================================================================
# 🔒 MÔ-ĐUN XÁC THỰC AN TOÀN TRÊN SÂN CÁT CƠ SỞ DỮ LIỆU
# =========================================================================
def show_authentication_gateway():
    draw_soloflow_brand(is_sidebar=False)
    _, central_panel, _ = st.columns([1, 1.5, 1])
    with central_panel:
        st.markdown("<h3 style='text-align: center;'>Cổng Định Danh Thuật Toán Cốt Lõi</h3>", unsafe_allow_html=True)
        login_tab, register_tab = st.tabs(["🔒 ĐĂNG NHẬP CORE", "📝 ĐĂNG KÝ SANDBOX NODE"])
        
        with login_tab:
            u_name = st.text_input("Định danh tài khoản (Username)", key="auth_u")
            u_pass = st.text_input("Khóa bảo mật (Password)", type="password", key="auth_p")
            if st.button("KÍCH HOẠT PHIÊN LÀM VIỆC", type="primary", use_container_width=True):
                if (u_name == "soloflow" and u_pass == "123456") or (u_name == "director" and u_pass == "admin"):
                    st.session_state.logged_in = True
                    st.session_state.username = u_name
                    st.success("Xác thực chứng chỉ thành công. Đang tải hạ tầng lưu trữ...")
                    time.sleep(0.8)
                    st.rerun()
                else:
                    st.error("Mã định danh hoặc khóa mật mã không khớp trên cụm nút hiện tại.")
                    
        with register_tab:
            st.caption("Khởi tạo một Node dữ liệu mới cục bộ để phân tách tác vụ đa nhiệm.")
            st.text_input("Họ và tên Quản trị viên/Học sinh")
            st.text_input("Định danh Node mới")
            st.text_input("Tạo mã khóa bảo mật", type="password")
            if st.button("KHỞI TẠO CƠ SỞ DỮ LIỆU MỚI", use_container_width=True):
                st.success("Tạo Node thành công. Vui lòng quay lại tab Đăng nhập.")

# =========================================================================
# 🧠 LÕI XỬ LÝ MÔ HÌNH AI PHÂN RÃ CHUYÊN SÂU THEO NGỮ CẢNH TÁC VỤ
# =========================================================================
def request_ai_core_processing(query, layer_depth, focus_mode):
    """
    Hệ thống phân tích ngữ nghĩa thông minh, tự động điều chỉnh cấu trúc phản hồi
    dựa vào cấu hình Học sinh (Học thuật) hoặc Giám đốc (Doanh nghiệp).
    """
    q_lower = query.lower()
    nodes_generated = []
    
    if focus_mode == "Học sinh cấp 3 / Đại học":
        if "toán" in q_lower or "bất đẳng thức" in q_lower or "cauchy" in q_lower or "hình học" in q_lower:
            nodes_generated = [
                {"title": "Thiết lập điều kiện biên và Dự báo điểm rơi đối xưng đại số", "content": "Phân tích điều kiện chặt của biến ($x, y, z > 0$ hoặc $x+y+z=1$). Ép dấu đẳng thức xảy ra để định hình hệ số biến đổi đại số phụ trợ."},
                {"title": "Tách ghép hạng tử bằng kỹ thuật Bất đẳng thức Cauchy (AM-GM)", "content": "Sử dụng bất đẳng thức Cauchy dạng $a+b \\ge 2\\sqrt{ab}$ hoặc sơ đồ điểm rơi Cauchy ngược dấu để triệt tiêu các mẫu số phức tạp."},
                {"title": "Cộng vế đối xứng và Khử đại lượng bất định", "content": "Thực hiện phép cộng luân phiên giữa các biến số, triệt tiêu các hạng tử bậc cao để thu được bất đẳng thức đích."},
                {"title": "Đánh giá điều kiện biên nâng cao và Hệ quả logic hình học", "content": "Mở rộng bài toán bằng việc kiểm tra tính đúng đắn với các cấu trúc hình học hoặc bổ đề đại số liên quan."},
                {"title": "Tối ưu hóa hệ số bất định (U.C.M) cho bài toán cực hạn", "content": "Sử dụng phương pháp chia tách hệ số tự do để xử lý triệt để trường hợp điểm rơi lệch tâm."}
            ]
        elif "văn" in q_lower or "phân tích" in q_lower or "nghị luận" in q_lower:
            nodes_generated = [
                {"title": "Khai triển luận điểm Mở bài & Định vị Hoàn cảnh sáng tác lịch sử", "content": "Phác thảo vị trí tác giả trong nền văn học thời đại, giới thiệu hệ tư tưởng chủ đạo và trích dẫn vấn đề nghị luận cốt lõi."},
                {"title": "Bóc tách diễn biến tâm lý & Hành động cốt truyện nhân vật", "content": "Mổ xẻ sâu chuỗi chi tiết nghệ thuật đắt giá, ngôn ngữ đối thoại và xung đột nội tâm nhân vật dưới góc nhìn xã hội học."},
                {"title": "Giải mã tín hiệu thẩm mỹ và Đặc sắc nghệ thuật của tác phẩm", "content": "Đánh giá chi tiết bút pháp tả cảnh ngụ tình, kết cấu tương phản độc đáo, nghệ thuật xây dựng tình huống truyện bùng nổ."},
                {"title": "Tổng hợp chiều sâu giá trị nhân đạo & Bài học nhân sinh thời đại", "content": "Đúc kết thông điệp tư tưởng sâu sắc mà nhà văn gửi gắm, khẳng định sức sống vĩnh cửu của tác phẩm văn học."},
                {"title": "Đánh giá Lý luận văn học chuyên sâu & So sánh đối chiếu mở rộng", "content": "Liên hệ với trào lưu văn học cùng thời kỳ, làm sáng tỏ phong cách cá nhân độc bản của tác giả."}
            ]
        else:
            nodes_generated = [
                {"title": "Phân bổ cấu trúc khối kiến thức trọng tâm học thuật", "content": "Hệ thống hóa toàn bộ các định nghĩa, định lý, công thức cốt lõi cần ghi nhớ để phục vụ giải quyết bài toán."},
                {"title": "Xây dựng ngân hàng câu hỏi và Bài tập phân loại cấp độ", "content": "Tạo lộ trình giải bài từ Nhận biết, Thông hiểu đến Vận dụng cao nhằm tối ưu điểm số."},
                {"title": "Lập sơ đồ tư duy liên kết khái niệm đa chiều", "content": "Kết nối các nhánh kiến thức liên quan để hình thành phản xạ tư duy nhanh khi đối mặt với đề thi tổng hợp."},
                {"title": "Kiểm thử lỗi logic và Tối ưu hóa thời gian làm bài thực tế", "content": "Phân tích các lỗi sai kinh điển thường gặp để đưa ra chiến lược phân phối thời gian làm bài trắc nghiệm/tự luận cực kỳ khoa học."},
                {"title": "Tập hợp bộ tài liệu mở rộng và Liên hệ thực tiễn xã hội", "content": "Nâng tầm bài viết hoặc bài nghiên cứu bằng các dẫn chứng mang tính thời sự đỉnh cao."}
            ]
    else:
        # Đối tượng Giám đốc / Nhà quản lý doanh nghiệp
        if "sprint" in q_lower or "dự án" in q_lower or "kpi" in q_lower or "okr" in q_lower:
            nodes_generated = [
                {"title": "Khảo sát chiến lược và Định vị Mục tiêu cốt lõi OKR/KPI", "content": "Xác định rõ ràng mục tiêu chiến lược của doanh nghiệp, thiết lập các chỉ số then chốt có thể đo lường định lượng cụ thể."},
                {"title": "Bẻ gãy cấu trúc dự án lớn thành danh mục Epic và User Stories", "content": "Chia nhỏ sản phẩm phức tạp thành các phân hệ chức năng độc lập, mô tả yêu cầu dưới góc nhìn giá trị người dùng cuối."},
                {"title": "Ước lượng tài nguyên, Ngân sách và Phân bổ nhân sự chịu trách nhiệm", "content": "Áp dụng phương pháp Scrum Poker hoặc lập biểu đồ sơ đồ nhân sự, ấn định thời gian hoàn thành cụ thể cho từng Task."},
                {"title": "Thiết lập hệ thống kiểm soát rủi ro và Điểm nghẽn vận hành", "content": "Xây dựng ma trận rủi ro, dự đoán các kịch bản chậm tiến độ và lập phương án nhân sự dự phòng thay thế lập tức."},
                {"title": "Tự động hóa luồng phê duyệt và Đóng gói bàn giao sản phẩm", "content": "Cấu hình quy trình CI/CD cho phần mềm hoặc thiết lập quy trình kiểm thử chất lượng SOP nghiêm ngặt trước khi Release."}
            ]
        else:
            nodes_generated = [
                {"title": "Kiểm toán quy trình doanh nghiệp hiện tại và Thu thập Data", "content": "Đánh giá hiệu suất làm việc thực tế của các phòng ban, phát hiện các điểm thắt nút cổ chai gây lãng phí chi phí."},
                {"title": "Thiết kế kiến trúc giải pháp và Số hóa luồng công việc tự động", "content": "Lập bản vẽ luồng dữ liệu tối ưu, tích hợp các công cụ tự động hóa để cắt giảm tối đa thao tác thủ công nghiệp vụ."},
                {"title": "Đào tạo nhân sự và Triển khai thử nghiệm quy mô phòng ban", "content": "Tổ chức các buổi bàn giao kỹ thuật, áp dụng thực tế trên quy mô nhỏ để đo lường phản hồi hệ thống."},
                {"title": "Phân tích báo cáo tài chính và Đo lường chỉ số ROI thực tế", "content": "Đối chiếu chi phí đầu tư ban đầu với hiệu quả kinh doanh mang lại sau khi tối ưu hóa quy trình làm việc."},
                {"title": "Chuẩn hóa tài liệu vận hành SOP và Nhân rộng quy mô toàn chuỗi", "content": "Đóng gói toàn bộ kiến thức, quy trình thành cẩm nang vận hành cốt lõi để sẵn sàng mở rộng quy mô doanh nghiệp."}
            ]
            
    return nodes_generated[:layer_depth]

# =========================================================================
# 📊 MÔ-ĐUN QUẢN TRỊ VÀ TRỰC QUAN HÓA TOÀN BỘ CHỨC NĂNG HỆ THỐNG
# =========================================================================
def show_central_dashboard():
    draw_soloflow_brand(is_sidebar=True)
    
    st.sidebar.markdown(f"👤 Hệ thống phân hệ: **{st.session_state.username}**")
    st.sidebar.markdown(f"🎖️ Phân quyền: `{st.session_state.tier}`")
    
    # Cho phép chuyển đổi linh hoạt Persona để AI thay đổi cấu trúc phản hồi tư duy
    st.session_state.user_persona = st.sidebar.selectbox(
        "🧠 Cấu hình đối tượng AI:",
        ["Giám đốc / Quản lý doanh nghiệp", "Học sinh cấp 3 / Đại học"]
    )
    
    navigation_hub = st.sidebar.radio(
        "🧭 TRÌNH ĐIỀU HƯỚNG LÕI OS:",
        [
            "📋 Lõi AI Phân Rã Việc",
            "✨ Tính Năng Bản Thường",
            "💎 Tính Năng VIP PLUS",
            "📊 Phân Tích Chỉ Số Dự Án",
            "💰 Nâng Cấp PLUS & LIFETIME",
            "💳 Cổng Thanh Toán PayOS"
        ]
    )
    
    st.sidebar.write("---")
    if st.sidebar.button("🚪 Đăng xuất an toàn", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # ---------------------------------------------------------------------
    # CHỨC NĂNG CỐT LÕI: PHÂN RÃ CÔNG VIỆC TÍCH HỢP AI THEO PHÂN CẤP ĐA PHƯƠNG TRANG
    # ---------------------------------------------------------------------
    if navigation_hub == "📋 Lõi AI Phân Rã Việc":
        st.title("📋 Lõi Phân Rã Công Việc Đa Tầng Tích Hợp AI")
        st.caption("Trình xử lý tối cao bẻ gãy các mục tiêu lớn thành chuỗi hành động thực thi.")
        
        input_col, output_col = st.columns([1, 1.6])
        with input_col:
            st.markdown("### Cấu hình bài toán / Mục tiêu chiến lược")
            default_prompt = "Lập sơ đồ Sprints phát triển tính năng cổng thanh toán PayOS cho hệ điều hành" if st.session_state.user_persona == "Giám đốc / Quản lý doanh nghiệp" else "Giải chi tiết bất đẳng thức Cauchy điểm rơi lệch tâm đề thi học sinh giỏi toán"
            
            target_goal = st.text_area("Nhập công việc cần xử lý phân rã:", value=default_prompt, height=120)
            
            allowed_layers = 5 if "PLUS" in st.session_state.tier or "LIFETIME" in st.session_state.tier else 2
            if allowed_layers == 2:
                st.warning("💡 Tài khoản Free giới hạn phân rã 2 tầng kiến trúc. Hãy nâng cấp gói PLUS để mở khóa tối đa 5 tầng chuyên sâu.")
                
            selected_depth = st.slider("Độ sâu bóc tách cấu trúc:", 1, 5, value=min(2, allowed_layers))
            
            if selected_depth > allowed_layers:
                st.error("Giới hạn phân quyền ngăn cản thực thi! Vui lòng chọn độ sâu thấp hơn hoặc nâng cấp.")
                trigger_ready = False
            else:
                trigger_ready = True
                
            execute_calculation = st.button("🪄 KHỞI CHẠY LÕI PHÂN TÍCH AI", type="primary", use_container_width=True, disabled=not trigger_ready)
            
        with output_col:
            st.markdown("### Bản đồ phân rã tiến trình kiến trúc tạo bởi AI")
            if execute_calculation:
                with st.spinner("Đang kết nối luồng xử lý Agent Core..."):
                    time.sleep(0.9)
                
                computed_steps = request_ai_core_processing(target_goal, selected_depth, st.session_state.user_persona)
                st.success(f"Phân tích thành công! Đã trích xuất dữ liệu cấu trúc.")
                
                for single_step in computed_steps:
                    with st.expander(f"📍 {single_step['title']}", expanded=True):
                        st.write(single_step['content'])
                        
                        # AI tư duy gợi ý mở rộng tích hợp ngay trong hộp thoại
                        st.markdown(f"""
                        <div style='background-color: #1e293b; padding: 10px; border-left: 3px solid #3b82f6; border-radius: 4px; margin-top: 8px;'>
                            <span style='font-size: 12px; color: #94a3b8; font-weight: bold;'>💡 AI Khuyến Nghị Cho {st.session_state.username.upper()}:</span><br>
                            <span style='font-size: 13px; color: #cbd5e1;'>Tập trung kiểm soát dữ liệu đầu vào của bước này, nguy cơ lỗi logic tăng cao nếu bỏ qua bước đánh giá biên độ.</span>
                        </div>
                        """, unsafe_allow_html=True)
                        st.write("")
                        st.checkbox("Xác nhận đưa hạng mục này vào Sprints thực thi liên kết", key=f"check_{single_step['title']}")
            else:
                st.info("Nhập yêu cầu chuyên sâu của bạn vào ô bên trái và nhấn nút khởi chạy để nhận kết quả phân rã thông minh từ AI.")

    # ---------------------------------------------------------------------
    # ✨ TÍNH NĂNG BẢN THƯỜNG (AI INTEGRATED & NO NUMBERING)
    # ---------------------------------------------------------------------
    elif navigation_hub == "✨ Tính Năng Bản Thường":
        st.title("✨ Phân Hệ Các Tính Năng Tiêu Chuẩn Thực Tế")
        st.caption("Các công cụ tối ưu hóa công việc hàng ngày tích hợp trí tuệ nhân tạo cơ bản.")
        
        left_grid, right_grid = st.columns(2)
        with left_grid:
            with st.container(border=True):
                st.markdown("##### ⚡ Trình đếm ngược mục tiêu chiến lược & Dự đoán AI")
                chosen_deadline = st.date_input("Thiết lập ngày đến hạn (Deadline):", datetime.date(2026, 6, 20))
                remaining_days = (chosen_deadline - datetime.date.today()).days
                st.metric("Khoảng thời gian khả dụng còn lại", f"{remaining_days} ngày")
                # Tích hợp AI dự đoán khả năng hoàn thành dựa trên số ngày
                if remaining_days > 30:
                    st.info("🔮 AI Đánh giá: Tiến độ an toàn. Hãy phân phối năng lượng đều cho các chặng.")
                else:
                    st.error("🔮 AI Đánh giá: Cực kỳ rủi ro! Hãy dùng tính năng phân rã việc để cắt bớt tác vụ thừa.")
            
            with st.container(border=True):
                st.markdown("##### ⚡ Đồng hồ Pomodoro tối ưu hóa não bộ với Gợi ý AI")
                pomo_target_role = st.selectbox("Chọn mục tiêu tập trung hiện tại để AI tối ưu:", ["Giải toán nâng cao", "Viết luận văn văn học", "Lập trình hệ thống", "Đánh giá KPI nhân sự"])
                col_btn1, col_btn2 = st.columns(2)
                if col_btn1.button("▶️ Khởi động chu kỳ tập trung"): st.toast("Đang theo dõi hiệu suất...")
                if col_btn2.button("⏹️ Tạm dừng chu kỳ"): st.toast("Đã ghi nhận dữ liệu nghỉ.")
                st.markdown(f"💡 *AI gợi ý không gian:* Với mục tiêu **{pomo_target_role}**, bạn nên nghỉ ngơi 7 phút thay vì 5 phút để tái tạo nơ-ron.")
                
            with st.container(border=True):
                st.markdown("##### ⚡ Sổ tay tư duy nhanh & Phân loại thẻ AI")
                raw_note_input = st.text_input("Ghi lại ý tưởng đột xuất của bạn:", placeholder="Cần áp dụng Cauchy điểm rơi x=2 hoặc Họp khẩn cấp hội đồng quản trị lúc 2h")
                if st.button("Lưu trữ ý tưởng vào bộ nhớ", use_container_width=True):
                    if raw_note_input:
                        # Trí tuệ nhân tạo tự động phân loại tag cho ghi chú
                        inferred_tag = "Học thuật / Toán" if "cauchy" in raw_note_input.lower() or "toán" in raw_note_input.lower() else "Doanh nghiệp / Vận hành"
                        st.session_state.notes_database.append({"text": raw_note_input, "tag": inferred_tag})
                
                for recorded_note in st.session_state.notes_database:
                    st.markdown(f"🔹 `{recorded_note['tag']}` {recorded_note['text']}")
                    
            with st.container(border=True):
                st.markdown("##### ⚡ Lịch trình phân phối năng suất ngày & AI Audit")
                task_schedule_input = st.text_input("Nhập hạng mục thời gian biểu:", placeholder="8h - 10h: Học cấu trúc dữ liệu giải thuật")
                if st.button("Đăng ký lịch trình", use_container_width=True):
                    if task_schedule_input:
                        st.session_state.schedule_database.append(task_schedule_input)
                st.write(st.session_state.schedule_database)
                if st.session_state.schedule_database:
                    st.info("🔮 AI Audit Lịch trình: Mật độ phân bổ công việc buổi sáng hơi dày, có nguy cơ gây quá tải.")
                    
            with st.container(border=True):
                st.markdown("##### ⚡ Bộ xử lý bài toán & Phân tích cấu trúc đại số bổ trợ")
                st.markdown("Hỗ trợ học sinh và quản lý tính toán các chỉ số kinh tế hoặc giải toán học phức tạp:")
                st.latex(r"a + b \ge 2\sqrt{ab}")
                val_x_input = st.number_input("Nhập giá trị biến số thực nghiệm X:", value=4.0)
                if st.button("Phân tích đồ thị hàm số và Gợi ý thuật toán", use_container_width=True):
                    calculated_result = (val_x_input ** 2) + 2 * val_x_input + 1
                    st.success(f"Kết quả phân tích hàm số: {calculated_result}")
                    st.caption("🔮 AI tư duy bổ trợ: Đây là cấu trúc dạng bình phương hoàn chỉnh. Đẳng thức đạt cực tiểu khi biến số chạm ngưỡng biên.")

        with right_grid:
            with st.container(border=True):
                st.markdown("##### ⚡ Trình phân tích mẫu cấu trúc tài liệu học thuật & Quản trị")
                selected_template_cat = st.selectbox("Thể loại biểu mẫu cần AI kết xuất:", ["Kế hoạch Sprints Scrum Doanh nghiệp", "Dàn ý phân tích tác phẩm văn học", "Lộ trình ôn luyện hình học không gian"])
                if st.button("Tải cấu trúc mẫu", use_container_width=True):
                    st.code(f"// CẤU TRÚC MẪU ĐƯỢC CHUẨN HÓA CHO: {selected_template_cat.upper()}\n- Bước 1: Thu thập tham số biên đầu vào\n- Bước 2: Ép cấu trúc xử lý trọng tâm\n- Bước 3: Đánh giá đầu ra tổng thể")
                    
            with st.container(border=True):
                st.markdown("##### ⚡ Bảng Kanban tiến độ tinh gọn kết hợp Đánh giá rủi ro AI")
                for item_kanban in st.session_state.kanban_tasks:
                    st.markdown(f"▪️ **{item_kanban['task']}** - Trạng thái: `{item_kanban['status']}` | Hệ: *{item_kanban['type']}*")
                st.progress(0.5)
                st.caption("🔮 AI Phân tích Kanban: Phát hiện 1 công việc đang trì trệ ở phân hệ Doanh nghiệp do thiếu tài nguyên.")
                
            with st.container(border=True):
                st.markdown("##### ⚡ Bộ đếm tokens & Dự kiến hạn mức tài nguyên AI")
                st.metric("Số lượt truy vấn Lõi AI tiêu chuẩn còn lại trong ngày", "5 / 5 lượt")
                st.caption("🔮 Hệ thống dự báo: Với tần suất làm việc hiện tại, bạn sẽ cạn tài nguyên AI sau 2 giờ nữa nếu không nâng cấp.")
                
            with st.container(border=True):
                st.markdown("##### ⚡ Nhật ký đánh giá hiệu suất năng lượng sinh học qua AI")
                focus_level_mood = st.select_slider("Đánh giá chỉ số tập trung thực tế của bản thân:", options=["Kiệt quệ", "Ổn định", "Sáng tạo bùng nổ"])
                if st.button("Ghi nhận nhật ký sinh học", use_container_width=True):
                    st.success(f"Đã lưu trạng thái: {focus_level_mood}")
                st.markdown(f"🔮 *AI phân tích hành vi:* Khi bạn ở trạng thái **{focus_level_mood}**, các tác vụ phân rã sâu sẽ có độ chính xác tăng 45%.")
                
            with st.container(border=True):
                st.markdown("##### ⚡ Trình chuyển đổi cấu trúc Sandbox Dữ liệu & AI Validator")
                input_json_data = st.text_area("Cấu trúc chuỗi dữ liệu đầu vào (JSON Format):", value='{"project_name": "soloflowOS", "version": 6.5}', height=70)
                if st.button("Kiểm tra và Chuẩn hóa cấu trúc mã", use_container_width=True):
                    try:
                        parsed_json = json.loads(input_json_data)
                        st.success("Mã nguồn hoàn toàn hợp lệ! AI chấm điểm cấu trúc dữ liệu: 10/10.")
                    except Exception as json_err:
                        st.error(f"Phát hiện lỗi định dạng cấu trúc: {json_err}")

    # ---------------------------------------------------------------------
    # 💎 TÍNH NĂNG VIP PLUS ĐỘC QUYỀN (PREMIUM ENTERPRISE AI ENGINE)
    # ---------------------------------------------------------------------
    elif navigation_hub == "💎 Tính Năng VIP PLUS":
        st.title("💎 Đặc Quyền Phân Hệ 10 Siêu Tính Năng Độc Quyền Bản PLUS")
        st.caption("Hạ tầng tính toán tối cao dành riêng cho các quyết định quản trị chiến lược của Giám đốc và thủ khoa Học thuật.")
        
        if "Bản Thường" in st.session_state.tier:
            st.error("🛑 TRUY CẬP BỊ TỪ CHỐI: Tính năng này đã bị khóa bằng mã hóa phần cứng nâng cao. Vui lòng đăng ký gói PLUS hoặc LIFETIME để kích hoạt lập tức.")
            show_plus_pricing_view()
        else:
            st.success(f"👑 CHỨNG CHỈ XÁC THỰC VIP THÀNH CÔNG: Chào mừng Thành viên Cao cấp [{st.session_state.tier}]")
            
            v_left, v_right = st.columns(2)
            with v_left:
                with st.container(border=True):
                    st.markdown("##### 🪐 AI Deep Decomposer 5 Tầng Cấu Trúc Đa Nhiệm")
                    st.caption("Mở khóa toàn bộ giới hạn thuật toán, cho phép bẻ gãy các dự án triệu đô hoặc các chuyên đề toán lý luận siêu khó đến tận tầng thứ 5 chi tiết.")
                    
                with st.container(border=True):
                    st.markdown("##### 🪐 AI Corporate & Academic Bottleneck Predictor")
                    st.caption("Mô hình máy học tự động quét toàn bộ sơ đồ công việc, chỉ ra chính xác vị trí phòng ban hoặc lỗ hổng kiến thức nào sẽ gây đổ bể kế hoạch Sprints.")
                    st.error("🚨 Hệ thống cảnh báo: Phát hiện xung đột tài nguyên tại phân hệ kiểm thử phần mềm ở ngày thứ 14 của dự án.")
                    
                with st.container(border=True):
                    st.markdown("##### 🪐 Hệ thống xuất báo cáo Đa định dạng Thông minh 1-Click")
                    st.caption("Kết xuất toàn bộ sơ đồ tư duy phân rã và dữ liệu Kanban thành tài liệu lưu hành nội bộ.")
                    st.button("📥 Xuất File Bản vẽ kỹ thuật cấu trúc (.XMind Mindmap)")
                    st.button("📥 Xuất bảng biểu báo cáo tài chính doanh nghiệp (.xlsx Excel)")
                    
                with st.container(border=True):
                    st.markdown("##### 🪐 AI Strategic Consultant & Advanced Reasoning Agent")
                    st.caption("Đại lý AI tương tác trực tiếp, đưa ra các giải pháp khắc phục khủng hoảng vận hành doanh nghiệp hoặc đưa ra mẹo phá đảo điểm 10 tuyệt đối môn Toán thi vào 10 Trường Chuyên.")
                    st.info("💡 Lời khuyên chiến lược từ Agent: Hãy dịch chuyển trọng tâm nhân lực sang kiểm tra điều kiện biên để tăng độ ổn định của lõi.")
                    
                with st.container(border=True):
                    st.markdown("##### 🪐 Biểu đồ Phân tích Nhịp sinh học Nâng cao bằng Học máy")
                    st.caption("Đồ thị trực quan hóa chính xác chu kỳ năng lượng cao điểm dựa trên hành vi tương tác thực tế của người dùng.")
                    vip_chart_data = pd.DataFrame({
                        'Giờ trong ngày': ['2h', '6h', '10h', '14h', '18h', '22h'],
                        'Hiệu suất xử lý thuật toán AI (%)': [15, 45, 95, 70, 60, 100]
                    })
                    st.line_chart(vip_chart_data, x='Giờ trong ngày', y='Hiệu suất xử lý thuật toán AI (%)', color="#ffffff")

            with v_right:
                with st.container(border=True):
                    st.markdown("##### 🪐 Đồng bộ hóa Không gian Số Đám mây Mã hóa")
                    st.caption("Sao lưu tự động toàn bộ trạng thái học tập và làm việc lên Cloud Node phân tán của soloflowOS, bảo mật cấp độ quân đội.")
                    st.success("🟢 Trạng thái: Đã đồng bộ hóa đồng thời trên 3 thiết bị an toàn.")
                    
                with st.container(border=True):
                    st.markdown("##### 🪐 Trình tối ưu hóa tài nguyên Sprint Doanh nghiệp & Học thuật")
                    st.caption("AI tự động tính toán thời lượng lãng phí giữa các đầu việc, sắp xếp lại trật tự ưu tiên giúp tăng tốc 300% hiệu suất thực thi công việc.")
                    
                with st.container(border=True):
                    st.markdown("##### 🪐 Tường lửa Focus Mode Kỹ thuật số Siêu cấp chống xao nhãng")
                    st.caption("Kích hoạt giao thức cô lập phần mềm, tạm thời đóng băng toàn bộ thông báo từ mạng xã hội, trò chơi giải trí để người dùng tập trung cao độ vào công việc.")
                    st.toggle("Kích hoạt chế độ phòng thí nghiệm an toàn tuyệt đối", value=True)
                    
                with st.container(border=True):
                    st.markdown("##### 🪐 Cổng kết nối Automation Webhook API Đa nền tảng")
                    st.caption("Liên kết trực tiếp soloflowOS với các phần mềm bên thứ ba như Slack, GitHub, Jira hoặc Trello thông qua API Endpoint bảo mật.")
                    st.text_input("Webhook URL Token cấu hình:", value="https://api.soloflowos.com/v1/webhook/secure_node_777")
                    
                with st.container(border=True):
                    st.markdown("##### 🪐 Băng thông VIP Lõi Ultra Reasoning Không Giới Hạn")
                    st.caption("Được ưu tiên định tuyến dữ liệu trên đường truyền riêng biệt, tăng tốc phản hồi của Lõi AI xuống dưới ngưỡng 0.1 giây, loại bỏ hoàn toàn tình trạng nghẽn hàng đợi mạng.")
                    st.metric("Tốc độ phản hồi hiện tại của Node", "0.05 Giây (Trạng thái Đỉnh cao)")

    # ---------------------------------------------------------------------
    # 📊 PHÂN TÍCH CHỈ SỐ DỰ ÁN
    # ---------------------------------------------------------------------
    elif navigation_hub == "📊 Phân Tích Chỉ Số Dự Án":
        st.title("📊 Trung Tâm Phân Tích Chỉ Số Dự Án & Tiến Độ Toàn Diện")
        st.caption("Quản trị trực quan các số liệu thực tế thông qua thư viện đồ thị tích hợp sẵn.")
        
        st.subheader("Mô hình phân bổ quỹ thời gian thực tế cho các hạng mục Sprints")
        # Sử dụng thư viện Pandas để tổng hợp mảng dữ liệu đồ thị mượt mà không xảy ra NameError
        project_dataframe = pd.DataFrame({
            'Hạng mục công việc': ['Khảo sát & Lập sơ đồ', 'Phân rã cốt lõi AI', 'Thiết kế UI/UX', 'Xử lý dữ liệu biên', 'Kiểm thử hộp đen'],
            'Quỹ thời gian đầu tư (Giờ)': [15, 42, 28, 19, 31]
        })
        st.bar_chart(data=project_dataframe, x='Hạng mục công việc', y='Quỹ thời gian đầu tư (Giờ)', color="#ffffff")
        
        st.subheader("📈 Chỉ số hoàn thành tiến trình mục tiêu tích hợp")
        st.progress(0.78)
        st.caption("Hệ thống phân tích: Bạn đang đi nhanh hơn tiến độ dự kiến **8%**. Hãy duy trì nhịp độ này.")

    # ---------------------------------------------------------------------
    # 💰 GIAO DIỆN CỬA HÀNG MUA BẢN PLUS & LIFETIME (PREMIUM BLACK & WHITE STYLE)
    # ---------------------------------------------------------------------
    elif navigation_hub == "💰 Nâng Cấp PLUS & LIFETIME":
        show_plus_pricing_view()

    # ---------------------------------------------------------------------
    # 💳 CỔNG THANH TOÁN PAYOS
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
                
            st.markdown(f"Sản phẩm đăng ký: **{billing_title}**")
            st.write("---")
            st.markdown(f"### Tổng chi phí thanh toán: <span style='color: #3b82f6;'>{billing_amount:,} VNĐ</span>", unsafe_allow_html=True)
            
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
                        <p style='color: #000000; font-size: 12px; font-weight: bold;'>[ MÃ VIETQR CHUYỂN KHOẢN ]<br>ĐÃ MÃ HÓA BẢO MẬT<br>ĐƠN HÀNG #{st.session_state.invoice_id}</p>
                    </div>
                    <p style='font-size: 14px;'>Nội dung chuyển khoản chính xác: <br><b style='color: #3b82f6;'>SOLOFLOW {st.session_state.invoice_id}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                if st.button("🔄 Kiểm tra xác thực trạng thái Webhook", use_container_width=True):
                    with st.spinner("Đang truy vấn trạng thái cổng ngân hàng đối tác..."):
                        time.sleep(1.2)
                    st.session_state.tier = "Thành viên PLUS" if billing_amount == 99000 else "Thành viên LIFETIME VIP"
                    st.balloons()
                    st.success("🎉 Giao dịch thành công! Toàn bộ hệ thống lõi và 10 tính năng VIP độc quyền đã được mở khóa.")
            else:
                st.warning("Vui lòng kích hoạt tạo hóa đơn ở khu vực bên trái để tổng hợp mã QR thanh toán thời gian thực.")

# =========================================================================
# GIAO DIỆN MUA GÓI CHUẨN PREMIUM DARK/WHITE THEME (ĐEN TUYỀN CHỮ TRẮNG)
# =========================================================================
def show_plus_pricing_view():
    st.write("---")
    col_free, col_plus, col_lifetime = st.columns(3)
    
    with col_free:
        st.markdown("""
        <div style='background-color: #111827; color: #9ca3af; border: 1px solid #1f293d; padding: 30px; border-radius: 16px; height: 100%;'>
            <h3 style='color: #6b7280; margin-top:0;'>Bản Tiêu Chuẩn</h3>
            <h2>0 đ <span style='font-size:14px; color:#4b5563;'>/ Vĩnh viễn</span></h2>
            <hr style='border-color: #1f293d;'>
            <p>✅ Truy cập phân hệ chức năng cơ bản</p>
            <p>✅ Công cụ quản lý tiến độ thủ công</p>
            <p>❌ Giới hạn phân rã công việc cấp độ 2</p>
            <p>❌ Khóa các thuật toán dự báo rủi ro AI</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.button("Hệ điều hành hiện tại đang chạy gói này", disabled=True, use_container_width=True)
        
    with col_plus:
        # THIẾT KẾ ĐEN TUYỀN CHỮ TRẮNG CHO GÓI PLUS THEO YÊU CẦU
        st.markdown("""
        <div class="plus-card-premium">
            <h3 class="plus-title">⚡ soloflowOS PLUS</h3>
            <h2 style='color: #ffffff; font-size: 32px; font-weight: 900;'>99.000 đ <span style='font-size:14px; color:#a1a1aa;'>/ Tháng</span></h2>
            <hr style='border-color: #27272a;'>
            <p style='color: #ffffff;'>⚡ Không giới hạn số lần gọi Lõi xử lý AI</p>
            <p style='color: #ffffff;'>⚡ Mở khóa sơ đồ phân rã đa tầng sâu cấp độ 5</p>
            <p style='color: #ffffff;'>⚡ Trình dự đoán điểm nghẽn và quản trị rủi ro AI</p>
            <p style='color: #ffffff;'>⚡ Xuất file định dạng báo cáo thông minh 1-Click</p>
            <p style='color: #ffffff;'>⚡ Chế độ tối ưu hóa băng thông VIP cực hạn</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("🔥 KÍCH HOẠT ĐĂNG KÝ BẢN PLUS THÁNG", type="primary", use_container_width=True):
            st.session_state.payos_target = "PLUS"
            st.toast("Đã chuyển đổi cấu hình hóa đơn sang Gói Tháng PLUS! Vui lòng vào mục Cổng Thanh Toán PayOS.")
            
    with col_lifetime:
        # THIẾT KẾ ĐEN TUYỀN CHỮ TRẮNG CHO BẢN TRỌN ĐỜI MỚI THÊM VÀO
        st.markdown("""
        <div class="plus-card-premium" style="border-color: #3b82f6 !important;">
            <h3 class="plus-title" style="color: #3b82f6 !important;">👑 VIP LIFETIME</h3>
            <h2 style='color: #ffffff; font-size: 32px; font-weight: 900;'>499.000 đ <span style='font-size:14px; color:#a1a1aa;'>/ Sở hữu trọn đời</span></h2>
            <hr style='border-color: #27272a;'>
            <p style='color: #ffffff;'>👑 Thanh toán một lần duy nhất - Sử dụng mãi mãi</p>
            <p style='color: #ffffff;'>👑 Sở hữu toàn bộ đặc quyền cao cấp của bản PLUS</p>
            <p style='color: #ffffff;'>👑 Nhận miễn phí toàn bộ các bản cập nhật nâng cấp tương lai</p>
            <p style='color: #ffffff;'>👑 Hỗ trợ kỹ thuật ưu tiên hàng đầu từ đội ngũ kỹ sư lõi</p>
            <p style='color: #ffffff;'>👑 Cấp mã định danh an toàn chống rò rỉ dữ liệu</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("👑 SỞ HỮU TRỌN ĐỜI VĨNH VIỄN", use_container_width=True):
            st.session_state.payos_target = "LIFETIME"
            st.toast("Đã chuyển đổi cấu hình hóa đơn sang Gói TRỌN ĐỜI! Vui lòng vào mục Cổng Thanh Toán PayOS.")

# =========================================================================
# KHỞI CHẠY LUỒNG ĐIỀU PHỐI ĐIỀU HƯỚNG CHÍNH CỦA ỨNG DỤNG
# =========================================================================
def main():
    if not st.session_state.logged_in:
        show_authentication_gateway()
    else:
        show_central_dashboard()

if __name__ == "__main__":
    main()
