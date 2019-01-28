import base64
import datetime
import hashlib
import hmac
import json
import requests


class PaySimpleAPI:
    def __init__(self, username, api_key, sandbox=False):
        self.username = username
        self.api_key = bytes(api_key, "latin-1")
        self.sandbox = sandbox

    @property
    def base_url(self):
        if self.sandbox:
            return "https://sandbox-api.paysimple.com/v4"
        return "https://api.paysimple.com/v4"

    def get_headers(self):
        timestamp = datetime.datetime.utcnow().isoformat()
        _hmac = base64.encodebytes(
            hmac.new(self.api_key, timestamp.encode(), hashlib.sha256).digest()
        ).strip()
        _signature = "PSSERVER accessid={}; timestamp={}; signature={}"
        return {
            "Authorization": _signature.format(
                self.username, timestamp, _hmac.decode("utf-8")
            )
        }

    def _request(self, method, endpoint, **data):
        _method = getattr(requests, method)
        response = _method(
            self.base_url + endpoint, headers=self.get_headers(), json=data
        )
        if response.status_code >= 300:
            text = "about to throw an error.\nurl: {}\ndata:{}\nresponse text:{}\n"
            print(text.format(response.url, data, response.text))
        response.raise_for_status()
        try:
            # delete returns nothing for this
            data = response.json()
        except json.decoder.JSONDecodeError:
            return response.text
        else:
            self._last_metadata = data["Meta"]
            return data["Response"]

    def _get(self, *args, **kwargs):
        return self._request("get", *args, **kwargs)

    def create_customer_token(self, _id):
        """ Make a customer token that can be used to make purchases via javascript """
        return self._get("/customer/{}/token".format(_id))
