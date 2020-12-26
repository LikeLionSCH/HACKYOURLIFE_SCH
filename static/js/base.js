async function googleSignIn() {
    const firebaseConfig = {
        apiKey: "AIzaSyA3NMvkdpSoKYsPPkNgDtrppzurxOMJbQQ",
        authDomain: "likelion-sch.firebaseapp.com",
        databaseURL: "https://likelion-sch.firebaseio.com/",
        projectId: "likelion-sch",
        storageBucket: "likelion-sch.appspot.com",
        messagingSenderId: "654141769540",
        appId: "1:654141769540:web:c744ef4d2df58003093911",
        measurementId: "G-PXNX9ZZCEN"
    };

    firebase.initializeApp(firebaseConfig);

    let provider = new firebase.auth.GoogleAuthProvider();
    await firebase.auth().signInWithPopup(provider).then(function (result) {
        // let accessToken = result.credential.accessToken;
        // let idToken = result.credential.idToken;
        let uid = result.user.uid;
        $.ajax({
            type: "POST",
            url: "/",
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            },
            data: {
                uid: uid
            },
            dataType: "json"
        });
    });
}