import logging
import json

from flask import Flask, request


app = Flask(__name__)
logger = logging.getLogger(__name__)
MYSTORE = []


@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        num_media = int(request.values.get('NumMedia', 0))
        data = {
            'phone_number': request.values.get('From'),
            'urls': [request.values.get('MediaUrl{}'.format(d)) for d in range(num_media)]
        }
        MYSTORE.append(data)
        return ''
    return json.dumps(MYSTORE)

if __name__ == "__main__":
    app.run(debug=True)
