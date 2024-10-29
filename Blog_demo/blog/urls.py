from django.urls import path
from . import  views

app_name = 'blog'

urlpatterns = [
    path("index", views.index, name="index"),
    path("<int:blog_id>", views.blog_detail, name="blog_detail"),
    path("post", views.post_blog, name="post_list"),
]