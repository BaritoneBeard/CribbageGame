from behave import *
from scoring import calc_15

@given('I have a list of card ranks')
def step_impl(context):
    card_ranks = [4, 5, 5, 6, 10]
    assert len(card_ranks) != 0, "the list is non empty"

@then('I can tally how many combinations total fifteen')
def step_impl(context):
    card_ranks = [4, 5, 5, 6, 10]
    assert calc_15(card_ranks) == 4     # 4,5,6 is 15, 5,10 is 15, that's it: 2+2 points = 4 points.
    card_ranks = [3,5,7,9,11]
    assert calc_15(card_ranks) == 2     # 3,5,7 = 15. That's it. 2 points.
    card_ranks = []
    assert calc_15(card_ranks) == 0     # no cards, returns 0. May need some error handling in-function
