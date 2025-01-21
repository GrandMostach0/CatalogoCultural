const listarEscuelasPerfil = async (id_actor) => {
    try{
        const response = await fetch(`/escuelaActor/${id_actor}`)
        const data = await response.json();
        console.log(data);
        
        const radioPersonal = document.getElementById("publicacionPersonal");
        console.log(radioPersonal);
        const radioInstituto = document.getElementById("publicacionInstituto");
        console.log(radioInstituto);
        const institucionOpcional = document.querySelector(".institucion-opcional");

        if (data.message === 'Success'){
            const setEscuelas = document.getElementById('listarEscuelas');
            setEscuelas.innerHTML = '<option value="0">Seleccione una Escuela</option>';

            console.log(data);
            data.escuelas.forEach(escuela =>{
                const option = document.createElement('option');
                option.value = escuela.id;
                option.textContent = escuela.nombre_escuela;
                setEscuelas.appendChild(option);
            });
            console.log("Opciones cargadas correctamente.");
        } else {
            radioInstituto.disabled = true;
            radioPersonal.checked = true;
            institucionOpcional.style.display = "none";
            console.log("Error: Respuesta inesperada de la API")
        }

    }catch(error){
        console.error("Error al obtener la lista de escuelas", error)
    }
}

const listarDisciplinasProyectoPerfil = async () => {
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

    institucionOpcional.style.display = "none";

    abrirModal.addEventListener("click", async function(event){
        event.preventDefault();
        modal.style.display = "block";
        document.body.style.overflow = "hidden";

        const data_id = event.target.getAttribute("data-id");

        // --- Cargar la lista de escuelas ---
        await listarEscuelasPerfil(data_id);
        await listarDisciplinasProyectoPerfil();

        const imagenPreview = document.getElementById("previewImagen_edit");
        const btnImagenPreview = document.getElementById("imagenPortada");

        btnImagenPreview.addEventListener("change", function(event){
            const file = event.target.files[0];

            if(file){
                if (file.type !== "image/jpeg" && file.type !== "image/jpg" && file.type !== "image/png") {
                    alert("Solo se permiten archivos de tipo JPG, JPEG y PNG");
                    event.target.value = ""; // Limpia el input correctamente
                    return;
                }

                const reader = new FileReader();
                reader.onload = (e) => {
                    imagenPreview.src = e.target.result;
                };
                reader.readAsDataURL(file)
            } else {
                imagenPreview.src = "#";
            }
        });

        const inputs = document.querySelectorAll('input[type="file"]');
        inputs.forEach(input =>{
            input.addEventListener("change", function(e){
                const file = e.target.files[0]; // Obtiene el archivo seleccionado
                const previewId = `preview${input.id.charAt(0).toUpperCase() + input.id.slice(1)}`; 
                const previewImg = document.getElementById(previewId);

                if (!previewImg) {
                    console.error(`No se encontró un elemento con el ID: ${previewId}`);
                    return; // Evita continuar si no existe el elemento
                }

                if (file) {
                    // Validar el tipo de archivo
                    if (file.type !== "image/jpeg" && file.type !== "image/jpg" && file.type !== "image/png") {
                        alert("Solo se permiten archivos de tipo JPG, JPEG y PNG");
                        e.target.value = ""; // Limpia el input
                        return;
                    }

                    // Crear una vista previa con FileReader
                    const reader = new FileReader();
                    reader.onload = function (e) {
                        previewImg.src = e.target.result; // Asigna la imagen al src
                    };
                    reader.readAsDataURL(file);
                } else {
                    previewImg.src = "#"; // Limpia la vista previa si no hay archivo
                }
            });
        });

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
