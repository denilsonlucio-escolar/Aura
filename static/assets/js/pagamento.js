document.addEventListener("DOMContentLoaded", () => {
  const carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];

  if (carrinho.length === 0) {
    alert("Carrinho vazio.");
    window.location.href = "../carrinho/carrinho.html";
    return;
  }

  let total = 0;

  carrinho.forEach(p => {
    total += p.preco * p.quantidade;
  });

  document.getElementById("valor-produtos").innerText =
    `R$ ${total.toFixed(2).replace(".", ",")}`;

  document.getElementById("valor-total").innerText =
    `R$ ${total.toFixed(2).replace(".", ",")}`;
});

function finalizarPagamento() {
  window.location.href = "../confirmacao/confirmacao.html";
}
