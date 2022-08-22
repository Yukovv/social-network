from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import CreateView, DeleteView

from social.social_network.forms import PostCreationForm
from social.social_network.models import Post


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