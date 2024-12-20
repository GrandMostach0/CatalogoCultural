const listadoLocalidades = async (id_localidad) =>{
    try{
        const response = await fetch('/municipios/');
        const result = await response.json();

        if(result.message === 'Success'){
            const setListaLocalidades = document.getElementById("ListadoUbicaciones");

            result.Localidad.forEach(local => {
                const option = document.createElement("option");
                option.value = local.id;
                option.textContent = local.nombre_ubicacion;

                //validacion para maracr unicamente su localidad de la persona por mientras
                if(local.id === id_localidad){
                    option.selected = true;
                }

                setListaLocalidades.appendChild(option);
            });
        }else{
            console.log("Error al listar las opciones")
        }


    }catch(e){
        console.error("Error al obtener el listado", e)
    }
};




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


    /* SECCION DE LA EDICION DE LA ESCUELA */
    var btnAbrirModalEditEscuela = document.querySelectorAll(".btnAbrirModalEditEscuela");
    var abrirModalEditEscuela = document.getElementById("modalEditEscuela");
    var btnCancelarEditEscuela = document.getElementById("btnCancelarEditEscuela");
    var cerrarModalEditEscuela = document.getElementsByClassName("clsModEditEscuela")[0];

    btnAbrirModalEditEscuela.forEach(btn => {
        btn.addEventListener("click", async (event) => {
            event.preventDefault();
            var data_id_atribute = btn.getAttribute("data-id");

            try{
                const response = await fetch(`/editarEscuela/${data_id_atribute}`);
                const result = await response.json();
                if(result.message === "Success"){

                    console.log(result)

                    await listadoLocalidades(result.Escuela.id_localidad_id);

                    document.getElementById("escuela_id").value = result.Escuela.id;
                    document.getElementById("nombre_escuela_edit").value = result.Escuela.nombre_escuela;
                    if(result.Escuela.tipo_escuela){
                        document.getElementById("tipo_escuela_publica_edit").checked = true;
                    }else{
                        document.getElementById("tipo_escuela_privada_edit").checked = true;
                    }


                    document.getElementById("descripcion_escuela_edit").value = result.Escuela.descripcion;
                    document.getElementById("telefono_edit").value = result.Escuela.telefono_escuela;
                    document.getElementById("correo_edit").value = result.Escuela.correo_escuela;
                    

                    if(result.Escuela.ubicacion_escuela === null){
                        document.getElementById("direccion_edit_escuela").value = "No tiene registro";
                    }else{
                        document.getElementById("direccion_edit_escuela").value = result.Escuela.ubicacion_escuela;
                    }
                    document.getElementById("hora_atencion_edit").value = result.Escuela.hora_atencion;
                    //document.getElementById("responsable_escuela_edit").value = result.Escuela.;

                    abrirModalEditEscuela.style.display = "block";
                    document.body.style.overflow = "hidden";


                }else{
                    console.log("Fallo la carga o no se que pedo")
                }

            }catch(e){
                console.error("Error al obtener los datos", error)
            }
        });
    });

    btnCancelarEditEscuela.onclick = function() {
        abrirModalEditEscuela.style.display = "none";
        document.body.style.overflow = "auto";
    }

    cerrarModalEditEscuela.onclick = function() {
        abrirModalEditEscuela.style.display = "none";
        document.body.style.overflow = "auto";
    }

    

});