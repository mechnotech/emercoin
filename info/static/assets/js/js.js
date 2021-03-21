$(document).ready(function() {
    function is_touch_device() {
        return !!('ontouchstart' in window);
    }

    is_touch_device();

    var touch =
        'ontouchstart' in document.documentElement ||
        navigator.MaxTouchPoints > 0 ||
        navigator.msMaxTouchPoints > 0;

    if (touch) {
        // remove all :hover stylesheets
        try {
            // prevent exception on browsers not supporting DOM styleSheets properly
            for (var si in document.styleSheets) {
                var styleSheet = document.styleSheets[si];
                if (!styleSheet.rules) continue;

                for (var ri = styleSheet.rules.length - 1; ri >= 0; ri--) {
                    if (!styleSheet.rules[ri].selectorText) continue;

                    if (styleSheet.rules[ri].selectorText.match(':hover')) {
                        styleSheet.deleteRule(ri);
                    }
                }
            }
        } catch (ex) {}
    }

    function footerToBottom() {
        var browserHeight = $(window).height(),
            footerOuterHeight = $('footer').outerHeight(true),
            headerOuterHeight = $('header').outerHeight(true),
            autoHeight = $('main'),
            mainHeightMarginPaddingBorder =
            autoHeight.outerHeight(true) - autoHeight.height();
        autoHeight.css({
            'min-height': browserHeight -
                footerOuterHeight -
                mainHeightMarginPaddingBorder -
                headerOuterHeight
        });
    }

    footerToBottom();
    $(window).resize(function() {
        footerToBottom();
    });

    $('#pull').click(function() {
        $('.header-right')
            .removeClass('fadeOutUpMenu')
            .addClass('fadeInDownMenu animatedMenu');
        $('html').addClass('limited');
        $('header').addClass('higher');
        setTimeout(function() {
            $('.logo')
                .addClass('fixed')
                .animate(1000);
        }, 1000);
    });

    $('.closeMenu').click(function() {
        $('.header-right')
            .removeClass('fadeInDownMenu')
            .addClass('fadeOutUpMenu animatedMenu')
            .hide();
        $('html').removeClass('limited');
        $('header').removeClass('higher');
        $('.logo').removeClass('fixed');
    });

    $('.js_menuDocs_click').click(function() {
        $('.docPage-menu')
            .removeClass('fadeOutUpMenu')
            .addClass('fadeInDownMenu animatedMenu');
        $('html').addClass('limited');
    });

    $('.closeDocs').click(function() {
        $('.docPage-menu')
            .removeClass('fadeInDownMenu')
            .addClass('fadeOutUpMenu animatedMenu')
            .hide();
        $('html').removeClass('limited');
    });

    var scrollbarWidth = function() {
        var outer = document.createElement('div');
        outer.style.visibility = 'hidden';
        outer.style.width = '100px';
        outer.style.msOverflowStyle = 'scrollbar'; // needed for WinJS apps

        document.body.appendChild(outer);

        var widthNoScroll = outer.offsetWidth;
        // force scrollbars
        outer.style.overflow = 'scroll';

        // add innerdiv
        var inner = document.createElement('div');
        inner.style.width = '100%';
        outer.appendChild(inner);

        var widthWithScroll = inner.offsetWidth;

        // remove divs
        outer.parentNode.removeChild(outer);

        return widthNoScroll - widthWithScroll;
    };

    function removeedClassHeader() {
        var w = $(window).width();
        var point = 1330 - scrollbarWidth();
        if (w >= point) {
            $('html').removeClass('limited');
            $('header').removeClass('higher');
            $('.logo').removeClass('fixed');
            $('.header-right').removeClass(
                'fadeInDownMenu fadeOutUpMenu animatedMenu'
            );
        }
        if (w >= point) {
            $('.header-right').css({
                display: 'flex'
            });
        }
        if (w < point) {
            $('.header-right').css({
                display: 'none'
            });
        }
    }

    removeedClassHeader();
    $(window).resize(function() {
        removeedClassHeader();
    });

    var owl1 = $('.owl-carousel-1');
    owl1.owlCarousel({
        items: 1,
        nav: true,
        pagination: false,
        dots: true,
        mouseDrag: false,
        autoHeight: false
    });

    var owl_swipe = $('.owl-swipe');
    owl_swipe.owlCarousel({
        loop: false,
        autoWidth: true,
        pagination: false,
        lazyLoad: false,
        dots: false,
        nav: false,
        margin: 0,
        mouseDrag: false,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            840: {
                items: 3
            },
            1240: {
                items: 4
            }
        }
    });

    var owl_2 = $('.owl-carousel-2');
    owl_2.owlCarousel({
        loop: false,
        pagination: false,
        lazyLoad: true,
        nav: false,
        dots: true,
        margin: 30,
        autoHeight: false,
        mouseDrag: false,
        responsive: {
            0: {
                items: 1
            },
            520: {
                items: 2
            },
            992: {
                items: 3
            }
        }
    });

    var owl_3 = $('.owl-carousel-3');
    owl_3.owlCarousel({
        loop: false,
        pagination: false,
        lazyLoad: true,
        nav: true,
        dots: false,
        margin: 12,
        startPosition: 6,
        autoHeight: false,
        mouseDrag: false,
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 3
            },
            868: {
                items: 4
            },
            992: {
                items: 5
            },
            1200: {
                items: 6
            }
        }
    });

    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent)) {
        $('.link_menu').on('click', function() {
            var $selfControlButton = $(this),
                $parentBox = $selfControlButton.closest('.menuTop li');
            $containerRelationFromCtrlBtn = $parentBox.find('.dropdown_menu');
            if ($containerRelationFromCtrlBtn.is(':visible')) {
                $containerRelationFromCtrlBtn.hide();
                $selfControlButton.removeClass('open');
            } else {
                $('.link_menu').removeClass('open');
                $('.dropdown_menu').hide();
                $containerRelationFromCtrlBtn.show();
                $selfControlButton.addClass('open');
            }
        });

        $(document).click(function(event) {
            if ($(event.target).closest('.menuTop li').length) return;
            $('.link_menu').removeClass('open');
            $('.dropdown_menu').hide();
            event.stopPropagation();
        });
    }

    function settings_tabPane() {
        $('.tab_js').click(function(event) {
            $(this).addClass('active');
            var id = $(this).data('id');
            $.each($('.tabePane'), function(i, c) {
                if ($(c).data('id') == id) {
                    $(c).addClass('active');
                } else {
                    $(c).removeClass('active');
                }
            });
            $.each($('.tab_js'), function(i, c) {
                if ($(c).data('id') == id) {
                    $(c).addClass('active');
                } else {
                    $(c).removeClass('active');
                }
            });
            event.preventDefault();
        });
    }

    settings_tabPane();

    function settings_tabPane2() {
        $('.tabTwo_js').click(function(event) {
            $(this).addClass('active');
            var id = $(this).data('id');
            $.each($('.tabePaneTwo'), function(i, c) {
                if ($(c).data('id') == id) {
                    $(c).addClass('active');
                } else {
                    $(c).removeClass('active');
                }
            });
            $.each($('.tabTwo_js'), function(i, c) {
                if ($(c).data('id') == id) {
                    $(c).addClass('active');
                } else {
                    $(c).removeClass('active');
                }
            });
            event.preventDefault();
        });
    }

    settings_tabPane2();

    $('.anchor-link').click(function() {
        var target = $(this).attr('href');
        var w = $(window).width();
        var point = 600;
        var htmlBody = $('html, body');
        htmlBody.animate({
            scrollTop: $(target).offset().top - 74
        }, 300);
        if (w > point) {
            htmlBody.animate({
                scrollTop: $(target).offset().top - 0
            }, 300);
        }
        return false;
    });

    var offset = 220;
    var duration = 500;
    $(window).scroll(function() {
        if ($(this).scrollTop() > offset) {
            $('.up').fadeIn(duration);
        } else {
            $('.up').fadeOut(duration);
        }
        if (
            /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent)
        ) {
            $('.up').addClass('mobile');
        }
    });

    $('.up').click(function(event) {
        event.preventDefault();
        $('html, body').animate({
            scrollTop: 0
        }, duration);
        return false;
    });

    $('.formOpen').click(function() {
        var w = $(window).width();
        var blockHideForm = $('.formHidden');
        var point = 600;
        var htmlBody = $('html, body');
        $('.formShow').hide();
        blockHideForm.show();
        htmlBody.animate({
            scrollTop: blockHideForm.offset().top - 74
        }, 300);
        if (w > point) {
            htmlBody.animate({
                scrollTop: blockHideForm.offset().top - 0
            }, 300);
        }
    });

    $('.subscription_ok_js').click(function() {
        $('.fix_ok').addClass('active');
        setTimeout(function() {
            $('.fix_ok').removeClass('active');
        }, 4000);
    });

    $('.modal_hide, .js_closeModal').click(function() {
        $('.modal_form')
            .removeClass('fadeInDownPopap')
            .addClass('fadeOutUpPopap animatedPopap')
            .hide();
        $('#overlay').hide();
        $('body').removeClass('fixed');
    });

    /* modal window открытие */
    function settings_modal_form() {
        $('.go').click(function(event) {
            var id = $(this).data('id');
            $.each($('.go_content'), function(i, c) {
                if ($(c).data('id') == id) {
                    $(c).show();
                } else {
                    $(c).hide();
                }
            });

            event.preventDefault();
            var modal1 = $('.modal_form');
            $('#overlay').fadeIn(400);
            modal1
                .removeClass('fadeOutUpPopap')
                .addClass('fadeInDownPopap animatedPopap');
            $('body').addClass('fixed');
        });
    }

    settings_modal_form();

    $('.js_search_click').click(function() {
        $('.boxSearchTop').toggleClass('open');
        return false;
    });

    $(document).click(function(event) {
        if ($(event.target).closest('.boxSearchTop').length) return;
        $('.boxSearchTop').removeClass('open');
        event.stopPropagation();
    });

    $('.dropDocs').click(function() {
        $(this)
            .toggleClass('open')
            .parents('.menuDocs li')
            .find('.dropDocsMenu')
            .toggleClass('open');
        return false;
    });
    // $(".boxOverflow").niceScroll({
    //     cursorcolor: "#7b6696",
    //     horizrailenabled: true,
    //     cursoropacitymax: true,
    //     touchbehavior: true,
    //     zindex: 2,
    //     background: "#b09cc9",
    //     disableoutline: false,
    //     enablemousewheel: false,
    //     cursoropacitymin: 1
    // });
});