console.log("ADMIN JS LOADED");

window.addEventListener("load", function () {

    console.log("FullCalendar =", typeof FullCalendar);

    const el = document.getElementById("calendar");

    if (!el) {
        console.error("calendar not found");
        return;
    }

    if (typeof FullCalendar === "undefined") {
        console.error("FullCalendar NOT LOADED ❌");
        return;
    }

    const calendar = new FullCalendar.Calendar(el, {
        initialView: "dayGridMonth"
    });

    calendar.render();

    console.log("calendar rendered ✔");
});