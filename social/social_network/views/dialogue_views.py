from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View


from social_network.models import Dialogue as DialogueModel
from social_network.forms import MessageForm


class DialoguesListView(LoginRequiredMixin, View):
    """
    List of users dialogues.
    """
    def get(self, request: HttpRequest, pk):
        dialogues = DialogueModel.objects.filter(members__in=[request.user.pk]).prefetch_related('members')
        context = {
            "user": request.user,
            "dialogues": dialogues,
        }
        return render(request, 'social_network/dialogues.html', context)


class DialogueView(LoginRequiredMixin, View):
    """
    Dialogue view.
    Show previous and send a new messages.
    """
    def get(self, request: HttpRequest, dialogue_pk):
        dialogue = get_object_or_404(DialogueModel.objects.prefetch_related('members'), id=dialogue_pk)
        if request.user not in dialogue.members.all():
            return render(request, "403.html")

        context = {
            "messages": dialogue.message.all(),
            "form": MessageForm()
        }
        return render(request, "social_network/dialogue.html", context)

    def post(self, request: HttpRequest, dialogue_pk):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.dialogue_id = dialogue_pk
            message.user = request.user
            message.save()

        return redirect(reverse("social_network:dialogue", kwargs={"dialogue_pk": dialogue_pk}))
