// Esperar a que el DOM se cargue
document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("myModal");
    var abrirModal = document.getElementById("abrirModal")
    var cerrarModal = document.getElementsByClassName("close")[0];


    const radioPersonal = document.getElementById("publicacionPersonal");
    const radioInstituto = document.getElementById("publicacionInstituto");
    const institucionOpcional = document.querySelector(".institucion-opcional");

    institucionOpcional.style.display = "none";

    abrirModal.onclick = function(event) {
        event.preventDefault();
        modal.style.display = "block";
    }

    cerrarModal.onclick = function() {
        modal.style.display = "none";
    }

    function toggleInstitucionOpcional(){
        if(radioInstituto.checked){
            institucionOpcional.style.display = "block";
            console.log("Publiación personal");
        } else {
            institucionOpcional.style.display = "none";
            console.log("Publiación Instituto");
        }
    }

    radioPersonal.addEventListener("change", toggleInstitucionOpcional);
    radioInstituto.addEventListener("change", toggleInstitucionOpcional);

});
