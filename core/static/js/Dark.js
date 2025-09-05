document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("dark-toggle");
    const body = document.body;

    // Load preference
    if (localStorage.getItem("dark-mode") === "enabled") {
        body.classList.add("dark-mode");
        toggleBtn.innerHTML = '<i class="fas fa-sun"></i>';
    }

    toggleBtn.addEventListener("click", function () {
        body.classList.toggle("dark-mode");

        if (body.classList.contains("dark-mode")) {
            localStorage.setItem("dark-mode", "enabled");
            toggleBtn.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            localStorage.setItem("dark-mode", "disabled");
            toggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
        }
    });
});
