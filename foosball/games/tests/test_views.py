import pytest
from django.core.urlresolvers import reverse

from foosball.games.tests.factories import GameFactory
from foosball.games.tests.utils import handle_login


@pytest.mark.django_db
@pytest.mark.client
def test_game_list_view_renders(client):
    handle_login(client)
    response = client.get(reverse("games:index"))
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.client
def test_game_detail_view_renders(client):
    handle_login(client)
    game = GameFactory()
    response = client.get(reverse("games:detail", kwargs={"pk": game.id}))
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.client
def test_game_create_view_renders(client):
    handle_login(client)
    response = client.get(reverse("games:new"))
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.client
def test_stats_view_renders(client):
    handle_login(client)
    response = client.get("%s?statistic=red_or_blue" % reverse("games:stats"))
    assert response.status_code == 200
    response = client.get("%s?statistic=players" % reverse("games:stats"))
    assert response.status_code == 200
