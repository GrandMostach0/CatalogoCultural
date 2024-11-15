const listarSubDisciplinas = async(idDisciplina) => {
    try{
        const response = await fetch(`./subdisciplinas/${idDisciplina}`);
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
        const response = await fetch("./disciplinas");
        const data = await response.json();

        if(data.message === "Success"){
            let opciones = ``;
            data.Disciplinas.forEach((disciplina) => {
                opciones += `<option value='${disciplina.id}'>${disciplina.nombre_disciplina}</option>`;
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

window.addEventListener("load", async () => {
    await cargaInicial();
})