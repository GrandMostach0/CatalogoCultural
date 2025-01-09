document.addEventListener("DOMContentLoaded", function(){
    var modal = document.getElementById("modalRedSocial");
    var abrirModal = document.getElementById("abrirModalRedSocial");
    var cerrarModal = document.getElementsByClassName("clsModRedSocial")[0];
    var btnCancelar = document.getElementById("btnCancelarRedSocial");

    abrirModal.onclick = function(event){
        event.preventDefault();
        modal.style.display = "block";
        document.body.style.overflow = "hidden";
    }

    cerrarModal.onclick = function(){
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }

    btnCancelar.onclick = function(){
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }
});