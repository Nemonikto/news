from django.urls import path

from .views import *

urlpatterns = [
    path('', LaptopHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name ='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', LaptopCategory.as_view(), name='category'),
    path('ajax/', LaptopAPIView.as_view(), name='ajax'),
]