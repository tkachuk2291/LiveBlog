from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views import generic

from blog.forms import UserLoginForm
from blog.models import Post, User


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


class UserLoginView(LoginView):
    template_name = 'blog-templates/accounts/sign-in.html'
    form_class = UserLoginForm


def logout_view(request):
    logout(request)
    return redirect("blog:home-page")


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog-templates/posts/post_detail.html"
    context_object_name = "post_detail"

    def get_context_data(self, **kwargs):
        context_data = super(PostDetailView, self).get_context_data(**kwargs)
        try:
            username = User.objects.first()
            post = self.get_object()
            user = User.objects.get(username=username.username)
            posts = user.owner_posts.all()
            context_data['posts'] = posts
            context_data['all_posts'] = posts.exclude(pk=post.pk)
        except User.DoesNotExist:
            pass

        return context_data
