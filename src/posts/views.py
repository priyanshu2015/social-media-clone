from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UploadPostForm
from posts.models import Tag

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