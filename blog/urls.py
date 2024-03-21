from django.urls import path, include
from blog.views import index, about_us, contact_us, author, PostListView, PostDetailView , UserLoginView , logout_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("home/", index, name="home-page"),
    path('about-us/', about_us, name='about-us'),
    path('contact-us/', contact_us, name='contact-us'),
    path('author/', author, name='author'),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("accounts/login/", UserLoginView.as_view(), name="login"),
    path("accounts/logout/", logout_view,  name="logout")

]

app_name = "blog"
