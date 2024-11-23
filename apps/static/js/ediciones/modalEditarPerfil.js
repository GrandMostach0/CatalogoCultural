const listarCatalogoRedesSociales = async() => {
    try {
        const response = await fetch("catalogoSocial/")
        const data2 = await response.json();
        console.log(data2);
    }catch(error){
        console.log(error);
    }
}

const cargaInicial = async() => {
    await listarCatalogoRedesSociales();
}

window.addEventListener("load", async () => {
    await listarCatalogoRedesSociales();
});


document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("editarPerfilModal");
    var abrirModal = document.getElementById("abrirEditarPerfilModal");
    var cerrarModal = document.getElementsByClassName("close")[2]; // no cambiar por que es el tercel modal que tengo dentro
    var btnCerrarModal = document.getElementById("btnCancelar3");
    var agregarRedSocialBtn = document.getElementById("agregar-red-social");
    var redesSocialesContainer = document.getElementById("redes-sociales-container");

    abrirModal.onclick = function(event) {
        event.preventDefault();
        modal.style.display = "block";
        document.body.style.overflow = "hidden";
    }

    cerrarModal.onclick = function() {
        modal.style.display = "none";
        document.body.overflow = "auto";
    }

    btnCerrarModal.onclick = function(){
        modal.style.display = "none";
        document.body.overflow = "auto";
    }

    // Agregar una nueva red social dinámicamente
    agregarRedSocialBtn.onclick = function() {
        console.log("Agregar una nueva red social dinámicament");
         
        // Crear un nuevo contenedor para la red social
        var nuevaRedSocial = document.createElement("div");
        nuevaRedSocial.classList.add("redes-sociales");

        // Crear el select y el input de URL
        var selectRedSocial = document.createElement("select");
        selectRedSocial.classList.add("redes-select");
        selectRedSocial.name = "red_social[]";

        // Crear las opciones de redes sociales registradas
        var opciones = '';

        selectRedSocial.innerHTML = opciones;

        var inputUrlRedSocial = document.createElement("input");
        inputUrlRedSocial.type = "url";
        inputUrlRedSocial.name = "url_red_social[]"; // Asegúrate de que el nombre sea el mismo para todos los campos
        inputUrlRedSocial.classList.add("url-input");
        inputUrlRedSocial.placeholder = "Ingrese la URL";

        // Añadir los elementos al nuevo contenedor
        nuevaRedSocial.appendChild(selectRedSocial);
        nuevaRedSocial.appendChild(inputUrlRedSocial);

        // Añadir el nuevo contenedor al contenedor de redes sociales
        redesSocialesContainer.appendChild(nuevaRedSocial);
    }
});