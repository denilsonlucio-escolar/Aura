document.addEventListener("DOMContentLoaded", function() {

    const tabFisica = document.getElementById('tab-fisica');
    const tabJuridica = document.getElementById('tab-juridica');
    const formFisica = document.getElementById('form-fisica');
    const formJuridica = document.getElementById('form-juridica');

    function ativarFisica() {
        tabFisica.classList.add('active');
        tabJuridica.classList.remove('active');
        formFisica.classList.add('active');
        formJuridica.classList.remove('active');
    }

    function ativarJuridica() {
        tabJuridica.classList.add('active');
        tabFisica.classList.remove('active');
        formJuridica.classList.add('active');
        formFisica.classList.remove('active');
    }

    tabFisica.onclick = ativarFisica;
    tabJuridica.onclick = ativarJuridica;

    formFisica.onsubmit = e => {
        alert('Cadastro realizado com sucesso! (simulação)');
    };

    formJuridica.onsubmit = e => {
         alert('Cadastro empresarial realizado com sucesso! (simulação)');
    };

});
