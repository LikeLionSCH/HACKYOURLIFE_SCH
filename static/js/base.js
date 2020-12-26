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

    if (!firebase.apps.length) {
        firebase.initializeApp(firebaseConfig);
    }

    firebase.auth().setPersistence(firebase.auth.Auth.Persistence.SESSION) // 왜 안될까
    let provider = new firebase.auth.GoogleAuthProvider();
    await firebase.auth().signInWithPopup(provider).then(function (result) {
        // let accessToken = result.credential.accessToken;
        // let idToken = result.credential.idToken;
        let uid = result.user.uid;
        let userEmail = result.user.email;
        $.ajax({
            type: "POST",
            url: "/",
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            },
            data: {
                uid: uid,
                userEmail: userEmail
            },
            dataType: "json"
        });
    });
}