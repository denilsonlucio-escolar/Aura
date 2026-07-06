const lista = document.getElementById("lista-carrinho");
const subtotalEl = document.getElementById("subtotal");
const totalEl = document.getElementById("total");

let carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];

function renderizar() {
  lista.innerHTML = "";
  let total = 0;

  carrinho.forEach((p, index) => {
    total += p.preco * p.quantidade;

    lista.innerHTML += `
      <div class="item-carrinho">
        <img src="${p.imagem}">
        <div>
          <p>${p.nome}</p>
          <small>Quantidade: ${p.quantidade}</small>
        </div>

        <div class="controle-qtd">
          <button onclick="alterarQtd(${index}, -1)">−</button>
          <span>${p.quantidade}</span>
          <button onclick="alterarQtd(${index}, 1)">+</button>
        </div>

        <div>R$ ${(p.preco * p.quantidade).toFixed(2)}</div>

        <button class="excluir" onclick="remover(${index})">✕</button>
      </div>
    `;
  });

  subtotalEl.innerText = `R$ ${total.toFixed(2)}`;
  totalEl.innerText = `R$ ${total.toFixed(2)}`;

  localStorage.setItem("carrinho", JSON.stringify(carrinho));
}

function alterarQtd(i, valor) {
  carrinho[i].quantidade += valor;
  if (carrinho[i].quantidade < 1) carrinho[i].quantidade = 1;
  renderizar();
}

function remover(i) {
  carrinho.splice(i, 1);
  renderizar();
}

function irParaPagamento() {
  window.location.href = "../pagamento/pagamento.html";
}

renderizar();

function irParaEntrega() {
  window.location.href = "../PG_06_Alterar_Endereco/Alterar_Endereco.html";
}



