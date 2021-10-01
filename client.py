import os  # is this included in base python? attempting to install throws error
import requests
import logging

logger = logging.getLogger("client.py")
logging.basicConfig(filename="clientlog.txt")
# logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)

def main():
    os.environ['NO_PROXY'] = '127.0.0.1'  # disable proxy or else request cannot find localhost
    parameters = {'data':"buy a new computer"}

    logger.info("attempting to connect with server . . .")
    try:
        r = requests.get('http://127.0.0.1:5000')  # /test1', data = parameters)
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
    print(r.status_code)

if __name__ == '__main__':
    main()
