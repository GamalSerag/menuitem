from django.urls import path, include
from menuitem_app.views import MenuItemCreateView

urlpatterns = [
    path('add/', MenuItemCreateView.as_view(), name='menuitem-create'),
]