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
    const modalEventoEdit = document.getElementById("modalEventoEdit");
    const abrirModalEventoEdit = document.querySelectorAll(".btnAbrirModalEditEvento");
    const cerrarModalEventoEdit = document.getElementsByClassName("clsModalEditEvento")[0];
    const btnCancelarEventoEdit = document.getElementById("btnCancelarEditEvento");

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
    const urlinput = document.querySelector('.URLPuntoVentalbl');

    urlinput.style.display = 'none';

    // --- Funcionalidad del Modal ---
    abrirModalEventoEdit.forEach(btn =>{
        btn.addEventListener("click", async (event) =>{
            event.preventDefault();
            const data_id = event.target.getAttribute("data-id");
            const data_autor = event.target.getAttribute("data-autor");

            console.log(data_id)
            // --- Cargar clasificaciones ---
            //await listarClasificaciones();
            //await listarDisciplinas();
            //await listarUbicaciones();
            try{
                const response = await fetch(`/obtenerPublicacionEvento/${data_id}`)
                const data = await response.json();

                if (data.message === "Success"){
                    console.log(data)

                    modalEventoEdit.style.display = "block";
                    document.body.style.overflow = "hidden";

                    data.publicaciones.forEach(publicacion => {
                        document.getElementById("id_publicacion").value = data_id;
                        document.getElementById("titulo_evento").value = publicacion.titulo_publicacion;
                        document.getElementById("autor_publicacion").value = data_autor;
                        document.getElementById("decripcion_evento_edit").value = publicacion.descripcion_publicacion;
                        document.getElementById("fecha_evento_edit").value = publicacion.fecha_publicacion;
                        document.getElementById("horaInicioEvento_edit")
                        document.getElementById("eventoPaga_edit")
                        document.getElementById("precioCU_edit")
                    });
                }else{
                    console.log("Ocurrio un error al obtener el dato")
                    console.log(data)
                }

            }catch (e){
                console.log("Error", e)
            }
        
        })
    });

    cerrarModalEventoEdit.onclick = function () {
        modalEventoEdit.style.display = "none";
        urlinput.style.display = 'none';
        precioUnitario.style.display = 'none';
        document.body.style.overflow = "auto";
    };

    btnCancelarEventoEdit.onclick = function () {
        modalEventoEdit.style.display = "none";
        urlinput.style.display = 'none';
        precioUnitario.style.display = 'none';
        document.body.style.overflow = "auto";
    };

    // Función para cerrar y restablecer estado
    const resetModalState = () => {
        modalEventoEdit.style.display = "none";
        urlinput.style.display = 'none';
        precioUnitario.style.display = 'none';
        subOpciones.style.display = 'none';
        eventoPaga.checked = false; // Restablece el checkbox
        document.body.style.overflow = "auto";
    };

    cerrarModalEventoEdit.onclick = resetModalState;
    btnCancelarEventoEdit.onclick = resetModalState;

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
});
