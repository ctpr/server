#!/usr/bin/env python

import os, sys, getopt
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
root = "/Users/chris/Documents/Work/SIMSCALE_2017/dev/server/data"

# manually insert cross-origin resource sharing for static file response
def static_file_crossdomain(*args, **kwargs):
    response = static_file(*args, **kwargs)
    response.set_header('Access-Control-allow-Origin', '*')
    return response

# Generic server message
@app.route('/', method=['OPTIONS', 'GET'])
def hello():
    return "You found the data server! Congratulations :)\n" + root

# List all available geometry paths
@app.route('/geometries', method=['OPTIONS', 'GET'])
def geometries_list():
    geometry_paths = []
    geometry_files = os.listdir( root + '/geometry' )
    for geometry_file in geometry_files:
        if ".ply" == os.path.splitext( geometry_file )[1]:
            geometry_paths.append( geometry_file )
    return { "success" : True, "paths" : geometry_paths }

# Return geometry file (or error message)
@app.route('/geometries/<filename:re:.*>', method=['OPTIONS', 'GET'])
def send_file(filename):
    if "" != filename:
        return static_file_crossdomain(filename, root=root + '/geometry')
    else:
        return { "success" : False, "error" : "Requested geometry called without a filename" }

# Help function
def print_help():
    print __file__+' -p --port <port> [9000] -r --root <dir> [/data]'

def main(argv):
    m_port = 9000
    m_root = "/data"
    try:
        opts, args = getopt.getopt(argv,"hpr:",["port=","root="])
    except getopt.GetoptError:
        print_help()
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-p", "--port"):
            m_port = int(arg)
        elif opt in ("-r", "--root"):
            # TODO: fix this
            m_root = arg

    root = m_root
    app.install(CORS())

    print "HTTP Bottle Server running on port: "+str(m_port)
    print "Data expected in: "+root
    run(app, host='0.0.0.0', port=m_port)

if __name__ == "__main__":
    main(sys.argv[1:])
