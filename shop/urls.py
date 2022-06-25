from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import ProductView, CategoryView, Categorize, CreateProduct, UpdateProduct, DeleteProduct, product_detail, AddReview

urlpatterns = [
    path('', ProductView.as_view(), name='home'),
    path('categories/', cache_page(60*15)(CategoryView.as_view()), name='categories'),
    path('create/', login_required(CreateProduct.as_view()), name='create'),
    path('update/<slug:slug>/', login_required(UpdateProduct.as_view()), name='update'),
    path('delete/<slug:slug>/', login_required(DeleteProduct.as_view()), name='delete'),
    path('review/<int:pk>/', AddReview.as_view(), name='add_review'),
    path('<slug:slug>/products/', Categorize.as_view(), name='categorize'),
    path('<slug:slug>/', product_detail, name='product_detail'),

]

