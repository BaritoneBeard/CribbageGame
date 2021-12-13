from behave import *
from scoring import calc_15, calc_pairs, calc_run, calc_flush, nob
import Card

@given('I have a list of card ranks')
def step_impl(context):
    card_ranks = [4, 5, 5, 6, 10]
    assert len(card_ranks) != 0, "the list is non empty"

@then('I can tally how many combinations total fifteen')
def step_impl(context):
    card_ranks = [4, 5, 5, 6, 10]
    assert calc_15(card_ranks) == 4     # 4,5,6 is 15, 5,10 is 15, that's it: 2+2 points = 4 points.
    card_ranks = [3,5,7,9,11]
    assert calc_15(card_ranks) == 4     # 3,5,7 = 15. That's it. 2 points.
    card_ranks = []
    assert calc_15(card_ranks) == 0     # no cards, returns 0. May need some error handling in-function

@step('I can tally how many cards of a kind exist')
def step_impl(context):
    card_list = [4,5]
    assert calc_pairs(card_list) == 0
    card_list = [4, 5, 5]
    assert calc_pairs(card_list) == 2
    card_list = [4, 5, 5, 5]
    assert calc_pairs(card_list) == 6
    card_list = [4, 5, 5, 5, 5]
    assert calc_pairs(card_list) == 12

@step('I can tally how many cards are in a run')
def step_impl(context):
    card_list = [4,5]
    assert calc_run(card_list) == 0
    card_list = [4,5,6]
    assert calc_run(card_list) == 3
    card_list = [4,5,7,8]
    assert calc_run(card_list) == 0

@step('I can determine a flush')
def step_impl(context):
    flipped_suit = Card.Card(7,"Diamonds")
    card_list = ['Diamonds','Diamonds','Diamonds','Diamonds']
    assert calc_flush(card_list, flipped_suit=flipped_suit) == 5
    card_list = ['Hearts','Hearts','Hearts','Hearts']
    assert calc_flush(card_list, flipped_suit) == 4
    card_list = ['Diamonds','Diamonds','Diamonds','Hearts']
    assert calc_flush(card_list, flipped_suit) == 4

@step('I can determine a nob')
def step_impl(context):
    rank_list = [3,5,7,11]
    suit_list = ['Diamonds','Hearts','Spades','Clubs']
    card_list = []
    for i in range(len(rank_list)):
        card = Card.Card(rank_list[i],suit_list[i])
        card_list.append(card)
    flipped_suit = 'Diamonds'                           # Jack of Clubs != <Rank> of Diamonds
    assert nob(rank_list,suit_list,flipped_suit) == 0
    flipped_suit = 'Clubs'                              # Jack of Clubs == <Rank> of Clubs
    assert nob(rank_list,suit_list,flipped_suit) == 1
    rank_list = [3,5,11,7]                              # Jack of Spades != <Rank> of Clubs
    assert nob(rank_list, suit_list, flipped_suit) == 0
