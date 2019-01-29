from flask import Flask, request, send_from_directory
from api import PaySimpleAPI
import json
import settings

app = Flask(__name__, static_url_path='')
api = PaySimpleAPI(settings.PAYSIMPLE_USERNAME,settings.PAYSIMPLE_API_KEY,sandbox=True)

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route('/api/token/',methods=['POST'])
def token():
    return json.dumps(api.create_customer_token(settings.CUSTOMER_ID))