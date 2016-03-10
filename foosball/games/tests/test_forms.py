# -*- coding: utf-8 -*-
import pytest
from django.utils.translation import ugettext_lazy as _

from foosball.games.forms import GameForm


@pytest.fixture
def four_users(user_factory):
    return user_factory.create_batch(4)


@pytest.fixture
def game_form_data():
    return {
        'form-game-played_at': '2016-03-03 12:00:00',
        'form-team1-players': [1, 2],
        'form-team2-players': [3, 4],
        'form-team1-score': 10,
        'form-team2-score': 0,
    }


@pytest.mark.django_db
def test_game_form_smoke_test(game_form_data, four_users):
    form = GameForm(data=game_form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_game_form_player_limit(game_form_data, four_users):
    game_form_data.update({
        'form-team1-players': [1, 2, 3],
        'form-team2-players': [4]
    })
    form = GameForm(data=game_form_data)
    assert not form.is_valid()
    assert _('Maximum number of players is two.') in form.forms['team1'].errors['players']


@pytest.mark.parametrize('team1, team2', [
    ([1, 2], [1, 2]),
    ([1, 2], [2, 3]),
    ([1], [1, 2]),
    ([1], [1])
])
@pytest.mark.django_db
def test_game_form_overlapping_players(game_form_data, four_users, team1, team2):
    game_form_data.update({
        'form-team1-players': team1,
        'form-team2-players': team2
    })
    form = GameForm(data=game_form_data)
    assert not form.is_valid()
    assert _('Teams contain same players.') in form.forms['team1'].errors['players']
