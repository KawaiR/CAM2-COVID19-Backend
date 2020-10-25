/*!
    * Start Bootstrap - Grayscale v6.0.1 (https://startbootstrap.com/themes/grayscale)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/BlackrockDigital/startbootstrap-grayscale/blob/master/LICENSE)
    */
    (function ($) {
    "use strict"; // Start of use strict

    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
        if (
            location.pathname.replace(/^\//, "") ==
                this.pathname.replace(/^\//, "") &&
            location.hostname == this.hostname
        ) {
            var target = $(this.hash);
            target = target.length
                ? target
                : $("[name=" + this.hash.slice(1) + "]");
            if (target.length) {
                $("html, body").animate(
                    {
                        scrollTop: target.offset().top - 70,
                    },
                    1000,
                    "easeInOutExpo"
                );
                return false;
            }
        }
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $(".js-scroll-trigger").click(function () {
        $(".navbar-collapse").collapse("hide");
    });

    // Activate scrollspy to add active class to navbar items on scroll
    $("body").scrollspy({
        target: "#mainNav",
        offset: 100,
    });

    // Collapse Navbar
    var navbarCollapse = function () {
        if ($("#mainNav").offset().top > 100) {
            $("#mainNav").addClass("navbar-shrink");
        } else {
            $("#mainNav").removeClass("navbar-shrink");
        }
    };
    // Collapse now if page is not at top
    navbarCollapse();
    // Collapse the navbar when page is scrolled
    $(window).scroll(navbarCollapse);
})(jQuery); // End of use strict


//curl -location --request GET 'https://api.smartable.ai/coronavirus/stats/US' --header 'Subscription-Key: 3009d4ccc29e4808af1ccc25c69b4d5d'
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

$("document").ready(function(){
    $.ajax({ 
        type : "GET", 
        url : "https://api.smartable.ai/coronavirus/stats/US-NY", 
        beforeSend: function(xhr){xhr.setRequestHeader('Subscription-Key', '3009d4ccc29e4808af1ccc25c69b4d5d');},
        success : function(result) { 
            //set your variable to the result 
            $("#casesNY").text(numberWithCommas(result.stats.totalConfirmedCases));
            console.log(result)
        }, 
        error : function(result) { 
          //handle the error 
            console.log(result)
        } 
    }); 
    $.ajax({ 
        type : "GET", 
        url : "https://api.smartable.ai/coronavirus/stats/global", 
        beforeSend: function(xhr){xhr.setRequestHeader('Subscription-Key', '3009d4ccc29e4808af1ccc25c69b4d5d');},
        success : function(result) { 
            //set your variable to the result 
            console.log(result)
        }, 
        error : function(result) { 
          //handle the error 
            console.log(result)
        } 
    });
})