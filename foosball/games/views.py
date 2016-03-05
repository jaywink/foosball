from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, FormView

from foosball.games.forms import GameForm
from .models import Game, Team


class GameListView(LoginRequiredMixin, ListView):
    model = Game
    paginate_by = 10
    template_name = "games/game_list.jinja"


class GameDetailView(LoginRequiredMixin, DetailView):
    model = Game
    template_name = "games/game_detail.jinja"


class GameCreateView(LoginRequiredMixin, FormView):
    template_name = "games/game_new.jinja"
    form_class = GameForm
    success_url = reverse_lazy("games:index")

    @transaction.atomic
    def form_valid(self, form):
        game = form.forms['game'].save(commit=False)
        game.created_by = game.modified_by = self.request.user
        game.save()

        self._save_team_score(game, Team.RED, form.forms['team1'])
        self._save_team_score(game, Team.BLUE, form.forms['team2'])

        return redirect(self.get_success_url())

    @staticmethod
    def _save_team_score(game, side, form):
        team = form.save(commit=False)
        team.game = game
        team.side = side
        team.save()
        form.save_m2m()
        return team
