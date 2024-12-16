// Esperar a que el DOM se cargue
document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("modalUbicación");
    var abrirModal = document.getElementById("abrirModalUbicacion");
    var abirModalEditUbicacion = document.querySelectorAll(".abrirModalEditUbicacion");
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

    abirModalEditUbicacion.forEach(btn => {
        btn.addEventListener("click", async (event) => {
            event.preventDefault();
            const data_id_atribute = event.target.getAttribute("data-id");
    
            try {
                const response = await fetch(`/getUbicacionRegistro/${data_id_atribute}`);
                const result = await response.json();

                if (result.message === "Success") {
                    console.log(result);
                } else {
                    console.log("Fallo esta chingadera");
                }
            } catch (error) {
                console.error("Error al obtener datos: ", error);
            }
        });
    });
    

});