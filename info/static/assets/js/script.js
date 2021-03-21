$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});

$('span.current__rate').html($('header .exchange').html());

$('.services__block .button').click(function(e) {
    e.preventDefault();
    $(this).parents('.services__block').find('.businesBox.all').slideToggle();
    $(this).remove();
});

$('form.subscribe')
    .submit(function(e) {
        e.preventDefault();

        let action = $(this).data('action'),
            data = $(this).serialize(),
            _this = $(this),
            loader = $('.loader');

        _this.find('[type=submit]').attr('disabled', 'disabled');

        _this.find('.box_input').each(function() {
            $(this).find('input').removeClass('error');
            $(this).find('.answer').remove();
        });

        loader.css('display', 'block');

        $.ajax({
            type: 'POST',
            url: action,
            data: data,
            dataType: 'json',
            success: function(response) {
                _this.parents('.blueBox-subscribe').find('.fix_ok').addClass('active').find('div').text(response.message);
                loader.css('display', 'none');
            },
            error: function(response) {
                loader.css('display', 'none');
                _this.find('[type=submit]').removeAttr('disabled');

                if (response.responseJSON.errors === undefined) {
                    alert(response.responseJSON.message);
                    return false;
                }

                $.each(response.responseJSON.errors, function(k, v) {
                    _this.find('[name= ' + k + ']').addClass('error');
                    _this.find('[name= ' + k + ']').parent().append('<p class="answer">' + (Array.isArray(v) ? v[0] : v) + '</p>');
                });
            }
        });
    })
    .on('keyup', 'input', function() {
        $(this).removeClass('error');
        $(this).parent().find('.answer').remove();
    });

$('form.feedback')
    .submit(function(e) {
        e.preventDefault();

        let answer = $(this).find('.answer'),
            action = $(this).data('action'),
            _this = $(this),
            loader = $('.loader'),
            formData = new FormData($(this)[0]);


        _this.find('[type=submit]').attr('disabled', 'disabled');

        _this.find('.box_input').each(function() {
            $(this).find('input, textarea').removeClass('error');
            $(this).find('.answer').remove();
        });

        loader.css('display', 'block');

        $.ajax({
            type: 'POST',
            url: action,
            data: formData,
            contentType: false,
            processData: false,
            dataType: 'json',
            success: function(response) {
                answer.text(response.message);
                loader.css('display', 'none');

                dataLayer.push({
                    'event': 'contact_form_success'
                });

                if ($('.contactFlex').length > 0 || $('.modal_form').length > 0) {
                    _this.css('display', 'none');
                    $('.contactFlex-left, .contactFlex-right').remove();
                    $('.fix_ok').addClass('active').find('div').text(response.message);
                } else {
                    _this.parent().find('.fix_ok').addClass('active').find('div').text(response.message);
                    _this.remove();
                }
            },
            error: function(response) {
                loader.css('display', 'none');
                _this.find('[type=submit]').removeAttr('disabled');

                if (response.responseJSON.errors === undefined) {
                    alert(response.responseJSON.message);
                    return false;
                }

                $.each(response.responseJSON.errors, function(k, v) {
                    _this.find('[name= ' + k + ']').addClass('error');
                    _this.find('[name= ' + k + ']').parent().append('<p class="answer">' + (Array.isArray(v) ? v[0] : v) + '</p>');
                });

                if (document.documentElement.clientWidth <= 899) {
                    var errorInput = _this.parents('.feedback').find('._error')
                    $('html, body').animate({
                        scrollTop: $(errorInput[0]).offset().top - parseInt($('.header').css('height'), 10)
                    }, 1000);
                }
            }
        });
    })
    .on('keyup', 'input, textarea', function() {
        $(this).removeClass('error');
        $(this).parent().find('.answer').remove();
    });

$('form.feedback_modern')
    .submit(function(e) {
        e.preventDefault();

        let action = $(this).data('action'),
            _this = $(this),
            loader = $('.loader'),
            formData = new FormData($(this)[0]);

        _this.find('[type=submit]').attr('disabled', 'disabled');

        _this.find('.form__group').each(function() {
            $(this).find('input, textarea, select').removeClass('_error');
            $(this).find('.form__error').remove();
        });

        loader.css('display', 'block');

        $.ajax({
            type: 'POST',
            url: action,
            data: formData,
            contentType: false,
            processData: false,
            dataType: 'json',
            success: function() {
                loader.css('display', 'none');
                _this.parents('.feedback').addClass('_success');
                _this.find('[type=submit]').removeAttr('disabled');

                let FormType = 0;
                if (_this.find('input[name=type]').length > 0) {
                    FormType = _this.find('input[name=type]').val();
                }


                switch (FormType) {
                    case 'testnet_coin':
                        dataLayer.push({
                            'event': 'testnet_coins_form_success'
                        });
                        break;
                    case 0:
                        dataLayer.push({
                            'event': 'contact_form_success'
                        });
                        break;
                    case '1':
                        dataLayer.push({
                            'event': 'article_approval_form_success'
                        });
                        break;
                    case '2':
                        dataLayer.push({
                            'event': 'video_approval_form_success'
                        });
                        break;
                    case '3':
                        dataLayer.push({
                            'event': 'cpc_apply_cooperation_form_success'
                        });
                        break;
                    case '4':
                        dataLayer.push({
                            'event': 'article_apply_reward_form_success'
                        });
                        break;
                    case '5':
                        dataLayer.push({
                            'event': 'video_apply_reward_form_success'
                        });
                        break;
                }
            },
            error: function(response) {
                loader.css('display', 'none');
                _this.find('[type=submit]').removeAttr('disabled');

                if (response.responseJSON.errors === undefined) {
                    alert(response.responseJSON.message);
                    return false;
                }

                $.each(response.responseJSON.errors, function(k, v) {
                    _this.find('[name= ' + k + ']').addClass('_error');
                    _this.find('[name= ' + k + ']').parent().append('<div class="form__error">' + (Array.isArray(v) ? v[0] : v) + '</div>');
                });

                if (document.documentElement.clientWidth <= 899) {
                    if (document.querySelector('.fancybox-is-open')) {
                        /* 	$('.fancybox-slide').animate({scrollTop: 80 }, 1000);
                        $('.fancybox-slide').find('_error:eq(0)').animate({ scrollTop: 80 }, 1000);
                        	  console.log($('.fancybox-is-open').find('.feedback ')) */
                    } else {
                        var errorInput = _this.parents('.feedback').find('._error');
                        $('html, body').animate({
                            scrollTop: $(errorInput[0]).offset().top - parseInt($('.header').css('height'), 10)
                        }, 1000);
                    }
                }
            }
        });
    })
    .on('keyup', 'input, select, textarea', function() {
        $(this).removeClass('_error');
        $(this).parent().find('.form__error').remove();
    });

