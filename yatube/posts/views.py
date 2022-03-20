from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Group, User
from .forms import PostForm

NUM_TITLE = 10


@login_required
def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, NUM_TITLE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'posts/index.html', context)


@login_required
def group_posts(request, slug):
    group = get_object_or_404(Group, pk=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:NUM_TITLE]
    context = {
        'group': group,
        'posts': posts
    }
    return render(request, 'posts/group_list.html', context)


@login_required
def profile(request, username):
    author = get_object_or_404(User, username=username)
    post = author.posts.order_by('-pub_date')
    paginator = Paginator(post, NUM_TITLE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'post': post,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    count = Post.objects.filter(author=author).count()
    context = {
        'post': post,
        'author': author,
        'count': count
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post_detail', post_id=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post_detail', post_id=post_id)
    else:
        form = PostForm(instance=post)
    context = {'form': form, 'post': post, 'is_edit': True}
    return render(request, 'posts/create_post.html', context)
