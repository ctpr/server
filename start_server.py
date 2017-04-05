#!/usr/bin/env python

# from bottle import route, run, template, static_file
from bottle import get, post, request, run, static_file


@get('/') # @route('/')
def hello():
    return "Hello SimScale! This is a tiny REST file server :)\n"

@get('/geometry/<filename:re:.*>') # @route('/geometry/<filename:re:.*>', method='GET')
def send_file(filename):
    if "" != filename:
        return static_file(filename, root='/data/geometry')
    else:
        return { "success" : False, "error" : "Requested geometry called without a filename" }

run(host='0.0.0.0', port=9000)
