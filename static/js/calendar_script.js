document.body.addEventListener('htmx:afterSwap', function(evt) {
  const calendarEl = document.getElementById('calendar-target');
  
  if (calendarEl && window.FullCalendar) {
    const calendar = new window.FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      events: '/api/eventos/'
    });
    calendar.render();
  } else if (!window.FullCalendar) {
    console.error("FullCalendar no está disponible en window.");
  }
});