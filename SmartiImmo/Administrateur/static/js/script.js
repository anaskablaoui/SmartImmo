document.addEventListener("DOMContentLoaded", () => {
    const links = document.querySelectorAll(".nav_link");
    const panels = document.querySelectorAll(".panel");

    links.forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();

            links.forEach(l => l.classList.remove("active"));
            link.classList.add("active");

            const target = link.getAttribute("data-target");
            panels.forEach(panel => panel.classList.remove("active"));

            const activePanel = document.getElementById(target);
            if (activePanel) activePanel.classList.add("active");
        });
    });
});

function filterTable(inputId, tableId) {
    const filter = document.getElementById(inputId).value.toLowerCase();
    const rows = document.getElementById(tableId).getElementsByTagName("tr");
    for (let i = 1; i < rows.length; i++) {
        rows[i].style.display = rows[i].innerText.toLowerCase().includes(filter) ? "" : "none";
    }
}