from behave import *
import Card
import Hand
import io
import sys

card = Card.Card(7, "Diamonds")
card2 = Card.Card(8, "Club")
card3 = Card.Card(13, "Diamonds")
card_list = [card,card2]
p1_hand = Hand.Hand(card_list=card_list)

@given('I have a hand object')
def step_impl(context):
    assert p1_hand

@then('I can put cards in my hand')
def step_impl(context):
    assert len(p1_hand.card_list) == 2
    p1_hand.add_card(card3)
    assert len(p1_hand.card_list) == 3

@step('remove cards from my hand')
def step_impl(context):
    p1_hand.remove_card(card2)
    assert card2 not in p1_hand.card_list
    assert len(p1_hand.card_list) == 2



