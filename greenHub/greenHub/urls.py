from django.contrib import admin
from django.urls import path, include
# urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('green/', include('green.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
