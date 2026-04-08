from django.urls import path
from . import views
from .views import order_create, order_update, order_delete
from .views import product_detail
from .views import (
    ProductCommentListView,
    ProductCommentCreateView,
    ProductCommentUpdateView,
    ProductCommentDeleteView,
)
from .views import product_comment_create
from .views import user_list, user_create, user_update, user_delete
from .views import employee_list, employee_create, employee_update, employee_delete
from .views import auto_assign_shifts
from .views import auto_assign_weekly_shifts
from .views import attendance_list, attendance_create, calculate_salary, attendance_update, attendance_delete
from .views import salary_list
from .views import upload_categories_excel

urlpatterns = [
    # Trang chủ và sản phẩm
    path('', views.home, name='home'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/', views.product_list, name='product_list'),
    path('search/', views.product_search, name='product_search'),

    # Xác thực người dùng (đăng nhập, đăng xuất, đăng ký, quên mật khẩu, profile)
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('profile/', views.profile_view, name='profile'),

    # Dashboard Admin (chỉ dành cho admin)
    path('dashboard/', views.dashboard, name='dashboard'),

    # Quản lý sản phẩm (các thao tác CRUD)
    path('products/add/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # Quản lý danh mục
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    path('categories/upload/', upload_categories_excel, name='upload_categories'),
    path('categories/export/', views.export_categories_excel, name='export_categories'),
    path('categories/print/', views.print_categories_report, name='print_categories_report'),
    # Quản lý nhà cung cấp
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/edit/', views.supplier_update, name='supplier_update'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),

    # Giỏ hàng
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:pk>/', views.cart_add, name='cart_add'),
    path('cart/update/', views.cart_update, name='cart_update'),
    path('cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),

    # Thanh toán và lịch sử đơn hàng (User)
    path('checkout/', views.checkout, name='checkout'),
    path('order-history/', views.order_history, name='order_history'),

    # Quản lý đơn hàng (Admin)
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/create/', order_create, name='order_create'),
    path('orders/<int:order_id>/update/', order_update, name='order_update'),
    path('orders/<int:order_id>/delete/', order_delete, name='order_delete'),

    # Gợi ý sản phẩm (nếu dùng)
    path('suggestions/', views.product_suggestions, name='product_suggestions'),

    path('revenue-report/', views.revenue_report, name='revenue_report'),

    # Quản lý khuyến mãi
    path('promotions/', views.promotion_list, name='promotion_list'),
    path('promotions/add/', views.promotion_create, name='promotion_create'),
    path('promotions/<int:pk>/edit/', views.promotion_update, name='promotion_update'),
    path('promotions/<int:pk>/delete/', views.promotion_delete, name='promotion_delete'),
    path('promotions/slide-show/', views.promotion_slide_show, name='promotion_slide_show'),
    path('promotions/sale/', views.product_sale, name='product_sale'),


# Flash Sale
    path('flash-sales/', views.flash_sale_list, name='flash_sale_list'),
    path('flash-sales/add/', views.flash_sale_create, name='flash_sale_create'),
    path('flash-sales/<int:pk>/edit/', views.flash_sale_update, name='flash_sale_update'),
    path('flash-sales/<int:pk>/delete/', views.flash_sale_delete, name='flash_sale_delete'),
    path('flash-sale-products/', views.flash_sale_products, name='flash_sale_products'),

    # Quản lý thông tin chi tiết sản phẩm (ProductDetail)
    path('products/add-with-detail/', views.product_create_with_detail, name='product_create_with_detail'),

    # Quản lý thông tin chi tiết sản phẩm (tạo, xem, sửa, xóa)
    path('product-details/', views.product_detail_list, name='product_detail_list'),
    path('products/<int:product_id>/detail/', views.product_detail_view, name='product_detail_view'),
    path('product-details/add/', views.product_detail_create, name='product_detail_create'),
    path('products/<int:product_id>/detail/edit/', views.product_detail_update, name='product_detail_update'),
    path('products/<int:product_id>/detail/delete/', views.product_detail_delete, name='product_detail_delete'),

    path('products/<int:product_id>/', product_detail, name='product_detail'),
    # --- Quản lý bình luận sản phẩm ---

    path('product-comments/', ProductCommentListView.as_view(), name='product_comment_list'),
    path('product-comments/add/', ProductCommentCreateView.as_view(), name='product_comment_create'),
    path('product-comments/<int:pk>/edit/', ProductCommentUpdateView.as_view(), name='product_comment_update'),
    path('product-comments/<int:pk>/delete/', ProductCommentDeleteView.as_view(), name='product_comment_delete'),
    path('comment/create/', product_comment_create, name='product_comment_create'),

    path('users/', user_list, name='user_list'),
    path('users/create/', user_create, name='user_create'),
    path('users/update/<int:user_id>/', user_update, name='user_update'),
    path('users/delete/<int:user_id>/', user_delete, name='user_delete'),

# Quản lý nhân viên
    path('employees/', employee_list, name='employee_list'),
    path('employees/create/', employee_create, name='employee_create'),
    path('employees/update/<int:employee_id>/', employee_update, name='employee_update'),
    path('employees/delete/<int:employee_id>/', employee_delete, name='employee_delete'),

    # phân lịch tự động
    path('work_schedule/auto_assign/', auto_assign_shifts, name='auto_assign_shifts'),
    path('work_schedule/auto_assign_weekly/', auto_assign_weekly_shifts, name='auto_assign_weekly_shifts'),

    # Chấm công
    path('attendance/', attendance_list, name='attendance_list'),
    path('attendance/create/', attendance_create, name='attendance_create'),
    path('attendance/update/<int:pk>/', attendance_update, name='attendance_update'),
    path('attendance/delete/<int:pk>/', attendance_delete, name='attendance_delete'),
    path('attendance/calculate/<int:employee_id>/', calculate_salary, name='calculate_salary'),
    path('salary/', salary_list, name='salary_list'),


]
