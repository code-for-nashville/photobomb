import datetime
import logging

from flask import Flask, request


app = Flask(__name__)
logger = logging.getLogger(__name__)
MYSTORE = []


@app.route("/", methods=['GET', 'POST'])
def hello():
    logger.debug('Request keys: '.format(request.values.keys()))
    from_number = request.values.get('From', None)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    media_url = request.values.get('MediaUrl')
    msg = '[{}] {} sent {}'.format(timestamp, from_number, media_url or '<nothing>')
    MYSTORE.append(msg)
    return u'<br>'.join(MYSTORE)

if __name__ == "__main__":
    app.run(debug=True)
