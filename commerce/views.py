from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import User, Role, Product, Category, Supplier, Order, OrderItem
from .forms import ProductForm, CategoryForm, SupplierForm
from .forms import OrderForm, OrderItemForm
from django.db.models import Sum, Avg
import datetime
from .models import Order


# --- Trang chủ ---
def home(request):
    products = Product.objects.filter(is_deleted=False).order_by('id')
    promotions = Promotion.objects.filter(
        active=True,
        start_date__lte=timezone.now().date(),
        end_date__gte=timezone.now().date()
    )
    # Lấy các flash sale đang được kích hoạt
    flash_sales = FlashSale.objects.filter(
        active=True,
        start_date__lte=timezone.now().date(),
        end_date__gte=timezone.now().date()
    )
    context = {
        'products': products,
        'promotions': promotions,
        'flash_sales': flash_sales,  # thêm flash_sales vào context
    }
    return render(request, 'products/index.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, ProductDetail  # Đảm bảo import ProductDetail
from django.core.paginator import Paginator


# def dashboard(request):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('login')
#     try:
#         user = User.objects.get(id=user_id)
#         if user.role.name.lower() != 'admin':
#             messages.error(request, 'Bạn không có quyền truy cập trang này.')
#             return redirect('home')
#     except User.DoesNotExist:
#         return redirect('login')
#
#     total_users = User.objects.count()
#     total_admins = User.objects.filter(role__name__iexact='admin').count()
#     total_customers = total_users - total_admins
#
#     # Lấy danh sách thông tin chi tiết sản phẩm
#     product_details = ProductDetail.objects.all().order_by('id')
#     # Phân trang nếu cần, ví dụ: 10 bản ghi mỗi trang
#     paginator = Paginator(product_details, 10)
#     page_number = request.GET.get("page")
#     product_details_page = paginator.get_page(page_number)
#
#     context = {
#         'user': user,
#         'total_users': total_users,
#         'total_admins': total_admins,
#         'total_customers': total_customers,
#         'product_details': product_details_page,  # Truyền danh sách chi tiết sản phẩm vào context
#     }
#     return render(request, 'dashboard.html', context)


# --- Product Detail ---
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk, is_deleted=False)
#     return render(request, 'products/product_detail.html', {'product': product})

# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk, is_deleted=False)
#     # Kiểm tra flash sale đang hoạt động cho sản phẩm
#     flash_sale = product.flash_sales.filter(
#         active=True,
#         start_date__lte=timezone.now().date(),
#         end_date__gte=timezone.now().date()
#     ).first()
#     if flash_sale:
#         product.final_price = flash_sale.sale_price
#     else:
#         product.final_price = product.price
#     return render(request, 'products/product_detail.html', {'product': product})
import json

def dashboard(request):
    # Kiểm tra phiên đăng nhập
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    try:
        user = User.objects.get(id=user_id)
        if user.role.name.lower() != 'admin':
            messages.error(request, 'Bạn không có quyền truy cập trang này.')
            return redirect('home')
    except User.DoesNotExist:
        return redirect('login')

    total_users = User.objects.count()
    total_admins = User.objects.filter(role__name__iexact='admin').count()
    total_customers = total_users - total_admins

    # Lấy danh sách thông tin chi tiết sản phẩm (phân trang)
    product_details = ProductDetail.objects.all().order_by('id')
    paginator = Paginator(product_details, 10)
    page_number = request.GET.get("page")
    product_details_page = paginator.get_page(page_number)


    revenue_data = {
        "labels": ["Tháng 12", "Tháng 1", "Tháng 2", "Tháng 3"],
        "data": [20000000, 18000000, 22000000, 25000000],
    }
    wage_data = {
        "labels": ["Tháng 12", "Tháng 1", "Tháng 2", "Tháng 3"],
        "data": [5000000, 5200000, 5100000, 5300000],
    }
    order_data = {
        "count": Order.objects.filter(status__iexact='completed').count()
    }
    comment_data = {
        "count": ProductComment.objects.filter(is_deleted=False).count()
    }

    context = {
        'user': user,
        'total_users': total_users,
        'total_admins': total_admins,
        'total_customers': total_customers,
        'product_details': product_details_page,
        # Dữ liệu thống kê cho biểu đồ (chuyển sang JSON)
        'revenue_data': json.dumps(revenue_data),
        'wage_data': json.dumps(wage_data),
        'order_data': json.dumps(order_data),
        'comment_data': json.dumps(comment_data),
    }
    return render(request, 'dashboard.html', context)


from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Product, ProductDetail, ProductComment

def product_detail(request, pk):
    # Lấy sản phẩm và kiểm tra is_deleted=False
    product = get_object_or_404(Product, pk=pk, is_deleted=False)

    # Lấy chi tiết sản phẩm (nếu có)
    detail = ProductDetail.objects.filter(product=product).first()

    # Kiểm tra flash sale đang hoạt động (nếu có)
    flash_sale = product.flash_sales.filter(
        active=True,
        start_date__lte=timezone.now().date(),
        end_date__gte=timezone.now().date()
    ).first()
    product.final_price = flash_sale.sale_price if flash_sale else product.price

    # Lấy danh sách bình luận chưa bị xóa mềm
    product_comments = ProductComment.objects.filter(product=product, is_deleted=False).order_by('-created_at')

    # Xử lý gửi bình luận
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = ProductCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.created_at = timezone.now()
            comment.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductCommentForm()

    context = {
        'product': product,
        'detail': detail,
        'product_comments': product_comments,
        'form': form,
    }
    return render(request, 'products/product_detail.html', context)

