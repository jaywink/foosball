import datetime

import factory
import factory.fuzzy

import pytz

from foosball.users.tests.factories import UserFactory


class TeamFactory(factory.django.DjangoModelFactory):
    score = factory.fuzzy.FuzzyInteger(10)

    @factory.post_generation
    def players(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(group)
            return

        self.players.add(UserFactory())
        self.players.add(UserFactory())

    class Meta:
        model = 'games.Team'


class GameFactory(factory.django.DjangoModelFactory):
    played_at = factory.fuzzy.FuzzyDateTime(
        datetime.datetime.utcnow().replace(tzinfo=pytz.utc) - datetime.timedelta(weeks=8))

    membership1 = factory.RelatedFactory(TeamFactory, 'game')
    membership2 = factory.RelatedFactory(TeamFactory, 'game')

    class Meta:
        model = 'games.Game'
