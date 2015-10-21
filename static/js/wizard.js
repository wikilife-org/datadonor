
// Prevent moving stuff with a touch input device
document.ontouchmove = function (e) {
    e.preventDefault();
}

$(function () {
    var interval = 0;
    var ira = 0;
    var show_animation = true;


    function go_to_slide (target) {
        show_animation = false
        clearInterval(interval)
        ira = parseFloat(target)

        if ($(this).parent().hasClass('active'))
            $(this).addClass('active')
        else
            $(this).parent().addClass('active')

        moves_slider()
        captions()
    }

    function captions() {
        var progres_ancho = 80 * (ira)
        $('#controles #thumb-' + ira) .addClass('active')
        $('#progress').stop(true, true).css({
            'width': progres_ancho
        })
        $('#controles li a') .each(function (i, el) {
          if (i > ira)
            $(this).parent().removeClass('active')
          else if (i < ira)
            $(this).parent().addClass('active')
        });
    }

    function moves_slider() {
        var slider = $('#slider .flexslider').data('flexslider')
        slider.flexAnimate(ira)
        $('.nav-slider .active').removeClass('active')
    }

    $('#slide-1').show();
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

    $('#controles li a') .click(function (event) {
        event.preventDefault()
        ira = parseFloat($(this) .attr('data-link'))
        if ($(this).parent().hasClass('active'))
            $(this).addClass('active')
        else
            $(this).parent().addClass('active')
        moves_slider()
        captions()
    });

    $('.inner-redes a') .click(function (event) {
        if ($(this).hasClass('checked'))
            $(this).removeClass('checked')
    })

    $('.back').click(function (event) {
        event.preventDefault();
        var slidee = $('#slider .flexslider') .data('flexslider');
        var actual = slidee.currentSlide;
        slidee.flexAnimate(actual - 1);
        thumb_actual = actual - 1;
        ira = thumb_actual;
        if (ira == 2)
            clearInterval(interval)
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
    });
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
    });
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

    $('#iagree').click(function (event) {
        $.post('/iagree/', {
            'user_agree': true,
            'dataType': ''
        }, function (data, textStatus) {
        }, 'json');
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

    $('div.inner-redes a.ajax') .click(function (e) {
        e.preventDefault();
        var href = $(this) .attr('href');
        console.log(href)
        $.get(href, function () {
            console.log(3333);
            window.location.reload();
        });
    });

    $('a#gender').on('click', function (event) {
        event.preventDefault();
        var href = $(this) .attr('href');
        $.get(href, function () {
            window.location = '/end-wizard/';
        });
    });

    console.log('Show wizard: ' + show_wizard);
    if (show_wizard) {
        $('section#disclaimer') .hide();
        $('#iagree').trigger('click');
    }
    console.log('Association Type: ');
    if (assoc_type == 'social')
    go_to_slide(0);
    if (assoc_type == 'physical')
    go_to_slide(1);
    if (assoc_type == 'nutrition')
    go_to_slide(2);
    if (assoc_type == 'health')
    go_to_slide(3);
    if (assoc_type == 'genomics')
    go_to_slide(4);
});