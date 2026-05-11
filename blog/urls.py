from django.urls import path
from . import views

urlpatterns = [
    path('',               views.blog_list,           name='blog-list'),
    path('create/',        views.blog_create,          name='blog-create'),
    path('manage/',        views.blog_manage,          name='blog-manage'),
    path('<slug:slug>/',   views.blog_detail,          name='blog-detail'),
    path('edit/<int:pk>/', views.blog_edit,            name='blog-edit'),
    path('delete/<int:pk>/', views.blog_delete,        name='blog-delete'),
    path('toggle/<int:pk>/', views.blog_toggle_publish, name='blog-toggle-publish'),
]
