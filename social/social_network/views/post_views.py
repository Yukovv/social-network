from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView

from social_network.forms import PostCreationForm, CommentForm
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

    # user can delete only their own posts
    def test_func(self):
        post: Post = Post.objects.get(pk=self.kwargs["pk"])
        return post.user.pk == self.request.user.pk

    def get_success_url(self):
        return reverse("social_network:profile", kwargs={"pk": self.request.user.pk})


class LikeView(LoginRequiredMixin, View):
    """
    Add or remove like from post
    """
    def post(self, request: HttpRequest, post_pk):
        post: Post = Post.objects.get(pk=post_pk)

        if request.user not in post.likes.all():
            post.add_like(request.user)
        else:
            post.remove_like(request.user)

        url = reverse("social_network:profile", kwargs={"pk": self.request.user.pk})
        HTTP_REFERER = request.META.get('HTTP_REFERER')
        if HTTP_REFERER:
            url = HTTP_REFERER + f"#post_{post_pk}"

        return redirect(url)


class FeedView(UserPassesTestMixin, ListView):
    """
    Friends posts view
    """
    template_name = 'social_network/feed.html'

    def get_queryset(self):
        friends = [friend.user for friend in self.request.user.friends.all()]
        queryset = Post.objects.filter(user__in=friends).select_related('user').prefetch_related('likes')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        context["form"] = form
        return context

    def test_func(self):
        return f"/feed/{self.request.user.pk}/" in self.request.path


class CommentView(LoginRequiredMixin, View):
    """
    View to add comment.
    """
    def post(self, request: HttpRequest, post_pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = self.request.user
            comment.post = post
            comment.save()

        url = reverse("social_network:profile", kwargs={"pk": self.request.user.pk})
        HTTP_REFERER = request.META.get('HTTP_REFERER')
        if HTTP_REFERER:
            url = HTTP_REFERER + f"#post_{post_pk}"

        return redirect(url)
