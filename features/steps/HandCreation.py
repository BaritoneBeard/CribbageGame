from behave import *
import Card
import Hand
import io
import sys

card = Card.Card(7, "Diamonds")
card2 = Card.Card(8, "Club")
card3 = Card.Card(13, "Diamonds")
card_list = [card,card2]
p1_hand = Hand.Hand(card_list)

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

@step('I can view my hand')
def step_impl(context):     # Admittedly this is a silly thing to test, so I just had fun with it instead of deleting.
    capture = io.StringIO()  # Create StringIO object
    sys.stdout = capture  # and redirect stdout.
    p1_hand.display_hand()
    sys.stdout = sys.__stdout__
    assert capture == p1_hand.display_hand()



