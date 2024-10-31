from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from blog.models import Post, Commentary


def index(request):
    post_list = Post.objects.all().order_by("-created_time")

    paginator = Paginator(post_list, 5)
    page_number = request.GET.get("page", 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "post_list": posts,
    }
    return render(request, "blog/index.html", context=context)


class PostDetailView(generic.DetailView):
    model = Post


def post_create_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Commentary.objects.create(post=post, content=content, user=request.user)
    return redirect(reverse("blog:post-detail", kwargs={"pk": pk}))
