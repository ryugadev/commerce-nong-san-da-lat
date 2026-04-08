from .models import Category
from .models import User
from django.shortcuts import get_object_or_404


def header_categories(request):
    # Lấy các danh mục chưa bị xóa
    categories = Category.objects.filter(is_deleted=False)
    return {'header_categories': categories}

def current_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = get_object_or_404(User, id=user_id)
            return {'user': user}
        except:
            return {}
    return {}