const listarSubDisciplinas = async(idDisciplina) => {
    try{
        const response = await fetch(`/subdisciplina/${idDisciplina}`);
        const data = await response.json();

        if(data.message === "Success"){

            console.log(data)

            const setSubdisciplina = document.getElementById("listaSubDisciplinaUsuario");
            setSubdisciplina.innerHTML = "";

            data.Subdisciplinas.forEach(subdisciplina =>{
                const option = document.createElement("option");
                option.value = subdisciplina.id;
                option.textContent = subdisciplina.nombre_subdisciplina;

                setSubdisciplina.appendChild(option);
            });

        }else{
            alert("Disciplinas no encontradas");
        }
    }catch(error){
        console.log(error);
    }
}

const listarDisciplinas = async() => {
    try{
        const response = await fetch("/disciplinas/");
        const data = await response.json();

        if(data.message === "Success"){
            const setDisciplinas = document.getElementById('listaDisciplinasUsuario');

            data.Disciplinas.forEach(disciplina =>{
                const option = document.createElement('option');
                option.value = disciplina.id;
                option.textContent = disciplina.nombre_disciplina;

                setDisciplinas.appendChild(option);
            });
            listarSubDisciplinas(data.Disciplinas[0].id);
        }else{
            alert("Disciplinas no encontradas");
        }
        console.log(data);
    }catch(error){
        console.log(error);
    }
}

const cargaInicial = async() => {
    await listarDisciplinas();

    document.getElementById("listaDisciplinasUsuario").addEventListener("change", (event)=>{
        listarSubDisciplinas(event.target.value);
    })
}

// Esperar a que el DOM se cargue
document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("modalAddUsuario");
    var abrirModal = document.getElementById("abrirModalAddUsuario");
    var cerrarModal = document.getElementsByClassName("clsModUsuario")[0];
    var btnCancelar = document.getElementById("btnCancelarAddUsuario");

    abrirModal.addEventListener("click", async (event) =>{
        event.preventDefault();
        modal.style.display = "block";
        document.body.style.overflow = "hidden";

        await cargaInicial();
    });

    cerrarModal.onclick = function() {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }

    btnCancelar.onclick = function() {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }

    /* SECCION PARA LA EDICION DE LOS DATOS DEL USUARIO */
    const modalEditUsuario = document.getElementById("modalEditUsuario");
    const abrirModalEditUsuario = document.querySelectorAll(".abrirModalEditUsuario");
    const cerrarModalEditUsuario = document.getElementsByClassName("clsModalEditUsuario")[0];
    const btnCancelarEditUsuario = document.getElementById("btnCancelarEditUsuario");

    abrirModalEditUsuario.forEach(btn => {
        btn.addEventListener("click", async (event) => {
            event.preventDefault();
            const data_id = event.target.getAttribute("data-id");
            const nombre_completo = event.target.getAttribute("data-nombre");

            try{
                const response = await fetch(`/getUsuario/${data_id}`);
                const data = await response.json();

                console.log(data);

                if (data.message === "Success"){
                    document.getElementById("actor_id").value = data.Actor.id;
                    document.getElementById("nombre_edit").value = data.Actor.nombre_Actor;
                    document.getElementById("primerApellido").value = data.Actor.primer_apellido_Actor;
                    document.getElementById("segundoApellido").value = data.Actor.segundo_apellido_Actor;
                    document.getElementById("biografia").value = data.Actor.biografia_Actor;
                    document.getElementById("correo_publico_edit").value = data.Actor.correo_publico_Actor;
                    document.getElementById("correo_privado_edit").value = data.Actor.correo_privado_actor;
                    document.getElementById("telefono_publico_edit").value = data.Actor.Telefono_publico_Actor;
                    document.getElementById("telefono_privado_edit").value = data.Actor.Telefono_privado_actor;
                }
                
            }catch(e){
                console.log("Error:" + e)
            }
            
            modalEditUsuario.style.display = "block";
            document.body.style.overflow = "hidden";

        })
    })

    cerrarModalEditUsuario.onclick  = function(){
        modalEditUsuario.style.display = "none";
        document.body.style.overflow = "auto";
    }

    btnCancelarEditUsuario.onclick = function(){
        modalEditUsuario.style.display = "none";
        document.body.style.overflow = "auto";
    }
});
