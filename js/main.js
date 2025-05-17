function filterProjects(type) {
    document.querySelectorAll(".card").forEach((card) => {
        card.style.display = type === "all" || card.dataset.type === type ? "block" : "none";
    });
}
