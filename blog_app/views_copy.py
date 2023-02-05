from django.shortcuts import render, redirect
from blog_app.models import Post
from django.utils import timezone

from blog_app.forms import PostForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_at__isnull = False).order_by("-published_at")
    return render(
        request,
        "post_list.html",
        {"posts": posts},
    )


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)

    return render(
        request,
        "post_detail.html",
        {"post": post},
    )

@login_required
def draft_list(request):
    posts = Post.objects.filter(published_at__isnull=True)
    return render(
        request,
        "post_list.html",
        {"posts": posts},
    )
    

@login_required
def post_publish(request, pk):
    post = Post.objects.get(pk=pk)
    post.published_at = timezone.now()
    post.save()
    return redirect("post-list")


@login_required
def post_create(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect("draft-list")
    return render(request, "post_create.html", {"form": form})


@login_required
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()

    return redirect("post-list")


@login_required
def post_update(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        form.save()
        return redirect("post-list")
    else:
        form = PostForm(instance=post)
        return render(request, "post_create.html", {"form": form})