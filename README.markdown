# Hướng dẫn cài đặt và chạy dự án Commerce trên máy khác

## Giới thiệu dự án

Commerce là một dự án thương mại điện tử được xây dựng bằng Django, tạo ra một website bán hàng chuyên nghiệp. Dự án này cho phép khách hàng mua sắm online và admin quản lý mọi thứ từ sản phẩm, đơn hàng đến nhân viên. Với giao diện thân thiện và tính năng đa dạng, đây là một dự án tuyệt vời để học cách xây dựng website bán hàng bằng Django.

Dự án có các tính năng chính:
- **Khách hàng**: Đăng ký, đăng nhập, xem sản phẩm, thêm vào giỏ hàng, thanh toán, xem lịch sử đơn, viết bình luận và đánh giá sản phẩm.
- **Admin**: Quản lý sản phẩm, danh mục, nhà cung cấp, đơn hàng, khuyến mãi, flash sale, nhân viên, phân ca tự động, chấm công và tính lương.
- **Excel**: Nhập/xuất danh mục sản phẩm qua file Excel.
- **Báo cáo**: Xem báo cáo doanh thu hoặc in danh sách danh mục trực tiếp trên trình duyệt.
- **Jinja2**: Kết hợp Django templates và Jinja2 để linh hoạt trong thiết kế giao diện.


---

## Yêu cầu trước khi bắt đầu

Trước khi cài đặt, cần chuẩn bị các thứ sau trên máy:

