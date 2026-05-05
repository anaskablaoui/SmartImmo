document.addEventListener("DOMContentLoaded", () => {
    const links = document.querySelectorAll(".nav_link");
    const panels = document.querySelectorAll(".panel");

    links.forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();

            const target = link.getAttribute("data-target");

            // hide all panels
            panels.forEach(panel => {
                panel.classList.remove("active");
            });

            // show selected panel
            const activePanel = document.getElementById(target);
            if (activePanel) {
                activePanel.classList.add("active");
            }
        });
    });
});