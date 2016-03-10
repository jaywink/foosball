from django import forms
from django.contrib import admin

from .models import Game, Team, Table

from .utils import clean_team_forms


class TeamForm(forms.ModelForm):
    model = Team

    def has_changed(self):
        # force Teams to be saved also when they aren't modified,
        # prevents Games with less than two Teams
        return True


class TeamInlineFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        clean_team_forms(self.forms[0], self.forms[1])


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