# --- Xác thực người dùng ---
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            messages.success(request, "Đăng nhập thành công.")
            if user.role.name.lower() == 'admin':
                return redirect('dashboard')
            else:
                return redirect('home')
        except User.DoesNotExist:
            messages.error(request, "Sai thông tin đăng nhập.")
    return render(request, 'login-user.html')

def logout_view(request):
    request.session.flush()
    return redirect('home')

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if not username or not password or not confirm_password:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin.")
        elif password != confirm_password:
            messages.error(request, "Mật khẩu không khớp.")
        else:
            try:
                User.objects.get(username=username)
                messages.error(request, "Tên đăng nhập đã tồn tại.")
            except User.DoesNotExist:
                role, created = Role.objects.get_or_create(name="user")
                User.objects.create(username=username, password=password, role=role)
                messages.success(request, "Đăng ký thành công. Vui lòng đăng nhập.")
                return redirect('login')
    return render(request, 'register.html')

@csrf_exempt
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Giả sử xử lý gửi email thành công
        if email:
            messages.success(request, "Email khôi phục mật khẩu đã được gửi.")
        else:
            messages.error(request, "Vui lòng nhập email.")
    return render(request, 'forgot_password.html')

def profile_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Bạn cần đăng nhập để xem thông tin cá nhân.")
        return redirect('login')
    user = get_object_or_404(User, id=user_id)
    return render(request, 'profile.html', {'user': user})

# --- Giỏ hàng ---
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk, is_deleted=False)
    cart = request.session.get('cart', {})
    if str(product.pk) in cart:
        cart[str(product.pk)] += 1
    else:
        cart[str(product.pk)] = 1
    request.session['cart'] = cart
    messages.success(request, f"Đã thêm {product.name} vào giỏ hàng.")
    return redirect('cart')

# def cart_view(request):
#     cart = request.session.get('cart', {})
#     cart_items = []
#     total_price = 0
#     for pk, quantity in cart.items():
#         product = get_object_or_404(Product, pk=pk, is_deleted=False)
#         subtotal = product.price * quantity
#         total_price += subtotal
#         cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
#     context = {'cart_items': cart_items, 'total_price': total_price}
#     return render(request, 'cart.html', context)
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for pk, quantity in cart.items():
        product = get_object_or_404(Product, pk=pk, is_deleted=False)
        price = product.current_price  # Dùng giá đã cập nhật
        subtotal = price * quantity
        total_price += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
            'final_price': price,  # Truyền thêm giá đã cập nhật
        })
    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'cart.html', context)


def cart_update(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                pk = key.split('_')[1]
                try:
                    quantity = int(value)
                    if quantity > 0:
                        cart[pk] = quantity
                    else:
                        cart.pop(pk, None)
                except ValueError:
                    continue
        request.session['cart'] = cart
        messages.success(request, "Giỏ hàng đã được cập nhật.")
    return redirect('cart')

def cart_remove(request, pk):
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        cart.pop(str(pk))
        request.session['cart'] = cart
        messages.success(request, "Sản phẩm đã được xóa khỏi giỏ hàng.")
    return redirect('cart')

# --- Thanh toán & Đơn hàng ---
# def checkout(request):
#     # Lấy giỏ hàng từ session
#     cart = request.session.get('cart', {})
#     if not cart:
#         messages.error(request, "Giỏ hàng của bạn đang trống.")
#         return redirect('cart')
#
#     total_price = 0
#     order_items = []
#     for pk, quantity in cart.items():
#         product = get_object_or_404(Product, pk=pk, is_deleted=False)
#         # Sử dụng giá hiện tại (nếu có flash sale thì là giá giảm, nếu không thì là giá gốc)
#         price = product.current_price
#         subtotal = price * quantity
#         total_price += subtotal
#         order_items.append({
#             'product': product,
#             'quantity': quantity,
#             'subtotal': subtotal,
#         })
#
#     if request.method == 'POST':
#         user_id = request.session.get('user_id')
#         if not user_id:
#             messages.error(request, "Bạn cần đăng nhập để thanh toán.")
#             return redirect('login')
#         user = get_object_or_404(User, id=user_id)
#         order = Order.objects.create(user=user, total_price=total_price, status='paid')
#         for item in order_items:
#             OrderItem.objects.create(
#                 order=order,
#                 product=item['product'],
#                 quantity=item['quantity'],
#                 # Ghi lại giá theo current_price
#                 price=item['product'].current_price
#             )
#         # Xóa giỏ hàng sau khi đặt hàng thành công
#         request.session['cart'] = {}
#         messages.success(request, f"Đơn hàng {order.id} của bạn đã được đặt thành công!")
#         return redirect('order_history')
#
#     context = {
#         'order_items': order_items,
#         'total_price': total_price,
#     }
#     return render(request, 'checkout.html', context)
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Giỏ hàng của bạn đang trống.")
        return redirect('cart')

    total_price = 0
    order_items = []
    for pk, quantity in cart.items():
        product = get_object_or_404(Product, pk=pk, is_deleted=False)
        price = product.current_price  # Dùng giá đã cập nhật theo Flash Sale nếu có
        subtotal = price * quantity
        total_price += subtotal
        order_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, "Bạn cần đăng nhập để thanh toán.")
            return redirect('login')
        user = get_object_or_404(User, id=user_id)
        order = Order.objects.create(user=user, total_price=total_price, status='paid')
        for item in order_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].current_price  # Ghi lại giá đã cập nhật
            )
        request.session['cart'] = {}
        messages.success(request, f"Đơn hàng {order.id} của bạn đã được đặt thành công!")
        return redirect('order_history')

    context = {'order_items': order_items, 'total_price': total_price}
    return render(request, 'checkout.html', context)

