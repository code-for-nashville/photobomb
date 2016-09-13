import os
import mimetypes
from distutils.util import strtobool

import dropbox
from dropbox.files import SaveUrlError, UploadError
from flask import Flask, request
from twilio.rest import Client as TwilioRestClient

app = Flask(__name__)
DROPBOX_TOKEN = os.environ.get('DROPBOX_TOKEN', 'INVALID')
dbx = dropbox.Dropbox(DROPBOX_TOKEN)

CONTENTTYPE_CONFIG = {
    'image/jpeg': '.jpeg'
}
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'INVALID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', 'INVALID')
TWILIO_DELETE_MEDIA = bool(strtobool(os.environ.get('TWILIO_DELETE_MEDIA', 'False')))
TWILIO_DELETE_MESSAGES = bool(strtobool(os.environ.get('TWILIO_DELETE_MESSAGES', 'False')))

twl = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


@app.route("/", methods=['GET', 'POST'])
def handle():
    """ Handle a Twilio SMS/MMS callback request by sending the contents to a Dropbox folder

    For information about the request: https://www.twilio.com/docs/api/twiml/sms/twilio_request
    Note: `MediaContentType{num}` and `MediaUrl{num}` where 'num' is a zero-based index derived from NumMedia
    """
    if request.method == 'POST':
        message_sid = request.form.get('MessageSid')
        phone_number = request.form.get('From')[-10:]  # original is E.164 format: https://en.wikipedia.org/wiki/E.164
        num_media = int(request.form.get('NumMedia', 0))
        for i in range(num_media):
            media_url = request.form.get('MediaUrl{}'.format(i))
            content_type = request.form.get('MediaContentType{}'.format(i))
            extension = CONTENTTYPE_CONFIG.get(content_type, mimetypes.guess_extension(content_type))
            upload_path = '/{}/{}-{}{}'.format(phone_number, message_sid, str(i), extension)
            try:
                dbx.files_save_url(upload_path, media_url)
            except SaveUrlError:
                # TODO: log error
                pass
            else:
                if TWILIO_DELETE_MEDIA is True:
                    medium_sid = media_url.rsplit('/', 1)[-1]
                    media_instance = twl.account.messages(message_sid).media(medium_sid).fetch()
                    media_instance.delete()
        file_contents = '{}\n\n'.format(request.form.get('Body'))
        for k, v in request.form.items():
            if k not in ['Body']:
                file_contents += '{}: {}\n'.format(k, str(v))
        try:
            dbx.files_upload(file_contents, '/{}/{}.txt'.format(phone_number, message_sid))
        except UploadError:
            # TODO: log error
            pass
        else:
            if TWILIO_DELETE_MESSAGES is True:
                message = twl.account.messages(message_sid)
                message.delete()
    # TODO: return an HTTP response code and XML
    return ''

if __name__ == "__main__":
    app.run(debug=True)
