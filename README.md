# PaySimple Bug

## Setup

The python code is not essential to this demo. If you can't get it working, all that is necessary is to serve the code in `/static/` with an end point `/api/token/` which returns the token for the current user (the python code fakes this by hard coding the user id).

Install python3 then run the following:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Edit `main.py` with your `CUSTOMER_ID`, `PAYSIMPLE_USERNAME`, and `PAYSIMPLE_API_KEY`. Then run the following to start a server on localhost:5000

```
FLASK_APP=main.py flask run
```

## Reproduce the bug

Open `http://localhost:5000/static/index.html` in a browser. I believe you can enter anything for first, last, and email, but I pre-filled the values in this demo to expediate testing. For the rest of the field use the following (taken from the paysimple documentation)

*CC Number: 5454 5454 5454 5454

*Expiration: 12/21

*Security Code: 996

*Zip: 12345

For me submitting the above returned error below. Note that if I use the expiration 09/21 the error goes away. It is only the exact expiration in the paysimple documentation that give this error.

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