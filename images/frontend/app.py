from flask import Flask, abort
from socket import gethostname
import math
import redis
import os

my_hostname = gethostname()
redis_host = os.environ['REDIS_HOST']

# Build a connection to Redis
my_redis = redis.Redis(host=redis_host, port=6379, decode_responses=True)


# Some stock code to calculate pi for load gen
def calcPi(limit):  # Generator function
    """
    Prints out the digits of PI
    until it reaches the given limit
    """

    q, r, t, k, n, l = 1, 0, 1, 1, 3, 3

    decimal = limit
    counter = 0

    while counter != decimal + 1:
            if 4 * q + r - t < n * t:
                    # yield digit
                    yield n
                    # insert period after first digit
                    if counter == 0:
                            yield '.'
                    # end
                    if decimal == counter:
                            print('')
                            break
                    counter += 1
                    nr = 10 * (r - n * t)
                    n = ((10 * (3 * q + r)) // t) - 10 * n
                    q *= 10
                    r = nr
            else:
                    nr = (2 * q + r) * l
                    nn = (q * (7 * k) + 2 + (r * l)) // (t * l)
                    q *= k
                    t *= l
                    l += 2
                    k += 1
                    n = nn
                    r = nr
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from k8s: ' + my_hostname + '\n'

@app.route('/healthz')
def health():
    return "alive"

@app.route('/nhealthz')
def unhealth():
    abort(500)

@app.route('/load')
def load():
    pi = calcPi(50)
    pi = ''.join(map(str, pi)) + '\n'
    return pi

@app.route('/<key>/<value>')
def set_value(key, value):
    my_redis.set(key, value)
    print('storing value: ' + value + ' for key: ' + key + '\n')
    return key + ":" + value + "\n"

@app.route('/<key>')
def get_value(key):
    value=''
    print('retreiving value for key: ' + key + '\n')
    value=my_redis.get(key)
    if value is None:
        abort(404)
    print('got value: ' + value + '\n')
    return value
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',threaded=True)
