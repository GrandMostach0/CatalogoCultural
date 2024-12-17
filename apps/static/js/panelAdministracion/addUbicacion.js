// Esperar a que el DOM se cargue
document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("modalUbicación");
    var abrirModal = document.getElementById("abrirModalUbicacion");
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

    /* PARTE DE LA EDICION */
    var abirModalEditUbicacion = document.querySelectorAll(".abrirModalEditUbicacion");
    var abrirModalEdicionUbicacion = document.getElementById("modalUbicacionEdit");
    var btnCancelarEditubicacion = document.getElementById("btnCancelarEditubicacion");
    var cerrarModalEditUbicacion = document.getElementsByClassName("clsModUbicacionEdit")[0];

    abirModalEditUbicacion.forEach(btn => {
        btn.addEventListener("click", async (event) => {
            event.preventDefault();
            const data_id_atribute = event.target.getAttribute("data-id");
    
            try {
                const response = await fetch(`/getUbicacionRegistro/${data_id_atribute}`);
                const result = await response.json();

                if (result.message === "Success") {
                    console.log(result);

                    document.getElementById("ubicacion_id").value = result.Ubicaciones_comunes.id;
                    document.getElementById("nombre_ubicacion_edit").value = result.Ubicaciones_comunes.nombre_ubicacion;
                    document.getElementById("direccion_edit").value = result.Ubicaciones_comunes.direccion_ubicacion
;
                    document.getElementById("latitud_edit").value = result.Ubicaciones_comunes.latitud;
                    document.getElementById("longitud_edit").value = result.Ubicaciones_comunes.longitud;

                    abrirModalEdicionUbicacion.style.display = "block";
                    document.body.style.overflow = "hidden";

                } else {
                    console.log("Fallo esta chingadera");
                }
            } catch (error) {
                console.error("Error al obtener datos: ", error);
            }
        });
    });
    

    btnCancelarEditubicacion.onclick = function() {
        abrirModalEdicionUbicacion.style.display = "none";
        document.body.style.overflow = "auto";
    }

    cerrarModalEditUbicacion.onclick = function(){
        abrirModalEdicionUbicacion.style.display = "none";
        document.body.style.overflow = "auto";
    }

});