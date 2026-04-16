const API = window.location.origin;

// =========================
// 1️⃣ 加载服务
// =========================
async function loadServices() {
    const res = await fetch(`${API}/services/`);
    const services = await res.json();

    const select = document.getElementById("service");

    services.forEach(s => {
        const option = document.createElement("option");
        option.value = s.name;
        option.innerText = `${s.name} (${s.duration} min)`;
        select.appendChild(option);
    });
}

// =========================
// 2️⃣ 加载员工
// =========================
async function loadStaff() {
    const res = await fetch(`${API}/staff/`);
    const staff = await res.json();

    const select = document.getElementById("staff");

    staff.forEach(s => {
        const option = document.createElement("option");
        option.value = s.id;
        option.innerText = s.name;
        select.appendChild(option);
    });
}

// =========================
// 3️⃣ 加载可用时间
// =========================
async function loadSlots() {
    const date = document.getElementById("date").value;
    const service = document.getElementById("service").value;
    const staff = document.getElementById("staff").value;

    if (!date || !service) return;

    const res = await fetch(
        `${API}/availability/?date=${date}&staff_id=${staff}`
    );

    const data = await res.json();

    const container = document.getElementById("slots");
    container.innerHTML = "";

    data.available_slots.forEach(time => {
        const btn = document.createElement("button");
        btn.innerText = time;
	btn.className = "btn btn-outline-dark m-1";

        btn.onclick = () => {
            document.getElementById("time").value = time;
        };

        container.appendChild(btn);
    });
}

// =========================
// 4️⃣ 提交预约（🔥核心升级）
// =========================
document.getElementById("bookingForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const phone = document.getElementById("phone").value;
    const service = document.getElementById("service").value;
    const date = document.getElementById("date").value;
    const time = document.getElementById("time").value;
    const staff_id = document.getElementById("staff").value;

    const response = await fetch(`${API}/appointments/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name,
            phone,
            service,
            date,
            time,
            staff_id: staff_id || null
        })
    });

    const data = await response.json();

    document.getElementById("result").innerText =
        data.error ? data.error : "Booking successful ✅";

    loadSlots(); // 刷新时间
});

// =========================
// 5️⃣ 监听变化（自动刷新时间）
// =========================
document.getElementById("date").addEventListener("change", loadSlots);
document.getElementById("service").addEventListener("change", loadSlots);
document.getElementById("staff").addEventListener("change", loadSlots);

// =========================
// 6️⃣ 初始化
// =========================
loadServices();
loadStaff();