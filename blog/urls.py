from django.urls import path

from blog.views import index, PostDetailView, post_create_view

urlpatterns = [
    path("", index, name="index"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/comment/create/", post_create_view, name="comment-create"),
]

app_name = "blog"
