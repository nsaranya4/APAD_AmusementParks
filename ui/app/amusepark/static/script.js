// This code is written by using SampleProject as reference
window.addEventListener('load', function () {

  var delete_cookie = function(name) {
	document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
  };

  document.getElementById('sign-out').onclick = function () {
    firebase.auth().signOut();
    delete_cookie("funtech_token");
  };
  signbtn = document.getElementById('sign-out-only')
  if (signbtn) {
      document.getElementById('sign-out-only').onclick = function () {
      firebase.auth().signOut();
      delete_cookie("funtech_token");
    };
  }

  var uiConfig = {
    signInSuccessUrl: '/login/app',
    signInOptions: [
      firebase.auth.GoogleAuthProvider.PROVIDER_ID,
      firebase.auth.EmailAuthProvider.PROVIDER_ID,
    ],
    tosUrl: '<your-tos-url>'
  };

  firebase.auth().onAuthStateChanged(function (user) {
    if (user) {
      document.getElementById('sign-out').hidden = false;
      if (document.getElementById('sign-out-only')) {
        document.getElementById('sign-out-only').hidden = false;
      }
      login = document.getElementById('login-info')
      if (login) {
        login.hidden = false;
      }
      console.log(`Signed in as ${user.displayName} (${user.email})`);
      user.getIdToken().then(function (token) {
        document.cookie = "funtech_token=" + token;
      });
    } else {
      var ui = new firebaseui.auth.AuthUI(firebase.auth());
      ui.start('#firebaseui-auth-container', uiConfig);
      document.getElementById('sign-out').hidden = true;
      if (document.getElementById('sign-out-only')) {
        document.getElementById('sign-out-only').hidden = true;
      }
      login = document.getElementById('login-info')
      if (login) {
        login.hidden = true;
      }
      delete_cookie("funtech_token");
    }
  }, function (error) {
    console.log(error);
    alert('Unable to log in: ' + error)
    delete_cookie("funtech_token")
  });
});