console.log("ADMIN JS LOADED");

const API = window.location.origin;

window.addEventListener("load", function () {

    console.log("FullCalendar =", typeof FullCalendar);

    const calendarEl = document.getElementById("calendar");

    if (!calendarEl) {
        console.error("❌ calendar div not found");
        return;
    }

    if (typeof FullCalendar === "undefined") {
        console.error("❌ FullCalendar not loaded (CDN issue)");
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

        editable: true,

        // =========================
        // 🔥 events 保持你的逻辑
        // =========================
        events: async function(fetchInfo, successCallback) {

            try {
                const res = await fetch(`${API}/appointments/`);
                const data = await res.json();

                console.log("appointments:", data);

                const events = data.map(a => ({
                    id: a.id,
                    title: `${a.name} - ${a.service}`,
                    start: `${a.date}T${a.time}`
                }));

                successCallback(events);

            } catch (err) {
                console.error("❌ fetch error:", err);
            }
        }
    });

    calendar.render();

    console.log("✅ calendar rendered");
});