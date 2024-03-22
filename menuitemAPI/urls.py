from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu-item/', include('menuitem_app.urls'))
]
