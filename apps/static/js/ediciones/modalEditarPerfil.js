const listaRedes = async (selectId, red_actor) =>{
    try{
        const response = await fetch('/listaCatalogoRedes/');
        const data = await response.json();
        //console.log(data);

        if(data.message === 'Success'){
            const setListaRedes = document.getElementById(selectId);
            setListaRedes.innerHTML = '<option value="0"> Seleccione una Red Social </option>'

            data.NombreRedesSociales.forEach(red =>{
                const option = document.createElement('option');
                option.value = red.id;
                option.textContent = red.nombre_redSocial;

                // Marcar la opción correspondiente como seleccionado por defecto
                if (red.id === red_actor){
                    option.selected = true;
                }

                setListaRedes.appendChild(option);
            });

            //console.log(`opciones cargadas correctamente para ${selectId}`);

        } else if(data.message === 'Not Found') {
            const setListaRedes = document.getElementById(selectId);
            setListaRedes.innerHTML = '<option value="0"> Seleccione una Red Social </option>'

            data.NombreRedesSociales.forEach(red =>{
                const option = document.createElement('option');
                option.value = red.id;
                option.textContent = red.nombre_redSocial;
                setListaRedes.appendChild(option);
            });
        }else{
            console.log("Error: Respuesta inesperada de la API");
        }

    }catch(error){
        console.log("Error: ", error);
    }
}

document.addEventListener("DOMContentLoaded", async function () {
    // Manejo del modal
    var modal = document.getElementById("editarPerfilModal");
    var abrirModal = document.getElementById("abrirEditarPerfilModal");
    var cerrarModal = document.getElementsByClassName("close")[2];
    var btnCerrarModal = document.getElementById("btnCancelar3");

    abrirModal.addEventListener("click", async function(event){
        event.preventDefault();
        modal.style.display = "block";
        document.body.style.overflow = "hidden";
        const data_atribute = abrirModal.getAttribute("data-id");

        try{
            const response = await fetch(`/getUsuario/${data_atribute}`);
            const data = await response.json();

            const responseRedes = await fetch(`/getRedesSociales/${data_atribute}`)
            const dataRedes = await responseRedes.json();
            console.log(dataRedes)
            
            if(data.message === "Success"){
                console.log(data)
                /* INGRENSANDO LOS DATOS DEL PERFIL */
                document.getElementById("nombre").value = data.Actor.nombre_Actor;
                document.getElementById("primerApellido").value = data.Actor.primer_apellido_Actor;
                document.getElementById("segundoApellido").value = data.Actor.segundo_apellido_Actor;
                document.getElementById("biografia").value = data.Actor.biografia_Actor;
                document.getElementById("correo_publico").value = data.Actor.correo_publico_Actor;
                document.getElementById("correo_privado").value = data.Actor.correo_privado_actor;
                document.getElementById("telefono_publico").value = data.Actor.Telefono_publico_Actor;
                document.getElementById("telefono_privado").value = data.Actor.Telefono_privado_actor;

                /* LISTAR LAS REDES SOCIALES DEL PERFIL */
                if(dataRedes.message === "Success"){
                    for (let i = 0; i < 3; i++){
                        const redSocial = dataRedes.RedSocial[i];
                        console.log(redSocial)
                        if(redSocial){
                            const selectId = `listaRedSocial0${i + 1}`;
                            await listaRedes(selectId, redSocial.id_redSocial_id);
                            document.getElementById(`redSocial0${i + 1}`).value = redSocial.enlace_redSocial;
                        }else{
                            console.log("nadota")
                        }
                    }
                }else if(dataRedes.message === "Not Found"){
                    console.log("No se encontro las redes sociales del pana")
                    for (let i = 0; i < 3; i++){
                        const selectId = `listaRedSocial0${i + 1}`;
                        await listaRedes(selectId, 0);
                    }
                }

            }else{
                console.log("Erro al obtener el dato")
            }
    
        }catch(error){
            console.log("Error: ", error);
        }
        
    });


    cerrarModal.onclick = function () {
        modal.style.display = "none";
        document.body.overflow = "auto";
    };

    btnCerrarModal.onclick = function () {
        modal.style.display = "none";
        document.body.overflow = "auto";
    };

});