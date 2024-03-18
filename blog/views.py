from django.shortcuts import render


def index(request):
    return render(request, 'blog-templates/index.html')


def about_us(request):
    return render(request, 'blog-templates/about-us.html')


def contact_us(request):
    return render(request, 'blog-templates/contact-us.html')


def author(request):
    return render(request, 'blog-templates/author.html')
