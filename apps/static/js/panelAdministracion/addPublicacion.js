const listarEscuelas = async (id_actorEscuela, id_EscuelaActual) => {
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
    var modal = document.getElementById("myModalPublicacion");
    var abrirModal = document.getElementById("abrirModalPublicacion");
    var cerrarModal = document.getElementsByClassName("close")[0];
    var btnCancelar = document.getElementById("btnCancelar");


    const radioPersonal = document.getElementById("publicacionPersonal");
    const radioInstituto = document.getElementById("publicacionInstituto");
    const institucionOpcional = document.querySelector(".institucion-opcional");

    institucionOpcional.style.display = "none";

    abrirModal.addEventListener("click", async function(event){
        event.preventDefault();
        modal.style.display = "block";
        document.body.style.overflow = "hidden";

        // --- Cargar la lista de escuelas ---
        await listarEscuelas();
        await listarDisciplinasProyecto();
    });

    cerrarModal.onclick = function() {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }

    btnCancelar.onclick = function() {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }

    function toggleInstitucionOpcional(){
        if(radioInstituto.checked){
            institucionOpcional.style.display = "block";
        } else {
            institucionOpcional.style.display = "none";
        }
    }

    radioPersonal.addEventListener("change", toggleInstitucionOpcional);
    radioInstituto.addEventListener("change", toggleInstitucionOpcional);

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

            const response = await fetch(`/obtenerPublicacion/${data_id}`);
            const data = await response.json();

            if(data.message === "Success"){
                console.log(data)
                await listarDisciplinasPublicaciones(data.publicaciones[0].id_Disciplina_id);

                if (data.publicaciones[0].tipo_publicacion){
                    const id_Actor_Escuela = data.publicaciones[0].id_actor_id;
                    const id_EscuelaActual = data.publicaciones[0].id_Escuela_id;
                    await listarEscuelas(id_Actor_Escuela, id_EscuelaActual);
                }else{
                    await listarEscuelasSin()
                }

                data.publicaciones.forEach(publicacion => {
                    document.getElementById("publicacion_id").value = publicacion.id;
                    document.getElementById("titulo_publicacion").value = publicacion.titulo_publicacion;
                    document.getElementById("autor_de_publicacion").value = data_autor;
                    document.getElementById("descripcion_publicacion").value = publicacion.descripcion_publicacion;
                    
                    if(publicacion.tipo_publicacion){
                        document.getElementById("publicacionInstitutoEdit").checked = true;
                        institucionOpcionalEdit.style.display = "block";
                    }else{
                        document.getElementById("publicacionPersonalEdit").checked = true;
                        institucionOpcionalEdit.style.display = "none";
                    }

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

            modalEditPublicacion.style.display = "block";
            document.body.style.overflow = "hidden";
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
            console.log(institucionOpcionalEdit.style.display);
        }
    }

    radioPersonalEdit.addEventListener("change", toggleInstitucionOpcionalEdit);
    radioInstitutoEdit.addEventListener("change", toggleInstitucionOpcionalEdit);

});