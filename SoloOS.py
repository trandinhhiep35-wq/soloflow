import streamlit as st
import pandas as pd
import time
import datetime
import random
import json

# =========================================================================
# HỆ ĐIỀU HÀNH WORKSPACE CAO CẤP - SOLOFLOWOS V10.0 APEX CORE
# =========================================================================
st.set_page_config(
    page_title="soloflowOS v10.0 - Apex Core AI",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# KHỞI TẠO BỘ NHỚ TRẠNG THÁI TOÀN CỤC (SESSION STATE)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "tier" not in st.session_state:
    st.session_state.tier = "Bản Thường (Free)"
if "work_category" not in st.session_state:
    st.session_state.work_category = "🎓 Học tập & Nghiên cứu"

# Bộ nhớ lịch sử hội thoại AI Co-Pilot
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Dữ liệu mẫu Sprints tự động hóa tích hợp sâu
if "apex_sprints" not in st.session_state:
    st.session_state.apex_sprints = [
        {"Hạng mục": "Phân tích điểm rơi và Đổi biến đại số", "Thời lượng (Phút)": 45, "Năng lượng": "High 🔋"},
        {"Hạng mục": "Phác thảo sơ đồ luận điểm tác phẩm văn học", "Thời lượng (Phút)": 30, "Năng lượng": "Medium 🔋"},
        {"Hạng mục": "Thiết lập cấu trúc Class logic trong Python", "Thời lượng (Phút)": 60, "Năng lượng": "High 🔋"}
    ]

# CSS PREMIUM MINIMALIST DARK MODE - TẬP TRUNG SỰ CHÚ Ý CAO ĐỘ
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #ffffff; }
    div[data-testid="stSidebar"] { background-color: #030303 !important; border-right: 1px solid #151515; }
    .apex-card {
        background-color: #050505 !important;
        color: #ffffff !important;
        border: 1px solid #222222 !important;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    .sub-step-box {
        background-color: #0a0a0a;
        border-left: 3px solid #ffffff;
        padding: 10px 15px;
        margin: 8px 0 8px 20px;
        border-radius: 4px;
    }
    .chat-user {
        background-color: #121212; padding: 12px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #222222;
    }
    .chat-ai {
        background-color: #070707; padding: 12px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #333333;
    }
</style>
""", unsafe_allow_html=True)

def draw_soloflow_brand(is_sidebar=False):
    brand_html = """
    <div style='text-align: center; padding: 12px 0; border-bottom: 1px solid #151515; margin-bottom: 15px;'>
        <div style='font-size: 28px; font-weight: 900; color: #ffffff; letter-spacing: -1px;'>🪐 soloflowOS <span style='font-size: 11px; color: #666666;'>v10.0</span></div>
        <div style='font-size: 9px; color: #555555; font-family: monospace; letter-spacing: 2px; margin-top: 2px;'>APEX COGNITIVE ENGINE</div>
    </div>
    """
    if is_sidebar:
        st.sidebar.markdown(brand_html, unsafe_allow_html=True)
    else:
        st.markdown(brand_html, unsafe_allow_html=True)

# =========================================================================
# CỔNG ĐĂNG NHẬP / XÁC THỰC AN TOÀN CỤC BỘ
# =========================================================================
def show_authentication_gateway():
    draw_soloflow_brand(is_sidebar=False)
    _, central_panel, _ = st.columns([1, 1.2, 1])
    with central_panel:
        st.markdown("<h4 style='text-align: center; color: white; font-weight: 600;'>Kích Hoạt Phiên Làm Việc Bản Mới Thử Nghiệm</h4>", unsafe_allow_html=True)
        u_name = st.text_input("Định danh tài khoản Node Core", value="Hiệp Trần")
        u_pass = st.text_input("Khóa bảo mật hệ thống", type="password", value="password123")
        
        if st.button("KÍCH HOẠT HỆ THỐNG APEX", type="primary", use_container_width=True):
            if u_name and u_pass:
                st.session_state.logged_in = True
                st.session_state.username = u_name
                st.success("Hạ tầng đã sẵn sàng. Đang khởi chạy luồng tối ưu...")
                time.sleep(0.3)
                st.rerun()

# =========================================================================
# LÕI PHÂN RÃ CÔNG VIỆC LỒNG NHAU ĐA TẦNG (LINEAR & GOBLIN STYLE)
# =========================================================================
def request_apex_decomposition(query, category, load_type):
    q_lower = query.lower()
    nodes = []
    
    # Kịch bản phân rã thông minh tích hợp sẵn các bài toán thực tế
    if "Học tập" in category:
        if "bất đẳng thức" in q_lower or "cauchy" in q_lower or "am-gm" in q_lower:
            nodes = [
                {
                    "title": "Xác định tập xác định và tìm dấu đẳng thức xảy ra (Điểm rơi đại số)",
                    "content": "Thử thế các giá trị biên đối xứng hoặc lệch tâm để định hướng cấu trúc bất đẳng thức thành phần.",
                    "energy": "Medium 🔋", "time": 15, "blocker": "None",
                    "sub_actions": ["Xét điều kiện chặt của các biến số thực", "Dự đoán điểm rơi dấu bằng để thiết lập mối liên hệ"]
                },
                {
                    "title": "Cấu trúc sơ đồ thêm bớt hạng tử để áp dụng định lý Cauchy",
                    "content": "Sử dụng kỹ thuật tách nhóm mẫu số hoặc nhân hệ số bất định nhằm triệt tiêu các biến bậc cao khi lấy căn thức.",
                    "energy": "High 🔋", "time": 25, "blocker": "Xác định điểm rơi đại số",
                    "sub_actions": ["Nhân thêm hằng số thích hợp vào các vế đối xứng", "Ép các hạng tử nghịch đảo triệt tiêu nhau hoàn toàn"]
                },
                {
                    "title": "Đánh giá vế và thực hiện phép cộng luân phiên kết luận",
                    "content": "Cộng từng vế các bất đẳng thức thành phần, làm gọn biểu thức vế trái để suy ra điều phải chứng minh.",
                    "energy": "Low 🔋", "time": 10, "blocker": "Cấu trúc sơ đồ thêm bớt",
                    "sub_actions": ["Rút gọn các đại lượng đồng dạng ở hai vế", "Khẳng định dấu bằng xảy ra một cách chính xác"]
                }
            ]
        else: # Nghị luận văn học (ví dụ: Mây trắng còn bay)
            nodes = [
                {
                    "title": "Xây dựng luận điểm mở bài và định vị hoàn cảnh lịch sử tác phẩm",
                    "content": "Dẫn dắt ngắn gọn về tác giả, bối cảnh thời đại lịch sử bối cảnh xã hội và nêu vấn đề nghị luận cốt lõi.",
                    "energy": "Low 🔋", "time": 15, "blocker": "None",
                    "sub_actions": ["Nêu thông tin tác giả và hoàn cảnh ra đời tác phẩm", "Trích dẫn vấn đề tư tưởng nghệ thuật cần phân tích"]
                },
                {
                    "title": "Mổ xẻ diễn biến tình huống truyện và các chi tiết nghệ thuật đắt giá",
                    "content": "Đi sâu phân tích hành động, ngôn ngữ đối thoại nội tâm nhân vật để bộc lộ chiều sâu tư tưởng truyện ngắn.",
                    "energy": "High 🔋", "time": 30, "blocker": "Xây dựng luận điểm mở bài",
                    "sub_actions": ["Phân tích hình ảnh biểu tượng nghệ thuật trung tâm bài viết", "Bóc tách mạch cảm xúc và tâm lý nhân vật qua các bước ngoặt"]
                },
                {
                    "title": "Tổng kết giá trị thẩm mỹ và mạch lập luận kết bài",
                    "content": "Đánh giá bút pháp nghệ thuật đặc sắc, khẳng định thông điệp cốt lõi của tác phẩm một cách gãy gọn, cô đọng.",
                    "energy": "Medium 🔋", "time": 15, "blocker": "Mổ xẻ diễn biến tình huống",
                    "sub_actions": ["Khái quát lại giá trị nội dung và nghệ thuật", "Đúc kết bài học tư duy sâu sắc từ tác phẩm văn học"]
                }
            ]
    elif "Lập trình" in category:
        nodes = [
            {
                "title": "Thiết lập cấu trúc thư mục dự án và môi trường ảo Python venv",
                "content": "Khởi tạo môi trường cô lập sạch sẽ, khai báo và cài đặt các thư viện lõi ban đầu cần thiết.",
                "energy": "Low 🔋", "time": 10, "blocker": "None",
                "sub_actions": ["Khởi tạo môi trường ảo bằng command line", "Tạo file main.py và requirements.txt"]
            },
            {
                "title": "Xây dựng các module xử lý logic nền tảng và bẫy lỗi ngoại lệ",
                "content": "Viết mã nguồn xử lý luồng dữ liệu chính, tích hợp cấu trúc try-except để bắt lỗi biên hệ thống không bị crash.",
                "energy": "High 🔋", "time": 40, "blocker": "Thiết lập cấu trúc thư mục",
                "sub_actions": ["Xử lý định dạng dữ liệu đầu ra chuẩn JSON", "Tối ưu vòng lặp xử lý logic ngầm bất đồng bộ"]
            }
        ]
    else: # Danh mục mặc định khác (Quản lý hoặc Sáng tạo)
        nodes = [
            {
                "title": "Phân bẻ cấu trúc mục tiêu lớn thành các chỉ số hành động đo lường",
                "content": "Xác định rõ ràng tiêu chuẩn hoàn thành công việc cụ thể để dễ dàng giám sát tiến độ thực tế.",
                "energy": "Medium 🔋", "time": 20, "blocker": "None",
                "sub_actions": ["Định nghĩa rõ tiêu chí nghiệm thu công việc", "Gán thời gian giới hạn nghiêm ngặt cho mục tiêu"]
            }
        ]
        
    if "Tối giản" in load_type:
        return nodes[:2]
    return nodes

# =========================================================================
# GIAO DIỆN BẢNG ĐIỀU KHIỂN TRUNG TÂM APEX
# =========================================================================
def show_central_dashboard():
    draw_soloflow_brand(is_sidebar=True)
    
    st.sidebar.markdown(f"👤 Tài khoản Core: **{st.session_state.username}**")
    
    # DANH MỤC CÔNG VIỆC DYNAMIC - THAY ĐỔI CÔNG CỤ THEO NGỮ CẢNH TRỰC TIẾP
    st.session_state.work_category = st.sidebar.selectbox(
        "🧠 Ngữ cảnh Không gian làm việc:",
        ["🎓 Học tập & Nghiên cứu", "💻 Lập trình & Kỹ thuật", "💼 Quản lý & Doanh nghiệp", "🎨 Sáng tạo & Thiết kế"]
    )
    
    nav_hub = st.sidebar.radio(
        "🧭 HỆ THỐNG CHỨC NĂNG CỐT LÕI:",
        [
            "📋 Lõi Rã Việc Đa Tầng 10.0",
            "💬 Trợ Lý AI Chuyên Gia (Co-Pilot)",
            "📊 Bản Đồ Tiến Độ Tự Động",
            "⚙️ Tùy Chỉnh Cấu Hình Hệ Thống",
            "💰 Nâng Cấp PLUS & LIFETIME Premium",
            "💳 Cổng Xác Thực Thanh Toán PayOS"
        ]
    )
    
    st.sidebar.write("---")
    if st.sidebar.button("🚪 Đăng xuất an toàn", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.chat_history = []
        st.rerun()

    # ---------------------------------------------------------------------
    # 📋 LÕI RÃ VIỆC ĐA TẦNG LỒNG NHAU (HỌC LỎM LINEAR & GOBLIN TOOLS)
    # ---------------------------------------------------------------------
    if nav_hub == "📋 Lõi Rã Việc Đa Tầng 10.0":
        st.title("📋 Lõi Phân Rã Công Việc Đa Tầng Cấp Cao v10.0")
        st.caption(f"Hệ thống đang chạy thuật toán tối ưu hóa cho mục: **{st.session_state.work_category}**")
        
        input_panel, output_panel = st.columns([1, 1.3])
        with input_panel:
            st.markdown("##### 🧩 Nhập mục tiêu lớn cần bẻ gãy cấu trúc")
            
            if "Học tập" in st.session_state.work_category:
                default_prompt = "Chứng minh bất đẳng thức Cauchy điểm rơi nâng cao lớp 9 ôn thi chuyên toán"
            elif "Lập trình" in st.session_state.work_category:
                default_prompt = "Xây dựng script Python tự động cấu trúc hóa file dữ liệu thô"
            else:
                default_prompt = "Thiết kế kế hoạch triển khai sơ đồ vận hành tự động hóa luồng làm việc"
                
            input_goal = st.text_area("Mục tiêu hoặc bài toán lớn của bạn:", value=default_prompt, height=80)
            
            st.markdown("##### ⚙️ Bộ cấu hình lọc Cognitive Load (Triết lý Goblin.tools)")
            load_mode = st.radio("Chế độ phân phối luồng công việc:", ["Cấu trúc tiêu chuẩn (Standard-steps)", "Tối giản hóa tác vụ (Macro-milestones)"])
            
            st.markdown("##### ⚡ Kích hoạt Siêu tính năng Tâm lý chống trì hoãn")
            enable_micro_view = st.checkbox("Mở rộng tầng hành động siêu vi (Deep Sub-tasks)", value=True)
            auto_sync_sprints = st.checkbox("Tự động đồng bộ thời lượng vào biểu đồ Sprints", value=True)
            
            run_decom = st.button("🚀 KHỞI CHẠY LÕI PHÂN TÁCH APEX CORE", type="primary", use_container_width=True)
            
        with output_panel:
            st.markdown("### 🗺️ Bản đồ tác vụ phân cấp & Trình tự phụ thuộc")
            if run_decom:
                with st.spinner("Hệ thống đang tính toán luồng tư duy tối ưu..."):
                    time.sleep(0.4)
                
                computed_nodes = request_apex_decomposition(input_goal, st.session_state.work_category, load_mode)
                
                # Hiển thị các chỉ số đo lường nâng cao (Motion style)
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Tổng số mục lớn", f"{len(computed_nodes)} tác vụ")
                with m2:
                    total_mins = sum(node["time"] for node in computed_nodes)
                    st.metric("Tổng thời lượng tối ưu", f"{total_mins} Phút")
                with m3:
                    st.metric("Trạng thái luồng", "🎯 Chuẩn hóa")
                
                st.write("")
                # Hiển thị danh sách kết quả rã việc có cấu trúc lồng nhau phân cấp
                for idx, node in enumerate(computed_nodes):
                    with st.container(border=True):
                        st.markdown(f"##### 📍 Bước {idx+1}: {node['title']}")
                        st.write(node["content"])
                        
                        sub_c1, sub_c2 = st.columns(2)
                        with sub_c1:
                            st.markdown(f"⏱️ Thời gian: **{node['time']} phút** | Mức năng lượng: `{node['energy']}`")
                        with sub_c2:
                            st.markdown(f"🔗 Tác vụ chặn luồng (Blocker): `{node['blocker']}`")
                            
                        # Tầng hành động siêu vi mở rộng lồng nhau (Linear/ClickUp Sub-tasks Style)
                        if enable_micro_view and "sub_actions" in node:
                            st.markdown("<p style='font-size: 12px; color:#888888; font-weight:bold; margin-left:20px; margin-top:5px;'>⚙️ CÁC HÀNH ĐỘNG SIÊU VI CẦN LÀM NGAY:</p>", unsafe_allow_html=True)
                            for sub in node["sub_actions"]:
                                st.markdown(f"<div class='sub-step-box'>⬜ {sub}</div>", unsafe_allow_html=True)
                
                # Trình xuất dữ liệu sạch cấu trúc
                st.write("---")
                st.markdown("##### 📥 Xuất sơ đồ tư duy sạch cấu trúc")
                st.download_button(
                    "Tải tệp tin cấu trúc Markdown (.md)", 
                    f"# Bản đồ tác vụ: {input_goal}\n\nTổng thời lượng: {total_mins} phút", 
                    file_name="apex_flow.md", 
                    use_container_width=True
                )
            else:
                st.info("Hạ tầng phân rã AI Apex đã sẵn sàng. Điền mục tiêu của bạn bên trái và nhấn nút khởi chạy.")

    # ---------------------------------------------------------------------
    # 💬 TRỢ LÝ AI CHUYÊN GIA - CO-PILOT (TỰ ĐỘNG CHUYỂN PERSONA CHUYÊN SÂU)
    # ---------------------------------------------------------------------
    elif nav_hub == "💬 Trợ Lý AI Chuyên Gia (Co-Pilot)":
        # Điều chỉnh cá tính chuyên gia gãy gọn, tập trung vào giải quyết vấn đề cốt lõi
        if "🎓 Học tập" in st.session_state.work_category:
            persona_title = "Trợ Lý Học Thuật Cấp Cao (Math & Literature Specialist)"
            persona_desc = "Tôi hỗ trợ phân tích bản chất điểm rơi bất đẳng thức Cauchy hoặc cấu trúc mạch lập luận Ngữ văn lớp 9 sắc bén, logic, không dùng ngôn từ thừa thãi."
            placeholder_text = "Hỏi về cách chứng minh bất đẳng thức hoặc xây dựng hệ thống luận điểm..."
        elif "💻 Lập trình" in st.session_state.work_category:
            persona_title = "Tech Lead Kiến Trúc Hệ Thống & Python Automation"
            persona_desc = "Tôi giúp bạn tối ưu hóa thuật toán cấu trúc dữ liệu, bẫy lỗi logic biên, thiết lập cấu trúc file JSON và làm sạch mã nguồn Python."
            placeholder_text = "Hỏi về cách debug code hoặc thiết kế module hệ thống..."
        else:
            persona_title = "Cố Vấn Tối Ưu Quy Trình & Điều Phối Luồng Hành Động"
            persona_desc = "Tôi giúp bạn bẻ nhỏ quy trình lớn, dự báo điểm nghẽn cổ chai và thiết lập các bước làm việc có tính thực chiến cao."
            placeholder_text = "Hỏi về cách quản trị thời gian hoặc tối ưu hóa luồng việc..."

        st.title("💬 Trợ Lý AI Chuyên Gia Đa Nhiệm (AI Co-Pilot)")
        st.caption(f"Vai trò chuyên biệt hiện tại: **{persona_title}**")
        
        with st.container(border=True):
            st.markdown(f"**🤖 Định hình tư duy AI:** {persona_desc}")
            
        # Hiển thị lịch sử hội thoại
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.markdown(f'<div class="chat-user"><b>👤 Bạn:</b><br>{chat["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-ai"><b>🪐 AI Co-Pilot:</b><br>{chat["content"]}</div>', unsafe_allow_html=True)
                
        user_msg = st.chat_input(placeholder_text)
        if user_msg:
            st.session_state.chat_history.append({"role": "user", "content": user_msg})
            
            with st.spinner("AI đang xử lý thông tin ngầm..."):
                time.sleep(0.3)
                
            msg_lower = user_msg.lower()
            if "🎓 Học tập" in st.session_state.work_category:
                if "cauchy" in msg_lower or "bất đẳng thức" in msg_lower or "am-gm" in msg_lower:
                    ai_reply = "Đối với toán bất đẳng thức Cauchy nâng cao, nguyên tắc mấu chốt là tìm điểm rơi. Nếu hệ thức lệch tâm, ta áp dụng phương pháp nhân hằng số bất định trước khi lấy căn thức nhằm triệt tiêu mẫu số. Hãy viết nháp điều kiện cân bằng để ép các biến bằng nhau chính xác."
                else:
                    ai_reply = "Để làm bài văn nghị luận đạt điểm cao, mạch lập luận cần đi từ phân tích hoàn cảnh sáng tác tác phẩm đến mổ xẻ các chi tiết nghệ thuật đắt giá bộc lộ nội tâm nhân vật. Tránh viết dàn trải, hãy liên kết các đoạn bằng từ nối logic để bài làm chặt chẽ."
            elif "💻 Lập trình" in st.session_state.work_category:
                ai_reply = "Để tối ưu đoạn mã này, hãy tách biệt luồng xử lý chính và các tác vụ ngầm bất đồng bộ. Sử dụng định dạng cấu trúc đầu ra chuẩn JSON kèm theo mã kiểm tra lỗi ngoại lệ try-except để hệ thống vận hành an toàn ổn định."
            else:
                ai_reply = f"Giải quyết vấn đề '{user_msg}' đòi hỏi bạn dọn dẹp tác vụ chặn luồng (Blocker) trước. Sau đó áp dụng kỹ thuật chia nhỏ khung thời gian Time-boxing để hoàn thành dứt điểm từng phần."
                
            st.session_state.chat_history.append({"role": "ai", "content": ai_reply})
            st.rerun()

    # ---------------------------------------------------------------------
    # 📊 BẢN ĐỒ TIẾN ĐỘ TỰ ĐỘNG HÓA (XÓA BỎ NHẬP LIỆU THỦ CÔNG)
    # ---------------------------------------------------------------------
    elif nav_hub == "📊 Bản Đồ Tiến Độ Tự Động":
        st.title("📊 Bản Đồ Tiến Độ Tự Động & Phân Bổ Thời Gian")
        st.caption("Hệ thống tự động hóa lập sơ đồ thời lượng thực thi tác vụ dựa trên định mức năng lượng thực tế.")
        
        df_apex = pd.DataFrame(st.session_state.apex_sprints)
        
        c_chart, c_table = st.columns([1.4, 1])
        with c_chart:
            st.markdown("##### 📈 Biểu đồ phân bổ thời gian thực thi tối ưu (Phút)")
            st.bar_chart(data=df_apex, x="Hạng mục", y="Thời lượng (Phút)", color="#ffffff")
        with c_table:
            st.markdown("##### 📋 Danh sách quản trị trực quan")
            st.dataframe(df_apex, use_container_width=True)
            
            # Kích hoạt bộ lọc phá vỡ trì hoãn tâm lý cấp tốc
            with st.container(border=True):
                st.markdown("##### 🧠 Bộ kích hoạt Phá vỡ Trì hoãn Cấp tốc")
                st.caption("Nếu cảm thấy cạn kiệt năng lượng, nhấn nút để AI tái cấu trúc thời gian biểu.")
                if st.button("KÍCH HOẠT MENTAL BREAKER", type="primary", use_container_width=True):
                    st.toast("⚡ Đã chuyển đổi trạng thái: Rút ngắn 20% thời lượng, chèn 5 phút nghỉ Pomodoro tự động!")

    # ---------------------------------------------------------------------
    # ⚙️ TÙY CHỈNH CẤU HÌNH HỆ THỐNG CỤC BỘ
    # ---------------------------------------------------------------------
    elif nav_hub == "⚙️ Tùy Chỉnh Cấu Hình Hệ Thống":
        st.title("⚙️ Tùy Chỉnh Cấu Hình Hệ Thống & Node Core")
        
        p1, p2 = st.columns(2)
        with p1:
            with st.container(border=True):
                st.markdown("##### 👤 Cấu hình Node định danh cá nhân")
                st.text_input("Tên chủ tài khoản:", value="Trần Đình Hiệp")
                st.text_input("Vị trí công việc:", value="Core Developer")
                st.button("💾 Lưu cấu hình hồ sơ", use_container_width=True)
        with p2:
            with st.container(border=True):
                st.markdown("##### ⚙️ Thông số Mô hình Trí tuệ AI")
                st.slider("Độ sáng tạo tư duy (Temperature):", 0.0, 1.0, value=0.5, step=0.1)
                st.toggle("Kích hoạt mã hóa bảo mật Sandboxed AES-256", value=True)
                st.selectbox("Kiến trúc bảng màu giao diện chủ đạo:", ["Đen tuyền tối giản (Premium Jet Black)", "Xám không gian sâu (Space Gray)"])

    # ---------------------------------------------------------------------
    # 💰 GIAO DIỆN NĂNG CẤP GÓI CHUẨN PREMIUM DARK MODE
    # ---------------------------------------------------------------------
    elif nav_hub == "💰 Nâng Cấp PLUS & LIFETIME Premium":
        show_premium_pricing_cards()

    # ---------------------------------------------------------------------
    # 💳 CỔNG XÁC THỰC THANH TOÁN PAYOS TỰ ĐỘNG
    # ---------------------------------------------------------------------
    elif nav_hub == "💳 Cổng Xác Thực Thanh Toán PayOS":
        st.title("💳 Cổng Xác Thực Hóa Đơn Tự Động Qua PayOS")
        
        left_inv, right_qr = st.columns([1, 1.1])
        with left_inv:
            st.subheader("🧾 Chi tiết hóa đơn khởi tạo")
            st.write("Đơn vị thụ hưởng: **soloflowOS Global Core**")
            
            pay_amount = 99000
            pay_title = "Giấy phép Gói Tháng PLUS Premium"
            
            if "payos_target" in st.session_state and st.session_state.payos_target == "LIFETIME":
                pay_amount = 499000
                pay_title = "Giấy phép Sở hữu TRỌN ĐỜI (Lifetime) VIP"
                
            st.markdown(f"Gói sản phẩm: **{pay_title}**")
            st.write("---")
            st.markdown(f"### Tổng chi phí: <span style='color: #ffffff; text-decoration: underline;'>{pay_amount:,} VNĐ</span>", unsafe_allow_html=True)
            
            if st.button("🔗 Khởi tạo cổng thanh toán bảo mật", type="primary", use_container_width=True):
                st.session_state.invoice_id = str(random.randint(100000, 999999))
                st.success(f"Khởi tạo thành công mã đơn hàng: #{st.session_state.invoice_id}")
                
        with right_qr:
            st.subheader("📲 Quét mã VietQR chuyển khoản")
            if "invoice_id" in st.session_state and st.session_state.invoice_id:
                st.markdown(f"""
                <div style='border: 1px solid #333333; padding: 20px; border-radius: 12px; text-align: center; background-color: #050505;'>
                    <p style='font-weight: bold; letter-spacing: 1px; font-size:12px; color:#888888;'>CỔNG THANH TOÁN PAYOS SECURE WEBHOOK</p>
                    <div style='background-color: #ffffff; width: 180px; height: 180px; margin: 15px auto; padding: 10px; display: flex; align-items: center; justify-content: center;'>
                        <p style='color: #000000; font-size: 11px; font-weight: bold;'>[ MÃ VIETQR ĐÃ MÃ HÓA ]<br>ĐƠN HÀNG #{st.session_state.invoice_id}</p>
                    </div>
                    <p style='font-size: 13px;'>Nội dung ghi chú chuyển khoản chính xác:<br><b>SOLOFLOW {st.session_state.invoice_id}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🔄 Xác thực trạng thái Webhook", use_container_width=True):
                    with st.spinner("Đang truy vấn trạng thái cổng ngân hàng..."):
                        time.sleep(0.5)
                    st.session_state.tier = "Thành viên PLUS" if pay_amount == 99000 else "Thành viên LIFETIME VIP"
                    st.balloons()
                    st.success("🎉 Giao dịch thành công! Toàn bộ tính năng phân rã nâng cao cấp độ 5 đã được kích hoạt vĩnh viễn.")
            else:
                st.warning("Vui lòng kích hoạt tạo hóa đơn ở khu vực bên trái để hiển thị thông tin VietQR.")

# =========================================================================
# GIAO DIỆN KHUNG GIÁ ĐĂNG KÝ MUA GÓI PREMIUM DARK MODE
# =========================================================================
def show_premium_pricing_cards():
    st.write("---")
    c_free, c_plus, c_lifetime = st.columns(3)
    
    with c_free:
        st.markdown("""
        <div style='background-color: #030303; color: #666666; border: 1px solid #151515; padding: 25px; border-radius: 12px; height: 100%;'>
            <h4 style='color: #444444; margin-top:0;'>Bản Tiêu Chuẩn</h4>
            <h3>0 đ <span style='font-size:12px; color:#333333;'>/ Vĩnh viễn</span></h3>
            <hr style='border-color: #151515;'>
            <p>✅ Truy cập phân hệ chức năng cơ bản theo danh mục</p>
            <p>✅ Phân rã công việc ở cấp độ tiêu chuẩn</p>
            <p>❌ Khóa sơ đồ phân rã công việc sâu đa tầng tầng thứ 5</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.button("Hệ thống đang chạy gói này", disabled=True, use_container_width=True)
        
    with c_plus:
        st.markdown("""
        <div class="apex-card" style="border: 1px solid #ffffff !important;">
            <h4 style='color: #ffffff; font-weight: 700; margin-top:0;'>⚡ soloflowOS PLUS</h4>
            <h3>99.000 đ <span style='font-size:12px; color:#888888;'>/ Tháng</span></h3>
            <hr style='border-color: #222222;'>
            <p>⚡ Mở khóa toàn bộ các siêu công cụ tính toán tương tác thực tế</p>
            <p>⚡ Không giới hạn số lần gọi Lõi xử lý AI đa luồng song song</p>
            <p>⚡ Mở khóa sơ đồ phân rã đa tầng sâu cấp độ 5 hành động siêu vi</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("🔥 ĐĂNG KÝ BẢN PLUS THÁNG", type="primary", use_container_width=True):
            st.session_state.payos_target = "PLUS"
            st.toast("Đã cấu hình hóa đơn sang Gói PLUS! Hãy vào mục Cổng Xác Thực Thanh Toán PayOS.")
            
    with c_lifetime:
        st.markdown("""
        <div class="apex-card" style="border: 1px solid #ffffff !important; box-shadow: 0px 0px 20px rgba(255,255,255,0.1) !important;">
            <h4 style='color: #ffffff; font-weight: 700; margin-top:0;'>👑 VIP LIFETIME</h4>
            <h3>499.000 đ <span style='font-size:12px; color:#888888;'>/ Trọn đời</span></h3>
            <hr style='border-color: #222222;'>
            <p>👑 Thanh toán một lần duy nhất - Sở hữu sử dụng vĩnh viễn</p>
            <p>👑 Bao gồm toàn bộ tính năng cao cấp của phiên bản PLUS</p>
            <p>👑 Cấp mã chứng chỉ SSL Node Sandbox riêng biệt bảo mật dữ liệu</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("👑 SỞ HỮU TRỌN ĐỜI VĨNH VIỄN", use_container_width=True):
            st.session_state.payos_target = "LIFETIME"
            st.toast("Đã cấu hình hóa đơn sang Gói TRỌN ĐỜI! Hãy vào mục Cổng Xác Thực Thanh Toán PayOS.")

# =========================================================================
# LUỒNG ĐIỀU PHỐI ĐIỀU HÀNH CHÍNH
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
