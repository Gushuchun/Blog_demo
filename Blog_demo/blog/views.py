from django.urls.base import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods,require_POST, require_GET
from .models import BlogCategory, Blog, BlogComment
from .forms import PublishForm
from django.db.models import Q

# Create your views here.
def index(request):
    blogs = Blog.objects.all()
    return render(request, 'index.html', context={"blogs": blogs})

def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Exception as e:
        blog = None
    return render(request, 'blog_detail.html', context={'blog': blog})

@require_http_methods(['GET', 'POST'])
@login_required(login_url=reverse_lazy("author:login"))
def post_blog(request):
    if request.method == 'GET':
        category = BlogCategory.objects.all()
        return render(request, 'post_blog.html', context={'category': category})
    else:
        form = PublishForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            content_2 = form.cleaned_data.get('content_2')
            print(content,content_2)
            blog = Blog.objects.create(title=title, content=content, category_id=category_id, author=request.user)
            return JsonResponse({"code": 200, "message": "Post success", "data": {"blog_id": blog.id}})
        else:
            return JsonResponse({"code":400, "message":form.errors})

@require_POST
@login_required(login_url=reverse_lazy("author:login"))
def post_comment(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    print(1)
    BlogComment.objects.create(blog_id=blog_id, content=content, author=request.user)

    #reload this page
    return redirect(reverse('blog:blog_detail', kwargs={"blog_id":blog_id}))

@require_GET
def search(request):
    # /search?q=xxx
    q = request.GET.get('q')
    # 从博客的标题和内容中查找含有q关键字的博客
    blogs = Blog.objects.filter(Q(title__icontains=q)|Q(content__icontains=q)).all()
    return render(request, 'index.html', context={"blogs": blogs})