from django.db import models
from django.utils import timezone
from datetime import datetime

class Role(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.name

def product_image_upload_path(instance, filename):
    return f'products/{instance.id}/{filename}'

class Product(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=product_image_upload_path, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name

    @property
    def current_price(self):
        # Tìm flash sale đang hoạt động cho sản phẩm này (nếu có)
        flash_sale = self.flash_sales.filter(
            active=True,
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date()
        ).first()
        if flash_sale:
            return flash_sale.sale_price
        return self.price


class ProductDetail(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='food_detail')

    # Thông tin thương hiệu và nhà sản xuất
    brand = models.CharField(max_length=100, blank=True, null=True, help_text="Thương hiệu sản phẩm")
    manufacturer = models.CharField(max_length=100, blank=True, null=True, help_text="Nhà sản xuất")
    country_of_origin = models.CharField(max_length=100, blank=True, null=True, help_text="Xuất xứ (quốc gia)")

    # Thông tin về khối lượng, thể tích và bao bì
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True,
                                 help_text="Trọng lượng (gam hoặc kg)")
    volume = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True,
                                 help_text="Thể tích (ml hoặc l)")
    packaging_type = models.CharField(max_length=100, blank=True, null=True,
                                      help_text="Loại bao bì, ví dụ: hộp, chai, túi")

    # Thông tin thành phần và dinh dưỡng
    ingredients = models.TextField(blank=True, null=True, help_text="Danh sách thành phần")
    nutrition_facts = models.TextField(blank=True, null=True,
                                       help_text="Thông tin dinh dưỡng (ví dụ: trên 100g hoặc mỗi khẩu phần)")
    allergens = models.CharField(max_length=255, blank=True, null=True, help_text="Cảnh báo dị ứng nếu có")

    # Thông tin sản xuất và hạn sử dụng
    manufacturing_date = models.DateField(blank=True, null=True, help_text="Ngày sản xuất")
    expiration_date = models.DateField(blank=True, null=True, help_text="Hạn sử dụng")

    # Hướng dẫn bảo quản và sử dụng
    storage_instructions = models.TextField(blank=True, null=True, help_text="Hướng dẫn bảo quản")
    usage_instructions = models.TextField(blank=True, null=True, help_text="Hướng dẫn sử dụng nếu cần")

    # Các thông tin bổ sung
    additional_info = models.TextField(blank=True, null=True, help_text="Thông tin bổ sung khác")

    def __str__(self):
        return f"Chi tiết thực phẩm: {self.product.name}"


# --- Đơn hàng ---
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Đang xử lý'),
        ('paid', 'Đã thanh toán'),
        ('shipped', 'Đã giao hàng'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"Đơn hàng {self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)  # Thêm trường ghi chú

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"

from django.utils import timezone

class Promotion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='promotions/', blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product, blank=True)  # Liên kết với sản phẩm

    def is_active(self):
        """Kiểm tra khuyến mãi có đang hoạt động không"""
        today = timezone.now().date()
        return self.active and self.start_date <= today <= self.end_date

    def __str__(self):
        return self.title


class FlashSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='flash_sales')
    discount_percent = models.PositiveIntegerField(
        help_text="Phần trăm giảm giá, ví dụ 20 cho 20% giảm giá"
    )
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        help_text="Giá bán trong flash sale (tính tự động từ % giảm)"
    )
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Tính sale_price dựa trên giá gốc và phần trăm giảm giá
        if self.product and self.discount_percent:
            self.sale_price = self.product.price * (100 - self.discount_percent) / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"FlashSale: {self.product.name} ({self.discount_percent}% off)"

    def is_active(self):
        today = timezone.now().date()
        return self.active and self.start_date <= today <= self.end_date

class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(help_text="Nội dung bình luận của khách hàng")
    rating = models.PositiveSmallIntegerField(
        blank=True, null=True,
        help_text="Đánh giá sản phẩm (từ 1 đến 5)"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Bình luận của {self.user.username} về {self.product.name}"


# --- Bảng Nhân viên ---
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    full_name = models.CharField(max_length=150, help_text="Họ và tên đầy đủ")
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True, help_text="Số điện thoại")
    address = models.TextField(blank=True, null=True, help_text="Địa chỉ liên hệ")
    position = models.CharField(max_length=100, help_text="Chức vụ trong công ty (VD: Quản lý, Nhân viên bán hàng)")
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Mức lương")
    date_joined = models.DateField(default=timezone.now, help_text="Ngày bắt đầu làm việc")
    is_active = models.BooleanField(default=True, help_text="Trạng thái hoạt động của nhân viên")

    def __str__(self):
        return f"{self.full_name} - {self.position}"

# Bảng lịch làm việc cho nhân viên
class WorkSchedule(models.Model):
    SHIFT_CHOICES = [
        ('morning', 'Sáng'),
        ('afternoon', 'Chiều'),
        ('night', 'Tối'),
        ('custom', 'Tùy chỉnh'),
    ]
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='work_schedules')
    date = models.DateField(help_text="Ngày làm việc")
    shift_type = models.CharField(max_length=20, choices=SHIFT_CHOICES, default='morning', help_text="Loại ca làm việc")
    start_time = models.TimeField(help_text="Giờ bắt đầu ca")
    end_time = models.TimeField(help_text="Giờ kết thúc ca")
    is_swapped = models.BooleanField(default=False, help_text="Đánh dấu ca đã được thay đổi hay chưa")
    swapped_with = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, help_text="Ca làm việc được thay đổi (nếu có)")

    class Meta:
        unique_together = ('employee', 'date', 'shift_type')
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.employee.full_name} - {self.date} ({self.get_shift_type_display()})"

# Bảng yêu cầu thay ca giữa các nhân viên
class ShiftSwapRequest(models.Model):
    SWAP_STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('approved', 'Đã duyệt'),
        ('rejected', 'Bị từ chối'),
    ]
    # Ca làm việc mà nhân viên muốn đổi (người gửi yêu cầu)
    schedule_from = models.ForeignKey(WorkSchedule, on_delete=models.CASCADE, related_name='swap_requests_sent', help_text="Ca làm việc của người gửi yêu cầu")
    # Ca làm việc mà nhân viên muốn nhận (người nhận yêu cầu)
    schedule_to = models.ForeignKey(WorkSchedule, on_delete=models.CASCADE, related_name='swap_requests_received', help_text="Ca làm việc của người nhận yêu cầu")
    requested_at = models.DateTimeField(auto_now_add=True, help_text="Thời gian gửi yêu cầu")
    status = models.CharField(max_length=20, choices=SWAP_STATUS_CHOICES, default='pending', help_text="Trạng thái yêu cầu")
    note = models.TextField(blank=True, null=True, help_text="Ghi chú hoặc lý do thay ca")

    def __str__(self):
        return f"Yêu cầu thay ca: {self.schedule_from} <-> {self.schedule_to} ({self.get_status_display()})"

class Attendance(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now, help_text="Ngày chấm công")
    check_in = models.TimeField(null=True, blank=True, help_text="Giờ vào")
    check_out = models.TimeField(null=True, blank=True, help_text="Giờ ra")

    @property
    def hours_worked(self):
        """Tính số giờ làm việc trong ngày dựa trên giờ check-in và check-out."""
        if self.check_in and self.check_out:
            dt_check_in = datetime.combine(self.date, self.check_in)
            dt_check_out = datetime.combine(self.date, self.check_out)
            delta = dt_check_out - dt_check_in
            return round(delta.total_seconds() / 3600, 2)
        return 0

    def __str__(self):
        return f"{self.employee.full_name} - {self.date}"