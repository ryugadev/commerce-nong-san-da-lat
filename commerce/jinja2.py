# commerce/jinja2.py
from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

def environment(**options):
    env = Environment(**options)
    # Thêm các biến và hàm toàn cục cho template nếu cần
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
