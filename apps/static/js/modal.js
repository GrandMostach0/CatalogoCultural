const listarEscuelas = async (id_actor) => {
    try{
        const response = await fetch(`/escuelaActor/${id_actor}`)
        const data = await response.json();

        if (data.message === 'Success'){
            // Limpi el contenido previo del select
            const setEscuelas = document.getElementById('listarEscuelas');
            setEscuelas.innerHTML = '<option value="0">Seleccione una Escuela</option>';

            console.log(data);
            // Agrega las nuevas opciones
            data.escuelas.forEach(escuela =>{
                const option = document.createElement('option');
                option.value = escuela.id;
                option.textContent = escuela.nombre_escuela;
                setEscuelas.appendChild(option);
            });
            console.log("Opciones cargadas correctamente.");
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
            const setDisciplinas = document.getElementById('listaCategoriaPublicacion');
            console.log(setDisciplinas)
            setDisciplinas.innerHTML = '<option value="0">Seleccione una Categoria</option>';

            data.Disciplinas.forEach(disciplina => {
                const option = document.createElement('option');
                option.value = disciplina.id;
                option.textContent = disciplina.nombre_disciplina;
                setDisciplinas.appendChild(option);
            });
            console.log("Opciones cargadas correctamente.");
        } else {
            console.error("Error: Respuesta inesperada de la API.");
        }
    } catch (error) {
        console.error("Error al obtener las Disciplinas:", error);
    }
};

document.addEventListener("DOMContentLoaded", async () => {
    var modal = document.getElementById("myModalPublicacion");
    var abrirModal = document.getElementById("abrirModalPublicacion");
    var cerrarModal = document.getElementsByClassName("close")[0];
    var btnCancelar = document.getElementById("btnCancelar");

    const radioPersonal = document.getElementById("publicacionPersonal");
    const radioInstituto = document.getElementById("publicacionInstituto");
    const institucionOpcional = document.querySelector(".institucion-opcional");

    institucionOpcional.style.display = "none";  // Asegúrate de que esté oculto al inicio

    abrirModal.addEventListener("click", async function(event){
        event.preventDefault();
        modal.style.display = "block";
        document.body.style.overflow = "hidden";

        const data_id = event.target.getAttribute("data-id");

        // --- Cargar la lista de escuelas ---
        await listarEscuelas(data_id);
        await listarDisciplinasProyecto();
    });

    cerrarModal.onclick = function() {
        modal.style.display = "none";
        institucionOpcional.style.display = "none";  // Ocultar la parte de institución opcional cuando se cierre
        document.body.style.overflow = "auto";
    }

    btnCancelar.onclick = function() {
        modal.style.display = "none";
        institucionOpcional.style.display = "none";  // Ocultar la parte de institución opcional al cancelar
        document.body.style.overflow = "auto";
    }

    // FUNCION PARA OCULTAR O MOSTRAR LA SELECCION DE LA ESCUELA
    function toggleInstitucionOpcional() {
        if (radioInstituto.checked) {
            institucionOpcional.style.display = "block";
        } else {
            institucionOpcional.style.display = "none";
        }
    }

    radioPersonal.addEventListener("change", toggleInstitucionOpcional);
    radioInstituto.addEventListener("change", toggleInstitucionOpcional);
});
