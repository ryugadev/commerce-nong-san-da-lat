import os
import django
import random

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commerce_project.settings') # Đổi 'commerce_project' thành tên thư mục chứa file settings.py của bạn nếu khác
django.setup()

from commerce.models import Product, Category, Supplier, ProductDetail

def seed_data():
    # 1. Lấy hoặc tạo Supplier và Category để làm mẫu
    supplier, _ = Supplier.objects.get_or_create(name="Nông Trại Đà Lạt Green")
    
    data = {
        "Rau Củ Tươi Sống": [
            {"name": "Bông cải xanh (Súp lơ)", "price": 35000, "origin": "Đà Lạt", "weight": 0.5},
            {"name": "Cà rốt hữu cơ", "price": 18000, "origin": "Đà Lạt", "weight": 0.3},
            {"name": "Bắp cải tím", "price": 22000, "origin": "Đà Lạt", "weight": 0.8},
            {"name": "Xà lách thủy canh", "price": 15000, "origin": "Lâm Đồng", "weight": 0.2},
        ],
        "Trái Cây": [
            {"name": "Táo Envy nhập khẩu", "price": 120000, "origin": "New Zealand", "weight": 1.0},
            {"name": "Dâu tây giống Mỹ", "price": 250000, "origin": "Đà Lạt", "weight": 0.5},
            {"name": "Cam sành Hàm Yên", "price": 45000, "origin": "Tuyên Quang", "weight": 1.0},
        ],
        "Nấm & Thực Phẩm Chay": [
            {"name": "Nấm Kim Châm tươi", "price": 12000, "origin": "Hàn Quốc", "weight": 0.15},
            {"name": "Nấm Đùi Gà", "price": 35000, "origin": "Việt Nam", "weight": 0.25},
        ]
    }

    for cat_name, products in data.items():
        # Lấy category, nếu chưa có thì tạo mới
        category, _ = Category.objects.get_or_create(name=cat_name)
        
        for item in products:
            # Tạo sản phẩm (nếu chưa có)
            product, created = Product.objects.get_or_create(
                name=item['name'],
                category=category,
                supplier=supplier,
                defaults={'price': item['price'], 'description': f"Sản phẩm {item['name']} tươi sạch, đảm bảo an toàn vệ sinh thực phẩm."}
            )
            
            if created:
                # Tự động tạo luôn ProductDetail gắn với sản phẩm đó
                ProductDetail.objects.create(
                    product=product,
                    brand="Đà Lạt Farm",
                    country_of_origin=item['origin'],
                    weight=item['weight'],
                    storage_instructions="Bảo quản ngăn mát tủ lạnh từ 5-10 độ C",
                    ingredients="100% tự nhiên"
                )
                print(f"--- Đã thêm: {item['name']}")
            else:
                print(f"--- Bỏ qua (đã tồn tại): {item['name']}")

if __name__ == "__main__":
    print("Đang bắt đầu bơm dữ liệu...")
    seed_data()
    print("Hoàn thành! Hãy kiểm tra trang web của bạn.")