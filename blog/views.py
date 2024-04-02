from django.contrib.auth import logout
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.contrib import messages
from django.views.generic import ListView
from hitcount.views import HitCountDetailView
from taggit.models import Tag
from django.http import JsonResponse
from blog.forms import UserLoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm, \
    RegistrationForm, ProfileForm, form_validation_error, PostCreateForm
from blog.models import Post, User, Comment, Like
from django.contrib.auth import views as auth_views


def index(request):
    num_post = Post.objects.all().count()
    num_likes = Like.objects.all().count()
    num_views = Post.objects.aggregate(total_views=Sum('hit_count_generic__hits'))['total_views']
    context = {
        'num_post': num_post,
        'num_likes': num_likes,
        'num_views': num_views
    }
    return render(request, 'blog-templates/index.html', context)


def home_view(request):
    return render(request, 'blog-templates/posts/post_list.html')


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
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(owner=user.pk)

    def get_context_data(self, **kwargs):
        context_data = super(UserPostsListView, self).get_context_data(**kwargs)
        context_data['user_id'] = self.request.user.id
        return context_data


class PostListView(generic.ListView):
    model = Post
    context_object_name = "post_list"
    template_name = "blog-templates/posts/post_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context_data = super(PostListView, self).get_context_data(**kwargs)
        user = self.request.user
        context_data['user'] = user
        return context_data


class PostdublicateListView(generic.ListView):
    model = Post
    context_object_name = "post_list"
    template_name = "blog-templates/posts/post_list_dublicate.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context_data = super(PostdublicateListView, self).get_context_data(**kwargs)
        user = self.request.user
        context_data['user'] = user
        return context_data

    # class PostListViewJs(generic.ListView):
    #     model = Post
    #     context_object_name = "post_list"
    #     template_name = "blog-templates/posts/post_list_dublicate.html"

    # def get(self, *args, **kwargs):
    #     print(kwargs)
    #     upper = kwargs.get("num_posts")
    #     lower = upper - 3
    #     posts = list(Post.objects.values()[lower:upper])
    #     posts_size = len(Post.objects.all())
    #     size = True if upper >= posts_size else False
    #     return JsonResponse({"data": posts, "max": size}, safe=False)


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
        print(context_data)
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


def like_post(request):
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
    return redirect("blog:post-list")


class PostCreateView(generic.CreateView):
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

        return redirect("blog:user-profile", pk=user.pk)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        messages.success(self.request, 'Profile updated successfully')
        return super().form_valid(form)


class PostUpdateView(generic.UpdateView):
    model = Post
    template_name = "blog-templates/posts/post_update.html"
    context_object_name = 'post_update'
    fields = ["title", "content", "picture"]
    success_url = reverse_lazy("blog:user-posts")

    def post(self, request, pk):
        post_form = PostCreateForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.owner = request.user
            post.picture = post.picture
            post.title = post.title
            post.save()
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
