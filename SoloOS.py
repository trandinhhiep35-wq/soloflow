import os
from weasyprint import HTML

html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Hệ Thống Phân Rã Công Việc & Quản Lý Dự Án - Supabase Architecture Blueprint</title>
    <style>
        @page {
            size: A4;
            margin: 15mm 12mm;
            background-color: #0f172a;
        }

        *, *::before, *::after {
            box-sizing: border-box;
        }

        body {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            color: #f8fafc;
            background-color: #0f172a;
            margin: 0;
            padding: 0;
            font-size: 10pt;
            line-height: 1.5;
        }

        .header-banner {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }

        h1 {
            color: #38bdf8;
            font-size: 18pt;
            margin: 0 0 8px 0;
            font-weight: 700;
            letter-spacing: -0.5px;
        }

        .subtitle {
            color: #94a3b8;
            font-size: 11pt;
            margin: 0;
        }

        .badge-container {
            margin-top: 12px;
        }

        .badge {
            display: inline-block;
            background-color: #1e293b;
            color: #38bdf8;
            border: 1px solid #0284c7;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 8pt;
            font-weight: 600;
            margin-right: 6px;
        }

        .section {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
            page-break-inside: avoid;
        }

        h2 {
            color: #f3f4f6;
            font-size: 13pt;
            margin-top: 0;
            margin-bottom: 12px;
            border-left: 4px solid #38bdf8;
            padding-left: 8px;
        }

        h3 {
            color: #38bdf8;
            font-size: 11pt;
            margin-top: 12px;
            margin-bottom: 6px;
        }

        p {
            margin: 0 0 10px 0;
            color: #cbd5e1;
        }

        ul, ol {
            margin: 0 0 10px 0;
            padding-left: 20px;
            color: #cbd5e1;
        }

        li {
            margin-bottom: 4px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            margin-bottom: 10px;
            font-size: 9pt;
        }

        th {
            background-color: #334155;
            color: #38bdf8;
            text-align: left;
            padding: 8px;
            border: 1px solid #475569;
            font-weight: 600;
        }

        td {
            padding: 8px;
            border: 1px solid #334155;
            color: #e2e8f0;
            background-color: #0f172a;
        }

        .code-block {
            background-color: #020617;
            border: 1px solid #1e293b;
            border-radius: 6px;
            padding: 10px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 8pt;
            color: #38bdf8;
            white-space: pre-wrap;
            word-break: break-all;
            margin-bottom: 10px;
        }

        .grid-table {
            display: table;
            width: 100%;
        }

        .grid-row {
            display: table-row;
        }

        .grid-cell {
            display: table-cell;
            width: 50%;
            padding: 6px;
            vertical-align: top;
        }

        .card {
            background-color: #0f172a;
            border: 1px solid #334155;
            border-radius: 6px;
            padding: 10px;
        }

        .card-title {
            color: #f1f5f9;
            font-weight: bold;
            font-size: 9.5pt;
            margin-bottom: 4px;
        }

        .footer {
            text-align: center;
            font-size: 8pt;
            color: #64748b;
            margin-top: 20px;
            border-top: 1px solid #334155;
            padding-top: 10px;
        }
    </style>
