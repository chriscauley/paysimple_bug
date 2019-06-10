function loadPaysimpleJs(token) {
  window.PS = window.paysimpleJs({
    // the element that will contain the iframe
    container: document.querySelector('#psjs'),
    // checkout_token is in auth
    auth: {token: token},
    // customized styles are optional
    styles: {
      body: {
        // set the background color of the payment page
        backgroundColor: '#f9f9f9'
      }
    }
  });
  PS.send.setMode('ach-key-enter');
  PS.on('accountRetrieved', result => {
    alert("SUCCESS: \n"+JSON.stringify(result,null,4))
  })
  PS.on('httpError', error => {
    alert('ERROR:'+error.errors[0].message)
  })
};

function getAuth(callback) {
  var xhr = new XMLHttpRequest();
  // change to address of the endpoint you created in step 2
  xhr.open('POST', '/api/token/');
  xhr.onload = function (e) {
    if (xhr.status < 300) {
      var data = JSON.parse(this.response);
      callback.call(null,data.JwtToken)
      return;
    }

    alert('Failed to get Auth Token: (' + xhr.status + ') '
          + xhr.responseText);
  }
  xhr.send();
}

getAuth(loadPaysimpleJs);

function onSubmit(event) {
  // Prevent the default submit behavior of the form
  event.preventDefault();

  // Request the PaySimpleJS SDK to add a new cc or ach account for the
  // customer which the server generated the customer token was granted
  const getValue = id => document.getElementById(id).value
  const formData = {
    firstName: getValue("firstName"),
    lastName: getValue("lastName"),
    email: getValue("email"),
  }
  PS.send.retrieveAccount(formData)
}

document.getElementById("submit").addEventListener("click",onSubmit)