// Esperar a que el DOM se cargue
document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("modalUbicación");
    var abrirModal = document.getElementById("abrirModalUbicacion");
    var abrirModalEdit = document.getElementById("modalUbicacionEdit");
    var cerrarModal = document.getElementsByClassName("clsModUbicacion")[0];
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
});