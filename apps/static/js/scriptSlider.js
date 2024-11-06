const swiper = new Swiper('.swiper-container', {
    slidesPerView: 5, // Cantidad de imágenes permitidas
    spaceBetween: 20, // Espacio entre imágenes
    loop: true, // Hace que el carrusel sea infinito
    pagination: { // Selector de paginación
        clickable: true,
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
});
