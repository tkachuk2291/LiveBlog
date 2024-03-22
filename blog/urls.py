from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from blog.views import (
    index,
    about_us,
    contact_us,
    author,
    PostListView,
    PostDetailView,
    UserLoginView,
    UserPasswordResetView,
    UserPasswordChangeView,
    UserPasswordResetConfirmView,
    logout_view,
    register
)

urlpatterns = [
    path("home/", index, name="home-page"),
    path('about-us/', about_us, name='about-us'),
    path('contact-us/', contact_us, name='contact-us'),
    path('author/', author, name='author'),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("accounts/login/", UserLoginView.as_view(), name="login"),
    path("accounts/logout/", logout_view, name="logout"),
    path('accounts/password-change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/register/', register, name='register'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='blog-templates/accounts/password_change_done.html'
    ), name='password_change_done'),
    path('accounts/password-reset/', UserPasswordResetView.as_view(
        success_url=reverse_lazy('blog:password_reset_done'),

    ), name='password_reset'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='blog-templates/accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/',
         UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password -reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='blog-templates/accounts/password_reset_complete.html'
    ), name='password_reset_complete'),

]

app_name = "blog"
