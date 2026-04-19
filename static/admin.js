alert("JS LOADED");

const API = window.location.origin;  // ✅ 必须加

window.onload = function () {

    const calendarEl = document.getElementById("calendar");

    console.log("calendarEl:", calendarEl);

    const calendar = new FullCalendar.Calendar(calendarEl, {

        initialView: "timeGridDay",
        height: 650,

        headerToolbar: {
            left: "prev,next today",
            center: "title",
            right: "timeGridDay,timeGridWeek"
        },

        editable: true,

        events: async function(fetchInfo, successCallback) {

            const res = await fetch(`${API}/appointments/`);
            const data = await res.json();

            console.log("appointments:", data);

            const events = data.map(a => ({
                id: a.id,
                title: `${a.name} - ${a.service}`,
                start: `${a.date}T${a.time}`
            }));

            successCallback(events);
        }
    });

    calendar.render();
};