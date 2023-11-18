from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostCommentForm, UploadPostForm
from posts.models import Tag
from users.models import Follow
from django.core.serializers import serialize
import json
from posts.models import Post, Comment
from django.db.models import Q, Prefetch
from django.views import View

# Create your views here.

class UploadPostView(LoginRequiredMixin, CreateView):
    form_class = UploadPostForm
    template_name = "mainapp/home.html"
    success_url = "/"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()

        tags = form.cleaned_data["tags"].split(",")
        for tag in tags:
            try:
                tag_instance = Tag.objects.create(
                    title=tag
                )
            except Exception as e:
                tag_instance = Tag.objects.get(title=tag.lower())
            instance.tags.add(tag_instance)
        return super().form_valid(form)
    

class ListPosts(LoginRequiredMixin, ListView):
    paginate_by = 1

    def get_queryset(self) -> QuerySet[Any]:
        posts = Post.objects.filter(user__username=self.kwargs["username"])
        return posts

    def get(self, request, *args, **kwargs):
        user_followee = Follow.objects.filter(follower=request.user, followee__username=kwargs["username"])
        if request.user.username != kwargs["username"] and user_followee.exists() is False:
            return HttpResponse("404 not found")
        response = super().get(request, *args, **kwargs)
        posts_serialized = serialize("json", response.context_data["object_list"], fields=("image"))

        page_obj = response.context_data["page_obj"]

        # previous
        if page_obj.has_previous():
            previous = page_obj.previous_page_number()
        
        else:
            previous = ""

        # next
        if page_obj.has_next():
            next = page_obj.next_page_number()

        else:
            next = ""

        return JsonResponse({
            "status": "success",
            "message": "",
            "payload": {
                "count": page_obj.paginator.count,
                "previous": previous,
                "next": next,
                "results": json.loads(posts_serialized)
            }
        })


class PostDetail(LoginRequiredMixin, DetailView):
    queryset = Post.objects.all()
    template_name = "posts/post_detail.html"

    def get_object(self, queryset = None):
        post = self.queryset.filter(
            (Q(user__followers__follower=self.request.user) | Q(user=self.request.user)),
            uuid=self.kwargs["uuid"]
        ).select_related("user", "user__profile").prefetch_related(Prefetch("comments", queryset=Comment.objects.order_by("-created_at").select_related("user", "user__profile")), Prefetch("comments__replies", queryset=Comment.objects.order_by("-created_at").select_related("user", "user__profile"))).distinct().first()
        if post is None:
            raise Http404("Not Foun")
        return post
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        response = super().get(request, *args, **kwargs)
        print(response.context_data)
        return response
    

class PostCommentView(LoginRequiredMixin, View):
    form_class = PostCommentForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid() is False:
            return JsonResponse({
                "status": "error",
                "message": "Some error occurred",
                "payload": {
                    "errors": form.errors
                }
            })
        post_uuid = kwargs["uuid"]
        post = Post.objects.filter(
            (Q(user__followers__follower=self.request.user) | Q(user=self.request.user)),
            uuid=self.kwargs["uuid"]
        ).distinct().first()
        if post is None:
            raise Http404("Not Found")
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            detail=form.cleaned_data["comment_detail"]
        )
        payload = {
            "user": comment.user.username,
            "profile_img": comment.user.profile.profile_img.url,
            "comment_id": comment.id,
            "comment_detail": comment.detail
        }
        return JsonResponse({
            "status": "success",
            "message": "Success",
            "payload": payload
        })


