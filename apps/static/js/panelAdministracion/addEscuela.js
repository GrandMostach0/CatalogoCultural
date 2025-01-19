const listadoLocalidades = async (id_localidad, nameSelect) => {
    try {
        const response = await fetch('/municipios/');
        const result = await response.json();
        console.log(result);

        if (result.message === 'Success') {
            const setListaLocalidades = document.getElementById(nameSelect);
            console.log(setListaLocalidades);

            // Limpiar las opciones existentes
            setListaLocalidades.innerHTML = "";

            result.Localidad.forEach(local => {
                const option = document.createElement("option");
                option.value = local.id;
                option.textContent = local.nombre_ubicacion;

                // Marcar la opción correspondiente como seleccionada
                if (local.id === id_localidad) {
                    option.selected = true;
                }

                setListaLocalidades.appendChild(option);
            });
        } else {
            console.log("Error al listar las opciones");
        }
    } catch (e) {
        console.error("Error al obtener el listado", e);
    }
};

// Escuchar eventos del DOM
document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("modalAddEscuela");
    const abrirModal = document.getElementById("abrirModalEscuela");
    const cerrarModal = document.getElementsByClassName("clsModEscuela")[0];
    const btnCancelar = document.getElementById("btnCancelar"); 

    abrirModal.onclick = async function (event) {
        event.preventDefault();

        const portadaInput = document.getElementById("imagen_portada");
        const portadaPreview = document.getElementById("previewImagen");

        portadaInput.addEventListener("change", function (e) {
            const file = e.target.files[0]; // Obtén el archivo seleccionado

            if (file) {
                // Valida el tipo de archivo
                if (file.type !== "image/jpeg" && file.type !== "image/jpg" && file.type !== "image/png") {
                    alert("Solo se permiten archivos de tipo JPG, JPEG y PNG");
                    e.target.value = ""; // Limpia el input
                    return;
                }

                // Crear una vista previa con FileReader
                const reader = new FileReader();
                reader.onload = function (e) {
                    portadaPreview.src = e.target.result; // Asigna la imagen al src
                };
                reader.readAsDataURL(file);
            } else {
                portadaPreview.src = "#"; // Limpia la vista previa si no hay archivo
            }
        });

        const inputs = document.querySelectorAll('input[type="file"]');

        inputs.forEach(input => {
        input.addEventListener("change", function (e) {
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

        modal.style.display = "block";
        document.body.style.overflow = "hidden";
        await listadoLocalidades(null, "ListadoUbicaciones");
    };

    cerrarModal.onclick = function () {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    };

    btnCancelar.onclick = function () {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    };

    const btnAbrirModalEditEscuela = document.querySelectorAll(".btnAbrirModalEditEscuela");
    const abrirModalEditEscuela = document.getElementById("modalEditEscuela");
    const btnCancelarEditEscuela = document.getElementById("btnCancelarEditEscuela");
    const cerrarModalEditEscuela = document.getElementsByClassName("clsModEditEscuela")[0];

    btnAbrirModalEditEscuela.forEach(btn => {
        btn.addEventListener("click", async (event) => {
            event.preventDefault();
            const data_id_atribute = btn.getAttribute("data-id");

            try {
                const response = await fetch(`/editarEscuela/${data_id_atribute}`);
                const result = await response.json();

                if (result.message === "Success") {
                    console.log(result);

                    // Cargar localidades con la localidad seleccionada
                    await listadoLocalidades(result.Escuela.id_localidad_id, "ListadoUbicacionesEdit");

                    document.getElementById("escuela_id").value = result.Escuela.id;
                    document.getElementById("nombre_escuela_edit").value = result.Escuela.nombre_escuela;

                    if (result.Escuela.tipo_escuela) {
                        document.getElementById("tipo_escuela_publica_edit").checked = true;
                    } else {
                        document.getElementById("tipo_escuela_privada_edit").checked = true;
                    }

                    document.getElementById("descripcion_escuela_edit").value = result.Escuela.descripcion;
                    document.getElementById("telefono_edit").value = result.Escuela.telefono_escuela;
                    document.getElementById("correo_edit").value = result.Escuela.correo_escuela;

                    if (result.Escuela.ubicacion_escuela === null) {
                        document.getElementById("direccion_edit_escuela").value = "No tiene registro";
                    } else {
                        document.getElementById("direccion_edit_escuela").value = result.Escuela.ubicacion_escuela;
                    }
                    document.getElementById("hora_atencion_edit").value = result.Escuela.hora_atencion;

                    var urlUbicado = window.location.origin;

                    document.getElementById("previewImagen_edit").src = `${urlUbicado}/imagenes/${result.Escuela.url_imagen_escuela}`

                    result.ImagenesExtras.forEach((imgExtra, index) => {
                        const name = `previewImagenExtra_edit${index + 1}`;
                        const imgElementPreview = document.getElementById(name);
                        const containerImagenExtra = imgElementPreview?.parentElement;
                    
                        if (imgElementPreview) {
                            imgElementPreview.src = `${urlUbicado}/imagenes/${imgExtra}`;
                    
                            // Crear el enlace "Eliminar"
                            const enlaceEliminar = document.createElement('a');
                            enlaceEliminar.href = `/quitarImagenExtra/${data_id_atribute}/${encodeURIComponent(imgExtra)}/`; // URL codificada
                            enlaceEliminar.textContent = 'Eliminar';
                            enlaceEliminar.classList.add('btnEliminar'); // Agregar estilos si es necesario
                    
                            // Agregar el enlace al contenedor
                            containerImagenExtra.appendChild(enlaceEliminar);
                        } else {
                            console.log(`Error: No se encontró el elemento con ID ${name}`);
                        }
                    });
                    
                    

                    abrirModalEditEscuela.style.display = "block";
                    document.body.style.overflow = "hidden";

                } else {
                    console.log(result);
                }
            } catch (error) {
                console.error("Error al obtener los datos", error);
            }
        });
    });

    btnCancelarEditEscuela.onclick = function () {
        abrirModalEditEscuela.style.display = "none";
        document.body.style.overflow = "auto";
    };

    cerrarModalEditEscuela.onclick = function () {
        abrirModalEditEscuela.style.display = "none";
        document.body.style.overflow = "auto";
    };
});
