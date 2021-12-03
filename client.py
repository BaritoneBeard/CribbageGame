import os  # is this included in base python? attempting to install throws error
import requests
import logging
import json

logger = logging.getLogger("client.py")
logging.basicConfig(filename="clientlog.txt")
# logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)

url = 'http://127.0.0.1:5000'

'''
def main():
    os.environ['NO_PROXY'] = '127.0.0.1'  # disable proxy or else request cannot find localhost

    # data for the hand
    # DEPRECATED : still here because it's data that gets sent
    cards = ["AC", "7D", "KH", "9S"]
    hand = { 'data':json.dumps(cards) }

    #parameters = {'data':"buy a new computer"}

    logger.info("attempting to connect with server . . .")
    try:
        r = requests.get(url + '/hand')
        logger.info("Successfully posted data to server")

    except ConnectionError:
        print("The server you are trying to reach is down. Try again later.")
        r = 500
        logger.error("Connection Error")
    except TypeError:
        print("Given parameters cannot be requested")
        r = 404
        logger.error("Type Error")
    except:
        print("Something went wrong")
        r = 500
        logger.error("Connection failed due to some unexpected error")

    print(r)
    print(r.text)
    print(r.status_code)
    
'''

def test_game_resource_post(game_ID):
    URL = url + '/games/' + str(game_ID)
    DATA = {'game_ID': game_ID}
    post_request = requests.post(url=URL, data=DATA)
    print(post_request.text)



test_game_resource_post(1234)

# if __name__ == '__main__':
#     #test_game_resource_post()
#     main()
