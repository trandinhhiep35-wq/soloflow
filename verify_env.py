import os
from dotenv import load_dotenv

# Nạp file .env từ thư mục hiện tại
load_result = load_dotenv()

def verify_environment():
    print("🔍 Đang kiểm tra cấu hình Environment Variables...")
    
    # Kiểm tra xem file .env có được tải thành công không
    if not load_result:
        print("❌ LỖI: Không tìm thấy file .env! Hãy kiểm tra lại tên file.")
        return

    # Lấy giá trị API Key từ môi trường
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        # Che bớt phần thân để đảm bảo bảo mật khi in ra màn hình
        masked_key = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "********"
        print("✅ THÀNH CÔNG! Đã tìm thấy Key.")
        print(f"   Key hiện tại: {masked_key}")
    else:
        print("❌ LỖI: Không tìm thấy biến 'GEMINI_API_KEY' trong file .env.")
        print("💡 Gợi ý: Kiểm tra lại tên biến và đảm bảo không có khoảng trắng thừa.")

if __name__ == "__main__":
    verify_environment()
