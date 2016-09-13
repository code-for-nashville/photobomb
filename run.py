import json
import os

import dropbox
from flask import Flask, request

app = Flask(__name__)
dbx = dropbox.Dropbox(os.environ.get('DROPBOX_TOKEN'))


@app.route("/", methods=['GET', 'POST'])
def hello():
    """ Handle a Twilio SMS/MMS callback request: https://www.twilio.com/docs/api/twiml/sms/twilio_request

    Request keys: MessageSid, ToZip, SmsSid, NumMedia, NumSegments, ToCountry, ApiVersion, Body, FromCountry, To,
        FromCity, ToState, From, SmsMessageSid, FromZip, FromState, AccountSid, ToCity, SmsStatus,
        MediaContentType{num}, MediaUrl{num} (where 'num' is a zero-based index derived from NumMedia)
    """
    if request.method == 'POST':
        phone_number = request.values.get('From')
        num_media = int(request.values.get('NumMedia', 0))
        uploads = []
        for i in range(num_media):
            media_url = request.values.get('MediaUrl{}'.format(i))
            content_type = request.values.get('MediaContentType{}'.format(i))
            message_id = media_url.rsplit('/', 1)[-1]
            extension = 'jpg'  # TODO: infer from MediaContentType
            upload_path = u'{}/{}.{}'.format(phone_number, message_id, extension)
            # dbx.files_save_url(upload_path, media_url)
            uploads.append({'upload_path': upload_path, 'content_type': content_type})
        # TODO: append metadata of the SMS/MMS to (if it exists - else create) a hidden file
        # TODO: return an HTTP response code and XML
        return json.dumps(uploads)  # temporarily using this to debug the value of MediaContentType
    return ''

if __name__ == "__main__":
    app.run(debug=True)
