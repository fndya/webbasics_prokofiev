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
document.querySelectorAll(".fav-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
        const id = btn.getAttribute("data-id");
        alert(`Альбом ${id} добавлен в избранное (пока только визуально)`);
        btn.classList.add("fav-btn-active");
        btn.textContent = "★";
    });
});
// Кликабельные названия
document.querySelectorAll(".clickable").forEach((el) => {
    el.addEventListener("click", () => {
        console.log("Открытие альбома");
    });
});
