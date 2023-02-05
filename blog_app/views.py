from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from blog_app.models import Post
from django.utils import timezone

from blog_app.forms import PostForm
from django.contrib.auth.decorators import login_required






from django.views.generic import ListView, DetailView, CreateView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published_at__isnull=False).order_by("-published_at")



class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"



class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published_at__isnull=True).order_by("-published_at")





class PostPublishView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        post.published_at = timezone.now()
        post.save()
        return redirect("post-list")



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "post_create.html"
    success_url = reverse_lazy("draft-list")


    def form_valid(self, form):
        # make logged-in user as a author of the post
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        post.delete()

        return redirect("post-list")



class PostUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = PostForm(instance=post)
        return render(request, "post_create.html", {"form": form})

    def post(seld, request, pk):
        post = Post.objects.get(pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            form.save()
            return redirect("post-list")

"""
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "post_create.html"
    success_url = reverse_lazy("post-list")"""
"""
@login_required
def post_update(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        form.save()
        return redirect("post-list")
    else:
        form = PostForm(instance=post)
        return render(request, "post_create.html", {"form": form})"""