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

});