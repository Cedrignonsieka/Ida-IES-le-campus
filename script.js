$(document).ready(function(){
    let currentIndex = 0;
    const slides = $('.slide');
    const totalSlides = slides.length;

    function showSlide(index) {
        slides.hide();
        slides.eq(index).show();
    }

    $('#next').click(function() {
        currentIndex = (currentIndex + 1) % totalSlides;
        showSlide(currentIndex);
    });

    $('#prev').click(function() {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        showSlide(currentIndex);
    });

    // Affiche la première image au démarrage
    showSlide(currentIndex);
});
