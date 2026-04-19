console.log("ADMIN JS LOADED ✔");

window.addEventListener("load", async function () {

    const el = document.getElementById("calendar");

    if (!el) {
        console.error("calendar not found");
        return;
    }

    if (typeof FullCalendar === "undefined") {
        console.error("FullCalendar not loaded");
        return;
    }

    const calendar = new FullCalendar.Calendar(el, {

        initialView: "timeGridDay",
        height: 650,

        headerToolbar: {
            left: "prev,next today",
            center: "title",
            right: "timeGridDay,timeGridWeek"
        },

        events: async function(fetchInfo, successCallback) {

            const res = await fetch("/api/calendar");
            const data = await res.json();

            successCallback(data);
        }
    });

    calendar.render();

    console.log("calendar rendered ✔");
});