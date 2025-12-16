from django.urls import path
from .views import ManufacturerList, ManufacturerDetail, ManufacturerUserList, ManufacturerUserDetail, ProductList, ProductDetail, ManufacturerProductListCreate


urlpatterns = [
    path('manufacturers/', ManufacturerList.as_view(), name="manufacturer-list"),
    path('manufacturers/<int:pk>/', ManufacturerDetail.as_view(), name="manufacturer-detail"),
    path('manufacturer-users/', ManufacturerUserList.as_view(), name="manufactureruser-list"),
    path('manufacturer-users/<int:pk>/', ManufacturerUserDetail.as_view(), name="manufactureruser-detail"),
    path('products/', ProductList.as_view(), name="product-view"),
    path('products/<int:pk>/', ProductDetail.as_view(), name="product-detail"),
    path('manufacturers/<int:manufacturer_id>/products', ManufacturerProductListCreate.as_view(), name="manufacturer-product-list-create"),
]