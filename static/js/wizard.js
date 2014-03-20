var interval = 0;
$('#slide-1') .show();
$('#slider .flexslider') .flexslider({
    animation: 'slide',
    useCSS: false,
    touch: false,
    keyboard: false,
    multipleKeyboard: true,
    pauseOnHover: true,
    slideshow: false,
    directionNav: false,
    video: true,
    animationSpeed: 800,
    animationLoop: true
});
$('#slider .flexslider') .flexslider('pause');
$('#controles li a') .click(function (event) {
    event.preventDefault();
    if ($(this) .parent() .hasClass('active'))
    $(this) .parent() .removeClass('active');
     else
    $(this) .parent() .addClass('active');
});
var ira = 0;
var show_animation = true;
$('#controles li a') .click(function (event) {
    event.preventDefault();
    ira = $(this) .attr('data-link');
    ira = parseFloat(ira);
    if ($(this) .parent() .hasClass('active')) {
        $(this) .addClass('active');
    } else {
        $(this) .parent() .addClass('active');
    }
    moves_slider();
    captions();
});
$('.slide_control') .click(function (event) {
    event.preventDefault();
    ira = $(this) .attr('data-link');
    ira = parseFloat(ira);
    if ($(this) .parent() .hasClass('active')) {
        $(this) .addClass('active');
    } else {
        $(this) .parent() .addClass('active');
    }
    moves_slider();
    captions();
});
function go_to_slide(ira_) {
    show_animation = false;
    clearInterval(interval);
    ira = parseFloat(ira_);
    if ($(this) .parent() .hasClass('active')) {
        $(this) .addClass('active');
    } else {
        $(this) .parent() .addClass('active');
    }
    moves_slider();
    captions();
}
function captions() {
    var progres_ancho = 80 * (ira);
    $('#controles #thumb-' + ira) .addClass('active');
    $('#progress') .stop(true, true) .css({
        'width': progres_ancho
    });
    $('#controles li a') .each(function (i, el) {
        if (i > ira) {
            $(this) .parent() .removeClass('active');
        } else if (i < ira) {
            $(this) .parent() .addClass('active');
        }
    });
}
function moves_slider() {
    var slider = $('#slider .flexslider') .data('flexslider');
    slider.flexAnimate(ira);
    $('.nav-slider .active') .removeClass('active');
}
/*
 *
 */

$('.inner-redes a') .click(function (event) {
    if ($(this) .hasClass('checked')) {
        $(this) .removeClass('checked');
    } else {
        //$(this).addClass('checked');
    }
});
$('.back') .click(function (event) {
    event.preventDefault();
    var slidee = $('#slider .flexslider') .data('flexslider');
    var actual = slidee.currentSlide;
    slidee.flexAnimate(actual - 1);
    thumb_actual = actual - 1;
    ira = thumb_actual;
    if (ira == 2) {
        clearInterval(interval);
        interval = setInterval('move_slider()', 8000);
    }
    $('#controles #thumb-' + thumb_actual) .addClass('active');
    progres_ancho = 80 * (thumb_actual);
    $('#progress') .css({
        'width': progres_ancho
    });
    $('#controles li a') .each(function (i, el) {
        if (i > ira) {
            $(this) .parent() .removeClass('active');
        } else if (i < ira) {
            $(this) .parent() .addClass('active');
        }
    });
}
);
$('.next') .click(function (event) {
    event.preventDefault();
    var slidee = $('#slider .flexslider') .data('flexslider');
    var actual = slidee.currentSlide;
    slidee.flexAnimate(actual + 1);
    thumb_actual = actual + 1;
    $('#controles #thumb-' + thumb_actual) .addClass('active');
    progres_ancho = 80 * (thumb_actual);
    $('#progress') .css({
        'width': progres_ancho
    });
}
);
function move_slider() {
    return ;
    ira++;
    var exampleSlider = $('#slider .flexslider') .data('flexslider');
    exampleSlider.flexAnimate(ira);
    captions();
    if (ira >= 3) {
        clearInterval(interval);
    }
}
$(function () {
    $('section.scrollsections') .scrollSections({
        createNavigation: false,
        alwaysStartWithFirstSection: true,
        animateScrollToFirstSection: true,
        touch: false,
        scrollbar: false,
        scrollMax: 0,
        navigation: true,
        keyboard: false,
        before: function ($currentSection, $nextSection) {
        },
        after: function ($currentSection, $previousSection) {
            if ($currentSection.attr('id') == 'whatfor' && show_animation) {
                clearInterval(interval);
                console.log('quilombo');
                interval = setInterval('move_slider()', 8000);
                $('#progress') .stop(true, true) .animate({
                    'width': ira * 80
                }, 0, function () {
                    return ;
                    $('#progress') .animate({
                        'width': 240
                    }, 24000 - ira * 8000, 'linear');
                });
            }
        }
    });
});
// Prevent moving stuff with a touch input device
document.ontouchmove = function (e) {
    e.preventDefault();
}
$(document) .ready(function () {
    $('#iagree') .click(function (event) {
        console.log('Conditions accepted.');
        $.post('/iagree/', {
            'user_agree': true,
            'dataType': ''
        }, function (data, textStatus) {
        }, 'json');
    });
});
// This handles the carousel for the fitness trackers tab
// 133 is the full width of a single bubble
$('#redes-inner-left') .click(function (e) {
    e.preventDefault();
    var panel = $('.inner-redes .container .scrollable')
    var margin = parseInt(panel.css('margin-left')) + 133;
    panel.stop() .animate({
        'margin-left': margin >= 0 ? 0 : margin + 'px'
    });
});
$('#redes-inner-right') .click(function (e) {
    e.preventDefault();
    var panel = $('.inner-redes .container .scrollable')
    var margin = parseInt(panel.css('margin-left')) - 133;
    panel.stop() .animate({
        'margin-left': margin <= - 399 ? - 399 : margin + 'px'
    });
});
$('.learnmore') .click(function (e) {
    e.preventDefault();
});
