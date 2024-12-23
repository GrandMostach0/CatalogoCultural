const listarSubDisciplinas = async(idDisciplina) => {
    try{
        const response = await fetch(`/subdisciplinas/${idDisciplina}`);
        const data = await response.json();

        if(data.message === "Success"){
            let opciones = ``;
            data.Subdisciplinas.forEach((subdisciplina) => {
                opciones += `<option value='${subdisciplina.id}'>${subdisciplina.nombre_subdisciplina}</option>`;
            });
            subDisciplina.innerHTML = opciones;
        }else{
            alert("Disciplinas no encontradas");
        }
        console.log(data);
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

            data.NombreClasificacion.forEach(clasificacion => {
                const option = document.createElement('option');
                
            });

            disciplina.innerHTML = opciones;
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

    disciplina.addEventListener("change", (event) => {
        listarSubDisciplinas(event.target.value);
    });
}

// Esperar a que el DOM se cargue
document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("modalAddUsuario");
    var abrirModal = document.getElementById("abrirModalAddUsuario");
    var cerrarModal = document.getElementsByClassName("clsModUsuario")[0];
    var btnCancelar = document.getElementById("btnCancelarAddUsuario");

    abrirModal.addEventListener("click", async () =>{
        event.preventDefault();
        modal.style.display = "block";
        document.body.style.overflow = "hidden";

        await listarDisciplinas();
    });

    cerrarModal.onclick = function() {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }

    btnCancelar.onclick = function() {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }
});