from django.urls import path, include
from . import  views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'cf'

urlpatterns= [
    path('', views.index, name='index'),
    path('menu/', views.Products, name='menu'),
    path('product/<slug>/', views.itemdetailView.as_view(), name='product'),
    path('add-cart/<slug>/',views.add_cart, name='add-cart'),
    path('remove-cart/<slug>/',views.remove_cart, name='remove-cart'),
    path('remove-single-item/<slug>/',views.remove_single_item, name='remove-single-item'),
    path('add-single-item/<slug>/',views.add_single_item, name='add-single-item'),
    path('cart/', views.cart.as_view(), name='cart'),
    path('accounts/', include('django.contrib.auth.urls')),
     
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)