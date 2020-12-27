function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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

    firebase.auth().setPersistence(firebase.auth.Auth.Persistence.SESSION).then(function() {
        let provider = new firebase.auth.GoogleAuthProvider();
        
        return firebase.auth().signInWithPopup(provider).then(function (result) {
            // 로그인된 상태로 front DOM 변경
            $.ajax({
                type: "POST",
                url: "/",
                headers: {
                    "X-CSRFToken": getCookie('csrftoken')
                },
                dataType: "json",
                data: {
                    uid: result.user.uid
                }
            });
        });
    });
    
}