const listarEscuelasEdit = async (id_actorEscuela, id_EscuelaActual) => {
    try{
        const response = await fetch(`/escuelaActor/${id_actorEscuela}`)
        const data = await response.json();

        if (data.message === 'Success'){
            // Limpi el contenido previo del select
            const setEscuelas = document.getElementById('listarEscuelasEdit');
            setEscuelas.innerHTML = '<option value="0">Seleccione una Escuela</option>';

            data.escuelas.forEach(escuela =>{
                const option = document.createElement('option');
                option.value = escuela.id;
                option.textContent = escuela.nombre_escuela;

                if(escuela.id === id_EscuelaActual){
                    option.selected = true;
                }

                setEscuelas.appendChild(option);
            });
        } else {
            console.log(data)
            console.log("Error: Respuesta inesperada de la API")
        }

    }catch(error){
        console.error("Error al obtener la lista de escuelas", error)
    }
}

const listarEscuelasSin = async () => {
    try{
        const response = await fetch('/escuelas/')
        const data = await response.json();

        if (data.message === 'Success'){
            const setEscuelas = document.getElementById('listarEscuelasEdit');
            setEscuelas.innerHTML = '<option value="0">Seleccione una Escuela</option>';

            data.escuelas.forEach(escuela =>{
                const option = document.createElement('option');
                option.value = escuela.id;
                option.textContent = escuela.nombre_escuela;

                setEscuelas.appendChild(option);
            });
        } else {
            console.log("Error: Respuesta inesperada de la API")
        }

    }catch(error){
        console.error("Error al obtener la lista de escuelas", error)
    }
}

const listarDisciplinasProyecto = async () => {
    try {
        const response = await fetch('/disciplinas/');
        const data = await response.json();

        if (data.message === 'Success') {
            // Limpia el contenido previo del select
            const setDisciplinas = document.getElementById('listaCatagoriaPublicacion');
            setDisciplinas.innerHTML = '<option value="0">Seleccione una Categoria</option>';

            data.Disciplinas.forEach(disciplina => {
                const option = document.createElement('option');
                option.value = disciplina.id;
                option.textContent = disciplina.nombre_disciplina;
                setDisciplinas.appendChild(option);
            });
        } else {
            console.error("Error: Respuesta inesperada de la API.");
        }
    } catch (error) {
        console.error("Error al obtener las Disciplinas:", error);
    }
};

const listarDisciplinasPublicaciones = async (id_disciplina) => {
    try {
        const response = await fetch('/disciplinas/');
        const data = await response.json();

        if (data.message === 'Success') {
            // Limpia el contenido previo del select
            const setDisciplinas = document.getElementById('listaCatagoriaPublicacionEdit');
            setDisciplinas.innerHTML = '<option value="0">Seleccione una Categoria</option>';

            data.Disciplinas.forEach(disciplina => {
                const option = document.createElement('option');
                option.value = disciplina.id;
                option.textContent = disciplina.nombre_disciplina;

                if (disciplina.id === id_disciplina){
                    option.selected = true;
                }

                setDisciplinas.appendChild(option);
            });
        } else {
            console.error("Error: Respuesta inesperada de la API.");
        }
    } catch (error) {
        console.error("Error al obtener las Disciplinas:", error);
    }
};