$('body')
    .on('click', '.filter__list > a:not(._active)', function(e) {
        e.preventDefault();
        let _this = $(this),
            link = $(this).data('to');

        _this.parent().find('._active').removeClass('_active');
        _this.addClass('_active');

        $.post(link, null, function(response) {
            $('.eventsBoxRoad, .newsAllBox').html(response.view);
            $('.pagination').remove();
            $('.wrapper.content').append(response.pagination);
        });
    })
    .on('click', '.news .pagination .box-newsButton > a', function(e) {
        e.preventDefault();
        let _this = $(this),
            link = $(this).attr('href');

        $.post(link, null, function(response) {
            let pagination = $(response.pagination);
            pagination.find('.pagination_box .ditto_page').each(function() {
                if (parseInt($(this).text().toString()) < response.current) {
                    $(this).addClass('ditto_currentpage');
                }
            });

            _this.parents('.pagination').html(pagination.html());
            $('.newsAllBox').append(response.view);
            response.next === null ? _this.remove() : _this.attr('href', response.next);
            filterInit();
        });
    })
    .on('click', '.events .pagination .box-newsButton > a', function(e) {
        e.preventDefault();
        let _this = $(this),
            link = $(this).attr('href'),
            current = $(this).parents('.tabePaneTwo').data('id');

        $.post(link, null, function(response) {
            let pagination = $(response[current].pagination);
            pagination.find('.pagination_box .ditto_page').each(function() {
                if (parseInt($(this).text().toString()) < response[current].current) {
                    $(this).addClass('ditto_currentpage');
                }
            });

            _this.parents('.tabePaneTwo').find('.eventsBoxRoad').append(response[current].view);
            _this.parents('.pagination').html(pagination.html());
            response[current].next === null ? _this.remove() : _this.attr('href', response[current].next);
            filterInit();
        });
    });


$('.teamPage-box .product .go').click(function(e) {
    e.preventDefault();
    let _this = $(this).parents('.product'),
        modal = $('.modal_form'),
        content = $('.go_content');

    modal.find('.relative.actions .answer').empty();
    modal.find('input, textarea').val('');

    content.find('.product-img').html(_this.find('.product-img').html());
    content.find('.product-title').html(_this.find('.product-title').html());
    content.find('.product-text').html(_this.find('.product-text').html());
    content.find('.product-social').empty().html(_this.find('.product-social').html());
    content.find('.modalTteam-text').html(_this.find('.detail-text').html());
    content.find('.mail').remove();

    if ($(this).hasClass('mail')) {
        content.find('input[name=cooperator_id]').val(_this.data('cooperator'));
        content.find('.modalTteam-text').css('display', 'none');
        content.find('form').css('display', 'block');
        modal.find('.modalTteam-title').css('display', 'block').find('span').text(_this.find('.product-title').text());
        modal.find('.fix_ok').removeClass('active');
    } else {
        content.find('.modalTteam-text').css('display', 'block');
        content.find('form').css('display', 'none');
        modal.find('.modalTteam-title').css('display', 'none');
    }

    content.show();
    $('#overlay').fadeIn(400);
    modal.removeClass('fadeOutUpPopap').addClass('fadeInDownPopap animatedPopap');
    $('body').addClass('fixed');
});

$('form.calculator').submit(function(e) {
    e.preventDefault();

    let answer_block = $(this).find('.calculator__result'),
        answer = $(this).find('#calculator_result'),
        action = $(this).data('action'),
        data = $(this).serializeArray(),
        loader = $('.loader');

    if (window.innerWidth < 900) {
        var $type_data = 'select';
    } else {
        var $type_data = 'range';
    }

    data[data.length] = {
        name: "type_data",
        value: $type_data
    };

    loader.css('display', 'block');

    $.ajax({
        type: 'POST',
        url: action,
        data: data,
        dataType: 'json',
        success: function(response) {
            answer.text(response.message);
            loader.css('display', 'none');
            answer_block.css('display', 'block');
            if (window.innerWidth < 900) {
                $('html, body').animate({
                    scrollTop: answer_block.offset().top - 100
                }, 500);
            }
        },
        error: function(response) {
            answer.text("error");
            loader.css('display', 'none');
            answer_block.css('display', 'block');
            if (window.innerWidth < 900) {
                $('html, body').animate({
                    scrollTop: answer_block.offset().top - 100
                }, 500);
            }
        }
    });
});

$('.range_slider_label').on('click', function() {

    $value = $(this).attr('data-value');
    $(this).closest('.slidercontainer').find(".range_slider").val($value);
});