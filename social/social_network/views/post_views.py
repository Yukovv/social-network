from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView

from social_network.forms import PostCreationForm
from social_network.models import Post


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a post.
    """
    model = Post
    form_class = PostCreationForm
    template_name = "social_network/post_creation.html"

    def get_success_url(self):
        return reverse("social_network:profile", kwargs={"pk": self.request.user.pk})

    def form_valid(self, form):
        self.object: Post = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class PostDeleteView(UserPassesTestMixin, DeleteView):
    """
    View to delete a post.
    """
    queryset = Post.objects.select_related("user")
    template_name = "social_network/post_confirm_delete.html"

    def test_func(self):
        post = Post.objects.get(pk=self.kwargs["pk"])
        return post.user.pk == self.request.user.pk

    def get_success_url(self):
        return reverse("social_network:profile", kwargs={"pk": self.request.user.pk})


class LikeView(LoginRequiredMixin, View):
    """
    Add or remove like from post
    """
    def post(self, request: HttpRequest, post_pk):
        post = Post.objects.get(pk=post_pk)

        if request.user not in post.likes.all():
            post.add_like(request.user)
        else:
            post.remove_like(request.user)

        return redirect(request.META.get('HTTP_REFERER') + f"#post_{post_pk}")


class FeedView(LoginRequiredMixin, ListView):
    """
    Friends's posts view
    """
    def get_queryset(self):
        friends = [friend.user for friend in self.request.user.friends.all()]
        queryset = Post.objects.filter(user__in=friends).select_related('user').prefetch_related('likes')
        return queryset

    template_name = 'social_network/feed.html'



