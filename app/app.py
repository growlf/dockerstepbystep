#!/usr/bin/python

# Library imports
import time
from flask import Flask
from pathlib import Path


app = Flask(__name__)
START = time.time()
COUNTER_FILE = Path('/var/app_data/counter.txt')


def get_hit_count():
    count = 0
    
    with COUNTER_FILE.open('r') as cf:
        # Read counter from file and increment it
        count = int(cf.readline() or 0)
    
    count += 1
    
    with COUNTER_FILE.open('w') as cf:
        # Write the counter back to file
        cf.write(str(count))

    return count


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

    # Check that the counter file exists or create it
    # if needed.
    COUNTER_FILE.touch()

    # Start the application
    app.run(debug=True, host="0.0.0.0", port=8080)
