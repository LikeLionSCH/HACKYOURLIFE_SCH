const REGISTERD_USER_REQUEST = "verify_registered_user_request";
const DELETE_USER_REQUEST = "delete_authenticated_user_request";

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

function transaction(code, data, onSuccess, onFail) {
    $.ajax({
        type: "POST",
        url: "/",
        headers: {"X-CSRFToken": getCookie("csrftoken")},
        dataType: "json",
        data: $.extend({requestCode: code}, data),
        success: onSuccess,
        error: onFail
    });
}

function onGapiLoad() {
    gapi.load('auth2', function() {
        gapi.auth2.init();
        gapi.auth2.getAuthInstance().currentUser.listen(onSignIn);
    });
}

// 테스트할 때 반드시 localhost:8000으로 접속하세요
function onSignIn(googleUser) {
    // google OAuth2.0으로 로그인 한 정보를 firebase auth에 전달하여 로그인
    if (googleUser.isSignedIn()) {
        let idToken = googleUser.getAuthResponse().id_token;
        let credential = firebase.auth.GoogleAuthProvider.credential(idToken);
        firebase.auth().setPersistence(firebase.auth.Auth.Persistence.LOCAL).then(function() {
            return firebase.auth().signInWithCredential(credential);
        });
    }
}

function onAuthStateChanged(user) {
    if (user) {
        transaction(REGISTERD_USER_REQUEST,
            // 전송할 데이터
            { email: user.email },
            // 등록된 유저인 경우
            function() { },
            // 등록되지 않은 유저인 경우
            function() {
                // 승인 신청되지 않은 유저인 경우
                if (confirm("등록되지 않은 사용자 입니다. 승인 신청하시겠습니까?")) {
                    alert("승인 신청되었습니다.");
                }
                else {
                    transaction(DELETE_USER_REQUEST, { uid: user.uid });
                }
                
                signOut();
            }
        );
    }
}

function signIn() {
    gapi.auth2.getAuthInstance().signIn();
}

function signOut() {
    firebase.auth().signOut();
    gapi.auth2.getAuthInstance().signOut();
}

// Firebase 초기화
if (!firebase.apps.length) {
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
    firebase.auth().onAuthStateChanged(onAuthStateChanged);
}
