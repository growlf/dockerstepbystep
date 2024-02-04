#!/usr/bin/python

import time
from flask import Flask
import redis


app = Flask(__name__)
START = time.time()
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)
    
    # Redis is meant to be a caching database.  However, we are desiring 
    # immediate results in the filesystem and to keep this demo simple, 
    # so we are using the following command here to force it
    cache.save(True)


def get_get_elapsed():
    running = time.time() - START
    minutes, seconds = divmod(running, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)


@app.route('/')
def root():
    count = get_hit_count()
    elapsed = get_get_elapsed()
    
    return f"Hello World (Python)! (up {elapsed}). This page has been seen {count} times.\n" 


@app.route('/config/')
def config():
    str = []
    str.append(app.config['DEBUG'])
    str.append('port:'+app.config['PORT'])
    str.append('ip_address:'+app.config['IP'])
    return '\t'.join(str)


if __name__ == "__main__":

    # Start the application
    app.run(debug=True, host="0.0.0.0", port=8080)
