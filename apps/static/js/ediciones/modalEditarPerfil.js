const listaRedes = async () =>{
    try{
        const response = await fetch('/listaCatalogoRedes/');
        const data = await response.json();

        console.log(data);

        if(data.message === 'Success'){
            const setListaRedes = document.getElementById('listaRedSocial01');
            setListaRedes.innerHTML = '<option value="0"> Seleccione una Red Social </option>'

            data.NombreRedesSociales.forEach(red =>{
                const option = document.createElement('option');
                option.value = red.id;
                option.textContent = red.nombre_redSocial;
                setListaRedes.appendChild(option);
            });

            console.log("opciones cargadas correctamente.");

        } else {
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

        // --- LISTA DE LAS REDES SOCIALES ---
        await listaRedes();
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