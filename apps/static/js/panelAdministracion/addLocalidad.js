// Esperar a que el DOM se cargue
document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("modalLocalidad");
    var abrirModal = document.getElementById("abrirModalLocalidad");
    var cerrarModal = document.getElementsByClassName("clsModLocalidad")[0];
    var btnCancelar = document.getElementById("btnCancelarLocalidad");

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
    var abirModalEditLocalidad = document.querySelectorAll(".abrirModalEditLocalidad");
    var abrirModalEdicionLocalidad = document.getElementById("modalEditLocalidad");
    var btnCancelarEditLocalidad = document.getElementById("btnCancelarEditLocalidad");
    var cerrarModalEditLocalidad = document.getElementsByClassName("clsModEditLocalidad")[0];

    abirModalEditLocalidad.forEach(btn => {
        btn.addEventListener("click", async (event) => {
            event.preventDefault();
            const data_id_atribute = event.target.getAttribute("data-id");
    
            try {
                const response = await fetch(`/getLocalidad/${data_id_atribute}`);
                const result = await response.json();

                if (result.message === "Success") {
                    console.log(result);

                    document.getElementById("localidadEdit_id").value = result.Localidad.id;
                    document.getElementById("nombre_editlocalidad").value = result.Localidad.nombre_ubicacion;

                    abrirModalEdicionLocalidad.style.display = "block";
                    document.body.style.overflow = "hidden";

                } else {
                    console.log("Fallo esta chingadera");
                }
            } catch (error) {
                console.error("Error al obtener datos: ", error);
            }
        });
    });
    

    btnCancelarEditLocalidad.onclick = function() {
        abrirModalEdicionLocalidad.style.display = "none";
        document.body.style.overflow = "auto";
    }

    cerrarModalEditLocalidad.onclick = function(){
        abrirModalEdicionLocalidad.style.display = "none";
        document.body.style.overflow = "auto";
    }

});