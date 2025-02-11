const listarClasificaciones = async () => {
    try {
        const response = await fetch('/audiencia/');
        const data = await response.json();

        if (data.message === 'Success') {
            // Limpia el contenido previo del select
            const setClasificaciones = document.getElementById('Listaclasificacion');
            setClasificaciones.innerHTML = '<option value="0">Seleccione la Categoría</option>';

            // Agrega las nuevas opciones
            data.NombreClasificacion.forEach(clasificacion => {
                const option = document.createElement('option');
                option.value = clasificacion.id;
                option.textContent = clasificacion.nombre_clasificacion;
                setClasificaciones.appendChild(option);
            });
            // console.log("Opciones cargadas correctamente.");
        } else {
            console.error("Error: Respuesta inesperada de la API.");
        }
    } catch (error) {
        console.error("Error al obtener las clasificaciones:", error);
    }
};

const listarDisciplinas = async () => {
    try {
        const response = await fetch('/disciplinas/');
        const data = await response.json();

        if (data.message === 'Success') {
            // Limpia el contenido previo del select
            const setDisciplinas = document.getElementById('Listacategoria');
            setDisciplinas.innerHTML = '<option value="0">Seleccione una Categoria</option>';

            data.Disciplinas.forEach(disciplina => {
                const option = document.createElement('option');
                option.value = disciplina.id;
                option.textContent = disciplina.nombre_disciplina;
                setDisciplinas.appendChild(option);
            });
             // console.log("Opciones cargadas correctamente.");
        } else {
            console.error("Error: Respuesta inesperada de la API.");
        }
    } catch (error) {
        console.error("Error al obtener las Disciplinas:", error);
    }
};

const listarUbicaciones = async () => {
    try {
        const response = await fetch('/ubicaciones/');
        const data = await response.json();

        if (data.message === 'Success') {
            // Limpia el contenido previo del select
            const setUbicaciones = document.getElementById('ListaUbicaciones');
            setUbicaciones.innerHTML = '<option value="0">Seleccione una Ubicacion</option>';

            data.ubicacion.forEach(ubicacione => {
                const option = document.createElement('option');
                option.value = ubicacione.id;
                option.textContent = ubicacione.nombre_ubicacion;
                setUbicaciones.appendChild(option);
            });
            // console.log("Opciones cargadas correctamente.");
        } else {
            console.error("Error: Respuesta inesperada de la API.");
        }

    } catch (error) {
        console.error("Error al obtener las Disciplinas:", error);
    }
};

document.addEventListener("DOMContentLoaded", async () => {
    const modal = document.getElementById("myModalProyecto");
    const abrirModal = document.getElementById("abrirModalProyecto");
    var cerrarModal = document.getElementsByClassName("close")[1];
    const btnCancelar = document.getElementById("btnCancelar2");

    // --- Dinámica para saber si es de paga ---
    const eventoPaga = document.getElementById("eventoPaga");
    const precioUnitario = document.querySelector('.precioUnitario');
    const subOpciones = document.querySelector('.subOpciones2');

    precioUnitario.style.display = 'none';
    subOpciones.style.display = 'none';

    console.log("PRECION UNITARIO " + precioUnitario.style.display);
    console.log("SUB OPCIONES DEPENDIENTES DEL ANTERIOR " + subOpciones.style.display);

    // --- Dinámica del punto de venta ---
    const presencial = document.getElementById('puntoVentaPresencial');
    const digital = document.getElementById('puntoVentaDigital');
    const ambos = document.getElementById('puntoVentaAmbos');
    const urlinput = document.querySelector('.URLPuntoVentalbl');

    urlinput.style.display = 'none';

    // --- Funcionalidad del Modal ---
    abrirModal.addEventListener("click", async function (event) {
        event.preventDefault();
        modal.style.display = "block";
        document.body.style.overflow = "hidden";
        // --- Cargar clasificaciones ---
        await listarClasificaciones();
        await listarDisciplinas();
        await listarUbicaciones();

        const previewImagenPortada = document.getElementById("previewImagenEvento");
        const btnImageFile = document.getElementById("imagenPortadaEvento");

        btnImageFile.addEventListener("change", function(event){
            const file = event.target.files[0];

            if(file){
                if (file.type !== "image/jpeg" && file.type !== "image/jpg" && file.type !== "image/png") {
                    alert("Solo se permiten archivos de tipo JPG, JPEG y PNG");
                    event.target.value = ""; // Limpia el input correctamente
                    return;
                }

                const reader = new FileReader();
                reader.onload = (e) => {
                    previewImagenPortada.src = e.target.result;
                };
                reader.readAsDataURL(file)
            }else{
                previewImagenPortada.src = "#"
            }
        });

    });

    cerrarModal.onclick = function () {
        modal.style.display = "none";
        urlinput.style.display = 'none';
        precioUnitario.style.display = 'none';
        document.body.style.overflow = "auto";
    };

    btnCancelar.onclick = function () {
        modal.style.display = "none";
        urlinput.style.display = 'none';
        precioUnitario.style.display = 'none';
        document.body.style.overflow = "auto";
    };

    // Función para cerrar y restablecer estado
    const resetModalState = () => {
        modal.style.display = "none";
        urlinput.style.display = 'none';
        precioUnitario.style.display = 'none';
        subOpciones.style.display = 'none';
        eventoPaga.checked = false; // Restablece el checkbox
        document.body.style.overflow = "auto";
    };

    cerrarModal.onclick = resetModalState;
    btnCancelar.onclick = resetModalState;

    // --- Funcionalidades dinámicas ---
    eventoPaga.addEventListener("change", () => {
        if (eventoPaga.checked) {
            console.log("PAGO")
            precioUnitario.style.display = "block";
            subOpciones.style.display = "block";
        } else {
            console.log("GRATIS")
            precioUnitario.style.display = "none";
            subOpciones.style.display = "none";
        }
    });

    presencial.addEventListener("change", () => {
        urlinput.style.display = "none";
    });

    digital.addEventListener("change", () => {
        urlinput.style.display = "block";
    });
    
    ambos.addEventListener("change", () => {
        urlinput.style.display = "block";
    });
});
