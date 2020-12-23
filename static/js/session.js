var user = firebase.auth().currentUser;

if (user) {
  // User is signed in.
  document.getElementsById("host").value = user.displayName;
} else {
  // No user is signed in.
  document.getElementsById("host").value = "Anonymous Host";
}