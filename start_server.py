#!/usr/bin/env python

import sys, getopt
from bottle import Bottle, route, get, post, request, response, run, static_file

# allow cross-origin resource sharing
class CORS(object):
    name = 'CORS'
    api = 2
    def apply(self, fn, context):
        def _cors(*args, **kwargs):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
            if request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)
        return _cors

app = Bottle()

@app.route('/', method=['OPTIONS', 'GET'])
def hello():
    return "Hello SimScale! This is a tiny REST file server :)\n"

def static_file_crossdomain(*args, **kwargs):
    response = static_file(*args, **kwargs)
    response.set_header('Access-Control-allow-Origin', '*')
    return response

@app.route('/data/geometry/<filename:re:.*>', method=['OPTIONS', 'GET'])
def send_file(filename):
    if "" != filename:
        return static_file_crossdomain(filename, root='/data/geometry')
    else:
        return { "success" : False, "error" : "Requested geometry called without a filename" }

@app.route('/geometries', method=['OPTIONS', 'GET'])
def geometries_list(filename):
    geometry_paths = []
    geometry_files = os.listdir( '/data/geometry' )
    for geometry_file in geometry_files:
        if ".ply" == os.path.splitext( geometry_file )[1]:
            geometry_paths.append( geometry_file )
    return { "success" : True, "paths" : geometry_paths }

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

    app.install(CORS())

    print "HTTP Bottle Server running on port: "+str(m_port)
    run(app, host='0.0.0.0', port=m_port)

if __name__ == "__main__":
    main(sys.argv[1:])
