# from .commonsteps import server_running
import requests
import json
from behave import *

url = 'http://127.0.0.1:5000'

@given('I can create my hand')
def step_impl(context):
    # data for the hand
    cards = ["AC", "7D", "KH", "9S"]
    hand = { 'data':json.dumps(cards) }
    r = requests.post(url + '/hand', data= hand)
    context.response = r.status_code
    assert context.response == 201

@then('I can see my hand')
def step_impl(context):
    r = requests.get(url + '/hand')
    hand = json.loads(r.text)
    hand = hand['hand']
    hand = hand.replace('"', '')
    hand = hand.replace('[', '')
    hand = hand.replace(']', '')
    hand = list(hand.split(","))
    hand = [hand.strip(' ') for hand in hand]
    print(hand[3])
    assert hand is not None
    assert hand[0] == "AC"
    assert hand[3] == "9S"