def order_history(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Bạn cần đăng nhập để xem đơn hàng.")
        return redirect('login')
    orders = Order.objects.filter(user__id=user_id).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

def order_list(request):
    query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "")

    # Truy vấn dữ liệu với tìm kiếm và bộ lọc
    orders = Order.objects.all()
    if query:
        orders = orders.filter(user__username__icontains=query)
    if status_filter:
        orders = orders.filter(status=status_filter)

    # Phân trang
    paginator = Paginator(orders, 10)  # 10 đơn hàng mỗi trang
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "admin/order_list.html", {
        "orders": page_obj,
        "query": query,
        "status_filter": status_filter,
    })

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/order_detail.html', {'order': order})

def order_create(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        order_item_form = OrderItemForm(request.POST)
        if order_form.is_valid() and order_item_form.is_valid():
            order = order_form.save()
            # Lưu thông tin chi tiết đơn hàng
            order_item = order_item_form.save(commit=False)
            order_item.order = order
            # Sử dụng giá sản phẩm hiện tại
            order_item.price = order_item.product.price
            order_item.save()
            messages.success(request, "Đơn hàng đã được tạo thành công.")
            return redirect('order_list')
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin.")
    else:
        order_form = OrderForm()
        order_item_form = OrderItemForm()
    return render(request, 'orders/order_form.html', {
        'order_form': order_form,
        'order_item_form': order_item_form,
        'action': 'Thêm'
    })

def order_update(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Lấy OrderItem đầu tiên (nếu có); nếu không có, để None
    order_item = order.items.first() if order.items.exists() else None

    if request.method == "POST":
        order_form = OrderForm(request.POST, instance=order)
        order_item_form = OrderItemForm(request.POST, instance=order_item)
        if order_form.is_valid() and order_item_form.is_valid():
            order = order_form.save()
            order_item = order_item_form.save(commit=False)
            order_item.order = order
            # Lấy giá sản phẩm từ đối tượng product đã chọn
            order_item.price = order_item.product.price
            order_item.save()
            messages.success(request, "Đơn hàng đã được cập nhật thành công.")
            return redirect('order_list')
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin.")
    else:
        order_form = OrderForm(instance=order)
        order_item_form = OrderItemForm(instance=order_item)
    return render(request, 'orders/order_form.html', {
        'order_form': order_form,
        'order_item_form': order_item_form,
        'action': 'Sửa',
        'order': order
    })


def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.delete()
        return redirect('order_list')
    return render(request, 'orders/order_confirm_delete.html', {'order': order})
# --- Quản lý Sản phẩm ---
def product_list(request):
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    supplier_filter = request.GET.get('supplier', '')
    products = Product.objects.filter(is_deleted=False).order_by('id')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_filter:
        products = products.filter(category__id=category_filter)
    if supplier_filter:
        products = products.filter(supplier__id=supplier_filter)
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.filter(is_deleted=False)
    suppliers = Supplier.objects.filter(is_deleted=False)
    context = {
        'page_obj': page_obj,
        'query': query,
        'categories': categories,
        'suppliers': suppliers,
        'selected_category': category_filter,
        'selected_supplier': supplier_filter,
    }
    return render(request, 'products/product_list.html', context)

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Sản phẩm đã được tạo thành công.")
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Thêm'})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, is_deleted=False)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Sản phẩm đã được cập nhật thành công.")
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Sửa'})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, is_deleted=False)
    product.is_deleted = True
    product.save()
    messages.success(request, "Sản phẩm đã được xóa thành công.")
    return redirect('product_list')

def product_search(request):
    q = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=q, is_deleted=False)
    context = {'products': products, 'q': q}
    return render(request, 'products/index.html', context)

# --- Quản lý Danh mục ---
def category_list(request):
    q = request.GET.get('q', '')
    categories = Category.objects.all()

    if q:
        categories = categories.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )

    paginator = Paginator(categories, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'categories/category_list.htm', {
        'categories': categories,
        'q': q,
    })
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Danh mục đã được tạo thành công.")
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'categories/category_form.htm', {'form': form, 'action': 'Thêm'})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk, is_deleted=False)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Danh mục đã được cập nhật thành công.")
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/category_form.htm', {'form': form, 'action': 'Sửa'})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, is_deleted=False)
    category.is_deleted = True
    category.save()
    messages.success(request, "Danh mục đã được xóa thành công.")
    return redirect('category_list')

import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .forms import UploadCategoryForm
from .models import Category
from django.http import HttpResponse
from io import BytesIO

