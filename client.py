import os  # is this included in base python? attempting to install throws error
import requests

def main():
    os.environ['NO_PROXY'] = '127.0.0.1'  # disable proxy or else request cannot find localhost
    r = requests.get('http://127.0.0.1:5000')

    # when server is up, returns 200
    print(r)


if __name__ == '__main__':
    main()