from behave import *
import requests
import json
import Card

url = 'http://pcms.game-host.org:8543/'
deckname = 'decks/tdn'

post_req = requests.post(url+deckname)
get_req = requests.get(url+deckname+'/cards/6')
deck_info = json.loads(get_req.text) # takes the json string and converts it into a python DS
delete_req = requests.delete(url+deckname)

@given('I have a dictionary of card rank and suit')
def step_impl(context):
    requests.post(url + deckname)
    context.response = requests.get(url + deckname + '/cards/1')
    card_dict = json.loads(context.response.text)  # list of dictionaries
    requests.delete(url + deckname)
    print("\ndeleted deck, test finished")

    assert card_dict

@then('I can create a card')
def step_impl(context):
    card_dict = json.loads(context.response.text)
    card = Card.make_card(card_dict[0])
    card.print_card()

    assert card.rank
    assert card.suit


