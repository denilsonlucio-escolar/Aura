const mostrarSenha = document.querySelector(".mostrar-senha");
const campoSenha = document.querySelector('input[type="password"]');
if (mostrarSenha && campoSenha) {
  mostrarSenha.addEventListener("click", () => {
    const tipo = campoSenha.type === "password" ? "text" : "password";
    campoSenha.type = tipo;
    mostrarSenha.textContent = tipo === "password" ? "👁️" : "🙈";
  });
}

document.getElementById("form-login")?.addEventListener("submit", (e) => {
  e.preventDefault();
  alert("✅ Login efetuado com sucesso! (simulação)");
});

document.getElementById("form-cadastro")?.addEventListener("submit", (e) => {
  e.preventDefault();
  alert("📝 Conta criada! (simulação)");
});
