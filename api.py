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

    def match_account(self, customer_id, account_id):
        account_sets = self.list_customer_accounts(customer_id)
        for _type, accounts in account_sets.items():
            for account in accounts:
                if str(account["Id"]) == str(account_id):
                    account["_type"] = _type
                    return account
        # e.g. the user tried use an account they don't own
        m = "An error occurred when trying to access this account."
        m += " Please try again or contact the staff."
        raise ValueError(m)

    def _get(self, *args, **kwargs):
        return self._request("get", *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._request("post", *args, **kwargs)

    def _put(self, *args, **kwargs):
        return self._request("put", *args, **kwargs)

    def _delete(self, *args, **kwargs):
        return self._request("delete", *args, **kwargs)

    def create_customer_token(self, _id):
        """ Make a customer token that can be used to make purchases via javascript """
        return self._get("/customer/{}/token".format(_id))

    def new_customer(self, first_name, last_name, **kwargs):
        kwargs["FirstName"] = first_name
        kwargs["LastName"] = last_name
        return self._post("/customer", **kwargs)

    def list_customers(self):
        return self._get("/customer")

    def delete_customer(self, _id):
        return self._delete("/customer/{}".format(_id))

    def list_customer_accounts(self, _id):
        return self._get("/customer/{}/accounts".format(_id))

    def delete_credit_card(self, _id):
        return self._delete("/account/creditcard/{}".format(_id))

    def delete_ach(self, _id):
        return self._delete("/account/ach/{}".format(_id))

    def new_payment(self, **kwargs):
        return self._post("/payment", **kwargs)

    def get_payment(self, _id):
        return self._get("/payment/{}".format(_id))

    def list_payments(self):
        return self._get("/payment")

    def get_recurring_payment(self, _id):
        return self._get("/recurringpayment/{}".format(_id))
