/* eslint-disable no-unused-vars */

var idToken = null;

// [START load_auth_library]
function loadAuthClient () {
  initGoogleAuth();
}
// [END load_auth_library]

// [START init_google_auth]
function initGoogleAuth (clientId = 'Replace Client ID') {
  google.accounts.id.initialize({
    client_id: clientId,
    callback: handleCredentialResponse
  });

  google.accounts.id.renderButton(
    document.getElementById('google-sign-in'),
    { theme: 'outline', size: 'large', text: 'signin', width: 120 }
  );
}
// [END init_google_auth]

// [START user_signin]
function signIn () {
}
// [END user_signin]

function handleCredentialResponse (response) {
  idToken = response.credential;

  document.getElementById('google-sign-in').hidden = true;
  document.getElementById('sign-out-btn').hidden = false;
  document.getElementById('send-api-btn').disabled = false;
}

function apiGatewayRequest(projectId = 'Replace Project Id') {
  if (!idToken) {
    window.alert('Sign in before calling the API.');
    return;
  }
  
  //Replace API Gateway host url below, keep https:// and getUser as is.
  var endpoint = `https://<api_gateway_host>/getUser`;  

  var xhr = new XMLHttpRequest();
  xhr.open('GET', endpoint + '?access_token=' + encodeURIComponent(idToken));

  xhr.onreadystatechange = function () {
    if (this.readyState === XMLHttpRequest.DONE) {
      if (this.status === 200) {
        window.alert(xhr.responseText);
      } else {
        window.alert(`API request failed (${this.status}): ${xhr.responseText}`);
      }
    }
  }
  xhr.send();
}
// [END send_sample_request]

// [START user_signout]
function signOut () {
  idToken = null;
  google.accounts.id.disableAutoSelect();

  document.getElementById('google-sign-in').hidden = false;
  document.getElementById('sign-out-btn').hidden = true;
  document.getElementById('send-api-btn').disabled = true;
}
// [END user_signout]
