import datetime
import logging
import json

from flask import Flask, request


app = Flask(__name__)
logger = logging.getLogger(__name__)
MYSTORE = []


@app.route("/", methods=['GET', 'POST'])
def hello():
    msg = 'Request keys: {}'.format(u', '.join(list(request.values.keys())))
    if request.method == 'POST':
        MYSTORE.append(msg)
    return u'<br>'.join(MYSTORE)

if __name__ == "__main__":
    app.run(debug=True)
