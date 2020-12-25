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

$(function() {
  $.ajax({
    type: "POST",
    url:"/calendar/",
    headers: {
      "X-CSRFToken": getCookie('csrftoken')
    },
    dataType: "json"
  }).done(function(data) {
    let events = data["list"];

    $('#calendar').fullCalendar({
      defaultView: 'month',
      defaultDate: '2020-12-01',
  
      // html을 통해 가져오는 값들.
      calendar_day : {
        _title :  document.getElementById('input_title').value,
        _desc :  document.getElementById('input_desc').value,
        _start : document.getElementById('input_start').value,
        _end :  document.getElementById('input_end').value
      },
  
      eventRender: function(eventObj, $el) {
        $el.popover({
          title: eventObj.title,
          content: eventObj.description,
          trigger: 'hover',
          placement: 'top',
          container: 'body'
        });
      },
  
      events: events
    });
  });
});