from django.urls import path
from .views import ProductView, CategoryView, Categorize, ProductDetail

urlpatterns = [
    path('', ProductView.as_view(), name='home'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('<slug:slug>/products/', Categorize.as_view(), name='categorize'),
    path('<slug:slug>/', ProductDetail.as_view(), name='product_detail'),

]
