document.addEventListener("DOMContentLoaded", () => {
  const busca = document.getElementById("campoBusca");
  const items = Array.from(document.querySelectorAll(".imagem-container"));

  if (busca) {
    busca.addEventListener("input", (e) => {
      const q = e.target.value.trim().toLowerCase();
      if (!q) {
        items.forEach(i => i.style.display = "");
        return;
      }
      items.forEach(item => {
        const keys = (item.dataset.keywords || "").toLowerCase();
        const title = (item.textContent || "").toLowerCase();
        const match = keys.includes(q) || title.includes(q);
        item.style.display = match ? "" : "none";
      });
    });

    busca.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        const q = busca.value.trim();
        if (q.length) {
          window.location.href = `/PG_2_Pedro Neto/index.html?q=${encodeURIComponent(q)}`;
        } else {
          window.location.href = `/PG_2_Pedro Neto/index.html`;
        }
      }
    });
  }

  document.querySelectorAll(".imagem-container, .botao-imagens").forEach(el => {
    el.addEventListener("click", (e) => {
      const target = el.tagName.toLowerCase() === "a" ? el : el.querySelector("a");
      if (target && target.getAttribute("href")) {
        window.location.href = target.getAttribute("href");
      } else {
        window.location.href = "/PG_2_Pedro Neto/index.html";
      }
    });
  });

  const prefersReduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (prefersReduce.matches) {
    document.documentElement.style.scrollBehavior = "auto";
  } else {
    document.documentElement.style.scrollBehavior = "smooth";
  }
});
