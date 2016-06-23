import re

from foosball.games.utils import random_colour


def test_random_colour():
    assert re.match(r"#[A-Z0-9]{6}", random_colour())
