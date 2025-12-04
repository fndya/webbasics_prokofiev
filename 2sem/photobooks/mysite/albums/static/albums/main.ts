// Подсветка элементов
document.querySelectorAll(".hoverable").forEach((el) => {
    el.addEventListener("mousemove", () => {
        el.classList.add("hover-active");
    });
    el.addEventListener("mouseleave", () => {
        el.classList.remove("hover-active");
    });
});

// Кнопки «★ избранное»
// Кнопки «избранное»
document.querySelectorAll(".fav-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
        btn.classList.toggle("fav-btn-active");
    });
});


// Кликабельные названия
document.querySelectorAll(".clickable").forEach((el) => {
    el.addEventListener("click", () => {
        console.log("Открытие альбома");
    });
});

const themeToggle = document.getElementById("themeToggle");
const themeIcon = document.getElementById("themeIcon");

// при загрузке — применяем тему из localStorage
if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark");
    if (themeIcon) themeIcon.textContent = "☀️";
}

// переключение темы
themeToggle?.addEventListener("click", () => {
    const isDark = document.body.classList.toggle("dark");
    localStorage.setItem("theme", isDark ? "dark" : "light");

    if (themeIcon) themeIcon.textContent = isDark ? "☀️" : "🌙";
});
