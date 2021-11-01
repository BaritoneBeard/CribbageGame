import os  # is this included in base python? attempting to install throws error
import requests
import logging
import json

logger = logging.getLogger("client.py")
logging.basicConfig(filename="clientlog.txt")
# logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)

def main():
    os.environ['NO_PROXY'] = '127.0.0.1'  # disable proxy or else request cannot find localhost
    url = 'http://127.0.0.1:5000'
    cards = ["AC", "7D", "KH", "9S"]
    # data for the hand
    hand = { 'data':json.dumps(cards) }
    parameters = {'data':"buy a new computer"}

    logger.info("attempting to connect with server . . .")
    try:
        #r = requests.post('http://127.0.0.1:5000/hand')  # {'data': "buy a new computer"})
        r = requests.post(url + '/hand', data= hand)
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

if __name__ == '__main__':
    main()
