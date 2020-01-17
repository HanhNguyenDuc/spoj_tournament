import requests
import time
import logging



if __name__ == '__main__':
    prev_time = time.time()
    while True:
        if time.time() - prev_time > 300:
            prev_time = time.time()
            r = requests.get("http://spoj-tour.herokuapp.com/update_all_user")