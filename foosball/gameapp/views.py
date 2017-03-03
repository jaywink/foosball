from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class GameAppView(LoginRequiredMixin, TemplateView):
    template_name = "gameapp/index.html"
