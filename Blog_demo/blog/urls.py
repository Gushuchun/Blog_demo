from django.urls import path
from . import  views

app_name = 'blog'

urlpatterns = [
    path("", views.index, name="index"),
    path("blog/detail/<int:blog_id>", views.blog_detail, name="blog_detail"),
    path("blog/post", views.post_blog, name="post"),
    path("blog/comment/post", views.post_comment, name="post_comment"),
    path("search", views.search, name="search_blog"),
]