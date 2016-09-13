import os
import mimetypes

import dropbox
from flask import Flask, request

app = Flask(__name__)
dbx = dropbox.Dropbox(os.environ.get('DROPBOX_TOKEN'))

CONTENTTYPE_CONFIG = {
    'image/jpeg': '.jpeg'
}


@app.route("/", methods=['GET', 'POST'])
def handle():
    """ Handle a Twilio SMS/MMS callback request by sending the contents to a Dropbox folder

    For information about the request: https://www.twilio.com/docs/api/twiml/sms/twilio_request
    Note: `MediaContentType{num}` and `MediaUrl{num}` where 'num' is a zero-based index derived from NumMedia
    """
    if request.method == 'POST':
        message_id = request.form.get('MessageSid')
        phone_number = request.form.get('From')[-10:]
        num_media = int(request.form.get('NumMedia', 0))
        for i in range(num_media):
            media_url = request.form.get('MediaUrl{}'.format(i))
            content_type = request.form.get('MediaContentType{}'.format(i))
            extension = CONTENTTYPE_CONFIG.get(content_type, mimetypes.guess_extension(content_type))
            upload_path = '/{}/{}-{}{}'.format(phone_number, message_id, str(i), extension)
            dbx.files_save_url(upload_path, media_url)
        file_contents = ''
        for k, v in request.form.items():
            file_contents += '{}: {}\n'.format(k, str(v))
        dbx.files_upload(file_contents, '/{}/{}.txt'.format(phone_number, message_id))
    # TODO: return an HTTP response code and XML
    return ''

if __name__ == "__main__":
    app.run(debug=True)
