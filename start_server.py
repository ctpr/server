#!/usr/bin/env python

from bottle import route, run

@route('/')
def hello():
    return "Hello SimScale! This is a tiny REST file server :)\n"

@route('/geometry/<filename:re:.*\.ply>', method='GET')
def send_ply(filename):
    if "" == filename:
        return { "success" : False, "error" : "Requested PLY geometry called without a filename" }
    return static_file(filename, root='/data/geometry')

run(host='0.0.0.0', port=9000)
