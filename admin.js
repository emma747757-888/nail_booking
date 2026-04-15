const API = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", async function () {

    // =========================
    // 1️⃣ 获取 staff
    // =========================
    const staffRes = await fetch(`${API}/staff/`);
    const staffData = await staffRes.json();

    const resources = staffData.map(s => ({
        id: s.id,
        title: s.name
    }));

    // =========================
    // 2️⃣ 获取 appointments
    // =========================
    const res = await fetch(`${API}/appointments/`);
    const data = await res.json();

    const events = data.map(a => ({
        id: a.id,
        title: `${a.name} - ${a.service}`,
        start: `${a.date}T${a.time}`,
        resourceId: a.staff_id,   // 🔥关键：分配到员工列
        backgroundColor:
            a.status === "completed" ? "green" :
            a.status === "cancelled" ? "red" : "orange"
    }));

    // =========================
    // 3️⃣ 初始化 FullCalendar
    // =========================
    const calendarEl = document.getElementById("calendar");

    const calendar = new FullCalendar.Calendar(calendarEl, {

        initialView: "resourceTimeGridDay",

        resources: resources,   // 👈 staff列

        headerToolbar: {
            left: "prev,next today",
            center: "title",
            right: "resourceTimeGridDay,resourceTimeGridWeek"
        },

        editable: true,   // 🔥可拖拽

        events: events,

        // =========================
        // 4️⃣ 拖拽更新
        // =========================
        eventDrop: async function(info) {

            const newDate = info.event.start.toISOString().split("T")[0];
            const newTime = info.event.start.toTimeString().slice(0,5);
            const newStaff = info.event.getResources()[0]?.id;

            await fetch(`${API}/appointments/${info.event.id}/reschedule`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    date: newDate,
                    time: newTime,
                    staff_id: newStaff
                })
            });

            alert("Updated ✔");
        }
    });

    calendar.render();
});