</head>
<body>

    <div class="header-banner">
        <h1>BẢN THIẾT KẾ HỆ THỐNG PHÂN RÃ CÔNG VIỆC (WBS)</h1>
        <div class="subtitle">Tiêu Chuẩn Quốc Tế • Supabase Backend • Next.js & Modern UI Architecture</div>
        <div class="badge-container">
            <span class="badge">Enterprise Standard</span>
            <span class="badge">Supabase RLS & Realtime</span>
            <span class="badge">Work Breakdown Structure</span>
            <span class="badge">Linear/Jira Design Pattern</span>
        </div>
    </div>

    <div class="section">
        <h2>1. Kiến Trúc Tổng Quan (System Architecture)</h2>
        <p>Hệ thống được thiết kế theo tiêu chuẩn SaaS hiện đại hàng đầu thế giới (tương tự Linear.app, ClickUp, Jira Enterprise), hỗ trợ phân rã công việc đa tầng (Hierarchical WBS), tính toán tiến độ tự động (Progress Rollup) và đồng bộ thời gian thực (Real-time Collaboration).</p>

        <div class="grid-table">
            <div class="grid-row">
                <div class="grid-cell">
                    <div class="card">
                        <div class="card-title">Frontend Tier</div>
                        <ul>
                            <li><strong>Framework:</strong> Next.js 14+ App Router, React 18, TypeScript</li>
                            <li><strong>Styling:</strong> Tailwind CSS + Glassmorphism UI Design</li>
                            <li><strong>Components:</strong> Radix UI Primitives / Shadcn UI</li>
                            <li><strong>Icons & Visuals:</strong> Lucide Icons + Recharts</li>
                        </ul>
                    </div>
                </div>
                <div class="grid-cell">
                    <div class="card">
                        <div class="card-title">Backend & Data Tier (Supabase)</div>
                        <ul>
                            <li><strong>Database:</strong> PostgreSQL with CTE & Recursive Queries</li>
                            <li><strong>Auth & Security:</strong> Supabase Auth + Row Level Security (RLS)</li>
                            <li><strong>Realtime Engine:</strong> Supabase Realtime (WebSockets)</li>
                            <li><strong>Automation:</strong> Postgres Triggers for Auto-rollup & WBS Codes</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>2. Tính Năng Phục Vụ Phân Rã Công Việc (Work Breakdown Features)</h2>
        <table>
            <thead>
                <tr>
                    <th>Tính Năng</th>
                    <th>Mô Tả Chi Tiết</th>
                    <th>Lợi Ích Nghiệp Vụ</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Phân Rã Đa Tầng (Multi-level WBS)</strong></td>
                    <td>Chia nhỏ dự án thành các Epic, Feature, Task, Subtask với mã WBS tự động (1.1, 1.1.1, 1.1.2)</td>
                    <td>Giúp quản lý khối lượng công việc phức tạp một cách rõ ràng và mạch lạc</td>
                </tr>
                <tr>
                    <td><strong>Rollup Tiến Độ Tự Động</strong></td>
                    <td>Triggers trong Postgres tự động tính toán % hoàn thành của task cha dựa trên trọng số/giờ của subtasks</td>
                    <td>Đảm bảo dữ liệu tổng quan luôn chính xác 100% mà không cần tính toán thủ công</td>
                </tr>
                <tr>
                    <td><strong>Đa Chế Độ Hiển Thị (Multi-View)</strong></td>
                    <td>Hỗ trợ WBS Tree Explorer, Kanban Board, Gantt Timeline, và Matrix View</td>
                    <td>Phù hợp với nhiều vai trò: Manager (Gantt/WBS), Developer (Board), QA (Matrix)</td>
                </tr>
                <tr>
                    <td><strong>Gợi Ý Phân Rã Bằng AI (AI WBS Splitter)</strong></td>
                    <td>Tích hợp Prompt/Edge Function tự động phân tích mục tiêu dự án và đề xuất cây công việc chuẩn</td>
                    <td>Tiết kiệm 80% thời gian lập kế hoạch dự án ban đầu</td>
                </tr>
                <tr>
                    <td><strong>Time Tracking & Log Hours</strong></td>
                    <td>Ghi nhận thời gian dự kiến (Estimated) vs thực tế (Actual), cảnh báo vượt budget giờ làm</td>
                    <td>Tối ưu hóa nguồn lực và kiểm soát chi phí thực hiện dự án</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>3. Mô Hình Dữ Liệu PostgreSQL / Supabase Schema (Core)</h2>
        <p>Cấu trúc bảng <code>wbs_nodes</code> lưu trữ cây thư mục công việc với truy vấn đệ quy hiệu năng cao:</p>
        <div class="code-block">CREATE TABLE public.wbs_nodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    parent_id UUID REFERENCES public.wbs_nodes(id) ON DELETE CASCADE,
    wbs_code VARCHAR(50), -- e.g., '1.2.1'
    title TEXT NOT NULL,
    description TEXT,
    node_type VARCHAR(20) DEFAULT 'TASK', -- 'EPIC', 'FEATURE', 'TASK', 'SUBTASK'
    status VARCHAR(20) DEFAULT 'TODO', -- 'TODO', 'IN_PROGRESS', 'REVIEW', 'DONE'
    priority VARCHAR(10) DEFAULT 'MEDIUM',
    assigned_to UUID REFERENCES auth.users(id),
    estimated_hours NUMERIC(8,2) DEFAULT 0,
    actual_hours NUMERIC(8,2) DEFAULT 0,
    progress INT DEFAULT 0 CHECK (progress BETWEEN 0 AND 100),
    start_date DATE,
    due_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);</div>
    </div>

    <div class="section">
        <h2>4. Hướng Dẫn Triển Khai & Kết Nối Supabase</h2>
        <ol>
            <li><strong>Khởi tạo Supabase Project:</strong> Tạo dự án mới trên Supabase Console, lấy <code>SUPABASE_URL</code> và <code>SUPABASE_ANON_KEY</code>.</li>
            <li><strong>Chạy SQL Script Migration:</strong> Thực thi đoạn mã SQL định nghĩa cơ sở dữ liệu, Row Level Security (RLS) và Triggers tự động cập nhật thời gian & tính toán phần trăm.</li>
            <li><strong>Cấu hình Frontend Next.js:</strong> Khởi tạo các client SDK <code>@supabase/supabase-js</code> và <code>@supabase/ssr</code>.</li>
            <li><strong>Kích hoạt Realtime Subscriptions:</strong> Bật tính năng Realtime trong Supabase Table Settings cho bảng <code>wbs_nodes</code> để thông báo thay đổi tức thì cho đồng nghiệp.</li>
        </ol>
    </div>

    <div class="footer">
        Bản quyền tài liệu kiến trúc © 2026 Enterprise WBS System Architecture • Generated for Supabase & Next.js Integration
    </div>

</body>
</html>
"""

with open("blueprint.html", "w", encoding="utf-8") as f:
    f.write(html_content)

output_pdf = "Kien_Truc_He_Thong_Phan_Ra_Cong_Viec_Supabase.pdf"
HTML("blueprint.html").write_pdf(output_pdf)
print(f"PDF generated successfully: {output_pdf}")
