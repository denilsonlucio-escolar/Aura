document.addEventListener("DOMContentLoaded", () => {
  const busca = document.getElementById("campoBusca");
  const lista = document.getElementById("lista");

  busca.addEventListener('keyup',()=>{
    const termo = busca.value.toLowerCase();
    const linhas = lista.querySelectorAll('.card-link');

    for (let i = 0; i < linhas.length; i++) {
      const ele = linhas[i];
      const nome = ele.id.toLocaleLowerCase();
     
    
      ele.style.display = nome.includes(termo) ? "block" : "none";
    
      

    }
    

  })


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
