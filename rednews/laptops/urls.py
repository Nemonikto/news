from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', LaptopHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name ='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:slug>/', ShowPost.as_view(), name='post'),
    path('post/<slug:slug>/update/', UpPost.as_view(), name='update'),
    path('post/<slug:slug>/delete/', DeletePost.as_view(), name='delete'),
    path('category/<slug:cat_slug>/', LaptopCategory.as_view(), name='category'),
    path('ajax/', LaptopAPIView.as_view(), name='ajax'),
]
