const listarEscuelas = async () => {
    try{
        const response = await fetch('/escuelas/')
        const data = await response.json();

        if (data.message === 'Success'){
            // Limpi el contenido previo del select
            const setEscuelas = document.getElementById('listarEscuelas');
            setEscuelas.innerHTML = '<option value="0">Seleccione una Escuela</option>';

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
            const setDisciplinas = document.getElementById('listaCatagoriaPublicacion');
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

    abrirModalEditPublicacion.forEach(btn => {
        btn.addEventListener("click", (event) => {
            event.preventDefault();
            console.log("hola soy un modal");

            modalEditPublicacion.style.display = "block";
            document.body.style.overflow = "hidden";
        });
    });

    cerrarModalEditPublicacion.onclick = function(){
        modalEditPublicacion.style.display = "none";
        document.body.style.overflow = "auto";
    }

    btnCancelarModalEditPublicacion.onclick = function(){
        modalEditPublicacion.style.display = "none";
        document.body.style.overflow = "auto";
    }

    

});