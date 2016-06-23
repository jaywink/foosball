# -*- coding: utf-8 -*-
import random

from django.utils.translation import ugettext as _


def clean_team_forms(team_form_1, team_form_2):
    """
    Extra validation for Team forms.

    Checks max number of players and that a player can only play in one team.
    Adds error messages to the forms. Returns info whether all the extra
    validations are valid.

    :type team_form_1: TeamModelForm
    :type team_form_2: TeamModelForm
    :rtype: bool
    """
    teams = [list(), list()]
    valid = True

    for i, form in enumerate((team_form_1, team_form_2)):
        players = form.cleaned_data.get('players')
        if not players:
            continue  # 'This field is required' error is shown here
        if players.count() > 2:
            form.add_error('players', _('Maximum number of players is two.'))
            valid = False
        teams[i] = list(players.all())

    if len(set(teams[0]).union(teams[1])) != len(teams[0] + teams[1]):
        for form in (team_form_1, team_form_2):
            form.add_error('players', _('Teams contain same players.'))
        valid = False

    return valid


def random_colour():
    """Generate random colour.

    Thanks: http://stackoverflow.com/a/14019260/1489738
    """
    r = lambda: random.randint(0, 255)
    return '#%02X%02X%02X' % (r(), r(), r())