def upload_categories_excel(request):
    """
    - Đọc file Excel
    - Bỏ qua các dòng name trống.
    - Dùng get_or_create tránh duplicate.
    - Đếm số bản ghi thêm mới.
    - Thông báo thành công hoặc lỗi chi tiết.
    """
    if request.method == 'POST':
        form = UploadCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            try:
                df = pd.read_excel(file, engine='openpyxl')
            except Exception as e:
                messages.error(request, f'Không thể đọc file Excel: {e}')
                return redirect('upload_categories')

            # Kiểm tra cột bắt buộc
            if 'name' not in df.columns:
                messages.error(request, "File Excel phải có cột 'name'.")
                return redirect('upload_categories')

            added = 0
            updated = 0
            with transaction.atomic():
                for idx, row in df.iterrows():
                    name = row.get('name')
                    # Skip nếu name NaN hoặc chuỗi rỗng
                    if not pd.notna(name) or str(name).strip() == '':
                        continue
                    name = str(name).strip()
                    description = row.get('description', '') or ''
                    obj, created = Category.objects.get_or_create(
                        name=name,
                        defaults={'description': description}
                    )
                    if created:
                        added += 1
                    else:
                        # nếu muốn cập nhật description khi record đã tồn tại, bỏ comment:
                        # obj.description = description
                        # obj.save(update_fields=['description'])
                        updated += 1

            msg = []
            if added:
                msg.append(f'<strong>{added}</strong> danh mục mới')
            if updated:
                msg.append(f'<strong>{updated}</strong> danh mục đã tồn tại')
            if msg:
                messages.success(request, 'Nhập Excel thành công: ' + ', '.join(msg))
            else:
                messages.info(request, 'Không có dòng hợp lệ nào để thêm.')

            return redirect('category_list')
        else:
            # form không hợp lệ (như extension sai)
            for err in form.errors.get('file', []):
                messages.error(request, err)
            return redirect('upload_categories')
    else:
        form = UploadCategoryForm()

    return render(request, 'categories/upload.html', {'form': form})

# Export báo cáo Excel
def export_categories_excel(request):
    qs = Category.objects.filter(is_deleted=False).values('id', 'name', 'description')
    df = pd.DataFrame(list(qs))
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Categories')
    writer.close()
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="categories_report.xlsx"'
    return response

from django.utils.timezone import now

# In báo cáo từ trình duyệt
def print_categories_report(request):
    categories = Category.objects.all()
    current_time = now()
    current_time_str = current_time.strftime("Ngày %d tháng %m năm %Y")
    return render(request, 'categories/print_report.html', {
        'categories': categories,
        'current_time_str': current_time_str
    })



# --- Quản lý Nhà cung cấp ---
def supplier_list(request):
    suppliers = Supplier.objects.filter(is_deleted=False)
    return render(request, 'suppliers/supplier_list.html', {'suppliers': suppliers})

def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Nhà cung cấp đã được tạo thành công.")
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'suppliers/supplier_form.html', {'form': form, 'action': 'Thêm'})

def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk, is_deleted=False)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, "Nhà cung cấp đã được cập nhật thành công.")
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'suppliers/supplier_form.html', {'form': form, 'action': 'Sửa'})

def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk, is_deleted=False)
    supplier.is_deleted = True
    supplier.save()
    messages.success(request, "Nhà cung cấp đã được xóa thành công.")
    return redirect('supplier_list')

from django.http import JsonResponse


def product_suggestions(request):
    query = request.GET.get('q', '').strip()
    suggestions = []
    if query:
        products = Product.objects.filter(name__icontains=query, is_deleted=False)[:5]  # Lọc sản phẩm không bị xóa mềm
        for product in products:
            image_url = product.image.url if product.image else '/static/images/no-image.png'  # Kiểm tra nếu không có ảnh
            suggestions.append({
                'id': product.id,
                'name': product.name,
                'image_url': request.build_absolute_uri(image_url)  # Chuyển thành URL đầy đủ
            })

    return JsonResponse({'suggestions': suggestions})
def revenue_report(request):
    # Lấy khoảng thời gian từ GET parameters, nếu không có thì mặc định là 30 ngày gần nhất
    start_date_param = request.GET.get('start_date')
    end_date_param = request.GET.get('end_date')
    today = datetime.date.today()

    if start_date_param:
        try:
            start_date = datetime.datetime.strptime(start_date_param, '%Y-%m-%d').date()
        except ValueError:
            start_date = today - datetime.timedelta(days=30)
    else:
        start_date = today - datetime.timedelta(days=30)

    if end_date_param:
        try:
            end_date = datetime.datetime.strptime(end_date_param, '%Y-%m-%d').date()
        except ValueError:
            end_date = today
    else:
        end_date = today

    # Xác định khoảng thời gian chính xác với thời gian bắt đầu và kết thúc của ngày
    start_datetime = datetime.datetime.combine(start_date, datetime.time.min)
    end_datetime = datetime.datetime.combine(end_date, datetime.time.max)

    # Lọc đơn hàng theo khoảng thời gian (có thể điều chỉnh trạng thái nếu cần)
    orders = Order.objects.filter(created_at__range=(start_datetime, end_datetime))

    total_revenue = orders.aggregate(total=Sum('total_price'))['total'] or 0
    order_count = orders.count()
    average_order = orders.aggregate(avg=Avg('total_price'))['avg'] or 0

    context = {
        'orders': orders,
        'total_revenue': total_revenue,
        'order_count': order_count,
        'average_order': average_order,
        # Chuyển đổi sang định dạng YYYY-MM-DD cho input type="date"
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
    }
    return render(request, 'reports/revenue_report.html', context)

from .models import Promotion
from django.utils import timezone
from django.db.models import F
from .forms import PromotionForm


def promotion_list(request):
    query = request.GET.get('q', '')
    promotions = Promotion.objects.all()
    if query:
        promotions = promotions.filter(title__icontains=query)

    paginator = Paginator(promotions, 10)  # 10 chương trình mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'promotions': page_obj,
        'query': query,
    }
    return render(request, 'promotions/promotion_list.html', context)

def promotion_slide_show(request):
    promotions = Promotion.objects.filter(
        active=True,
        start_date__lte=timezone.now().date(),
        end_date__gte=timezone.now().date()
    )
    return render(request, 'promotions/slide_show.html', {'promotions': promotions})

