

document.addEventListener("DOMContentLoaded", async() => {
    var modal = document.getElementById("myModalProyecto");
    var abrirModal = document.getElementById("abrirModalProyecto");
    var cerrarModal = document.getElementsByClassName("close")[1];
    var btnCancelar = document.getElementById("btnCancelar2");

    // DINAMICA PARA SABER SI ES DE PAGA
    const eventoPaga = document.getElementById("eventoPaga");
    const precioUnitario = document.querySelector('.precioUnitario');
    const subOpciones = document.querySelector('.subOpciones2');

    precioUnitario.style.display = 'none';
    subOpciones.style.display = 'block';
    
    // DINAMICA DEL PUNTO DE VENTA
    const presencial = document.getElementById('puntoVentaPresencial');
    const digital = document.getElementById('puntoVentaDigital');
    const urlinput = document.querySelector('.URLPuntoVentalbl');

    urlinput.style.display = 'none';

    abrirModal.addEventListener("click", function(event){
        event.preventDefault();
        modal.style.display = "block";
        document.body.style.overflow = "hidden";
    });

    cerrarModal.onclick = function() {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }

    btnCancelar.onclick = function() {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }

    // FUNCIONALIDADES DINAMICAS
    // ------ FUNCIO PARA SABER SI ES DE PAGA ------
    function togglePaga(){
        if(eventoPaga.checked){
            precioUnitario.style.display = "block";
            subOpciones.style.display = "block";
        }else{
            precioUnitario.style.display = "none";
            subOpciones.style.display = 'none';
        }
    }

    eventoPaga.addEventListener("change", togglePaga);

    function togglePuntoVenta(){
        if(digital.checked){
            urlinput.style.display = "block";
        }else{
            urlinput.style.display = "none";
        }
    }

    await listarClasificaciones();

    // asignacion de las funcionalidades
    presencial.addEventListener("change", togglePuntoVenta);
    digital.addEventListener("change", togglePuntoVenta);

});