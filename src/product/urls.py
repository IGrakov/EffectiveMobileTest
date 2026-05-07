from django.urls import path

from product.views import ProductListView

app_name = "product"

urlpatterns = [
    path("list-product/", ProductListView.as_view(), name="product-list"),
]
