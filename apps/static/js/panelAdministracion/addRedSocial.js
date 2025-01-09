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

    /* FUNCION PARA LA PARTE DE EDICION DE LAS REDES SOCIALES*/
    var abirModalEditRedSocial = document.getElementById("modalEditRedSocial");
    var clsModalEditRedSocial = document.getElementsByClassName("clsModEditRedSocial")[0];
    var btnAbrirModalEditRedSocial = document.querySelectorAll(".btnAbrirModalEditRedSocial");
    var btnCancelarEditRedSocial = document.getElementById("btnCancelarEditRedSocial");

    btnAbrirModalEditRedSocial.forEach(btn => {
        btn.addEventListener("click", function(event){
            event.preventDefault();
            const data_id_atribute = event.target.getAttribute("data-id");

            abirModalEditRedSocial.style.display = "block"
            document.body.style.overflow = "hidden";

        });
    });

    clsModalEditRedSocial.addEventListener("click", function(){
        abirModalEditRedSocial.style.display = "none";
        document.body.style.overflow = "auto";
    });

    btnCancelarEditRedSocial.addEventListener("click", function(){
        abirModalEditRedSocial.style.display = "none";
        document.body.style.overflow = "auto";
    });

});