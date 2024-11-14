document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("myModalProyecto");
    var abrirModal = document.getElementById("abrirModalProyecto");
    var cerrarModal = document.getElementsByClassName("close")[1];
    var btnCancelar = document.getElementById("btnCancelar2");

    abrirModal.addEventListener("click", function(event){
        event.preventDefault();
        modal.style.display = "block";
        console.log("MODAL PARA LAS PUBLICACIONES DE EVENTOS");
    });

    cerrarModal.onclick = function() {
        modal.style.display = "none";
    }

    btnCancelar.onclick = function() {
        modal.style.display = "none";
    }

});