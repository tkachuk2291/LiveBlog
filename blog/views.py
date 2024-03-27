from django.contrib.auth import logout
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib import messages
from blog.forms import UserLoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm, \
    RegistrationForm, ProfileForm, form_validation_error, PostCreateForm
from blog.models import Post, User
from django.contrib.auth import views as auth_views


def index(request):
    return render(request, 'blog-templates/index.html')


def user_create(request):
    return render(request, 'blog-templates/posts/post_create.html')


def about_us(request):
    return render(request, 'blog-templates/about-us.html')


def user_profile(request):
    return render(request, 'blog-templates/accounts/user_profile.html')


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
    success_url = reverse_lazy('blog:login')


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


class PostCreateView(generic.CreateView):
    model = Post
    template_name = "blog-templates/posts/post_create.html"
    context_object_name = "post_create"
    fields = ["title", "content", "tags"]

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title', None)
        tags = request.POST.get('tags', None)
        content = request.POST.get('content', None)
        post_v = PostCreateForm(request.POST)
        if post_v.is_valid():
            Post.objects.get_or_create(title=title, tags=tags, content=content, owner=request.user)
            return redirect("blog:post-list")
        else:
            return render(request, "blog-templates/posts/post_create.html", {'form': post_v})


class CustomPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    success_url = reverse_lazy('blog:login')


class UserProfileUpdateView(generic.UpdateView):
    model = User
    template_name = "blog-templates/accounts/user_profile.html"
    form_class = ProfileForm
    context_object_name = 'user_profile'

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone', None)
        birthday = request.POST.get('birthday', None)
        gender = request.POST.get('gender', None)
        user = self.get_object()
        user.phone = phone
        user.birthday = birthday
        user.gender = gender
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        messages.success(self.request, 'Profile updated successfully')

        return redirect("blog:user-profile", user.pk)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        messages.success(self.request, 'Profile updated successfully')
        return super().form_valid(form)
