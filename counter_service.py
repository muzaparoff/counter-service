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

@app.route("/health", methods=["GET"])
def health_check():
    # Add health check logic here
    # You can perform any checks you need and return an appropriate response
    # For simplicity, we'll just return a basic "OK" response.
    return "OK"

if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', 80), app)
    http_server.serve_forever()