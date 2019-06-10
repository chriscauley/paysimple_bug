# PaySimple Bug

This is a minimum sample of code for reproducing my bug. The bug is that we can't add the same account for two different customers. It works for the first customer but the second returns a message `"Current user does not have enough rights to execute this operation."`

## Setup

The python code is not essential to this demo. If you can't get it working, all that is necessary is to serve the code in `/static/` with an end point `/api/token/` which returns the token for the current user (the python code fakes this by hard coding the user id).

Install python3 then run the following:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `settings.template.py` to `settings.py` and edit `CUSTOMER_ID`, `PAYSIMPLE_USERNAME`, and `PAYSIMPLE_API_KEY`. Then run the following to start a server on localhost:5000

```
FLASK_APP=main.py flask run
```

## Reproduce the bug

Open `http://localhost:5000/static/index.html` in a browser. Fill in first, last and email (I think these can be anything). Using the values provided it should work for the first customer. Afterwards go into the settings, change CUSTOMER_ID to another ID, restart the server, and then re-enter the same routing number, account number, bank name, and account type.

On the second try you should be alerted with the appropriate error message. The full response body was:

```
{
    "Meta": {
        "Errors": {
            "ErrorCode": "InvalidInput",
            "ErrorMessages": [
                {
                    "Message": "Current user does not have enough rights to execute this operation."
                }
            ]
        },
        "HttpStatus": "BadRequest",
        "HttpStatusCode": 400,
        "PagingDetails": null
    },
    "Response": null
}
```