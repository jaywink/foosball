from foosball.games.models import Game, Team
from foosball.games.stats import update_player_stats
from foosball.games.tests.factories import TeamFactory
from foosball.users.tests.factories import UserFactory


def handle_login(client):
    """
    Create user and log the user in.
    """
    user = UserFactory(username="foobar")
    client.force_login(user)


def create_game(winner_loser=("RED", "BLUE"), players=(None, None)):
    """
    Create a game and teams.

    Optionally with given winner/loser sides and players passed in as tuples.
    """
    game = Game.objects.create()
    winners = TeamFactory(score=10, game=game, side=getattr(Team, winner_loser[0]), players=players[0])
    update_player_stats(winners)
    losers = TeamFactory(score=5, game=game, side=getattr(Team, winner_loser[1]), players=players[1])
    update_player_stats(losers)
    return game, winners, losers
