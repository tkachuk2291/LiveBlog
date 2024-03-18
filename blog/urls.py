from django.urls import path
from blog.views import index,about_us,contact_us,author

urlpatterns = [
    path("new/", index, name="index-task"),
    path('about-us/', about_us, name='about-us'),
    path('contact-us/', contact_us, name='contact-us'),
    path('author/', author, name='author'),
]

app_name = "blog"
