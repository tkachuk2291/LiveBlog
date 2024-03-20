from django.urls import path
from blog.views import index, about_us, contact_us, author, PostListView, PostDetailView

urlpatterns = [
    path("home/", index, name="home-page"),
    path('about-us/', about_us, name='about-us'),
    path('contact-us/', contact_us, name='contact-us'),
    path('author/', author, name='author'),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail")
]

app_name = "blog"
