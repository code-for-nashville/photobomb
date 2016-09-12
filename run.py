import logging

from flask import Flask, request


app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello():
    from_number = request.values.get('From', None)

    logger.debug('Request: '.format(request))
    logger.debug('From: '.format(from_number))
    return "Hello {}".format(from_number or 'world!')

if __name__ == "__main__":
    app.run(debug=True)
