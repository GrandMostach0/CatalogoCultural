async function fetchRedesSociales() {
    try {
        const response = await fetch("/listaCatalogoRedes/");
        const data = await response.json();

        if (data.message === "Success") {
            return data.NombreRedesSociales; // Regresamos las opciones
        } else {
            console.log("No se encontraron las redes sociales.");
            return []; // Devolver un arreglo vacío en caso de fallo
        }
    } catch (error) {
        console.error("Error al obtener el catálogo", error);
        return []; // Devolver un arreglo vacío en caso de error
    }
}

async function cargarOpciones(selectElement) {
    const redesSociales = await fetchRedesSociales();
    if (redesSociales.length > 0) {
        redesSociales.forEach(red => {
            const option = document.createElement("option");
            option.value = red.id;
            option.textContent = red.nombre_redSocial;
            selectElement.appendChild(option);
        });
    }
}

let contadorRedes = document.querySelectorAll(".red-social").length; // Contar redes precargadas
const maxRedes = 4;

document.getElementById("btn-agregar").addEventListener("click", async () => {
    if (contadorRedes < maxRedes) {
        contadorRedes++;
        const container = document.getElementById("redes-container");

        // Crear nuevo campo
        const nuevaRed = document.createElement("div");
        nuevaRed.classList.add("red-social");
        nuevaRed.innerHTML = `
            <label for="redSocial${contadorRedes}">Red Social:</label>
            <select class="inputs" name="redSocial${contadorRedes}" id="redSocial${contadorRedes}">
                <option value="" selected>Selecciona una red social</option>
            </select>
            <label for="urlRed${contadorRedes}">URL:</label>
            <input type="url" class="inputs" name="urlRed${contadorRedes}" id="urlRed${contadorRedes}" placeholder="Ingresa la URL">
        `;

        container.appendChild(nuevaRed);

        // Si se alcanzó el máximo, deshabilitar botón
        if (contadorRedes === maxRedes) {
            document.getElementById("btn-agregar").disabled = true;
        }

        // Llenar opciones del select desde el catálogo
        const select = document.getElementById(`redSocial${contadorRedes}`);
        await cargarOpciones(select); // Asegurarse de esperar a que se carguen las opciones
    }
});

document.addEventListener("DOMContentLoaded", async function () {
    // Inicializar opciones para los selects precargados
    const selectsPrecargados = document.querySelectorAll(".red-social select");
    for (const select of selectsPrecargados) {
        await cargarOpciones(select); // Cargar opciones en los selects ya existentes
    }

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
});