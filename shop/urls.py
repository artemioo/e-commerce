from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import ProductView, CategoryView, Categorize, ProductDetail, CreateProduct, UpdateProduct, DeleteProduct

urlpatterns = [
    path('', ProductView.as_view(), name='home'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('create/', login_required(CreateProduct.as_view()), name='create'),
    path('update/<slug:slug>/', login_required(UpdateProduct.as_view()), name='update'),
    path('delete/<slug:slug>/', login_required(DeleteProduct.as_view()), name='delete'),
    path('<slug:slug>/products/', Categorize.as_view(), name='categorize'),
    path('<slug:slug>/', ProductDetail.as_view(), name='product_detail'),

]
