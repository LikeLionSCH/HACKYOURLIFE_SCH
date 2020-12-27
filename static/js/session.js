let user = firebase.auth().currentUser;

try {
  firebase.auth().onAuthStateChanged(function (user) {
    // User is signed in.
    document.getElementById("host").value = user.displayName;
    console.log(user.displayName); // test code
  })
} catch (error) {
  document.getElementById("host").value = "Anonymous Host";
  console.log('현재 user값은 ', user, '입니다.'); // test code
}