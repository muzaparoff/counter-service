import flask
from gevent.pywsgi import WSGIServer

app = flask.Flask(__name__)

counter = 0

@app.route("/")
def index():
    global counter
    counter += 1
    return str(counter)

@app.route("/post", methods=["POST"])
def post():
    global counter
    counter += 1
    return "OK"

if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', 80), app)
    http_server.serve_forever()