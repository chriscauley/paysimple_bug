from flask import Flask, request, send_from_directory
from api import PaySimpleAPI
import json

app = Flask(__name__, static_url_path='')

CUSTOMER_ID = 0
PAYSIMPLE_USERNAME=""
PAYSIMPLE_API_KEY=""

api = PaySimpleAPI(PAYSIMPLE_USERNAME,PAYSIMPLE_API_KEY,sandbox=True)

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route('/api/token/',methods=['POST'])
def token():
    return json.dumps(api.create_customer_token(CUSTOMER_ID))