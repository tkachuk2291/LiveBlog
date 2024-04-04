from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from blog.views import (
    PostDetailView,
    UserLoginView,
    UserPasswordResetView,
    UserPasswordChangeView,
    UserPasswordResetConfirmView,
    logout_view,
    register_view,
    UserProfileUpdateView,
    PostCreateView,
    UserPostsListView,
    PostDeleteView,
    PostUpdateView,
    SearchView,
    like_post_view,
    home_view,
    PostListView,
)

urlpatterns = [
    path("", home_view, name="home-page"),
    path("home/", home_view, name="home-page"),
    path(
        "accounts/user_posts/", UserPostsListView.as_view(), name="user-posts"
    ),
    path(
        "accounts/post-delete/<int:pk>/",
        PostDeleteView.as_view(),
        name="post-delete",
    ),
    path("post/create", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post-update/<int:pk>", PostUpdateView.as_view(), name="post-update"),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("accounts/login/", UserLoginView.as_view(), name="login"),
    path("accounts/logout/", logout_view, name="logout"),
    path(
        "accounts/password-change/",
        UserPasswordChangeView.as_view(),
        name="password_change",
    ),
    path("accounts/register/", register_view, name="register"),
    path(
        "accounts/password-change-done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="blog-templates/accounts/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "accounts/password-reset/",
        UserPasswordResetView.as_view(
            success_url=reverse_lazy("blog:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "accounts/password-reset-done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="blog-templates/accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "accounts/password-reset-confirm/<uidb64>/<token>/",
        UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "accounts/password -reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name=
            "blog-templates/accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "accounts/user-profile/<int:pk>",
        UserProfileUpdateView.as_view(),
        name="user-profile",
    ),
    path("search_blogs/", SearchView.as_view(), name="search_blog"),
    path("like/", like_post_view, name="like-post"),
]

app_name = "blog"
