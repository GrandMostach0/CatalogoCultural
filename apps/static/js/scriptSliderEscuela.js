const obtenerEscuela = document.getElementById("imagenPortada");
console.log("que paso broder " + obtenerEscuela)
const obtenerContainerSwiperPublicaciones = document.getElementsByClassName("container-swiper-Publicaciones")[0];
const cerrarSwiper = document.getElementById("cerrarContainerSwiper");

obtenerEscuela.onclick = function() {
    obtenerContainerSwiperPublicaciones.style.display = "block";
}

cerrarSwiper.onclick = function(){
    obtenerContainerSwiperPublicaciones.style.display = "none";
}

// Cerrar el swiper haciendo clic fuera del contenido
obtenerContainerSwiperPublicaciones.onclick = function (event) {
    const contenidoSwiper = document.querySelector('.container-content-swiper-publicaciones');
    
    // Si el clic no ocurrió dentro del contenido del swiper, se cierra
    if (!contenidoSwiper.contains(event.target)) {
        obtenerContainerSwiperPublicaciones.style.display = "none";
    }
};

const swiper = new Swiper('.swiper-container', {
    slidesPerView: 1, // Configuración inicial para tamaños pequeños
    spaceBetween: 10, // Espacio pequeño entre slides
    loop: true,
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    }
});