def product_sale(request):
    """
    Giả sử sản phẩm giảm giá là những sản phẩm có giá giảm (giá khuyến mãi nhỏ hơn giá gốc).
    Nếu bạn có thêm trường 'discount' hoặc 'sale_price' trong Product, thay đổi điều kiện lọc cho phù hợp.
    Ví dụ, nếu dùng 'sale_price', ta lọc:
       Product.objects.filter(is_deleted=False, sale_price__lt=F('price'))
    """
    sale_products = Product.objects.filter(is_deleted=False, sale_price__lt=F('price'))
    return render(request, 'promotions/product_sale.html', {'sale_products': sale_products})

def promotion_create(request):
    if request.method == 'POST':
        form = PromotionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Chương trình khuyến mãi đã được tạo thành công.")
            return redirect('promotion_list')
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin.")
    else:
        form = PromotionForm()
    return render(request, 'promotions/promotion_form.html', {'form': form, 'action': 'Thêm'})

def promotion_update(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    if request.method == 'POST':
        form = PromotionForm(request.POST, request.FILES, instance=promotion)
        if form.is_valid():
            form.save()
            messages.success(request, "Chương trình khuyến mãi đã được cập nhật thành công.")
            return redirect('promotion_list')
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin.")
    else:
        form = PromotionForm(instance=promotion)
    return render(request, 'promotions/promotion_form.html', {'form': form, 'action': 'Sửa'})

def promotion_delete(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    if request.method == "POST":
        promotion.delete()
        messages.success(request, "Chương trình khuyến mãi đã được xóa thành công.")
        return redirect('promotion_list')
    return render(request, 'promotions/promotion_confirm_delete.html', {'promotion': promotion})
from .models import FlashSale
from .forms import FlashSaleForm

def flash_sale_list(request):
    """
    Hiển thị danh sách các chương trình flash sale đang được kích hoạt
    """
    flash_sales = FlashSale.objects.filter(active=True, start_date__lte=timezone.now().date(), end_date__gte=timezone.now().date())
    paginator = Paginator(flash_sales, 10)  # 10 chương trình mỗi trang
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'flash_sales/flash_sale_list.html', {'page_obj': page_obj})

def flash_sale_create(request):
    products = Product.objects.filter(is_deleted=False)
    products_price = {str(p.id): float(p.price) for p in products}
    if request.method == 'POST':
        form = FlashSaleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Chương trình Flash Sale đã được tạo thành công.")
            return redirect('flash_sale_list')
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin.")
    else:
        form = FlashSaleForm()
    context = {
        'form': form,
        'action': 'Thêm',
        'products_price': products_price
    }
    return render(request, 'flash_sales/flash_sale_form.html', context)


def flash_sale_update(request, pk):
    flash_sale = get_object_or_404(FlashSale, pk=pk)
    if request.method == 'POST':
        form = FlashSaleForm(request.POST, instance=flash_sale)
        if form.is_valid():
            form.save()
            messages.success(request, "Chương trình Flash Sale đã được cập nhật thành công.")
            return redirect('flash_sale_list')
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin.")
    else:
        form = FlashSaleForm(instance=flash_sale)
    return render(request, 'flash_sales/flash_sale_form.html', {'form': form, 'action': 'Sửa'})

def flash_sale_delete(request, pk):
    flash_sale = get_object_or_404(FlashSale, pk=pk)
    if request.method == "POST":
        flash_sale.delete()
        messages.success(request, "Chương trình Flash Sale đã được xóa thành công.")
        return redirect('flash_sale_list')
    return render(request, 'flash_sales/flash_sale_confirm_delete.html', {'flash_sale': flash_sale})

def flash_sale_products(request):
    """
    Hiển thị danh sách sản phẩm đang được flash sale, cùng với giá đã giảm.
    Tính toán giá giảm dựa trên sale_price hoặc tính theo discount_percent.
    """
    flash_sales = FlashSale.objects.filter(active=True, start_date__lte=timezone.now().date(), end_date__gte=timezone.now().date())
    # Nếu muốn tính lại giá giảm dựa trên discount_percent, bạn có thể làm như sau:
    for flash in flash_sales:
        # Giả sử sản phẩm ban đầu có trường 'price'
        flash.product.discounted_price = flash.sale_price  # hoặc tính theo flash.product.price * (1 - flash.discount_percent/100)
    return render(request, 'flash_sales/flash_sale_products.html', {'flash_sales': flash_sales})


from .forms import ProductDetailForm
from .models import ProductDetail


def product_create_with_detail(request):
    """
    Tạo mới sản phẩm và (tùy chọn) thông tin chi tiết sản phẩm.
    Nếu form thông tin chi tiết có ít nhất 1 trường (ngoại trừ trường product) được nhập,
    thì thông tin chi tiết sẽ được lưu kèm theo.
    """
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        detail_form = ProductDetailForm(request.POST)
        if product_form.is_valid():
            product = product_form.save()
            # Nếu detail_form hợp lệ, ta kiểm tra xem có ít nhất 1 trường (ngoại trừ 'product') có giá trị hay không.
            if detail_form.is_valid():
                # Lấy dữ liệu đã sạch của detail_form
                detail_data = detail_form.cleaned_data
                # Loại bỏ trường 'product' vì form tạo mới sẽ cho phép chọn sản phẩm
                detail_data_no_product = {k: v for k, v in detail_data.items() if k != 'product'}
                if any(detail_data_no_product.values()):
                    detail = detail_form.save(commit=False)
                    detail.product = product
                    detail.save()
            messages.success(request, "Sản phẩm và thông tin chi tiết (nếu có) đã được tạo thành công.")
            return redirect('product_list')
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin sản phẩm.")
    else:
        product_form = ProductForm()
        detail_form = ProductDetailForm()
    context = {
        'action': 'Thêm',
        'product_form': product_form,
        'detail_form': detail_form,
    }
    return render(request, 'products/product_create_with_detail.html', context)


def product_detail_create(request):
    """
    Tạo mới thông tin chi tiết cho sản phẩm.
    Cho phép chọn sản phẩm từ dropdown. Nếu sản phẩm đã có thông tin chi tiết, chuyển hướng sang trang cập nhật.
    """
    if request.method == 'POST':
        form = ProductDetailForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']

            # Kiểm tra xem sản phẩm đã có thông tin chi tiết chưa
            if ProductDetail.objects.filter(product=product).exists():
                messages.warning(request,
                                 "Thông tin chi tiết của sản phẩm đã tồn tại, vui lòng sử dụng chức năng cập nhật.")
                return redirect('product_detail_update', product_id=product.id)

            detail = form.save(commit=False)
            detail.save()  # Lưu vào database

            messages.success(request, "Thông tin chi tiết của sản phẩm đã được tạo thành công.")
            return redirect('product_detail_view', product_id=product.id)
        else:
            # Debug lỗi form
            print(" Form không hợp lệ! Lỗi:", form.errors.as_data())
            messages.error(request, "Vui lòng kiểm tra lại thông tin nhập vào.")
    else:
        form = ProductDetailForm()

    context = {
        'form': form,
        'action': 'Thêm',
    }
    return render(request, 'product_detail/product_detail_form.html', context)

def product_detail_update(request, product_id):
    """
    Cập nhật thông tin chi tiết của sản phẩm.
    Nếu chưa tồn tại, chuyển hướng đến view tạo mới.
    """
    product = get_object_or_404(Product, id=product_id, is_deleted=False)
    try:
        detail = product.food_detail
    except ProductDetail.DoesNotExist:
        messages.warning(request, "Chưa có thông tin chi tiết cho sản phẩm này. Vui lòng tạo mới.")
        return redirect('product_detail_create')

    if request.method == 'POST':
        form = ProductDetailForm(request.POST, instance=detail)
        if form.is_valid():
            form.save()
            messages.success(request, "Thông tin chi tiết của sản phẩm đã được cập nhật thành công.")
            return redirect('product_detail_view', product_id=product.id)
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin nhập vào.")
    else:
        form = ProductDetailForm(instance=detail)
    context = {
        'form': form,
        'action': 'Sửa',
        'product': product,
    }
    return render(request, 'product_detail/product_detail_form.html', context)


def product_detail_view(request, product_id):
    """
    Hiển thị thông tin chi tiết của sản phẩm.
    Nếu chưa có thông tin chi tiết, trả về None.
    """
    product = get_object_or_404(Product, id=product_id, is_deleted=False)
    detail = ProductDetail.objects.filter(product=product).first()  # Tránh lỗi nếu không có chi tiết

    if not detail:
        messages.warning(request, "Sản phẩm này chưa có thông tin chi tiết.")
        return redirect('product_detail_create')

    context = {
        'product': product,
        'detail': detail,
    }
    return render(request, 'product_detail/product_detail_view.html', context)


def product_detail_list(request):
    """
    Hiển thị danh sách các thông tin chi tiết sản phẩm.
    """
    product_details = ProductDetail.objects.all().order_by('id')
    paginator = Paginator(product_details, 10)  # 10 bản ghi mỗi trang
    page_number = request.GET.get("page")
    product_details_page = paginator.get_page(page_number)
    context = {
        'product_details': product_details_page,
    }
    return render(request, 'product_detail/product_detail_list.html', context)


def product_detail_delete(request, product_id):
    """
    Xóa thông tin chi tiết của sản phẩm.
    """
    product = get_object_or_404(Product, id=product_id, is_deleted=False)
    detail = get_object_or_404(ProductDetail, product=product)
    if request.method == 'POST':
        detail.delete()
        messages.success(request, "Thông tin chi tiết của sản phẩm đã được xóa thành công.")
        return redirect('product_list')
    context = {
        'product': product,
        'detail': detail,
    }
    return render(request, 'product_detail/product_detail_confirm_delete.html', context)


from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import ProductComment
from .forms import ProductCommentForm

# --- Danh sách bình luận sản phẩm ---
class ProductCommentListView(ListView):
    model = ProductComment
    template_name = "product_comments/list.html"  # Tạo file template ở thư mục product_comments
    context_object_name = "comments"
    paginate_by = 10  # Hiển thị 10 bình luận trên mỗi trang

    def get_queryset(self):
        # Chỉ lấy các bình luận chưa bị xóa mềm (is_deleted=False) và sắp xếp mới nhất trước
        return ProductComment.objects.filter(is_deleted=False).order_by('-created_at')

# --- Tạo mới bình luận sản phẩm ---
from django.contrib.auth.decorators import login_required
from .models import ProductComment

def product_comment_create(request):
    if request.method == "POST":
        product_id = request.POST.get("product")
        content = request.POST.get("content")
        rating = request.POST.get("rating")

        if not product_id or not content:
            return JsonResponse({"error": "Thiếu dữ liệu"}, status=400)

        product = get_object_or_404(Product, id=product_id)

        user = request.user if request.user.is_authenticated else None  # Cho phép không có user

        ProductComment.objects.create(
            user=user,
            product=product,
            content=content,
            rating=rating
        )

        return redirect("product_detail", product_id=product_id)

    return JsonResponse({"error": "Chỉ hỗ trợ phương thức POST"}, status=405)
class ProductCommentCreateView(CreateView):
    model = ProductComment
    form_class = ProductCommentForm
    template_name = "product_comments/form.html"  # Cập nhật đường dẫn đúng với file của bạn
    success_url = reverse_lazy("product_comment_list")


# --- Cập nhật bình luận sản phẩm ---
class ProductCommentUpdateView(UpdateView):
    model = ProductComment
    form_class = ProductCommentForm
    template_name = "product_comments/form.html"
    success_url = reverse_lazy("product_comment_list")

# --- Xóa mềm bình luận sản phẩm ---
class ProductCommentDeleteView(DeleteView):
    model = ProductComment
    template_name = "product_comments/confirm_delete.html"  # Tạo file xác nhận xóa
    success_url = reverse_lazy("product_comment_list")

    def delete(self, request, *args, **kwargs):
        # Thực hiện xóa mềm: đánh dấu is_deleted = True thay vì xóa hoàn toàn bản ghi
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return redirect(self.get_success_url())


# Danh sách User (có tìm kiếm, phân trang)
from .forms import UserForm
from django.db.models import Q
def user_list(request):
    search_query = request.GET.get('q', '')
    users = User.objects.filter(
        Q(username__icontains=search_query) | Q(role__name__icontains=search_query)
    ).order_by('-id')

    paginator = Paginator(users, 10)  # Phân trang (10 user/trang)
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)

    return render(request, 'user/user_list.html', {'users': users_page, 'search_query': search_query})

