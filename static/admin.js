console.log("ADMIN JS LOADED");

const API = window.location.origin;

function initCalendar() {

    const calendarEl = document.getElementById("calendar");

    if (!calendarEl) {
        console.error("calendar not found");
        return;
    }

    if (!window.FullCalendar) {
        console.error("FullCalendar not loaded yet");
        return;
    }

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "timeGridDay",
        height: 650,

        headerToolbar: {
            left: "prev,next today",
            center: "title",
            right: "timeGridDay,timeGridWeek"
        },

        events: async function (info, successCallback) {

            const res = await fetch(`${API}/appointments/`);
            const data = await res.json();

            const events = data.map(a => ({
                id: a.id,
                title: `${a.name} - ${a.service}`,
                start: `${a.date}T${a.time}`
            }));

            successCallback(events);
        }
    });

    calendar.render();

    console.log("calendar rendered");
}

// 🔥 等 FullCalendar 真加载出来
const wait = setInterval(() => {
    if (window.FullCalendar) {
        clearInterval(wait);
        initCalendar();
    }
}, 50);