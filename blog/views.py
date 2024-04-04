from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordChangeView,
)
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib import messages
from django.views.generic import ListView
from hitcount.views import HitCountDetailView
from blog.forms import (
    UserLoginForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
    UserPasswordChangeForm,
    RegistrationForm,
    ProfileForm,
    PostCreateForm,
)
from blog.models import Post, User, Comment, Like
from django.contrib.auth import views as auth_views


def home_view(request):
    num_post = Post.objects.all().count()
    print(num_post)
    num_likes = Like.objects.all().count()
    num_views = Post.objects.aggregate(total_views=Sum('hit_count_generic__hits'))['total_views']
    context = {
        'num_post': num_post,
        'num_likes': num_likes,
        'num_views': num_views
    }
    return render(request, 'blog-templates/home/home.html', context)


def logout_view(request):
    logout(request)
    return redirect("blog:login")


def register_view(request):
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


@login_required
def like_post_view(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post_obj = Post.objects.get(id=post_id)
        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)
        like, created = Like.objects.get_or_create(user=user, post_id=post_id)
        if not created:
            if like.value == "🤍︎":
                like.value = "❤️"

            else:
                like.value = "🤍️"
        like.save()
    redirect_to = request.META.get('HTTP_REFERER', 'blog:post-list')

    return redirect(redirect_to)


class UserPostsListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'blog-templates/accounts/user_posts.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(owner=user.pk)

    def get_context_data(self, **kwargs):
        context_data = super(UserPostsListView, self).get_context_data(**kwargs)
        context_data['user_id'] = self.request.user.id
        return context_data


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


class UserLoginView(LoginView):
    template_name = 'blog-templates/accounts/sign-in.html'
    form_class = UserLoginForm


class CustomPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    success_url = reverse_lazy('blog:login')


class UserProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = "blog-templates/accounts/user_profile.html"
    form_class = ProfileForm
    context_object_name = 'user_profile'

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone', None)
        birthday = request.POST.get('birthday', None)
        email = request.POST.get('email', None)
        gender = request.POST.get('gender', None)
        avatar = request.FILES.get('avatar', None)
        user = self.get_object()
        user.phone = phone
        user.format_birthday = birthday
        user.gender = gender
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if avatar:
            user.avatar = avatar
        user.save()

        return redirect("blog:user-profile", pk=user.pk)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        return super().form_valid(form)


class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    context_object_name = "post_list"
    template_name = "blog-templates/posts/post_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context_data = super(PostListView, self).get_context_data(**kwargs)
        user = self.request.user
        context_data['user'] = user
        return context_data


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = "blog-templates/accounts/user_posts.html"
    success_url = reverse_lazy('blog:user-posts')


class PostDetailView(HitCountDetailView):
    model = Post
    template_name = "blog-templates/posts/post_detail.html"
    context_object_name = "post_detail"
    count_hit = True

    def get_context_data(self, **kwargs):
        context_data = super(PostDetailView, self).get_context_data(**kwargs)
        post = self.get_object()
        author_post = Post.objects.filter(owner=post.owner).exclude(pk=post.pk)
        context_data['posts'] = author_post
        all_comments = post.post_comment.all()
        per_page = 3
        paginator = Paginator(all_comments, per_page)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context_data['page_obj'] = page_obj
        context_data.update({
            'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
        })
        return context_data

    def post(self, request, pk):
        post_commentary = get_object_or_404(Post, pk=pk)
        date_comment = request.POST.get("created_time_comment")
        content = request.POST.get("content")
        Comment.objects.create(
            user=request.user,
            post=post_commentary,
            content=content,
            created_time_comment=date_comment
        )
        return HttpResponseRedirect(
            reverse("blog:post-detail", kwargs={"pk": pk}) + f"?page={self.request.GET.get('page')}"
        )


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = "blog-templates/posts/post_create.html"
    context_object_name = "post_create"
    fields = ["title", "content", "picture"]

    def post(self, request, *args, **kwargs):
        post_form = PostCreateForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.owner = request.user
            post.picture = post.picture
            post.save()
            if 'from_user_first_posts' in request.GET:
                return redirect("blog:user-posts")
            else:
                return redirect('blog:post-list')
        else:
            return render(request, "blog-templates/posts/post_create.html", {'form': post_form})


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    template_name = "blog-templates/posts/post_update.html"
    context_object_name = 'post_update'
    fields = ["title", "content", "picture"]
    success_url = reverse_lazy("blog:user-posts")

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return super().form_valid(form)


class SearchView(LoginRequiredMixin, ListView):
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
