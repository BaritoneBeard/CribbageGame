import os  # is this included in base python? attempting to install throws error
import requests

def main():
    os.environ['NO_PROXY'] = '127.0.0.1'  # disable proxy or else request cannot find localhost
    try:
        r = requests.get('http://127.0.0.1:5000')
    except ConnectionError:
        print("The server you are trying to reach is down. Try again later.")
        r = 500
    except:
        print("Something went wrong")
        r = 500

    # when server is up, returns 200. When down
    print(r)


if __name__ == '__main__':
    main()
