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

    // Masquer les boutons par défaut
    $('.carousel-button').hide();

    // Afficher les boutons lorsque la souris survole le carrousel
    $('.carousel').hover(
        function() {
            $('.carousel-button').fadeIn();
        },
        function() {
            $('.carousel-button').fadeOut();
        }
    );
});
