from django import forms
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import ModelSelect2MultipleWidget
from django_superform import ModelFormField, SuperForm

from foosball.users.models import User
from .models import Team, Game
from .utils import clean_team_forms


class MultiPlayerWidget(ModelSelect2MultipleWidget):
    model = User
    search_fields = [
        'username__icontains',
        'first_name__icontains',
        'last_name__icontains',
        'email__icontains',
    ]

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super().build_attrs(extra_attrs=extra_attrs, **kwargs)
        attrs['data-maximum-selection-length'] = 2
        return attrs

    def label_from_instance(self, obj):
        return " - ".join(filter(None, [obj.username, obj.name]))


class TeamModelForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('score', 'players')
        widgets = {
            'players': MultiPlayerWidget,
            'score': forms.Select(choices=((i, i) for i in range(11)))
        }

        labels = {
            "score": _("Score"),
            "players": _("Players")
        }


class GameModelForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('played_at', 'table')


class GameForm(SuperForm):
    game = ModelFormField(GameModelForm)
    team1 = ModelFormField(TeamModelForm)
    team2 = ModelFormField(TeamModelForm)

    def is_valid(self):
        return super().is_valid() & clean_team_forms(self.forms['team1'], self.forms['team2'])
