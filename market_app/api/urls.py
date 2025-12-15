from django.urls import path, include
from .views import MarketView,ProductViewSet, MarketDetailView,SellerOfMarketList, seller_view, single_seller_view, product_view, single_product_view
from rest_framework import routers
router = routers.SimpleRouter()
router.register(r'Product', ProductViewSet, basename='product')


urlpatterns = [
    path('markets/', MarketView.as_view(), name="market-view"),
    path('markets/<int:pk>/', MarketDetailView.as_view(), name="market-detail"),
    path('markets/<int:pk>/sellers', SellerOfMarketList.as_view(),),
    path('sellers/', seller_view, name="seller-view"),
    path('sellers/<int:pk>/', single_seller_view, name="seller-detail"),
    path('products/', product_view, name="product-view"),
    path('products/<int:pk>/', single_product_view, name="product-detail"),
    path('', include(router.urls))
]