1. **Python**: Phiên bản 3.8 trở lên (khuyên dùng 3.10 hoặc 3.11). Kiểm tra bằng:
   ```bash
   python --version
   ```
   - Chưa có? Tải tại [python.org/downloads](https://www.python.org/downloads/).
   - Lưu ý: Khi cài, chọn **Add Python to PATH** để dễ chạy lệnh `python`.

2. **MySQL**: Phiên bản 5.7 hoặc 8.0, đảm bảo server đang chạy. Kiểm tra:
   ```bash
   mysql --version
   ```
   - Chưa cài? Tải tại [dev.mysql.com/downloads/installer](https://dev.mysql.com/downloads/installer/).
   - Trên Windows, dùng **XAMPP** hoặc **MySQL Workbench** cho tiện.

3. **pip**: Công cụ cài gói Python. Kiểm tra:
   ```bash
   pip --version
   ```
   - Không có? Cài bằng: `python -m ensurepip --upgrade`.
   - Cập nhật pip: `python -m pip install --upgrade pip`.

4. **Virtualenv**: Dùng để tạo môi trường ảo, tránh xung đột thư viện. Cài bằng:
   ```bash
   pip install virtualenv
   ```

5. **Hệ điều hành**: Hướng dẫn này áp dụng cho **Windows**, **Linux**, hoặc **macOS**. Lệnh dùng kiểu Linux/macOS (dùng `/`). Nếu dùng Windows, đổi `/` thành `\` và dùng `venv\Scripts\activate` thay vì `source venv/bin/activate`.

6. **Dung lượng đĩa**: Cần khoảng **1-2GB** trống cho code, môi trường ảo, thư viện, và file media/static (ảnh, CSS, JS).

7. **Trình duyệt**: Chrome, Firefox, hoặc Edge để kiểm tra web.

8. **Công cụ giải nén**: Nếu code ở dạng file nén (zip, tar.gz), cần WinRAR, 7-Zip (Windows), hoặc lệnh `unzip`/`tar` (Linux/macOS).

---

## Các bước cài đặt

Giả sử đã tải mã nguồn dự án (thư mục hoặc file nén) và giải nén vào thư mục, ví dụ `commerce_project`. Nếu là file nén, giải nén bằng:

- **Windows**: Chuột phải > Extract Here (dùng 7-Zip hoặc WinRAR).
- **Linux/macOS**:
  ```bash
  unzip commerce_project.zip
  # Hoặc nếu là tar.gz
  tar -xvzf commerce_project.tar.gz
  ```

### 1. Vào thư mục dự án

Mở terminal (hoặc Command Prompt trên Windows) và vào thư mục dự án:

```bash
cd path/to/commerce_project
```

Thay `path/to/commerce_project` bằng đường dẫn thực tế, ví dụ: `~/Desktop/commerce_project` (Linux/macOS) hoặc `C:\Users\YourName\Desktop\commerce_project` (Windows).

Kiểm tra xem có file `manage.py` và thư mục `commerce_project` (chứa `settings.py`) không. Nếu có, đang đúng thư mục.

### 2. Xóa migrations cũ

Để tránh lỗi do các file migration cũ từ máy khác, nên xóa thư mục `migrations` trong các ứng dụng (như `commerce` hoặc `ticket_app`) trước khi chạy migration mới. Làm như sau:

- Tìm thư mục `migrations` trong các ứng dụng (thường ở `commerce/migrations` hoặc `ticket_app/migrations`).
- Xóa tất cả file trong `migrations` trừ `__init__.py`. Ví dụ:
  ```bash
  rm -rf commerce/migrations/*
  touch commerce/migrations/__init__.py
  ```
  Hoặc trên Windows, xóa thủ công bằng File Explorer, giữ lại `__init__.py`.

- Lặp lại cho các ứng dụng khác như `ticket_app` nếu có.

Xóa migrations cũ giúp tạo các migration mới phù hợp với database và tránh lỗi liên quan đến schema không khớp.

### 3. Tạo và kích hoạt môi trường ảo

Để tránh xung đột thư viện, tạo môi trường ảo:

```bash
python -m venv venv
```

Kích hoạt môi trường ảo:
- **Linux/macOS**:
  ```bash
  source venv/bin/activate
  ```
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```

Khi kích hoạt, sẽ thấy `(venv)` ở đầu dòng lệnh, ví dụ `(venv) user@machine:~/commerce_project$`. Lệnh `pip install` từ đây chỉ ảnh hưởng trong môi trường ảo.

### 4. Cài các thư viện cần thiết

Dự án cần nhiều thư viện Python cho database, xử lý ảnh, Excel, v.v. Nếu có file `requirements.txt`, chạy:

```bash
pip install -r requirements.txt
```

Nếu không có, tạo file `requirements.txt` với nội dung:

```
django>=3.2,<4.0
pymysql
mysqlclient
pandas>=1.5
openpyxl>=3.0
Pillow>=9.0
django-widget-tweaks>=1.4
django-humanize>=0.2
```

Rồi chạy lại `pip install -r requirements.txt`.

Hoặc cài thủ công:

```bash
pip install django pymysql mysqlclient pandas openpyxl Pillow django-widget-tweaks django-humanize
```

**Chức năng các thư viện**:
- `django`: Core của dự án.
- `pymysql`: Kết nối MySQL.
- `pandas`, `openpyxl`: Nhập/xuất file Excel.
- `Pillow`: Xử lý ảnh sản phẩm, khuyến mãi.
- `django-widget-tweaks`: Tùy chỉnh form giao diện.
- `django-humanize`: Định dạng số, ngày tháng (ví dụ: 1000000 thành 1,000,000).

dùng `pymysql` bằng cách thêm vào `settings.py`:
    ```python
    import pymysql
    pymysql.install_as_MySQLdb()
    ```
- Lỗi `ModuleNotFoundError`? Kiểm tra phiên bản Python (`python --version`) và đảm bảo đang trong môi trường ảo (thấy `(venv)`).

### 5. Cấu hình MySQL database

Dự án dùng MySQL để lưu dữ liệu sản phẩm, đơn hàng, người dùng. Thực hiện các bước sau:

1. **Khởi động MySQL server**:
   - **Linux**: `sudo service mysql start` hoặc `systemctl start mysql`.
   - **Windows**: Mở XAMPP, bật MySQL, hoặc dùng MySQL Workbench.
   - **macOS**: `mysql.server start`.
   - Kiểm tra: `mysqladmin -u root -p version`.

2. **Đăng nhập MySQL**:
   ```bash
   mysql -u root -p
   ```
   Nhập mật khẩu (nếu chưa đặt thì để trống). Quên mật khẩu? Tìm cách reset trên mạng.

3. **Tạo database**:
   Trong MySQL, chạy:
   ```sql
   CREATE DATABASE commerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
   - `utf8mb4` hỗ trợ tiếng Việt và ký tự đặc biệt.
   - Kiểm tra: `SHOW DATABASES;`.

4. **Cấu hình database** trong `commerce_project/settings.py`:

   Mở file `commerce_project/settings.py`, tìm `DATABASES` và sửa:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'commerce_db',
           'USER': 'root',  # Điền username MySQL
           'PASSWORD': '',   # Điền password MySQL
           'HOST': '127.0.0.1',
           'PORT': '3306',
           'OPTIONS': {
               'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
               'charset': 'utf8mb4',
           },
       }
   }
   ```

   - `USER`, `PASSWORD`: Điền thông tin MySQL.
   - `HOST`, `PORT`: Để nguyên nếu MySQL chạy trên máy. Dùng server khác thì đổi.
   - `OPTIONS`: Hỗ trợ tiếng Việt và chế độ nghiêm ngặt.

5. **Kiểm tra kết nối**:
   Chạy:
   ```bash
   python manage.py check
   ```
   Không lỗi là ổn. Có lỗi? Xem phần **Xử lý lỗi thường gặp**.

### 6. Chạy migration để tạo bảng

Sau khi xóa migrations cũ, chạy migration mới để tạo bảng:

```bash
python manage.py makemigrations
python manage.py migrate
```

**Giải thích**:
- `makemigrations`: Tạo file migration mới dựa trên model trong `commerce` hoặc `ticket_app`.
- `migrate`: Tạo bảng trong `commerce_db`.

**Kiểm tra**:
- Đăng nhập MySQL: `mysql -u root -p`.
- Chuyển database: `USE commerce_db;`
- Xem bảng: `SHOW TABLES;`
- Thấy bảng như `commerce_product`, `ticket_app_user`, `ticket_app_role` là đúng.

**Lưu ý**:
- Migration lỗi? Xem log, thường do thiếu `mysqlclient` hoặc database chưa tạo.
- Muốn làm lại? Xóa database (`DROP DATABASE commerce_db;`), tạo lại, xóa migrations cũ, rồi chạy migration.

### 7. Tạo tài khoản admin và user

Để quản lý qua giao diện admin (`http://localhost:8000/dashboard/`), cần tạo tài khoản superuser và tài khoản mẫu (admin, user) với vai trò.

#### 7.1. Tạo superuser
Chạy:

```bash
python manage.py createsuperuser
```

Nhập:
- **Username**: Ví dụ `admin` hoặc tên tùy chọn.
- **Email**: Có thể bỏ qua (Enter).
- **Password**: Nhập mật khẩu (ít nhất 8 ký tự, ví dụ `Admin1234`). Nhập lại để xác nhận.

Ghi lại thông tin để đăng nhập `/dashboard/` hoặc `/admin/`.

#### 7.2. Tạo tài khoản admin và user với Role
Dự án dùng model `Role` và `User` trong `ticket_app.models`. Để tạo tài khoản mẫu:

1. Mở Django shell:
   ```bash
   python manage.py shell
   ```

2. Gõ code:

   ```python
   from ticket_app.models import Role, User

   # Tạo quyền Admin và User
   admin_role = Role.objects.create(name="Admin")
   user_role = Role.objects.create(name="User")

   # Tạo tài khoản admin
   admin = User(username="admin", email="admin@example.com", role=admin_role)
   admin.set_password("admin123")
   admin.save()

   # Tạo tài khoản user
   user = User(username="user", email="user@example.com", role=user_role)
   user.set_password("user123")
   user.save()

   print("Tài khoản admin và user đã được tạo!")
   ```

3. Thoát shell:
   ```python
   exit()
   ```

**Giải thích**:
- `Role.objects.create`: Tạo vai trò `Admin` và `User`.
- `User(username, email, role)`: Tạo user với username, email, vai trò.
- `set_password`: Mã hóa mật khẩu (`admin123` cho admin, `user123` cho user).
- `save()`: Lưu vào database.

**Kiểm tra**:
- Chạy server (bước 9), vào `http://localhost:8000/dashboard/`.
- Đăng nhập:
  - Admin: `admin` / `admin123`
  - User: `user` / `user123`
- Hoặc vào `http://localhost:8000/admin/` với superuser.

**Lưu ý**:
- Nếu `ticket_app.models` không tồn tại, kiểm tra `ticket_app/models.py` có `Role` và `User` không. Nếu không, thay `ticket_app` bằng app chứa model (ví dụ: `commerce.models`).
- Lỗi `Role matching query does not exist`? Chạy lại migration hoặc kiểm tra bảng `ticket_app_role`.

### 8. Cấu hình thư mục media và static

Dự án dùng **media** để lưu ảnh (sản phẩm, khuyến mãi) và **static** để lưu CSS, JS. Làm các bước sau:

1. **Tạo thư mục media**:
   ```bash
   mkdir -p media/products media/promotions
   ```
   - `media/products`: Chứa ảnh sản phẩm.
   - `media/promotions`: Chứa ảnh khuyến mãi.

2. **Copy file media từ máy gốc** (nếu có):
   - Nếu máy gốc có thư mục `media`, copy nguyên sang máy mới (giữ cấu trúc `media/products`, `media/promotions`).
   - Không có? Thêm ảnh qua dashboard sau.

3. **Thu thập static files**:
   Chạy để copy CSS, JS từ `static` sang `staticfiles`:
   ```bash
   python manage.py collectstatic
   ```
   - Nhấn `yes` khi được hỏi.
   - Lệnh này gom file tĩnh từ `STATICFILES_DIRS` vào `STATIC_ROOT`.

4. **Kiểm tra cấu hình trong settings.py**:
   Mở `commerce_project/settings.py`, đảm bảo có:

   ```python
   STATIC_URL = '/static/'
   STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
   MEDIA_URL = '/media/'
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
   ```

   - `STATICFILES_DIRS`: Thư mục chứa CSS, JS gốc.
   - `STATIC_ROOT`: Nơi lưu file tĩnh sau `collectstatic`.
   - `MEDIA_ROOT`: Nơi lưu ảnh media.

5. **Kiểm tra thư mục static**:
   - Thư mục `static` cần có `static/css/style.css`, `static/js/script.js`, v.v.
   - Thiếu? Copy từ máy gốc hoặc kiểm tra template có gọi đúng file không.

### 9. Chạy server để kiểm tra

Chạy server Django:

```bash
python manage.py runserver
```

- Server chạy tại `http://localhost:8000/`.
- Muốn đổi port? Dùng: `python manage.py runserver 0.0.0.0:8001`.

Mở trình duyệt, vào:
- **Trang mua sắm**: `http://localhost:8000/` – Nơi khách hàng xem sản phẩm, thêm giỏ hàng, mua sắm, đánh giá.
- **Trang admin (dashboard)**: `http://localhost:8000/dashboard/` – Đăng nhập bằng `admin`/`admin123` hoặc superuser để quản lý.
- **Django admin**: `http://localhost:8000/admin/` – Dùng superuser để quản lý chi tiết.

**Kiểm tra**:
- Trang mua sắm hiển thị sản phẩm? Hoàn thành bước đầu!
- Dashboard hiện và đăng nhập được bằng `admin`/`admin123`? Tốt lắm!

---

## Kiểm tra và chạy thử

Sau khi cài đặt, kiểm tra các tính năng chính để đảm bảo mọi thứ hoạt động:

### 1. Kiểm tra trang mua sắm (http://localhost:8000/)
- Vào `http://localhost:8000/`:
  - Xem danh sách sản phẩm, danh mục.
  - Click sản phẩm để xem chi tiết (`/products/<id>/`).
  - Thêm sản phẩm vào giỏ, kiểm tra giỏ tại `/cart/`.
  - Thanh toán thử tại `/checkout/`, xem lịch sử đơn tại `/order-history/`.
  - Đăng nhập bằng `user`/`user123`, viết bình luận, đánh giá sản phẩm.

### 2. Kiểm tra giao diện admin (dashboard)
- Vào `http://localhost:8000/dashboard/`, đăng nhập bằng `admin`/`admin123` hoặc superuser.
- Thử các tính năng:
  - **Products**: Thêm sản phẩm (tên, danh mục, nhà cung cấp, giá, ảnh).
  - **Categories**: Thêm danh mục (ví dụ: "Laptop", "Áo thun").
  - **Suppliers**: Thêm nhà cung cấp.
  - **Users**: Thêm user với role `user` hoặc `admin`.
  - **FlashSales**: Tạo flash sale (chọn sản phẩm, % giảm, ngày bắt đầu/kết thúc).
  - **Employees**: Thêm nhân viên, kiểm tra chấm công/phân ca.

**Lưu ý**: Tạo danh mục, nhà cung cấp trước, vì sản phẩm cần chúng.

### 3. Kiểm tra tính năng admin
- **Quản lý đơn hàng**: Vào `/orders/` (dashboard) để xem, cập nhật trạng thái đơn (pending, paid, shipped).
- **Khuyến mãi, Flash Sale**:
  - Tạo khuyến mãi tại `/promotions/add/`, kiểm tra slide show ở `/promotions/slide-show/`.
  - Tạo flash sale tại `/flash-sales/add/`, xem giá giảm trên trang sản phẩm.
- **Quản lý nhân viên**:
  - Thêm nhân viên tại `/employees/`.
  - Phân ca tự động ở `/work_schedule/auto_assign/` hoặc `/auto_assign_weekly_shifts/`.
  - Chấm công tại `/attendance/`, xem lương ở `/salary/`.
- **Excel**: Nhập danh mục qua `/categories/upload/`, xuất báo cáo ở `/categories/export/`.

### 4. Kiểm tra dữ liệu mẫu
- **Có file SQL dump từ máy gốc?** Nhập dữ liệu:
  ```bash
  mysql -u root -p commerce_db < dump_file.sql
  ```
  - Kiểm tra dữ liệu trong dashboard (`/dashboard/`) hoặc trang mua sắm (`/products/`).
- **Không có dump?** Tạo thủ công qua dashboard:
  - Thêm 2-3 danh mục.
  - Thêm 1-2 nhà cung cấp.
  - Thêm 5-10 sản phẩm với ảnh.
  - Tạo flash sale, khuyến mãi để kiểm tra giá giảm.

### 5. Kiểm tra báo cáo
- **Doanh thu**: Vào `/revenue-report/`, chọn thời gian để xem.
- **Danh mục**: In báo cáo tại `/categories/print/`.

---

## Những lưu ý quan trọng

- **File template**:
  - Kiểm tra `commerce/templates` có đủ file HTML như `index.html`, `dashboard.html`, `products/product_detail.html`, `promotions/slide_show.html`.
  - Thiếu file? Copy từ máy gốc hoặc xem log lỗi để tìm.

- **File static**:
  - Thư mục `static` cần có `static/css/style.css`, `static/js/script.js`, v.v.
  - Giao diện xấu, thiếu kiểu? Chạy lại `python manage.py collectstatic`, kiểm tra `STATIC_ROOT`.

- **File media**:
  - Ảnh sản phẩm/khuyến mãi không hiện? Kiểm tra `media/products`, `media/promotions`.
  - Đảm bảo quyền:
    - Linux/macOS: `chmod -R 755 media`.
    - Windows: Chuột phải > Properties > Security > Full control.

- **Múi giờ**:
  - Dự án dùng `Asia/Ho_Chi_Minh`. Kiểm tra `settings.py`:
    ```python
    TIME_ZONE = 'Asia/Ho_Chi_Minh'
    USE_TZ = True
    ```
  - Sai múi giờ có thể làm flash sale, đơn hàng hiển thị sai.

- **Debug mode**:
  - Hiện tại `DEBUG = True` trong `settings.py`, tốt cho kiểm tra.
  - Deploy thật thì đổi `DEBUG = False` và thêm:
    ```python
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'your-domain.com']
    ```

- **Jinja2 templates**:
  - Dự án dùng cả Django templates và Jinja2. Kiểm tra `settings.py` có:
    ```python
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'commerce', 'templates')],
            'APP_DIRS': True,
            ...
        },
        {
            'BACKEND': 'django.template.backends.jinja2.Jinja2',
            'DIRS': [os.path.join(BASE_DIR, 'commerce', 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'environment': 'commerce.jinja2.environment',
            },
        },
    ]
    ```
  - Jinja2 lỗi? Kiểm tra `commerce/jinja2.py`.

- **Hiệu suất**:
  - Chạy chậm khi nhiều dữ liệu? Kiểm tra số bản ghi: `SELECT COUNT(*) FROM table_name;`.
  - Xóa dữ liệu thừa hoặc tối ưu query trong `views.py`.

---

## Xử lý lỗi thường gặp

Gặp lỗi là bình thường, đây là cách xử lý các lỗi phổ biến:

1. **Lỗi kết nối MySQL**:
   - **Thông báo**: `django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")` hoặc `(1045, "Access denied")`.
   - **Cách xử lý**:
     - Kiểm tra MySQL server chạy chưa: `mysqladmin -u root -p version`.
     - Xác nhận `USER`, `PASSWORD`, `HOST`, `PORT` trong `settings.py`.
     - Quên mật khẩu? Reset:
       - Linux: `sudo mysql_secure_installation`.
       - Windows: Dùng MySQL Workbench hoặc `--skip-grant-tables`.
     - Kiểm tra database `commerce_db`: `CREATE DATABASE commerce_db;`.

2. **Lỗi thiếu thư viện**:
   - **Thông báo**: `ModuleNotFoundError: No module named 'X'` (ví dụ: `mysqlclient`, `Pillow`).
   - **Cách xử lý**:
     - Cài thiếu gì: `pip install X`.
     - `mysqlclient` lỗi? Xem bước 4.
     - `Pillow` lỗi? Kiểm tra Python version (`python --version`), cài lại: `pip install Pillow --force-reinstall`.

3. **Lỗi template không tìm thấy**:
   - **Thông báo**: `TemplateDoesNotExist at /some/path/`.
   - **Cách xử lý**:
     - Kiểm tra file HTML trong `commerce/templates` (như `index.html`, `dashboard.html`).
     - Đảm bảo `TEMPLATES` trong `settings.py` có:
       ```python
       'DIRS': [os.path.join(BASE_DIR, 'commerce', 'templates')],
       ```
     - Jinja2 lỗi? Kiểm tra `commerce/jinja2.py` và template.

4. **Lỗi static/media không tải**:
   - **Thông báo**: 404 cho CSS/JS (`GET /static/css/style.css HTTP/1.1" 404`) hoặc ảnh.
   - **Cách xử lý**:
     - Chạy lại `python manage.py collectstatic`.
     - Kiểm tra `staticfiles` có CSS/JS không.
     - Media lỗi? Kiểm tra `media/products`, `media/promotions` và quyền:
       - Linux/macOS: `chmod -R 755 media`.
       - Windows: Chuột phải > Properties > Security > Full control.
     - Kiểm tra `STATIC_ROOT`, `MEDIA_ROOT` trong `settings.py`.

5. **Lỗi migration**:
   - **Thông báo**: `django.db.utils.ProgrammingError: (1146, "Table 'commerce_db.X' doesn't exist")`.
   - **Cách xử lý**:
     - Kiểm tra database `commerce_db`: `mysql -u root -p -e "SHOW DATABASES;"`.
     - Đã xóa migrations cũ (bước 2)? Nếu chưa, xóa thư mục `migrations` trong `commerce` hoặc `ticket_app` (trừ `__init__.py`) và chạy:
       ```bash
       python manage.py makemigrations
       python manage.py migrate
       ```
     - Vẫn lỗi? Xóa database:
       ```sql
       DROP DATABASE commerce_db;
       CREATE DATABASE commerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
       ```
     - Xóa migrations cũ, chạy lại migration.

6. **Lỗi tài khoản admin/user**:
   - **Thông báo**: `Role matching query does not exist` hoặc lỗi trong shell.
   - **Cách xử lý**:
     - Kiểm tra `ticket_app/models.py` có `Role` và `User` không.
     - Đảm bảo migration đã chạy (`python manage.py migrate`).
     - Lỗi? Xóa database, xóa migrations cũ, chạy lại migration, thử code shell.

7. **Lỗi flash sale hoặc giá không cập nhật**:
   - **lỗi**: Giá không giảm dù có flash sale.
   - **Cách xử lý**:
     - Kiểm tra `start_date`, `end_date` của flash sale trong `/flash-sales/`.
     - Đảm bảo `active=True` trong model `FlashSale`.
     - Kiểm tra logic `sale_price` trong `views.py` (hàm `product_detail`).

8. **Lỗi phân ca hoặc chấm công**:
   - **lỗi**: Phân ca không tạo lịch, lương tính sai.
   - **Cách xử lý**:
     - Kiểm tra nhân viên (`/employees/`) có `is_active=True`.
     - Đảm bảo bảng `WorkSchedule`, `Attendance` có dữ liệu.
     - Xem log lỗi hoặc bật `DEBUG=True`.

---