from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Category, Post

POST_LIMIT = 5


def get_posts():
    return Post.objects.select_related(
        'author',
        'location',
        'category',
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )


def index(request):
    post_list = get_posts()[:POST_LIMIT]

    return render(request, 'blog/index.html', {
        'post_list': post_list
    })


def post_detail(request, post_id):
    post = get_object_or_404(
        get_posts(),
        pk=post_id,
    )

    return render(request, 'blog/detail.html', {
        'post': post
    })


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    post_list = category.posts.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
    )

    return render(request, 'blog/category.html', {
        'category': category,
        'post_list': post_list
    })
