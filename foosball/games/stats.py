from foosball.games.models import Game, Team, Player


def update_player_stats(instance):
    """
    Update player win and played counts for players of a Team.

    :param instance: Team that will be used to update players.
    :type instance: Team
    """
    for user in instance.players.all():
        totals = {1: 0, 2: 0}
        wins = {1: 0, 2: 0}
        teams = Team.objects.filter(players__id=user.id).prefetch_related("players")
        for team in teams:
            player_count = len(team.players.all())
            totals[player_count] += 1
            if team.score == 10:
                wins[player_count] += 1
        player, _created = Player.objects.get_or_create(user=user)
        player.singles_wins = wins[1]
        player.doubles_wins = wins[2]
        player.singles_played = totals[1]
        player.doubles_played = totals[2]
        if totals[1]:
            player.singles_win_percentage = round((wins[1]/totals[1])*100, 2)
        else:
            player.singles_win_percentage = 0
        if totals[2]:
            player.doubles_win_percentage = round((wins[2] / totals[2])*100, 2)
        else:
            player.doubles_win_percentage = 0
        player.total_played = totals[1] + totals[2]
        player.save()


def stats_red_or_blue(params):
    """
    Return statistics on the most important question.
    """
    red_wins = Game.objects.filter(teams__side=Team.RED, teams__score=10).count()
    blue_wins = Game.objects.filter(teams__side=Team.BLUE, teams__score=10).count()
    return {
        "type": "pie",
        "data": {
            "labels": [
                "Red",
                "Blue",
            ],
            "datasets": [
                {
                    "data": [red_wins, blue_wins],
                    "backgroundColor": [
                        "#FF6384",
                        "#36A2EB",
                    ],
                }]
        },
        "options": {}
    }


def stats_players(params):
    """
    Return statistics on player singles and doubles win percentages.
    """
    players = Player.objects.filter(total_played__gt=5).order_by("user__username").values_list(
        "user__username", "singles_win_percentage", "doubles_win_percentage"
    )
    if players:
        usernames, singles_win_percentages, doubles_win_percentages = zip(*players)
    else:
        usernames = singles_win_percentages = doubles_win_percentages = []
    return {
        "type": "bar",
        "data": {
            "labels": usernames,
            "datasets": [
                {
                    "label": "Win % - singles",
                    "data": singles_win_percentages,
                    "backgroundColor": "#2E5168",
                },
                {
                    "label": "Win % - doubles",
                    "data": doubles_win_percentages,
                    "backgroundColor": "#65923B",
                },
            ]
        },
        "options": {}
    }