# Thêm User
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tài khoản đã được tạo thành công!")
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'user/user_form.html', {'form': form})

# Cập nhật User
def user_update(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật tài khoản thành công!")
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user/user_form.html', {'form': form})

# Xóa User
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "Xóa tài khoản thành công!")
        return redirect('user_list')
    return render(request, 'user/user_confirm_delete.html', {'user': user})

# Quản lý nhân viên
# --- Danh sách nhân viên (tìm kiếm và phân trang) ---
from .models import Employee
from .forms import EmployeeForm
def employee_list(request):
    search_query = request.GET.get('q', '')
    employees = Employee.objects.filter(
        Q(full_name__icontains=search_query) |
        Q(email__icontains=search_query) |
        Q(position__icontains=search_query)
    ).order_by('-id')

    paginator = Paginator(employees, 10)  # Hiển thị 10 nhân viên/trang
    page_number = request.GET.get('page')
    employees_page = paginator.get_page(page_number)

    context = {
        'employees': employees_page,
        'search_query': search_query,
    }
    return render(request, 'employee/employee_list.html', context)


# --- Tạo nhân viên ---
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Nhân viên được tạo thành công!")
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employee/employee_form.html', {'form': form})


# --- Cập nhật nhân viên ---
def employee_update(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Nhân viên được cập nhật thành công!")
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee/employee_form.html', {'form': form})


# --- Xóa nhân viên ---
def employee_delete(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, "Nhân viên được xóa thành công!")
        return redirect('employee_list')
    return render(request, 'employee/employee_confirm_delete.html', {'employee': employee})

from .forms import AutomaticWeeklyShiftAssignmentForm
from .models import Employee, WorkSchedule
from django.utils import timezone
from datetime import time, timedelta
from .forms import AutomaticShiftAssignmentForm


def auto_assign_shifts(request):
    if request.method == 'POST':
        form = AutomaticShiftAssignmentForm(request.POST)
        if form.is_valid():
            assign_date = form.cleaned_data['date']
            required_morning = form.cleaned_data['required_morning']
            required_afternoon = form.cleaned_data['required_afternoon']
            required_night = form.cleaned_data['required_night']

            shifts = {
                'morning': {'required': required_morning, 'start_time': time(8, 0), 'end_time': time(12, 0)},
                'afternoon': {'required': required_afternoon, 'start_time': time(13, 0), 'end_time': time(17, 0)},
                'night': {'required': required_night, 'start_time': time(18, 0), 'end_time': time(22, 0)},
            }

            assignments = {}
            for shift_type, data in shifts.items():
                required_count = data['required']
                assigned = []
                if required_count > 0:
                    available_employees = Employee.objects.filter(is_active=True).exclude(
                        work_schedules__date=assign_date
                    ).order_by('id')
                    count = 0
                    for emp in available_employees:
                        if count >= required_count:
                            break
                        schedule = WorkSchedule.objects.create(
                            employee=emp,
                            date=assign_date,
                            shift_type=shift_type,
                            start_time=data['start_time'],
                            end_time=data['end_time']
                        )
                        assigned.append(schedule)
                        count += 1
                assignments[shift_type] = assigned

            messages.success(request, f"Phân ca tự động cho ngày {assign_date} đã hoàn thành.")
            return render(request, 'auto_assign/auto_assign_shifts_result.html', {
                'assign_date': assign_date,
                'assignments': assignments
            })
    else:
        form = AutomaticShiftAssignmentForm()
    return render(request, 'auto_assign/auto_assign_shifts.html', {'form': form})

def auto_assign_weekly_shifts(request):
    """
    Phân ca tự động cho cả tuần dựa trên số lượng yêu cầu cho từng ca.
    Thuật toán cải tiến: Với mỗi ngày trong tuần (7 ngày), lấy danh sách nhân viên đang hoạt động chưa có lịch,
    sau đó phân bổ theo vòng (round robin) cho 3 ca (Sáng, Chiều, Tối) sao cho chia đều nếu có đủ.
    """
    if request.method == 'POST':
        form = AutomaticWeeklyShiftAssignmentForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            # Số lượng yêu cầu cho từng ca từ form
            required_counts = {
                'morning': form.cleaned_data['required_morning'],
                'afternoon': form.cleaned_data['required_afternoon'],
                'night': form.cleaned_data['required_night'],
            }
            # Định nghĩa thời gian ca làm việc mặc định
            shift_definitions = {
                'morning': {'start_time': time(8, 0), 'end_time': time(12, 0)},
                'afternoon': {'start_time': time(13, 0), 'end_time': time(17, 0)},
                'night': {'start_time': time(18, 0), 'end_time': time(22, 0)},
            }

            weekly_assignments = {}  # Key: ngày, Value: dict { ca: list(schedule) }
            shift_order = ['morning', 'afternoon', 'night']

            # Duyệt qua 7 ngày của tuần
            for day_offset in range(7):
                current_date = start_date + timedelta(days=day_offset)
                daily_assignments = {'morning': [], 'afternoon': [], 'night': []}
                # Lấy danh sách nhân viên đang hoạt động chưa có lịch cho ngày hiện tại
                available_employees = list(
                    Employee.objects.filter(is_active=True)
                    .exclude(work_schedules__date=current_date)
                    .order_by('id')
                )
                # Sử dụng thuật toán round-robin:
                # cứ lặp qua các ca theo thứ tự, gán 1 nhân viên nếu ca đó chưa đủ số yêu cầu
                while available_employees and any(len(daily_assignments[shift]) < required_counts[shift] for shift in shift_order):
                    for shift in shift_order:
                        if available_employees and len(daily_assignments[shift]) < required_counts[shift]:
                            emp = available_employees.pop(0)
                            schedule = WorkSchedule.objects.create(
                                employee=emp,
                                date=current_date,
                                shift_type=shift,
                                start_time=shift_definitions[shift]['start_time'],
                                end_time=shift_definitions[shift]['end_time']
                            )
                            daily_assignments[shift].append(schedule)
                weekly_assignments[current_date] = daily_assignments

            messages.success(request, f"Phân ca tự động cho tuần bắt đầu từ {start_date} đã hoàn thành.")
            return render(request, 'auto_assign/auto_assign_weekly_shifts_result.html', {
                'start_date': start_date,
                'weekly_assignments': weekly_assignments,
            })
    else:
        form = AutomaticWeeklyShiftAssignmentForm()
    return render(request, 'auto_assign/auto_assign_weekly_shifts.html', {'form': form})

from .models import Attendance, Employee
from .forms import AttendanceForm
def attendance_list(request):
    attendances = Attendance.objects.all().order_by('-date')
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})

