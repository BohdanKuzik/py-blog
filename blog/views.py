from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic

from blog.forms import CommentForm
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


class PostCreateView(generic.CreateView):
    form_class = CommentForm
    template_name = "blog/post_detail.html"

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['pk'])

        content = form.cleaned_data.get("content")
        if content:
            comment = form.save(commit=False)
            comment.post = post
            comment.user = self.request.user
            comment.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("blog:post-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, id=self.kwargs['pk'])
        return context
