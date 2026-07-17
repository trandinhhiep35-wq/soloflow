import os
from supabase import create_client, Client
from typing import List, Dict, Any, Optional

class SupabaseManager:
    """
    Class quản lý kết nối và thao tác với Supabase chuyên nghiệp.
    """
    def __init__(self, url: str, key: str):
        self.url = url
        self.key = key
        self.client: Optional[Client] = None
        self._connect()

    def _connect(self):
        """Khởi tạo kết nối tới Supabase."""
        try:
            self.client = create_client(self.url, self.key)
            print("✅ Đã kết nối Supabase thành công qua Class Manager!")
        except Exception as e:
            print(f"❌ Lỗi khởi tạo Supabase: {e}")
            self.client = None

    def get_tasks(self) -> List[Dict[str, Any]]:
        """Lấy tất cả task từ bảng 'tasks'."""
        if not self.client:
            return []
        try:
            response = self.client.table("tasks").select("*").execute()
            return response.data
        except Exception as e:
            print(f"❌ Lỗi lấy dữ liệu: {e}")
            return []

    def add_task(self, title: str, project: str = "Mặc định", priority: str = "Trung bình"):
        """Thêm một task mới vào Supabase."""
        if not self.client:
            return None
        
        new_task = {
            "title": title,
            "project": project,
            "priority": priority,
            "status": "Cần làm",
            "archived": False
        }
        
        try:
            response = self.client.table("tasks").insert(new_task).execute()
            return response.data
        except Exception as e:
            print(f"❌ Lỗi thêm task: {e}")
            return None

    def update_task_status(self, task_id: int, new_status: str):
        """Cập nhật trạng thái task bằng ID."""
        if not self.client:
            return
        
        try:
            self.client.table("tasks").update({"status": new_status}).eq("id", task_id).execute()
            print(f"✅ Đã cập nhật task {task_id} sang {new_status}")
        except Exception as e:
            print(f"❌ Lỗi cập nhật task: {e}")