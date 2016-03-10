from django import forms
from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Game, Team, Table


class TeamForm(forms.ModelForm):
    model = Team

    def has_changed(self):
        # force Teams to be saved also when they aren't modified,
        # prevents Games with less than two Teams
        return True


class TeamInlineFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        teams = []
        for form in self.forms:
            players = form.cleaned_data.get('players')
            if not players:
                continue  # 'This field is required' error is shown here anyway
            if players.count() > 2:
                form.add_error('players', _('Maximum number of players is two.'))
            teams.append(players.all())
        if len(teams) == 2 and not set(teams[0]).isdisjoint(teams[1]):
            self.forms[0].add_error('players', _('Teams contain same players.'))


class TeamInline(admin.TabularInline):
    model = Team
    form = TeamForm
    formset = TeamInlineFormSet
    extra = 2
    max_num = 2

    class Media:
        css = {
            'all': ('css/admin_hide_team_str.css',)
        }

    def has_delete_permission(self, request, obj=None):
        # a Game should always have both teams
        return False


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'played_at', 'table', 'created_by', 'modified_by', 'created', 'modified')
    list_filter = ('table',)
    inlines = (TeamInline,)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.modified_by = request.user
        obj.save()


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