document.addEventListener("DOMContentLoaded", async () =>{

    /* PARTE DE LA EDICION DE DATOS */
    var modalEditPublicacion = document.getElementById("modalEditPublicacion");
    var abrirModalEditPublicacion = document.querySelectorAll(".abrirModalEditPublicacion");
    var cerrarModalEditPublicacion = document.getElementsByClassName("clsModalEditPublicacion")[0];
    var btnCancelarModalEditPublicacion = document.getElementById("btnCancelarEditPublicacion");

    //seccion para saber si es una publicacion personal o institucional
    const radioPersonalEdit = document.getElementById("publicacionPersonalEdit");
    const radioInstitutoEdit = document.getElementById("publicacionInstitutoEdit");
    const institucionOpcionalEdit = document.querySelector(".institucion-opcionalEdit");

    institucionOpcionalEdit.style.display = "none";

    abrirModalEditPublicacion.forEach(btn => {
        btn.addEventListener("click", async (event) => {
            event.preventDefault();
            const data_id = event.target.getAttribute("data-id");
            const data_autor = event.target.getAttribute("data-autor");
            let data_autor_id = event.target.getAttribute("data-autor-id");

            const response = await fetch(`/obtenerPublicacion/${data_id}`);
            const data = await response.json();

            if(data.message === "Success"){
                modalEditPublicacion.style.display = "block";
                document.body.style.overflow = "hidden";

                console.log(data)
                await listarDisciplinasPublicaciones(data.publicaciones[0].id_Disciplina_id);

                if (data.publicaciones[0].tipo_publicacion){
                    const id_Actor_Escuela = data.publicaciones[0].id_actor_id;
                    const id_EscuelaActual = data.publicaciones[0].id_Escuela_id;
                    await listarEscuelasEdit(id_Actor_Escuela, id_EscuelaActual);
                }else{
                    await listarEscuelasSin()
                }

                data.publicaciones.forEach(publicacion => {
                    document.getElementById("publicacion_id").value = publicacion.id;
                    if(data_autor_id != null){
                        document.getElementById("autor_id_publicacion_evento").value = data_autor_id;
                    }
                    document.getElementById("titulo_publicacion").value = publicacion.titulo_publicacion;
                    document.getElementById("autor_de_publicacion").value = data_autor;
                    document.getElementById("descripcion_publicacion").value = publicacion.descripcion_publicacion;
                    
                    if(publicacion.tipo_publicacion){
                        document.getElementById("publicacionInstitutoEdit").checked = true;
                        institucionOpcionalEdit.style.display = "block";
                    }else{
                        document.getElementById("publicacionPersonalEdit").checked = true;
                        console.log("Publicacion de tipo personal")
                        institucionOpcionalEdit.style.display = "none";
                    }


                    const urlOrigin = window.location.origin;
                    const previewImagen_edit = document.getElementById("previewImagenPublicacion_edit");
                    console.log(previewImagen_edit);
                    const btnFileImagen = document.getElementById("imagenPortada_edit");

                    previewImagen_edit.src = `${urlOrigin}/imagenes/${publicacion.url_imagen_publicacion}`;

                    btnFileImagen.addEventListener("change", function(event){
                        const file = event.target.files[0];

                        if (file){
                            if (file.type !== "image/jpeg" && file.type !== "image/jpg" && file.type !== "image/png" ){
                                alert("Solo se permiten archivos de tipo JPEG, JPEG o PNG");
                                event.target.value = ""
                                return;
                            }

                            const reader = new FileReader();
                            reader.onload = (e) => {
                                previewImagen_edit.src = e.target.result; // Mostrar la imagen seleccionada
                            };
                            reader.readAsDataURL(file);
                        }else{
                            previewImagen_edit.src = `${urlOrigin}/imagenes/${publicacion.url_imagen_publicacion}`;
                        }
                    });


                    data.ImagenesExtras.forEach((imgExtra, index) => {
                        const name = `previewImagenExtra_edit${index + 1}`;
                        const imgElementPreview = document.getElementById(name);
                        const containerImagenExtra = imgElementPreview?.parentElement;
                    
                        if (imgElementPreview) {
                            imgElementPreview.src = `${urlOrigin}/imagenes/${imgExtra.url_imagen}`;

                            const botonesExistentes = containerImagenExtra.querySelector('.btnEliminar');
                            if(botonesExistentes){
                                botonesExistentes.remove();
                            }
                    
                            // Crear el enlace "Eliminar"
                            const enlaceEliminar = document.createElement('a');
                            enlaceEliminar.href = `/quitarImagenExtraPublicacion/${publicacion.id}/${encodeURIComponent(imgExtra.url_imagen)}/`; // URL codificada
                            enlaceEliminar.textContent = 'Eliminar';
                            enlaceEliminar.classList.add('btnEliminar'); // Agregar estilos si es necesario
                    
                            // Agregar el enlace al contenedor
                            containerImagenExtra.appendChild(enlaceEliminar);
                        } else {
                            console.log(`Error: No se encontró el elemento con ID ${name}`);
                        }
                    });

                    // VALIDAR SI ESTA APROBADO O NO
                    if (publicacion.publicacion_aprobada){
                        document.getElementById("aprobarPublicacion").checked = true;
                    }else{
                        document.getElementById("aprobarPublicacion").checked = false;
                        document.getElementById("noAprobarPublicacion").checked = true;
                    }
                    
                });

            }else{
                console.log("Ocurrio un error al realizar la consulta")
            }
        });
    });

    cerrarModalEditPublicacion.onclick = function(){
        modalEditPublicacion.style.display = "none";
        institucionOpcionalEdit.style.display = "none";
        document.body.style.overflow = "auto";
    }

    btnCancelarModalEditPublicacion.onclick = function(){
        modalEditPublicacion.style.display = "none";
        institucionOpcionalEdit.style.display = "none"; 
        document.body.style.overflow = "auto";
    }

    function toggleInstitucionOpcionalEdit(){
        if  (radioInstitutoEdit.checked){
            institucionOpcionalEdit.style.display = "block";
        }else{
            institucionOpcionalEdit.style.display = "none";
            console.log(institucionOpcionalEdit.style.display);
        }
    }

    radioPersonalEdit.addEventListener("change", toggleInstitucionOpcionalEdit);
    radioInstitutoEdit.addEventListener("change", toggleInstitucionOpcionalEdit);

});