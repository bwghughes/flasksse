import redis
from flask import Flask, render_template, Response

app = Flask(__name__)
r = redis.Redis()


@app.route('/')
def index():
    return render_template('index.html')


def event_stream():
    pubsub = r.pubsub()
    pubsub.subscribe('build:events:*')
    for message in pubsub.listen():
        yield 'data: %s\n\n' % message['data']


@app.route('/stream')
def stream():
    return Response(event_stream(),
                    mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True)
