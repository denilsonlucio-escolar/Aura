document.addEventListener("DOMContentLoaded", () => {

  const busca = document.getElementById("campoBusca");
  const lista = document.getElementById("lista");

  if (busca && lista) {

    busca.addEventListener("keyup", () => {

      const termo = busca.value.toLowerCase();

      const produtos = lista.querySelectorAll(".card-link");

      produtos.forEach(produto => {

        const nome = produto
          .querySelector(".nome-produto")
          .textContent
          .toLowerCase();

        produto.style.display = nome.includes(termo)
          ? "block"
          : "none";

      });

    });

  }


  document.querySelectorAll(".imagem-container, .botao-imagens").forEach(el => {

    el.addEventListener("click", () => {

      const target = el.tagName.toLowerCase() === "a"
        ? el
        : el.querySelector("a");

      if (target && target.href) {
        window.location.href = target.href;
      }

    });

  });


});