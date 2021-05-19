from django.contrib import admin
from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.index, name="blog-index"),
    path('home/', PostListView.as_view(), name="blog-home"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path('post/new/', PostCreateView.as_view(), name="post-create"),
    path('about/', views.about, name="blog-about"),
    path('signin/', views.sign_in, name="sign_in"),
    path('signup/', views.sign_up, name="sign_up"),
    path('logout/', views.log_out, name="log_out"),
    path('profile/', views.profile, name="blog-profile"),

]
