// JavaScript (utilisant jQuery)
$(document).ready(function(){
    var currentIndex = 0;
    var slides = $('.slide');

    function showSlide(index) {
        if (index < 0) {
            index = slides.length - 1;
        } else if (index >= slides.length) {
            index = 0;
        }

        slides.css('transform', 'translateX(' + (-index * 100) + '%)');
        currentIndex = index;
    }

    $('#prev').click(function() {
        showSlide(currentIndex - 1);
    });

    $('#next').click(function() {
        showSlide(currentIndex + 1);
    });

    setInterval(function() {
        showSlide(currentIndex + 1);
    }, 3000); // Change slide every 3 seconds
});

