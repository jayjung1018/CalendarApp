$(function() {
  startTime();
  $('#calendar').fullCalendar({
    defaultView: 'agendaDay',
    allDaySlot: false,
    header: false,
    height: 700,
    minTime: '06:00:00',
    maxTime: '24:00:00',
    events: '/pages/events'
  })
  $.ajax({url:'https://quotes.rest/qod',
          accepts: {'Accept' : 'application/json'},
          dataType:'json',
          success: function(data) {
            if(data) {
              quote = data["contents"]["quotes"][0]["quote"]
              author = data["contents"]["quotes"][0]["author"]
              $('#qod').html('<i>"' + quote + '"</i>')
              $('#by').html("-" + author)
            }
          }
        });
});

function getEvents(data) {
  events = []
  for (model in data) {
    e = {}
    e["title"] = model["fields"]["name"]
    e["start"] = model["fields"]["start"]
    e["end"] = model["fields"]["end"]
    events.append(e)
  }
  return events
}

function startTime() {
  var today = new Date();
  var h = today.getHours();
  var m = today.getMinutes();
  var s = today.getSeconds();
  h = checkTime(h);
  m = checkTime(m);
  ampm = amorpm(h);
  if (ampm == 'PM' && h > 12) {
    h -= 12;
  }

  document.getElementById('time').innerHTML = h + ":" + m + " " + ampm;
  var t = setTimeout(startTime, 500);
}

function checkTime(i) {
  if (i < 10) {
    i = "0" + i
  }
  return i
}

function amorpm(h) {
  if (h >= 12) {
    return "PM"
  } else {
    return "AM"
  }
}
