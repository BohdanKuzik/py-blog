from django.urls import path

from blog.views import index, PostDetailView, PostCreateView

urlpatterns = [
    path("", index, name="index"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/comment/create/", PostCreateView.as_view(), name="comment-create"),
]

app_name = "blog"
