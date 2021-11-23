# from .commonsteps import server_running
import requests
from behave import *

url = 'http://127.0.01:5000/'

@given('The server is running')
def step_impl(context):
    r = requests.get(url)
    context.response = r.status_code

@then('I will be able to connect')
def step_impl(context):
    assert context.response == 200

@step("I will be able to give a pathway and data")
def step_impl(context):
    r = requests.post(url + 'comp', data={'data': "buy a new computer"})
    assert r.status_code == 201


@step("I will be able to update existing data")
def step_impl(context):
    r = requests.put(url + 'test1', data={'data': "buy a new computer"})
    assert r.status_code == 200


@step("I will be able to delete existing data")
def step_impl(context):
    r = requests.delete(url + 'test1')
    assert r.text == 'null\n'
    assert r.status_code == 200