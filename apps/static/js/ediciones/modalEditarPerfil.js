async function fetchRedesSociales() {
    try {
        const response = await fetch("/listaCatalogoRedes/");
        const data = await response.json();

        if (data.message === "Success") {
            return data.NombreRedesSociales;
        } else {
            console.log("No se encontraron las redes sociales.");
            return []; // Devolver un arreglo vacío en caso de fallo
        }
    } catch (error) {
        console.error("Error al obtener el catálogo", error);
        return []; // Devolver un arreglo vacío en caso de error
    }
}

const cargaInicial = async() => {
    await fetchRedesSociales();
}

document.addEventListener("DOMContentLoaded", async function () {
    // Manejo del modal
    var modal = document.getElementById("editarPerfilModal");
    var abrirModal = document.getElementById("abrirEditarPerfilModal");
    var cerrarModal = document.getElementsByClassName("close")[2];
    var btnCerrarModal = document.getElementById("btnCancelar3");

    abrirModal.onclick = function (event) {
        event.preventDefault();
        modal.style.display = "block";
        document.body.style.overflow = "hidden";
    };

    cerrarModal.onclick = function () {
        modal.style.display = "none";
        document.body.overflow = "auto";
    };

    btnCerrarModal.onclick = function () {
        modal.style.display = "none";
        document.body.overflow = "auto";
    };

    await cargaInicial();

});