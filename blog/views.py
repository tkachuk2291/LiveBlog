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
    return redirect("blog:home-page")


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
