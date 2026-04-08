from django import forms
from .models import Product, Category, Supplier, Order, OrderItem, Promotion, FlashSale, ProductDetail, ProductComment
import os


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class UploadCategoryForm(forms.Form):
    file = forms.FileField(label='Chọn file Excel (.xls hoặc .xlsx)')

    def clean_file(self):
        f = self.cleaned_data['file']
        ext = os.path.splitext(f.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise forms.ValidationError('Chỉ cho phép file .xls hoặc .xlsx')
        # Bạn có thể thêm kiểm tra kích thước, content_type...
        return f


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'supplier', 'description', 'price', 'image']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'total_price', 'status']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'note']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ghi chú (nếu có)'}),
        }

class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['title', 'description', 'image', 'start_date', 'end_date', 'active', 'products']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'products': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

class FlashSaleForm(forms.ModelForm):
    class Meta:
        model = FlashSale
        fields = ['product', 'discount_percent', 'sale_price', 'start_date', 'end_date', 'active']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(FlashSaleForm, self).__init__(*args, **kwargs)
        choices = [(product.id, f"{product.name}") for product in Product.objects.all()]
        self.fields['product'].choices = choices

class ProductDetailForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_deleted=False),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'data-live-search': 'true',
            'placeholder': 'Chọn sản phẩm...'
        })
    )

    class Meta:
        model = ProductDetail
        fields = [
            'product', 'brand', 'manufacturer', 'country_of_origin',
            'weight', 'volume', 'packaging_type', 'ingredients', 'nutrition_facts',
            'allergens', 'manufacturing_date', 'expiration_date',
            'storage_instructions', 'usage_instructions', 'additional_info'
        ]
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'country_of_origin': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'volume': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'packaging_type': forms.TextInput(attrs={'class': 'form-control'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nutrition_facts': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'allergens': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturing_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'storage_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'usage_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductDetailForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields.pop('product')

class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['product', 'user', 'content', 'rating']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Viết bình luận của bạn...'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5',
                'placeholder': 'Đánh giá từ 1 đến 5'
            }),
        }

from .models import User, Role
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }

from .models import Employee
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'user', 'full_name', 'email', 'phone', 'address',
            'position', 'salary', 'date_joined', 'is_active'
        ]
        widgets = {
            'date_joined': forms.DateInput(attrs={'type': 'date'}),
        }

class AutomaticShiftAssignmentForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Ngày phân ca"
    )
    required_morning = forms.IntegerField(
        min_value=0,
        label="Số nhân viên ca sáng",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=0
    )
    required_afternoon = forms.IntegerField(
        min_value=0,
        label="Số nhân viên ca chiều",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=0
    )
    required_night = forms.IntegerField(
        min_value=0,
        label="Số nhân viên ca tối",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=0
    )

class AutomaticWeeklyShiftAssignmentForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Ngày bắt đầu tuần (Thứ Hai)"
    )
    required_morning = forms.IntegerField(
        min_value=0,
        label="Số nhân viên ca Sáng",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=0
    )
    required_afternoon = forms.IntegerField(
        min_value=0,
        label="Số nhân viên ca Chiều",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=0
    )
    required_night = forms.IntegerField(
        min_value=0,
        label="Số nhân viên ca Tối",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=0
    )

from .models import Attendance
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'check_in', 'check_out']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_in': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'check_out': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
        }

class SalaryFilterForm(forms.Form):
    month = forms.IntegerField(
        label="Tháng",
        min_value=1,
        max_value=12,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tháng'})
    )
    year = forms.IntegerField(
        label="Năm",
        min_value=2000,
        max_value=2100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Năm'})
    )