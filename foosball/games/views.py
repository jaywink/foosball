import inspect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, FormView, View

from foosball.games import stats
from foosball.games.forms import GameForm
from foosball.games.stats import update_player_stats
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
        update_player_stats(team)
        return team


class StatsView(LoginRequiredMixin, View):
    """
    Given a `statistic` parameter, calls the stats function and returns the JSON configuration for Charts.js.
    """
    def get(self, request, *args, **kwargs):
        """Using given `statistic`, return the result JSON."""
        statistic = request.GET.get("statistic")
        if not statistic:
            return HttpResponseBadRequest()

        # Call the stats function with request.GET parameters
        stats_func = getattr(stats, "stats_%s" % statistic, None)
        if stats_func and inspect.isfunction(stats_func):
            result = stats_func(request.GET)
            return JsonResponse(result)

        return HttpResponseBadRequest()
