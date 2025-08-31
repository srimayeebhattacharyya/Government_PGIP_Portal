document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');
    
    // Check if calendar element exists
    if (!calendarEl) {
        console.error('Calendar element not found');
        return;
    }
    
    let currentEvent = null;

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        selectable: true,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,dayGridWeek,dayGridDay'
        },
        events: function(fetchInfo, successCallback, failureCallback) {
            fetch('/api/events/')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    successCallback(data);
                })
                .catch(error => {
                    console.error('Error fetching events:', error);
                    failureCallback(error);
                });
        },
        dateClick: function (info) {
            const dateInput = document.getElementById('reminderDate');
            const titleInput = document.getElementById('reminderTitle');
            
            if (dateInput && titleInput) {
                dateInput.value = info.dateStr;
                titleInput.value = '';
                
                const modalElement = document.getElementById('reminderModal');
                if (modalElement) {
                    const modal = new bootstrap.Modal(modalElement);
                    modal.show();
                }
            }
        },
        eventClick: function (info) {
            info.jsEvent.preventDefault();
            const event = info.event;
            currentEvent = event;
            
            // Only show delete modal for reminder events (not exams)
            if (event.id && event.id.startsWith('task-')) {
                const detailsElement = document.getElementById('reminderDetails');
                const idInput = document.getElementById('deleteReminderId');
                
                if (detailsElement && idInput) {
                    detailsElement.innerHTML = 
                        `<strong>Title:</strong> ${event.title}<br>
                         <strong>Date:</strong> ${event.startStr}`;
                    idInput.value = event.id;
                    
                    const modalElement = document.getElementById('viewReminderModal');
                    if (modalElement) {
                        const modal = new bootstrap.Modal(modalElement);
                        modal.show();
                    }
                }
            } else {
                // For exam events, just show details without delete option
                alert(`Event: ${event.title}\nDate: ${event.startStr}`);
            }
        }
    });

    calendar.render();

    // Add reminder form with null check
    const reminderForm = document.getElementById('reminderForm');
    if (reminderForm) {
        reminderForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const titleInput = document.getElementById('reminderTitle');
            const dateInput = document.getElementById('reminderDate');
            
            if (!titleInput || !dateInput) return;
            
            const title = titleInput.value;
            const date = dateInput.value;

            if (!title.trim()) {
                alert('Please enter a title for your reminder');
                return;
            }

            fetch('/add-reminder/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ title, date })
            })
            .then(res => {
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                return res.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    calendar.refetchEvents();
                    const modalElement = document.getElementById('reminderModal');
                    if (modalElement) {
                        const modal = bootstrap.Modal.getInstance(modalElement);
                        if (modal) modal.hide();
                    }
                    
                    // Show success message
                    showToast('Reminder added successfully!', 'success');
                } else if (data.status === 'duplicate') {
                    alert('This reminder already exists! You cannot add it again.');
                } else {
                    alert('Error: ' + (data.message || 'Unknown error occurred'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error adding reminder. Please try again.');
            });
        });
    }

    // Delete reminder functionality with null check
    const deleteReminderForm = document.getElementById('deleteReminderForm');
    if (deleteReminderForm) {
        deleteReminderForm.addEventListener('submit', function (e) {
            e.preventDefault();
            deleteCurrentReminder();
        });
    }

    // Also add click event listener for the delete button
    const deleteButton = document.getElementById('confirmDeleteBtn');
    if (deleteButton) {
        deleteButton.addEventListener('click', function() {
            deleteCurrentReminder();
        });
    }

    // Function to handle reminder deletion
    function deleteCurrentReminder() {
        if (!currentEvent) {
            alert('No reminder selected for deletion');
            return;
        }
        
        const reminderId = currentEvent.id;
        if (!reminderId || !reminderId.startsWith('task-')) {
            alert('Cannot delete this event type');
            return;
        }
        
        // Extract the actual ID (remove "task-" prefix)
        const actualId = reminderId.replace('task-', '');

        fetch(`/delete-reminder/${actualId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(res => {
            if (res.status === 401) {
                throw new Error('Unauthorized: Please log in again');
            }
            if (res.status === 404) {
                throw new Error('Reminder not found');
            }
            if (!res.ok) {
                throw new Error('Network response was not ok');
            }
            return res.json();
        })
        .then(data => {
            if (data.status === 'success' || data.success) {
                calendar.refetchEvents();
                const modalElement = document.getElementById('viewReminderModal');
                if (modalElement) {
                    const modal = bootstrap.Modal.getInstance(modalElement);
                    if (modal) modal.hide();
                }
                
                // Show success message
                showToast('Reminder deleted successfully!', 'success');
                currentEvent = null;
            } else {
                throw new Error(data.message || 'Unknown error occurred during deletion');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting reminder: ' + error.message);
        });
    }

    // CSRF token fetch helper function
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Toast notification function
    function showToast(message, type = 'info') {
        // Create toast element if it doesn't exist
        let toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toastContainer';
            toastContainer.style.position = 'fixed';
            toastContainer.style.top = '20px';
            toastContainer.style.right = '20px';
            toastContainer.style.zIndex = '9999';
            document.body.appendChild(toastContainer);
        }

        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show`;
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        toastContainer.appendChild(toast);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 3000);
    }
});