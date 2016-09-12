import datetime
import logging
import json

from flask import Flask, request


app = Flask(__name__)
logger = logging.getLogger(__name__)
MYSTORE = []


@app.route("/", methods=['GET', 'POST'])
def hello():
    logger.debug('Request :{}'.format(json.dumps(request.values)))
    if request.method == 'POST':
        MYSTORE.append(json.dumps(request.values))
    return u'<br>'.join(MYSTORE)

if __name__ == "__main__":
    app.run(debug=True)
