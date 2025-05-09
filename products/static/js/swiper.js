// creating swiper carousel for featured products here
var swiper = new Swiper(".feature-product-carousel", {
    loop: true,
    speed: 800,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    autoplay: {
        delay: 3000,
        pauseOnMouseEnter: true,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});