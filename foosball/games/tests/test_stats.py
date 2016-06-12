from decimal import Decimal

import pytest

from foosball.games.stats import stats_red_or_blue, stats_players
from foosball.games.tests.utils import create_game
from foosball.users.tests.factories import UserFactory


@pytest.mark.django_db
def test_stats_red_or_blue():
    for i in range(3):
        create_game()
    create_game(("BLUE", "RED"))
    stats = stats_red_or_blue(None)
    assert stats["data"]["datasets"][0]["data"] == [3, 1]


@pytest.mark.django_db
def test_stats_players():
    p4 = UserFactory(username="p4")
    p1 = UserFactory(username="p1")
    p3 = UserFactory(username="p3")
    p2 = UserFactory(username="p2")
    for i in range(4):
        create_game(players=([p1, p2], [p3, p4]))
    for i in range(2):
        create_game(players=([p2], [p4]))
        create_game(players=([p3], [p1]))
    stats = stats_players(None)
    assert stats["data"]["labels"] == ("p1", "p2", "p3", "p4")
    assert stats["data"]["datasets"][0]["data"] == (Decimal(0), Decimal(100), Decimal(100), Decimal(0))
    assert stats["data"]["datasets"][1]["data"] == (Decimal(100), Decimal(100), Decimal(0), Decimal(0))


@pytest.mark.django_db
def test_update_player_stats():
    # Doubles
    game, winners, losers = create_game()
    for user in winners.players.all():
        player = user.player
        assert player.singles_wins == 0
        assert player.singles_win_percentage == Decimal(0)
        assert player.doubles_wins == 1
        assert player.doubles_win_percentage == Decimal(100)
        assert player.total_played == 1
        assert player.singles_played == 0
        assert player.doubles_played == 1
    for user in losers.players.all():
        player = user.player
        assert player.singles_wins == 0
        assert player.singles_win_percentage == Decimal(0)
        assert player.doubles_wins == 0
        assert player.doubles_win_percentage == Decimal(0)
        assert player.total_played == 1
        assert player.singles_played == 0
        assert player.doubles_played == 1

    # Singles
    game, winners, losers = create_game(players=([UserFactory()], [UserFactory()]))
    player = winners.players.first().player
    assert player.singles_wins == 1
    assert player.singles_win_percentage == Decimal(100)
    assert player.doubles_wins == 0
    assert player.doubles_win_percentage == Decimal(0)
    assert player.total_played == 1
    assert player.singles_played == 1
    assert player.doubles_played == 0
    player = losers.players.first().player
    assert player.singles_wins == 0
    assert player.singles_win_percentage == Decimal(0)
    assert player.doubles_wins == 0
    assert player.doubles_win_percentage == Decimal(0)
    assert player.total_played == 1
    assert player.singles_played == 1
    assert player.doubles_played == 0
