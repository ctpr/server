#!/usr/bin/env python

import sys, getopt
from bottle import Bottle, get, post, request, response, run, static_file

app = Bottle()

# allow cross-origin resource sharing
@app.hook('after_request')
def cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@app.get('/')
def hello():
    return "Hello SimScale! This is a tiny REST file server :)\n"

@app.get('/geometry/<filename:re:.*>')
def send_file(filename):
    if "" != filename:
        return static_file(filename, root='/data/geometry')
    else:
        return { "success" : False, "error" : "Requested geometry called without a filename" }

def print_help():
    print __file__+' -p --port <port> [9000]'

def main(argv):
    m_port = 9000
    try:
        opts, args = getopt.getopt(argv,"hp:",["port="])
    except getopt.GetoptError:
        print_help()
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-p", "--port"):
            m_port = int(arg)

    print "HTTP Bottle Server running on port: "+str(m_port)
    run(app, host='0.0.0.0', port=m_port)

if __name__ == "__main__":
    main(sys.argv[1:])
