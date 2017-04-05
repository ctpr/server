#!/usr/bin/env python

import sys, getopt
from bottle import get, post, request, run, static_file

@get('/')
def hello():
    return "Hello SimScale! This is a tiny REST file server :)\n"

@get('/geometry/<filename:re:.*>')
def send_file(filename):
    if "" != filename:
        return static_file(filename, root='/data/geometry')
    else:
        return { "success" : False, "error" : "Requested geometry called without a filename" }

def main(argv):
    m_port = 9000
    try:
        opts, args = getopt.getopt(argv,"hp:",["port="])
    except getopt.GetoptError:
        print __file__+' -i <inputfile> -o <outputfile>'
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h':
            print __file__+' -p[--port] <port>'
            sys.exit()
        elif opt in ("-p", "--port"):
            m_port = int(arg)

    run(host='0.0.0.0', port=m_port)

if __name__ == "__main__":
    main(sys.argv[1:])
