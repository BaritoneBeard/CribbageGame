from behave import *
import requests

@given('The server is running')
def step_impl(context):
    r = requests.get('http://127.0.0.1:5000/')
    context.response = r.status_code

@then('I will be able to connect')
def step_impl(context):
    assert context.response == 200 or context.response == 201

# @then('behave will test it for us!')
# def step_impl(context):
#     assert context.failed is False