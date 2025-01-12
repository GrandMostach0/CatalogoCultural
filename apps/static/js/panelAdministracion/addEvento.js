const listarClasificaciones = async (clasificacionPublicacion) => {
    try {
        const response = await fetch('/audiencia/');
        const data = await response.json();

        if (data.message === 'Success') {
            // Limpia el contenido previo del select
            const setClasificaciones = document.getElementById('Listacategoria_Edit');
            setClasificaciones.innerHTML = '<option value="0">Seleccione la Categoría</option>';

            // Agrega las nuevas opciones
            data.NombreClasificacion.forEach(clasificacion => {
                const option = document.createElement('option');
                option.value = clasificacion.id;
                option.textContent = clasificacion.nombre_clasificacion;

                if(clasificacion.id === clasificacionPublicacion){
                    option.selected = true;
                }

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

const listarDisciplinas = async (disciplinaPublicacion) => {
    try {
        const response = await fetch('/disciplinas/');
        const data = await response.json();

        if (data.message === 'Success') {
            // Limpia el contenido previo del select
            const setDisciplinas = document.getElementById('ListaClasificacionEdit');
            setDisciplinas.innerHTML = '<option value="0">Seleccione una Categoria</option>';

            data.Disciplinas.forEach(disciplina => {
                const option = document.createElement('option');
                option.value = disciplina.id;
                option.textContent = disciplina.nombre_disciplina;

                if(disciplina.id === disciplinaPublicacion){
                    option.selected = true;
                }

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

const listarUbicaciones = async (ubicacionPublicacion) => {
    try {
        const response = await fetch('/ubicaciones/');
        const data = await response.json();

        if (data.message === 'Success') {
            // Limpia el contenido previo del select
            const setUbicaciones = document.getElementById('listaUbicacionesEdit');
            setUbicaciones.innerHTML = '<option value="0">Seleccione una Ubicacion</option>';

            data.ubicacion.forEach(ubicacione => {
                const option = document.createElement('option');
                option.value = ubicacione.id;
                option.textContent = ubicacione.nombre_ubicacion;

                if(ubicacione.id === ubicacionPublicacion){
                    option.selected = true;
                }

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
    const eventoPaga = document.getElementById("eventoPaga_edit");
    const precioUnitario = document.querySelector('.precioUnitarioEdit');
    const subOpciones = document.querySelector('.subOpciones4');

    precioUnitario.style.display = 'none';
    subOpciones.style.display = 'none';

    console.log("PRECION UNITARIO " + precioUnitario.style.display);
    console.log("SUB OPCIONES DEPENDIENTES DEL ANTERIOR " + subOpciones.style.display);

    // --- Dinámica del punto de venta ---
    const presencial = document.getElementById('puntoVentaPresencial_edit');
    const digital = document.getElementById('puntoVentaDigital_edit');
    const urlinput = document.querySelector('.URLPuntoVentalblEdit');

    urlinput.style.display = 'none';

    // --- Funcionalidad del Modal ---
    abrirModalEventoEdit.forEach(btn =>{
        btn.addEventListener("click", async (event) =>{
            event.preventDefault();
            const data_id = event.target.getAttribute("data-id");
            const data_autor = event.target.getAttribute("data-autor");

            try{
                const response = await fetch(`/obtenerPublicacionEvento/${data_id}`)
                const data = await response.json();

                if (data.message === "Success"){
                    console.log(data)

                    // --- Cargar clasificaciones ---
                    await listarClasificaciones(data.publicaciones[0].id_clasificacion_id);
                    await listarDisciplinas(data.publicaciones[0].id_disciplina_id);
                    await listarUbicaciones(data.publicaciones[0].id_ubicacionesComunes_id);

                    modalEventoEdit.style.display = "block";
                    document.body.style.overflow = "hidden";

                    data.publicaciones.forEach(publicacion => {
                        document.getElementById("id_publicacion").value = data_id;
                        document.getElementById("titulo_evento").value = publicacion.titulo_publicacion;
                        document.getElementById("autor_publicacion").value = data_autor;
                        document.getElementById("descripcion_evento_edit").value = publicacion.descripcion_publicacion;
                        document.getElementById("fechaEvento_edit").value = publicacion.fecha_inicio;
                        document.getElementById("horaInicioEvento_edit").value = publicacion.hora_inicio;

                        precio = Number(publicacion.precio_evento);
                        if(precio > 0){
                            document.getElementById("eventoPaga_edit").checked = true;
                            document.getElementById("precioCU_edit").value = precio;
                            precioUnitario.style.display = "block";
                            subOpciones.style.display = "block";
                        }else{
                            document.getElementById("eventoPaga_edit").checked = false;
                            document.getElementById("precioCU_edit").value = 0;
                            precioUnitario.style.display = "none";
                            subOpciones.style.display = "none";
                            urlinput.style.display = 'none';
                            
                        }

                        const lugarVenta = publicacion.puntoVenta;
                        console.log(lugarVenta)
                        if(lugarVenta === "digital"){
                            document.getElementById("puntoVentaDigital_edit").checked = true;
                            document.getElementById("URLPuntoVenta_edit").value = publicacion.enlace_venta;
                            urlinput.style.display = 'block';
                        }else if(lugarVenta === "presencial"){
                            document.getElementById("puntoVentaPresencial_edit").checked = true;
                            document.getElementById("URLPuntoVenta_edit").value = publicacion.enlace_venta;
                            urlinput.style.display = 'none';
                        }else{
                            document.getElementById("puntoVentaDigital_edit").value = true;
                        }

                        if(publicacion.publicacion_aprobada = false){
                            document.getElementById("noAprobarPublicacion").checked = false;
                            document.getElementById("aprobarPublicacion").checked = true;
                        }else{
                            document.getElementById("aprobarPublicacion").checked = false;
                            document.getElementById("noAprobarPublicacion").checked = true;
                        }
                        console.log("que pedo panita: " + urlinput.style.display);
                    });
                }else{
                    console.log("Ocurrio un error al obtener el dato")
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
