import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading

class TaskBreakdownApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("AI Task Decomposer Pro - Quản Lý & Rã Công Việc Thông Minh")
        self.geometry("1200x750")
        self.minimum_size = (1024, 650)
        self.minsize(*self.minimum_size)
        
        # Trạng thái người dùng (Mock Data)
        self.user_status = {
            "name": "Nguyễn Văn A",
            "email": "nguyenvana@gmail.com",
            "tier": "Free User",
            "ai_tokens_left": 5,
            "dark_mode": False
        }
        
        self.setup_styles()
        self.build_layout()
        self.show_frame("main_task")

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Cấu hình màu sắc chủ đạo
        self.colors = {
            "primary": "#2563eb",
            "secondary": "#475569",
            "bg_sidebar": "#0f172a",
            "bg_content": "#f8fafc",
            "accent": "#e11d48",
            "text_light": "#ffffff",
            "text_dark": "#1e293b"
        }
        
        # Cấu hình các widget ttk
        self.style.configure("Sidebar.TFrame", background=self.colors["bg_sidebar"])
        self.style.configure("Content.TFrame", background=self.colors["bg_content"])
        
        self.style.configure("NavButton.TButton", 
                             font=("Segoe UI", 11, "bold"), 
                             foreground=self.colors["text_light"], 
                             background=self.colors["bg_sidebar"], 
                             borderwidth=0, 
                             padding=12)
        self.style.map("NavButton.TButton",
                       background=[("active", "#1e293b"), ("pressed", "#334155")])
        
        self.style.configure("Action.TButton", 
                             font=("Segoe UI", 11, "bold"), 
                             foreground=self.colors["text_light"], 
                             background=self.colors["primary"])

    def build_layout(self):
        # 1. Sidebar bên trái
        self.sidebar = ttk.Frame(self, style="Sidebar.TFrame", width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Logo ứng dụng
        logo_label = tk.Label(self.sidebar, text="🔥 DECOMPOSER AI", 
                              font=("Segoe UI", 14, "bold"), 
                              fg=self.colors["text_light"], bg=self.colors["bg_sidebar"], 
                              pady=20)
        logo_label.pack(fill="x")
        
        # Menu điều hướng
        self.btn_main = ttk.Button(self.sidebar, text="📋 Rã Công Việc", style="NavButton.TButton", command=lambda: self.show_frame("main_task"))
        self.btn_main.pack(fill="x", pady=2)
        
        self.btn_profile = ttk.Button(self.sidebar, text="👤 Hồ Sơ Cá Nhân", style="NavButton.TButton", command=lambda: self.show_frame("profile"))
        self.btn_profile.pack(fill="x", pady=2)
        
        self.btn_settings = ttk.Button(self.sidebar, text="⚙️ Cài Đặt Hệ Thống", style="NavButton.TButton", command=lambda: self.show_frame("settings"))
        self.btn_settings.pack(fill="x", pady=2)
        
        self.btn_plus = ttk.Button(self.sidebar, text="⚡ Nâng Cấp PLUS", style="NavButton.TButton", command=lambda: self.show_frame("plus_details"))
        self.btn_plus.pack(fill="x", pady=2)
        
        self.btn_pay = ttk.Button(self.sidebar, text="💳 Thanh Toán", style="NavButton.TButton", command=lambda: self.show_frame("payment"))
        self.btn_pay.pack(fill="x", pady=2)
        
        # Vùng hiển thị phiên bản bên dưới sidebar
        self.lbl_version = tk.Label(self.sidebar, text=f"Phiên bản: 1.0.0 ({self.user_status['tier']})", 
                                    font=("Segoe UI", 9, "italic"), 
                                    fg="#64748b", bg=self.colors["bg_sidebar"])
                                    
        self.lbl_version.pack(side="bottom", pady=15)
        
        # 2. Vùng nội dung bên phải (Dynamic Container)
        self.container = ttk.Frame(self, style="Content.TFrame")
        self.container.pack(side="right", fill="both", expand=True)
        
        # Khởi tạo từ điển chứa các Frame giao diện
        self.frames = {}
        
        # Khởi tạo các class giao diện con
        self.frames["main_task"] = MainTaskFrame(self.container, self)
        self.frames["profile"] = ProfileFrame(self.container, self)
        self.frames["settings"] = SettingsFrame(self.container, self)
        self.frames["plus_details"] = PlusDetailsFrame(self.container, self)
        self.frames["payment"] = PaymentFrame(self.container, self)
        
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()

# ==========================================
# 1. GIAO DIỆN CHÍNH: RÃ CÔNG VIỆC
# ==========================================
class MainTaskFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Tiêu đề giao diện
        lbl_title = tk.Label(self, text="Bảng Phân Rã Công Việc Bằng Trợ Lý AI", font=("Segoe UI", 16, "bold"), fg=self.controller.colors["text_dark"])
        lbl_title.pack(anchor="w", padx=20, top=20, pady=10)
        
        # Khung nhập liệu dự án lớn
        input_frame = ttk.LabelFrame(self, text=" Nhập mục tiêu lớn cần rã nhỏ ")
        input_frame.pack(fill="x", padx=20, pady=10)
        
        self.txt_main_task = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.txt_main_task.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        self.txt_main_task.insert(0, "Xây dựng website bán hàng chuẩn SEO bằng Django trong 1 tuần")
        
        btn_decompose = ttk.Button(input_frame, text="🪄 Rã Việc Bằng AI", style="Action.TButton", command=self.trigger_ai_decomposition)
        btn_decompose.pack(side="right", padx=10, pady=10)
        
        # Thanh tiến độ ảo khi AI làm việc
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="indeterminate")
        
        # Cấu trúc cây (Treeview) hiển thị các task con sau khi rã
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.tree = ttk.Treeview(tree_frame, columns=("duration", "priority", "status"), show="tree headings")
        self.tree.heading("#0", text="Hạng mục công việc chi tiết", anchor="w")
        self.tree.heading("duration", text="Thời gian dự kiến", anchor="center")
        self.tree.heading("priority", text="Độ ưu tiên", anchor="center")
        self.tree.heading("status", text="Trạng thái", anchor="center")
        
        self.tree.column("#0", width=500, anchor="w")
        self.tree.column("duration", width=150, anchor="center")
        self.tree.column("priority", width=100, anchor="center")
        self.tree.column("status", width=120, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Menu chuột phải để tương tác phần tử dữ liệu chuyên sâu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Đánh dấu Hoàn Thành", command=self.mark_done)
        self.context_menu.add_command(label="Yêu cầu AI rã sâu thêm", command=self.deep_decompose)
        self.tree.bind("<Button-3>", self.show_context_menu)

    def trigger_ai_decomposition(self):
        task_text = self.txt_main_task.get().strip()
        if not task_text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập công việc cần rã!")
            return
            
        self.progress_bar.pack(fill="x", padx=20, pady=5)
        self.progress_bar.start(10)
        
        # Giả lập luồng chạy ngầm xử lý thuật toán AI
        threading.Thread(target=self.mock_ai_process, args=(task_text,), daemon=True).start()

    def mock_ai_process(self, task_text):
        time.sleep(2) # Giả lập độ trễ AI phản hồi
        
        # Xóa dữ liệu cũ trên cây
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Thêm cây dữ liệu mẫu chuyên sâu do AI tạo ra
        p1 = self.tree.insert("", "end", text="Bước 1: Chuẩn bị kiến trúc và Phân tích cơ sở dữ liệu", values=("Ngày 1-2", "Cao", "Chưa chạy"))
        self.tree.insert(p1, "end", text="Thiết kế sơ đồ ERD (Thực thể - Mối quan hệ)", values=("4 giờ", "Cao", "Chưa chạy"))
        self.tree.insert(p1, "end", text="Khởi tạo Project Django và cấu hình PostgreSQL", values=("3 giờ", "Trung bình", "Chưa chạy"))
        
        p2 = self.tree.insert("", "end", text="Bước 2: Xây dựng các chức năng Core Backend", values=("Ngày 3-5", "Cao", "Chưa chạy"))
        self.tree.insert(p2, "end", text="Xây dựng App Product (Quản lý sản phẩm, danh mục)", values=("8 giờ", "Cao", "Chưa chạy"))
        self.tree.insert(p2, "end", text="Tích hợp bộ lọc tìm kiếm nâng cao & Phân trang", values=("5 giờ", "Thấp", "Chưa chạy"))
        self.tree.insert(p2, "end", text="Xây dựng giỏ hàng (Cart) và API xử lý đơn hàng", values=("10 giờ", "Cao", "Chưa chạy"))
        
        p3 = self.tree.insert("", "end", text="Bước 3: Tích hợp Giao diện và Tối ưu SEO", values=("Ngày 6-7", "Trung bình", "Chưa chạy"))
        self.tree.insert(p3, "end", text="Render template HTML/Tailwind CSS tương thích Mobile", values=("8 giờ", "Trung bình", "Chưa chạy"))
        self.tree.insert(p3, "end", text="Tối ưu thẻ Meta, Sitemap, Robots.txt và tốc độ tải trang", values=("4 giờ", "Cao", "Chưa chạy"))

        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        messagebox.showinfo("Thành công", "AI đã phân rã công việc thành công thành cấu trúc cây sơ đồ!")

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def mark_done(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.item(selected_item[0], values=(self.tree.item(selected_item[0])['values'][0], 
                                                     self.tree.item(selected_item[0])['values'][1], 
                                                     "✓ Đã Xong"))

    def deep_decompose(self):
        if self.controller.user_status["tier"] == "Free User":
            messagebox.showwarning("Yêu cầu Nâng Cấp", "Tính năng rã sâu vô hạn lớp chỉ dành cho tài khoản PLUS!")
            self.controller.show_frame("plus_details")
        else:
            selected_item = self.tree.selection()
            if selected_item:
                self.tree.insert(selected_item[0], "end", text="[PLUS AI Deep Subtask] Phân tích xử lý edge-case lỗi hệ thống", values=("2 giờ", "Cao", "Chưa chạy"))

# ==========================================
# 2. GIAO DIỆN HỒ SƠ NGƯỜI DÙNG (PROFILE)
# ==========================================
class ProfileFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        lbl_title = tk.Label(self, text="Hồ Sơ Người Dùng", font=("Segoe UI", 16, "bold"), fg=self.controller.colors["text_dark"])
        lbl_title.pack(anchor="w", padx=20, top=20, pady=10)
        
        profile_card = ttk.LabelFrame(self, text=" Thông tin tài khoản ")
        profile_card.pack(fill="x", padx=20, pady=10)
        
        self.lbl_name = tk.Label(profile_card, text=f"Tên chủ tài khoản: {self.controller.user_status['name']}", font=("Segoe UI", 11))
        self.lbl_name.pack(anchor="w", padx=10, pady=5)
        
        self.lbl_email = tk.Label(profile_card, text=f"Email đăng ký: {self.controller.user_status['email']}", font=("Segoe UI", 11))
        self.lbl_email.pack(anchor="w", padx=10, pady=5)
        
        self.lbl_tier = tk.Label(profile_card, text=f"Gói dịch vụ hiện tại: {self.controller.user_status['tier']}", font=("Segoe UI", 11, "bold"), fg=self.controller.colors["primary"])
        self.lbl_tier.pack(anchor="w", padx=10, pady=5)
        
        # Thống kê lượng tài nguyên sử dụng
        stats_frame = ttk.LabelFrame(self, text=" Chỉ số sử dụng AI trong ngày ")
        stats_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.lbl_tokens = tk.Label(stats_frame, text=f"Số lượt rã việc AI miễn phí còn lại: {self.controller.user_status['ai_tokens_left']}/5", font=("Segoe UI", 11))
        self.lbl_tokens.pack(anchor="w", padx=10, pady=10)
        
        self.token_progress = ttk.Progressbar(stats_frame, orient="horizontal", length=300, mode="determinate")
        self.token_progress.pack(anchor="w", padx=10, pady=5)
        self.token_progress['value'] = (self.controller.user_status['ai_tokens_left'] / 5) * 100

    def on_show(self):
        # Cập nhật lại thông tin động mỗi khi bật tab profile
        self.lbl_tier.config(text=f"Gói dịch vụ hiện tại: {self.controller.user_status['tier']}")
        if self.controller.user_status['tier'] == "PLUS Active":
            self.lbl_tokens.config(text="Số lượt sử dụng AI: Vô Hạn (Gói PLUS)")
            self.token_progress['value'] = 100
            self.lbl_tier.config(fg="green")

# ==========================================
# 3. GIAO DIỆN CÀI ĐẶT HỆ THỐNG (SETTINGS)
# ==========================================
class SettingsFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        lbl_title = tk.Label(self, text="Cài Đặt Hệ Thống", font=("Segoe UI", 16, "bold"), fg=self.controller.colors["text_dark"])
        lbl_title.pack(anchor="w", padx=20, top=20, pady=10)
        
        # Nhóm cấu hình AI Engine
        ai_group = ttk.LabelFrame(self, text=" Cấu hình Mô hình AI (AI Engine) ")
        ai_group.pack(fill="x", padx=20, pady=10)
        
        tk.Label(ai_group, text="Lựa chọn LLM Core:", font=("Segoe UI", 10)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.model_combo = ttk.Combobox(ai_group, values=["Decomposer Free-Model v1", "Claude 3.5 Sonnet (PLUS)", "GPT-4o Reasoning (PLUS)"], state="readonly", width=30)
        self.model_combo.current(0)
        self.model_combo.grid(row=0, column=1, padx=10, pady=10)
        self.model_combo.bind("<<ComboboxSelected>>", self.check_model_permission)
        
        # Nhóm cấu hình giao diện
        ui_group = ttk.LabelFrame(self, text=" Tùy biến Giao diện ")
        ui_group.pack(fill="x", padx=20, pady=10)
        
        self.chk_dark_var = tk.BooleanVar(value=False)
        chk_dark = ttk.Checkbutton(ui_group, text="Kích hoạt Dark Mode (Chế độ tối)", variable=self.chk_dark_var, command=self.toggle_dark_mode)
        chk_dark.pack(anchor="w", padx=10, pady=10)
        
        # Nút Lưu cấu hình toàn cục
        btn_save_settings = ttk.Button(self, text="💾 Lưu Cấu Hình", style="Action.TButton", command=self.save_settings)
        btn_save_settings.pack(anchor="w", padx=20, pady=20)

    def check_model_permission(self, event):
        selected_model = self.model_combo.get()
        if "PLUS" in selected_model and self.controller.user_status["tier"] == "Free User":
            messagebox.showerror("Quyền truy cập bị chặn", "Mô hình cao cấp này yêu cầu kích hoạt bản quyền PLUS.")
            self.model_combo.current(0)

    def toggle_dark_mode(self):
        is_dark = self.chk_dark_var.get()
        if is_dark:
            self.controller.configure(bg="#1e1e1e")
            messagebox.showinfo("Giao diện", "Đã lưu bộ lọc Chế độ tối (Hệ thống giả lập).")
        else:
            self.controller.configure(bg="#f8fafc")

    def save_settings(self):
        messagebox.showinfo("Thông báo", "Toàn bộ cấu hình hệ thống đã được đồng bộ hóa thành công.")

# ==========================================
# 4. GIAO DIỆN BẢN PLUS NÂNG CẤP (PLUS DETAILS)
# ==========================================
class PlusDetailsFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        lbl_title = tk.Label(self, text="Tính Năng Độc Quyền Bản PLUS", font=("Segoe UI", 18, "bold"), fg=self.controller.colors["accent"])
        lbl_title.pack(anchor="w", padx=20, top=20, pady=10)
        
        intro_text = ("Nâng cấp lên phiên bản PLUS để giải phóng toàn bộ sức mạnh công nghệ AI. "
                      "Không còn giới hạn, xử lý logic sâu sắc hơn, giúp bạn bẻ gãy mọi dự án siêu lớn thành các mục tiêu chi tiết.")
        lbl_intro = tk.Label(self, text=intro_text, font=("Segoe UI", 11, "italic"), justify="left", wraplength=700)
        lbl_intro.pack(anchor="w", padx=20, pady=5)
        
        # Bảng so sánh tính năng (Feature Grid)
        grid_frame = ttk.Frame(self)
        grid_frame.pack(fill="x", padx=20, pady=20)
        
        headers = ["Tính năng cốt lõi", "Bản MIỄN PHÍ", "Bản PLUS CAO CẤP"]
        for col_idx, text in enumerate(headers):
            lbl = tk.Label(grid_frame, text=text, font=("Segoe UI", 11, "bold"), borderwidth=1, relief="solid", width=25, pady=8, bg="#e2e8f0")
            lbl.grid(row=0, column=col_idx, sticky="nsew")
            
        features = [
            ("Giới hạn rã việc hàng ngày", "5 lần / ngày", "VÔ HẠN KHÔNG GIỚI HẠN"),
            ("Độ sâu phân tầng cây mục tiêu", "Tối đa 2 tầng con", "Phân rã vô hạn lớp (Deep layers)"),
            ("Mô hình AI xử lý chuyên sâu", "Free Custom Engine", "GPT-4o & Claude 3.5 Sonnet"),
            ("Xuất dữ liệu Excel/Mindmap", "Không hỗ trợ", "Hỗ trợ xuất 1-Click chuyên nghiệp"),
            ("Hỗ trợ kỹ thuật ưu tiên", "Không có", "Đội ngũ kỹ sư hỗ trợ 24/7")
        ]
        
        for row_idx, row_data in enumerate(features, start=1):
            for col_idx, text in enumerate(row_data):
                bg_color = "#ffffff" if row_idx % 2 == 0 else "#f8fafc"
                fg_color = self.controller.colors["accent"] if col_idx == 2 else self.controller.colors["text_dark"]
                font_weight = "bold" if col_idx == 2 else "normal"
                
                lbl = tk.Label(grid_frame, text=text, font=("Segoe UI", 10, font_weight), fg=fg_color, bg=bg_color, borderwidth=1, relief="solid", pady=8)
                lbl.grid(row=row_idx, column=col_idx, sticky="nsew")
                
        # Nút hành động dẫn sang trang thanh toán luôn
        btn_go_to_pay = ttk.Button(self, text="⚡ Mua Bản Plus Ngay Chỉ Với 99.000đ/Tháng", style="Action.TButton", 
                                   command=lambda: self.controller.show_frame("payment"))
        btn_go_to_pay.pack(anchor="center", pady=30)

# ==========================================
# 5. GIAO DIỆN MUA PLUS & CỔNG THANH TOÁN
# ==========================================
class PaymentFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        lbl_title = tk.Label(self, text="Cổng Thanh Toán Hóa Đơn Dịch Vụ Plus", font=("Segoe UI", 16, "bold"), fg=self.controller.colors["text_dark"])
        lbl_title.pack(anchor="w", padx=20, top=20, pady=10)
        
        pay_container = ttk.Frame(self)
        pay_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Cột trái: Hóa đơn đơn hàng
        bill_frame = ttk.LabelFrame(pay_container, text=" Chi tiết đơn hàng ", width=400)
        bill_frame.pack(side="left", fill="y", padx=10, pady=10)
        bill_frame.pack_propagate(False)
        
        tk.Label(bill_frame, text="Sản phẩm: Upgrade Premium AI Plus", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10, pady=10)
        tk.Label(bill_frame, text="Thời hạn: 30 ngày (Gia hạn tự động)", font=("Segoe UI", 10)).pack(anchor="w", padx=10, pady=5)
        tk.Label(bill_frame, text="Đơn giá niêm yết: 199.000đ", font=("Segoe UI", 10, "strikethrough"), fg="gray").pack(anchor="w", padx=10, pady=5)
        tk.Label(bill_frame, text="Giá khuyến mãi: 99.000đ", font=("Segoe UI", 12, "bold"), fg="red").pack(anchor="w", padx=10, pady=5)
        
        # Cột phải: Chọn phương thức và thanh toán
        method_frame = ttk.LabelFrame(pay_container, text=" Phương thức thanh toán & Xác thực ")
        method_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(method_frame, text="Chọn cổng thanh toán kết nối trực tiếp:", font=("Segoe UI", 11)).pack(anchor="w", padx=15, pady=10)
        
        self.pay_method_var = tk.StringVar(value="qr")
        rdo_qr = ttk.Radiobutton(method_frame, text="Quét mã QR Code Chuyển khoản nhanh (VietQR)", variable=self.pay_method_var, value="qr", command=self.update_payment_view)
        rdo_qr.pack(anchor="w", padx=30, pady=5)
        
        rdo_card = ttk.Radiobutton(method_frame, text="Thẻ tín dụng Quốc tế (Visa / Mastercard / JCB)", variable=self.pay_method_var, value="card", command=self.update_payment_view)
        rdo_card.pack(anchor="w", padx=30, pady=5)
        
        # Vùng hiển thị động dựa trên phương thức thanh toán đã chọn
        self.dynamic_pay_area = ttk.Frame(method_frame, height=200)
        self.dynamic_pay_area.pack(fill="both", expand=True, padx=20, pady=15)
        
        self.update_payment_view()

    def update_payment_view(self):
        # Dọn sạch giao diện động cũ
        for widget in self.dynamic_pay_area.winfo_children():
            widget.destroy()
            
        method = self.pay_method_var.get()
        if method == "qr":
            # Giả lập bản thiết kế hiển thị mã QR
            qr_mock_box = tk.Frame(self.dynamic_pay_area, width=160, height=160, bg="#e2e8f0", borderwidth=1, relief="groove")
            qr_mock_box.pack(pady=10)
            qr_mock_box.pack_propagate(False)
            tk.Label(qr_mock_box, text="[MÃ QR VIETQR\nGIẢ LẬP]", bg="#e2e8f0", font=("Segoe UI", 10, "bold")).center_in_parent = True
            tk.Label(qr_mock_box, text="[MÃ QR VIETQR\nGIẢ LẬP]", bg="#e2e8f0", font=("Segoe UI", 10, "bold")).pack(expand=True)
            
            lbl_info = tk.Label(self.dynamic_pay_area, text="Quét mã bằng app Ngân hàng của bạn để hoàn tất giao dịch tự động.", font=("Segoe UI", 9, "italic"))
            lbl_info.pack()
            
            btn_verify = ttk.Button(self.dynamic_pay_area, text="🔄 Tôi Đã Chuyển Khoản - Kiểm Tra Ngay", style="Action.TButton", command=self.process_payment)
            btn_verify.pack(pady=15)
        else:
            # Giao diện nhập thông tin thẻ quốc tế
            tk.Label(self.dynamic_pay_area, text="Số thẻ tín dụng:").pack(anchor="w", pady=2)
            ent_card_num = ttk.Entry(self.dynamic_pay_area, width=40)
            ent_card_num.pack(anchor="w", pady=2)
            ent_card_num.insert(0, "4321 0987 6543 2100")
            
            sub_info_frame = ttk.Frame(self.dynamic_pay_area)
            sub_info_frame.pack(anchor="w", fill="x", pady=5)
            
            tk.Label(sub_info_frame, text="Hạn dùng (MM/YY):").grid(row=0, column=0, sticky="w", pady=2)
            ttk.Entry(sub_info_frame, width=10).grid(row=1, column=0, sticky="w", padx=(0, 20))
            
            tk.Label(sub_info_frame, text="Mã CVV/CVC:").grid(row=0, column=1, sticky="w", pady=2)
            ttk.Entry(sub_info_frame, width=10, show="*").grid(row=1, column=1, sticky="w")
            
            btn_verify = ttk.Button(self.dynamic_pay_area, text="💳 Xác Nhận Thanh Toán Ký Số", style="Action.TButton", command=self.process_payment)
            btn_verify.pack(pady=15)

    def process_payment(self):
        # Tạo hiệu ứng loading cổng thanh toán bằng Threading để chống đơ app
        self.top_loading = tk.Toplevel(self)
        self.top_loading.title("Đang xác thực...")
        self.top_loading.geometry("300x120")
        self.top_loading.transient(self)
        self.top_loading.grab_set()
        
        tk.Label(self.top_loading, text="Đang kết nối tới cổng thanh toán ngân hàng\nVui lòng không tắt ứng dụng...", font=("Segoe UI", 10)).pack(pady=20)
        p_bar = ttk.Progressbar(self.top_loading, mode="indeterminate", length=200)
        p_bar.pack()
        p_bar.start(15)
        
        threading.Thread(target=self.secure_payment_thread, daemon=True).start()

    def secure_payment_thread(self):
        time.sleep(3) # Giả lập giao tiếp kiểm tra webhook hoặc API Stripe
        self.top_loading.destroy()
        
        # Đổi trạng thái User trên bộ nhớ Runtime của phần mềm
        self.controller.user_status["tier"] = "PLUS Active"
        messagebox.showinfo("Thanh Toán Thành Công", "Chúc mừng! Tài khoản của bạn đã được nâng cấp lên bản PLUS cao cấp thành công.")
        self.controller.show_frame("main_task")

# Khởi chạy Driver ứng dụng chính
if __name__ == "__main__":
    app = TaskBreakdownApp()
    app.mainloop()
