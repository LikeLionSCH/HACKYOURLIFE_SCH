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

// async function googleSignIn() {
//     // 이미 로그인 되어있으면, 로그아웃
//     let user = firebase.auth().currentUser;
//     if (user) {
//         return firebase.auth().signOut();
//     }

//     // 창 닫기 전까지 로그인 상태 유지
//     firebase.auth().setPersistence(firebase.auth.Auth.Persistence.SESSION).then(function() {
//         let provider = new firebase.auth.GoogleAuthProvider();
        
//         // 팝업창으로 구글 로그인
//         return firebase.auth().signInWithPopup(provider).then(function (result) {
//             // 로그인한 유저의 uid를 서버에 전송
//             $.ajax({
//                 type: "POST",
//                 url: "/",
//                 headers: {
//                     "X-CSRFToken": getCookie('csrftoken')
//                 },
//                 dataType: "json",
//                 data: {
//                     uid: result.user.uid
//                 }
//             });
//         });
//     });
// }

function verifyUser(email, onSuccess, onFail) {
    $.ajax({
        type: "POST",
        url: "/",
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        },
        dataType: "json",
        data: {
            requestCode: 'verify_sign_in_user_request',
            email: email
        },
        success: onSuccess,
        error: onFail
    });
}

// 테스트할 때 반드시 localhost:8000으로 접속하세요
function onSignIn(googleUser) {
    let email = googleUser.getBasicProfile().getEmail();
    verifyUser(email,
        // 등록된 유저인 경우
        function() {
            let idToken = googleUser.getAuthResponse().id_token;
            let credential = firebase.auth.GoogleAuthProvider.credential(idToken);
            firebase.auth().signInWithCredential(credential).then(function() {
                console.log("signed in");
            });
        },
        // 등록되지 않은 유저인 경우
        function() {
            console.log(response);

            let result = confirm("등록되지 않은 사용자 입니다. 승인 신청?");
            if (result) {
                // 승인 신청
                console.log(`${email}, 7기/8기/9기, 멤버/운영진`);
            }

            gapi.auth2.getAuthInstance().signOut();
        }
    );
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
}

// 새로고침, 로그인, 로그아웃 등 상태가 변경되면 트리거
// @see: https://firebase.google.com/docs/auth/web/manage-users#get_the_currently_signed-in_user
firebase.auth().onAuthStateChanged(function (user) {
    let loginButton = document.querySelector(".login-box");
    if (user) {
        loginButton.innerHTML = `<img src="${user.photoURL}"> ${user.displayName} Logout`;
    } else {
        loginButton.innerHTML = `Login`;
    }
});



