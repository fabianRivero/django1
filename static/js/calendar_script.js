document.body.addEventListener('htmx:afterSwap', function() {
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

document.body.addEventListener('htmx:afterSwap', function (event) {
    if (event.detail.target.id !== 'modal-container') return;

    const calEl = document.body.querySelector('[id^="calendar-"]');
    if (!calEl) return;

    const serviceId = calEl.id.replace('calendar-', '');

    const calendar = new FullCalendar.Calendar(calEl, {
      initialView: 'dayGridMonth',
      locale: 'es',
      firstDay: 1,
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: ''
      },

      datesSet: function (info) {
        const inicio = info.startStr.slice(0, 10);   
        const fin = info.endStr.slice(0, 10);       
        fetch(`/api/disponibilidad/${serviceId}/?mes=${inicio}&fin=${fin}`)
        .then(r => r.json())
        .then(data => {
          const events = data.map(d => ({
            start: d.date,
            display: 'background',
            classNames: ['dia-con-horarios'],
            extendedProps: { horarios: d.horarios }
          }));
          calendar.removeAllEvents();
          calendar.addEventSource(events);
        });
      },

      dateClick: function (info) {
        const eventos = calendar.getEvents().filter(e => e.startStr === info.dateStr);
        const horarios = eventos.length ? eventos[0].extendedProps.horarios : [];
        const container = document.getElementById(`horarios-${serviceId}`);

        if (!horarios.length) {
          container.innerHTML = '<p class="text-muted">No hay horarios disponibles este día.</p>';
          return;
        }

        container.innerHTML = `
        <h6>Horarios disponibles — ${info.dateStr}</h6>
        <div class="d-flex flex-wrap gap-2">
          ${horarios.map(h => `
              <div class="horario-item">
                  <button class="btn btn-outline-primary btn-sm btn-horario"
                    data-reservation="${h.id}">
                    ${h.time}
                  </button>
              </div>
          `).join('')}
        </div>
        `;

        container.addEventListener('click', function (e) {
          const btn = e.target.closest('.btn-horario');
          if (!btn) return;
            mostrarConfirmacion(btn, btn.dataset.reservation);
        });
      },
    });

  calendar.render();
});


function mostrarConfirmacion(btn, reservationId) {
  const existing = btn.parentElement.querySelector('.confirm-box');
  if (existing) return;

  const box = document.createElement('div');
  box.className = 'confirm-box';
  box.innerHTML = `
    <p>¿Quieres confirmar la reserva?</p>
    <button class="btn btn-success btn-sm btn-confirm-yes">Sí</button>
    <button class="btn btn-secondary btn-sm btn-confirm-no">No</button>
  `;

  btn.parentElement.appendChild(box);

  box.querySelector('.btn-confirm-yes').addEventListener('click', () => {
    reservar(reservationId);
  });

  box.querySelector('.btn-confirm-no').addEventListener('click', () => {
    box.remove();
  });
}

function reservar(reservationId) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/reservar/${reservationId}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrfToken
      }
    })
    .then(r => {
      if (r.ok) {
        document.getElementById('modal-container').innerHTML = '';
        window.location.href = '/';
      } else {
        alert('No se pudo hacer la reserva. Prueba otra vez.');
      }
    });
}