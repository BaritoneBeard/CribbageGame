import requests
import json
from behave import *


url = 'http://pcms.game-host.org:8543/'
deckname = 'decks/tdn'


@given('The server is up')
def step_impl(context):
    # Just a health check
    r = requests.get(url + 'health/')
    print(r.status_code)
    assert r.status_code == 200

@then('I can create a deck')
def step_impl(context):
    r = requests.post(url + deckname)
    # context.response = r.status_code
    print(r.status_code)
    assert r.status_code == 201

#http://pcms.game-host.org:8543/decks/some_deck_name/cards/1
@step('I can draw from the deck')
def step_impl(context):
    r = requests.get(url + deckname + '/cards/1')

@step('I can delete the deck')
def step_impl(context):
    r = requests.delete(url + deckname)



