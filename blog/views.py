from django.shortcuts import render
from django.views import generic

from blog.models import Post


def index(request):
    return render(request, 'blog-templates/index.html')


def about_us(request):
    return render(request, 'blog-templates/about-us.html')


def contact_us(request):
    return render(request, 'blog-templates/contact-us.html')


def author(request):
    return render(request, 'blog-templates/author.html')


class PostListView(generic.ListView):
    model = Post
    context_object_name = "post_list"
    template_name = "blog-templates/posts/post_list.html"
