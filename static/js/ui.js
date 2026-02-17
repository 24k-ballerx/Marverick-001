// Shared UI interactions (dropdowns, sidebar toggle)
(() => {
  const closeAllDropdowns = (exceptEl) => {
    document.querySelectorAll("[data-dropdown].open").forEach((el) => {
      if (exceptEl && (el === exceptEl || el.contains(exceptEl))) return;
      el.classList.remove("open");
    });
  };

  document.addEventListener("click", (e) => {
    const toggle = e.target.closest("[data-dropdown-toggle]");
    if (toggle) {
      const root = toggle.closest("[data-dropdown]");
      if (!root) return;
      const willOpen = !root.classList.contains("open");
      closeAllDropdowns(root);
      root.classList.toggle("open", willOpen);
      e.preventDefault();
      return;
    }

    // Clicking inside menu shouldn't close it
    if (e.target.closest("[data-dropdown-menu]")) return;
    closeAllDropdowns();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeAllDropdowns();
  });

  // Mobile sidebar toggle (portal)
  const sidebarToggle = document.querySelector("[data-sidebar-toggle]");
  if (sidebarToggle) {
    sidebarToggle.addEventListener("click", () => {
      document.body.classList.toggle("sidebar-open");
    });
  }
})();