def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Bản ghi chấm công đã được tạo thành công.")
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'attendance/attendance_form.html', {'form': form})

def attendance_update(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, "Bản ghi chấm công đã được cập nhật thành công.")
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=attendance)
    return render(request, 'attendance/attendance_form.html', {'form': form})

def attendance_delete(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        attendance.delete()
        messages.success(request, "Bản ghi chấm công đã được xóa thành công.")
        return redirect('attendance_list')
    return render(request, 'attendance/attendance_confirm_delete.html', {'attendance': attendance})

from decimal import Decimal, InvalidOperation
def salary_list(request):
    # Lấy tháng và năm từ query params, mặc định là tháng, năm hiện tại
    month = int(request.GET.get('month', timezone.now().month))
    year = int(request.GET.get('year', timezone.now().year))

    # Lấy tất cả nhân viên đang hoạt động, sắp xếp theo ID
    employees = Employee.objects.filter(is_active=True).order_by('id')

    salary_data = []
    for emp in employees:
        # Lấy danh sách chấm công của nhân viên trong tháng, năm đã chọn
        attendances = Attendance.objects.filter(employee=emp, date__year=year, date__month=month)
        # Tính tổng số giờ làm việc (số giờ tính được là kiểu float)
        total_hours = sum(a.hours_worked for a in attendances)
        # Tính tiền theo giờ: chuyển đổi tổng giờ làm việc sang Decimal
        hourly_rate = emp.salary / Decimal('160') if emp.salary else Decimal('0')
        calculated_salary = Decimal(total_hours) * hourly_rate
        salary_data.append({
            'employee': emp,
            'total_hours': total_hours,
            'hourly_rate': hourly_rate,
            'calculated_salary': calculated_salary,
        })

    context = {
        'salary_data': salary_data,
        'month': month,
        'year': year,
    }
    return render(request, 'salary/salary_list.html', context)

def calculate_salary(request, employee_id):
    """Tính lương cho một nhân viên dựa trên chấm công trong tháng."""
    employee = get_object_or_404(Employee, id=employee_id)
    # Lấy tháng, năm từ query params (mặc định là tháng hiện tại)
    month = int(request.GET.get('month', timezone.now().month))
    year = int(request.GET.get('year', timezone.now().year))

    # Lấy danh sách chấm công của nhân viên trong tháng
    attendances = Attendance.objects.filter(employee=employee, date__year=year, date__month=month)
    total_hours = sum(a.hours_worked for a in attendances)

    # Giả sử: lương cơ bản của nhân viên là mức lương tháng và 160 giờ làm việc chuẩn
    hourly_rate = employee.salary / 160 if employee.salary else 0
    calculated_salary = total_hours * hourly_rate

    context = {
        'employee': employee,
        'attendances': attendances,
        'total_hours': total_hours,
        'hourly_rate': hourly_rate,
        'calculated_salary': calculated_salary,
        'month': month,
        'year': year,
    }
    return render(request, 'attendance/calculate_salary.html', context)
