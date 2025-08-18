document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        selectable: true,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,dayGridWeek,dayGridDay'
        },
        events: '/api/events/',
        dateClick: function (info) {
            document.getElementById('reminderDate').value = info.dateStr;
            document.getElementById('reminderTitle').value = '';
            new bootstrap.Modal(document.getElementById('reminderModal')).show();
        },
        eventClick: function (info) {
            const event = info.event;
            document.getElementById('reminderDetails').innerText = `Title: ${event.title}\nDate: ${event.startStr}`;
            document.getElementById('deleteReminderId').value = event.id;
            new bootstrap.Modal(document.getElementById('viewReminderModal')).show();
        }
    });

    calendar.render();

    document.getElementById('reminderForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const title = document.getElementById('reminderTitle').value;
        const date = document.getElementById('reminderDate').value;

        fetch('/add-reminder/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ title, date })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                calendar.refetchEvents();
                bootstrap.Modal.getInstance(document.getElementById('reminderModal')).hide();
            } else {
                alert('Error: ' + data.message);
            }
        });
    });

    document.getElementById('deleteReminderForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const taskId = document.getElementById('deleteReminderId').value;

        fetch(`/delete-reminder/${taskId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                calendar.refetchEvents();
                bootstrap.Modal.getInstance(document.getElementById('viewReminderModal')).hide();
            } else {
                alert('Error: ' + data.message);
            }
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
