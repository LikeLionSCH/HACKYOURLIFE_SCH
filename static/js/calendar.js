function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let calendarElement = document.getElementById("calendar");

document.addEventListener("DOMContentLoaded", function () {
    let calendar = new FullCalendar.Calendar(calendarElement, {
        initialView: "dayGridMonth",
        headerToolbar: {
            left: "title",
            right: "today prev,next"
        },
        eventColor: "#1BBCF0",
        eventDisplay: "block"
    });

    $.ajax({
        type: "POST",
        url: "/calendar/",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        dataType: "json"
    }).done(function (data) {
        let events = data["list"];
        console.log(events);

        for (let i = 0; i < events.length; ++i) {
            calendar.addEvent(events[i]);
        }
    });

    calendar.render();
});

// $(function() {
//   $.ajax({
//     type: "POST",
//     url:"/calendar/",
//     headers: {
//       "X-CSRFToken": getCookie("csrftoken")
//     },
//     dataType: "json"
//   }).done(function(data) {
//     let events = data["list"];

//     $("#calendar").fullCalendar({
//       defaultView: "month",
//       defaultDate: "2020-12-01",
//       eventRender: function(eventObj, $el) {
//         $el.popover({
//           title: eventObj.title,
//           content: eventObj.description,
//           trigger: "hover",
//           placement: "top",
//           container: "body"
//         });
//       },
//       events: events
//     });

//     console.log($("#calendar").fullCalendar("getDate"));
//   });
// });