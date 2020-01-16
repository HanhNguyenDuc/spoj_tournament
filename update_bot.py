import requests
import time
import logging


prev_time = time.time()


if __name__ == '__main__':
    while True:
        if time.time() - prev_time > 30:
            prev_time = time.time()
            r = requests.get("http://spoj-tour.herokuapp.com/update_all_user")