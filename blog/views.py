from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from blog.forms import UserLoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm, \
    RegistrationForm
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
    return redirect("blog:login")


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Account created successfully!")
            return redirect('/accounts/login')
        else:
            print("Registration failed!")
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'blog-templates/accounts/sign-up.html', context)


class UserPasswordResetView(PasswordResetView):
    template_name = "blog-templates/accounts/password_reset.html"
    form_class = UserPasswordResetForm
    success_url = reverse_lazy('blog:password_reset_done')
    email_template_name = "blog-templates/accounts/password_reset_email.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'blog-templates/accounts/password_reset_confirm.html'
    form_class = UserSetPasswordForm
    success_url = reverse_lazy('blog:password_reset_complete')


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'blog-templates/accounts/password_change.html'
    form_class = UserPasswordChangeForm


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog-templates/posts/post_detail.html"
    context_object_name = "post_detail"

    def get_context_data(self, **kwargs):
        context_data = super(PostDetailView, self).get_context_data(**kwargs)
        post = self.get_object()
        author_post = Post.objects.filter(owner=post.owner).exclude(pk=post.pk)
        context_data['posts'] = author_post

        return context_data
