// Esperar a que el DOM se cargue
document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("myModal");  // Obtenemos el modal
    var abrirModal = document.getElementById("abrirModal");  // Enlace para abrir el modal
    var cerrarModal = document.getElementsByClassName("close")[0];  // Botón de cerrar el modal (la "X")

    // Cuando se hace clic en el enlace "Crear Publicación", se abre el modal
    abrirModal.onclick = function(event) {
        event.preventDefault();  // Prevenir que el enlace redirija
        modal.style.display = "block";  // Mostrar el modal
    }

    // Cuando se hace clic en la "X", se cierra el modal
    cerrarModal.onclick = function() {
        modal.style.display = "none";  // Ocultar el modal
    }

    // Cuando se hace clic fuera del modal, se cierra
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";  // Ocultar el modal si se hace clic fuera de él
        }
    }
});
