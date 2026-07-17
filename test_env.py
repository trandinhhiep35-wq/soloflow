import os
from dotenv import load_dotenv, find_dotenv

print("🔍 Đang tìm kiếm file .env...")
dotenv_path = find_dotenv()

if not dotenv_path:
    print("❌ LỖI: Không tìm thấy file .env!")
    print("💡 Gợi ý: Hãy tạo file có tên .env ngay tại thư mục gốc của dự án.")
else:
    print(f"✅ Đã tìm thấy file .env tại: {dotenv_path}")
    # Nạp các biến môi trường
    load_dotenv(dotenv_path)

api_key = os.getenv("GEMINI_API_KEY")

print("-" * 30)
if api_key:
    # Che bớt phần thân để đảm bảo bảo mật
    masked_key = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "********"
    print(f"✅ Thành công! Hệ thống đã đọc được API Key.")
    print(f"   Key hiện tại: {masked_key}")
else:
    print("❌ KHÔNG TÌM THẤY KEY!")
    print("💡 Gợi ý:")
    print("   1. Kiểm tra lại tên biến trong file .env phải là: GEMINI_API_KEY")
    print("   2. Đảm bảo không có khoảng trắng thừa ở hai bên dấu bằng.")
    print("   3. Nội dung file nên là: GEMINI_API_KEY=AIzaSy...")
print("-" * 30)