// Esperar a que el DOM se cargue
document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("modalAddEscuela");
    var abrirModal = document.getElementById("abrirModalEscuela");
    var cerrarModal = document.getElementsByClassName("clsModEscuela")[0];
    var btnCancelar = document.getElementById("btnCancelar");

    abrirModal.onclick = function(event) {
        event.preventDefault();
        modal.style.display = "block";
        document.body.style.overflow = "hidden";
    }

    cerrarModal.onclick = function() {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }

    btnCancelar.onclick = function() {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }

    var btnAbrirModalEditEscuela = document.querySelectorAll(".btnAbrirModalEditEscuela");
    var abrirModalEditEscuela = document.getElementById("modalEditEscuela");
    var btnCancelarEditEscuela = document.getElementById("btnCancelarEditEscuela");
    var cerrarModalEditEscuela = document.getElementsByClassName("clsModEditEscuela")[0];

    btnAbrirModalEditEscuela.forEach(btn => {
        btn.addEventListener("click", (event) => {
            event.preventDefault();
            abrirModalEditEscuela.style.display = "block";
        });
    });

    btnCancelarEditEscuela.onclick = function() {
        abrirModalEditEscuela.style.display = "none";
    }

    cerrarModalEditEscuela.onclick = function() {
        abrirModalEditEscuela.style.display = "none";
    }

    

});