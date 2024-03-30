from django.contrib.auth import logout
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views import generic, View
from django.contrib import messages
from django.views.generic import ListView
from taggit.models import Tag

from blog.forms import UserLoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm, \
    RegistrationForm, ProfileForm, form_validation_error, PostCreateForm
from blog.models import Post, User, Comment
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


class UserPostsListView(generic.ListView):
    model = Post
    template_name = 'blog-templates/accounts/user_posts.html'
    context_object_name = 'post_list'

    def get_context_data(self, **kwargs):
        context_data = super(UserPostsListView, self).get_context_data(**kwargs)
        user = self.request.user
        author_posts = Post.objects.filter(owner=user.pk)
        context_data['posts'] = author_posts
        context_data['user_slug'] = user.slug

        return context_data


class PostListView(generic.ListView):
    model = Post
    context_object_name = "post_list"
    template_name = "blog-templates/posts/post_list.html"


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = "blog-templates/accounts/user_posts.html"
    success_url = reverse_lazy('blog:user-posts')


class UserLoginView(LoginView):
    template_name = 'blog-templates/accounts/sign-in.html'
    form_class = UserLoginForm


def logout_view(request):
    logout(request)
    return redirect("blog:login")


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)

            photo = request.FILES.get('photo')
            if photo:
                user.avatar = photo

            user.save()
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

    def post(self, request, slug):
        post_commentary = get_object_or_404(Post, slug=slug)
        date_comment = request.POST.get("created_time_comment")
        content = request.POST.get("content")
        Comment.objects.create(
            user=request.user,
            post=post_commentary,
            content=content,
            created_time_comment=date_comment
        )
        return HttpResponseRedirect(reverse("blog:post-detail", kwargs={"slug": slug}))


class PostCreateView(generic.CreateView):
    model = Post
    template_name = "blog-templates/posts/post_create.html"
    context_object_name = "post_create"
    fields = ["title", "content", "tags", "picture"]

    def post(self, request, *args, **kwargs):
        tags = request.POST.get('tags', None)
        post_form = PostCreateForm(request.POST, request.FILES)
        photo = request.FILES.get('photo')
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.slug = slugify(post.title)
            post.owner = request.user
            post.picture = post.picture
            post.save()
            post.tags.set(tags.split(','))
            return redirect('blog:post-list')
        else:
            return render(request, "blog-templates/posts/post_create.html", {'form': post_form})


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
        avatar = request.FILES.get('avatar', None)
        user = self.get_object()
        user.phone = phone
        user.birthday = birthday
        user.gender = gender
        user.first_name = first_name
        user.last_name = last_name
        if avatar:
            user.avatar = avatar
        user.save()
        messages.success(self.request, 'Profile updated successfully')

        return redirect("blog:user-profile", slug=user.slug)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        messages.success(self.request, 'Profile updated successfully')
        return super().form_valid(form)


class PostUpdateView(generic.UpdateView):
    model = Post
    template_name = "blog-templates/posts/post_update.html"
    context_object_name = 'post_update'
    fields = ["title", "content", "tags", "picture"]
    success_url = reverse_lazy("blog:user-posts")

    def post(self, request, slug):
        tags = request.POST.get('tags', None)
        post_form = PostCreateForm(request.POST, request.FILES)
        date = request.POST.get("created_time")
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.owner = request.user
            post.picture = post.picture
            post.title = post.title
            if post.title != post_form.instance.title:
                post.slug = slugify(post.title)
            post.save()
            post.tags.set(tags.split(','))
            return redirect("blog:post-list")
        else:
            return render(request, "blog-templates/posts/post_create.html", {'form': post_form})


class Search_View(ListView):
    model = Post
    template_name = "blog-templates/posts/post_list.html"
    context_object_name = "search_title"

    def get_queryset(self):
        query = self.request.GET.get('title_contains')
        if not query:
            messages.warning(self.request, 'Error! Enter text to search for')
            return Post.objects.none()

        queryset = Post.objects.filter(title__icontains=query) | Post.objects.filter(owner__username__icontains=query)
        if not queryset.exists():
            messages.warning(self.request, 'Error! No posts with that title or owner were found.')
        return queryset
