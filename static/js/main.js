/* main.html deadline에 [yyyy/mm/dd 00:00:00] 형식으로 입력 시 자동 적용*/
var choice_datetime = $('#deadline-time').text();
var targetDate = new Date(choice_datetime);   
var days;
var hrs;
var min;
var sec;


/*----------------- CURRICULUM hover 효과 삽입----------- */
// 1
function firstTextChange(obj){
    obj.innerHTML="3월-4월";
    obj.style.color="white";
    obj.style.fontfamily='IBMPlexSansKR-Text';
   }

   function firstTextChangeAgain(obj){
    obj.innerHTML="UI/UX 설계";
   }
// 2
function secondTextChange(obj){
    obj.innerHTML="5월-6월";
    obj.style.color="white";
    obj.style.fontfamily='IBMPlexSansKR-Text';
   }

function secondTextChangeAgain(obj){
    obj.innerHTML="HTML/CSS";
   } 

// 3

function ThirdTextChange(obj){
    obj.innerHTML="7월-10월";
    obj.style.color="white";
    obj.style.fontfamily='IBMPlexSansKR-Text';
   }

function ThirdTextChangeAgain(obj){
    obj.innerHTML="Python/Django";
   } 

//  4

function fourthTextChange(obj){
    obj.innerHTML="11월-12월";
    obj.style.color="white";
    obj.style.fontfamily='IBMPlexSansKR-Text';
   }

function fourthTextChangeAgain(obj){
    obj.innerHTML="해커톤";
   } 


/*--------------CountDown 배너 ------------- */

/* --------------------------
 * 선언된 전역변수
 * -------------------------- */
// 디데이 할 날짜 및 시간


/* --------------------------
 * 로드 값
 * -------------------------- */
$(function() {
   // Calculate time until launch date
   timeToLaunch();
  // Transition the current countdown from 0 
  numberTransition('#days .number', days, 1000, 'easeOutQuad');
  numberTransition('#hours .number', hrs, 1000, 'easeOutQuad');
  numberTransition('#minutes .number', min, 1000, 'easeOutQuad');
  numberTransition('#seconds .number', sec, 1000, 'easeOutQuad');
  // Begin Countdown
  setTimeout(countDownTimer,1001);
});

/* --------------------------
 * FIGURE OUT THE AMOUNT OF 
   TIME LEFT BEFORE LAUNCH
 * -------------------------- */
function timeToLaunch(){
    // Get the current date
    var currentDate = new Date();

    // Find the difference between dates
    var diff = (currentDate - targetDate)/1000;
    var diff = Math.abs(Math.floor(diff));  

    // Check number of days until target
    days = Math.floor(diff/(24*60*60));
    sec = diff - days * 24*60*60;

    // Check number of hours until target
    hrs = Math.floor(sec/(60*60));
    sec = sec - hrs * 60*60;

    // Check number of minutes until target
    min = Math.floor(sec/(60));
    sec = sec - min * 60;
}

/* --------------------------
 * 화면에 보여줄 값
 * -------------------------- */
function countDownTimer(){ 
    
    // Figure out the time to launch
    timeToLaunch();
    
    // Write to countdown component
    $( "#days .number" ).text(days);
    $( "#hours .number" ).text(hrs);
    $( "#minutes .number" ).text(min);
    $( "#seconds .number" ).text(sec);
    
    // Repeat the check every second
    setTimeout(countDownTimer,1000);
}

/* --------------------------
 * TRANSITION NUMBERS FROM 0
   TO CURRENT TIME UNTIL LAUNCH
 * -------------------------- */
function numberTransition(id, endPoint, transitionDuration, transitionEase){
  // Transition numbers from 0 to the final number
  $({numberCount: $(id).text()}).animate({numberCount: endPoint}, {
      duration: transitionDuration,
      easing:transitionEase,
      step: function() {
        $(id).text(Math.floor(this.numberCount));
      },
      complete: function() {
        $(id).text(this.numberCount);
      }
   }); 
};

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

async function googleSignIn(){
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
  await firebase.auth().signInWithPopup(provider).then(function(result) {
    // let accessToken = result.credential.accessToken;
    // let idToken = result.credential.idToken;
    let uid = result.user.uid;
    $.ajax({
      type: "POST",
      url:"/",
      headers: {
        "X-CSRFToken": getCookie('csrftoken')
      },
      data: {uid: uid},
      dataType: "json"
    });
  });
}