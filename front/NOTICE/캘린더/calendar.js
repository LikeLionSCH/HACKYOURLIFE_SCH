

$(function() {



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

      events: [
        {
          title: 'Long Event',
          description: 'description for Long Event',
          start: '2019-01-07',
          end: '2019-01-10'
        },
        {
          id: 999,
          title: 'Repeating Event',
          description: 'description for Repeating Event',
          start: '2019-01-09T16:00:00'
        },
        {
          id: 999,
          title: 'Repeating Event',
          description: 'description for Repeating Event',
          start: '2019-01-16T16:00:00'
        },
        {
          title: 'Conference',
          description: 'description for Conference',
          start: '2019-01-11',
          end: '2019-01-13'
        },
        {
          title: 'Meeting',
          description: 'description for Meeting',
          start: '2019-01-12'
        },
        {
          title: 'Lunch',
          description: 'description for Lunch',
          start: '2019-01-13'
        },
        {
          title: 'ㅎㅇㄹ',
          description: 'description for Meeting',
          start: '2019-01-12'
        },
        {
          title: 'Birthday Party',
          description: 'description for Birthday Party',
          start: '2019-01-13T07:00:00'
        },
        {
          title: '기말 고사',
          description: 'description for Birthday Party',
          start: '2020-12-07',
          end: '2020-12-15'
        },
      ]
    });
  
  });