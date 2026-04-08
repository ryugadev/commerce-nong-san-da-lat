🛒 Dự Án Thương Mại Điện Tử Nông Sản Sạch (Commerce Project)
📝 Giới thiệu
Commerce là hệ thống website thương mại điện tử chuyên biệt cho nông sản sạch được xây dựng trên nền tảng Django. Dự án cung cấp giải pháp toàn diện từ khâu mua sắm của khách hàng đến khâu quản trị vận hành kho bãi, nhân sự và khuyến mãi.

✨ Tính năng nổi bật
🛒 Trải nghiệm mua sắm: Giỏ hàng thông minh, thanh toán linh hoạt, hệ thống bình luận & đánh giá sản phẩm.

⚡ Marketing mạnh mẽ: Quản lý Flash Sale theo giờ vàng, Slide Show khuyến mãi động.

👥 Quản trị nhân sự (HRM): Phân ca làm việc tự động, chấm công thời gian thực và tính lương nhân viên.

📊 Quản lý kho & Báo cáo: Nhập/Xuất dữ liệu qua Excel, báo cáo doanh thu trực quan, in ấn danh mục sản phẩm trực tiếp.

🎨 Công nghệ: Kết hợp sức mạnh của Django Template và Jinja2 cho giao diện mượt mà, chuẩn Responsive.

🛠 Yêu cầu hệ thống
Ngôn ngữ: Python 3.10+

Cơ sở dữ liệu: MySQL 5.7 / 8.0

Thư viện xử lý: Pandas, Openpyxl, Pillow

Trình duyệt: Chrome, Edge, Firefox (phiên bản mới nhất)

🚀 Hướng dẫn cài đặt nhanh
1. Chuẩn bị mã nguồn
Bash
git clone https://github.com/ryugadev/commerce-nong-san-da-lat.git
cd commerce_project
2. Thiết lập môi trường ảo
Windows:

Bash
python -m venv venv
venv\Scripts\activate
Linux/macOS:

Bash
python3 -m venv venv
source venv/bin/activate
3. Cài đặt thư viện
Bash
pip install -r requirements.txt
4. Cấu hình Cơ sở dữ liệu
Tạo Database trong MySQL:

SQL
CREATE DATABASE commerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
Cập nhật thông tin USER và PASSWORD trong file commerce_project/settings.py.

5. Khởi tạo dữ liệu
Bash
# Xóa migrations cũ (nếu có) và khởi tạo lại
python manage.py makemigrations
python manage.py migrate

# Tạo tài khoản quản trị tối cao
python manage.py createsuperuser
6. Cấu hình Static & Media
Bash
python manage.py collectstatic
mkdir -p media/products media/promotions
🖥 Khởi chạy dự án
Bash
python manage.py runserver
Trang chủ: http://127.0.0.1:8000/

Trang Dashboard: http://127.0.0.1:8000/admin/

Tài khoản mẫu:

Admin: admin / admin123

User: user / user123

📂 Cấu trúc thư mục chính
commerce/: Chứa logic chính về sản phẩm, giỏ hàng, khuyến mãi.

ticket_app/: Quản lý người dùng, vai trò (Roles) và nhân sự.

static/: Chứa file CSS, JS, Images giao diện.

media/: Chứa hình ảnh sản phẩm người dùng tải lên.

templates/: Hệ thống giao diện HTML (Django & Jinja2).

⚠️ Lưu ý quan trọng
Múi giờ: Dự án mặc định sử dụng Asia/Ho_Chi_Minh. Hãy đảm bảo server đồng bộ thời gian để Flash Sale chạy chính xác.

Debug: Khi triển khai (Deploy), hãy đổi DEBUG = False trong settings.py.

Thư viện ảnh: Nếu gặp lỗi khi upload ảnh, hãy đảm bảo đã cài đặt Pillow.

📞 Liên hệ
Tác giả: Phúc Thành

Email: jaekyungdev203@gmail.com

Dự án: Đồ án tốt nghiệp / Bài tập lớn Thương mại điện tử.

Cảm ơn bạn đã quan tâm đến dự án Commerce!