const API = window.location.origin;

document.addEventListener("DOMContentLoaded", function () {

    const calendarEl = document.getElementById("calendar");

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
        // 🔥 动态加载 events（关键）
        // =========================
        events: async function(fetchInfo, successCallback, failureCallback) {
            try {
                const res = await fetch(`${API}/appointments/`);
                const data = await res.json();

                const events = data.map(a => ({
                    id: a.id,
                    title: `${a.name} - ${a.service}`,
                    start: `${a.date}T${a.time}`,
                    backgroundColor:
                        a.status === "completed" ? "green" :
                        a.status === "cancelled" ? "red" : "orange"
                }));

                successCallback(events);

            } catch (err) {
                console.error(err);
                failureCallback(err);
            }
        },

        // =========================
        // 🔥 拖拽更新时间
        // =========================
        eventDrop: async function(info) {

            const id = info.event.id;

            const newDate = info.event.startStr.slice(0, 10);
            const newTime = info.event.startStr.slice(11, 16);

            try {
                await fetch(`${API}/appointments/${id}/reschedule`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        date: newDate,
                        time: newTime,
                        staff_id: 1   // 先固定
                    })
                });

                alert("Updated ✔");

            } catch (err) {
                alert("Update failed ❌");
                console.error(err);
            }
        }

    });

    calendar.render();
}); 