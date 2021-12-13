from behave import *
import pegging
from scoring import *
import Card
import Move

rank_list = [3, 5, 7, 11]
suit_list = ['Diamonds', 'Hearts', 'Spades', 'Clubs']
card_list = []
for i in range(len(rank_list)):
    card = Card.Card(rank_list[i], suit_list[i])
    card_list.append(card)

move = Move.Move(1234,player=None,moves_so_far = card_list, move=None)

@given('There is a list of cards')
def step_impl(context):
    assert len(card_list) != 0

@step('The total number of points does not exceed 31')
def step_impl(context):
    assert pegging.detect_illegal_move(move) is False
    nrank_list = [8, 5, 6, 11]
    nsuit_list = ['Diamonds', 'Hearts', 'Spades', 'Clubs']
    ncard_list = []
    for i in range(len(nrank_list)):
        card = Card.Card(nrank_list[i], nsuit_list[i])
        ncard_list.append(card)
    m = Card.Card(7,"Diamonds")
    nmove = Move.Move(1234,player=None, moves_so_far = ncard_list, move = m)
    assert pegging.detect_illegal_move(nmove) is True

@then('I can check if a player added to the pegging')
def step_impl(context):
    nrank_list = [3,4,6]
    nsuit_list = ['Diamonds', 'Hearts', 'Spades']
    ncard_list = []
    for i in range(len(nrank_list)):
        card = Card.Card(nrank_list[i], nsuit_list[i])
        ncard_list.append(card)
    m = Card.Card(7, "Diamonds")
    nmove = Move.Move(1234, player=None, moves_so_far=ncard_list, move=m)
    assert pegging.check_score(nmove, calc_run) == 0    # no change
    assert pegging.check_score(nmove, calc_15) == 0     # no change
    assert pegging.check_score(nmove, calc_pairs) == 0  # no change
    n = Card.Card(5,"Clubs")
    nmove = Move.Move(1234, player=None, moves_so_far=ncard_list, move=n)
    assert pegging.check_score(nmove, calc_run) != 0    # change, points awarded
    assert pegging.check_score(nmove, calc_15) != 0     # change, points awarded
    assert pegging.check_score(nmove, calc_pairs) == 0  # still no pairs

    nrank_list = [3,4,6]
    nsuit_list = ['Diamonds', 'Diamonds', 'Diamonds']
    ncard_list = []
    for i in range(len(nrank_list)):
        card = Card.Card(nrank_list[i], nsuit_list[i])
        ncard_list.append(card)
    m = Card.Card(7, "Diamonds")
    nmove = Move.Move(1234, player=None, moves_so_far=ncard_list, move=m)
    flipped_card = Card.Card(11,"Diamonds")
    assert pegging.check_score(nmove, calc_flush, flipped_card) != 0

