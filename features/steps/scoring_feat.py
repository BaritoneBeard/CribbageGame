from behave import *
from scoring import calc_15

'''Feature: I can tally up the score of a player's hand.
  Scenario: I can tally up the score of a player's hand
    Given I have a list of card ranks
    Then I can tally how many combinations total fifteen'''

url = 'http://pcms.game-host.org:8543/'
deckname = 'decks/tdn'
card_ranks = [4,5,5,6,10]

@given('I have a list of card ranks')
def step_impl(context):
    assert len(card_ranks) != 0, "the list is non empty"

@then('I can tally how many combinations total fifteen')
def step_impl(context):
    card_ranks = [4, 5, 5, 6, 10]
    assert calc_15(card_ranks) == 4     # 4,5,6 is 15, 5,10 is 15, that's it: 2+2 points = 4 points.
