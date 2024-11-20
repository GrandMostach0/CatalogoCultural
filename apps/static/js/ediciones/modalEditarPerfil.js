document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("editarPerfilModal");
    var abrirModal = document.getElementById("abrirEditarPerfilModal");
    var cerrarModal = document.getElementsByClassName("close")[2];
    var btnCerrarModal = document.getElementById("btnCancelar3")

    abrirModal.onclick = function(event) {
        event.preventDefault();
        modal.style.display = "block";
        document.body.style.overflow = "hidden";
    }

    cerrarModal.onclick = function() {
        modal.style.display = "none";
        document.body.overflow = "auto";
    }

    btnCerrarModal.onclick = function(){
        modal.style.display = "none";
        document.body.overflow = "auto";
    }
});