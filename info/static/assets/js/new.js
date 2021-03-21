if (
    /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
        navigator.userAgent
    )
) {
    document.body.classList.add('mobile');
}

if (/android/i.test(navigator.userAgent)) {
    document.body.classList.add('android');
}

if (/iPhone|iPad|iPod/i.test(navigator.userAgent)) {
    document.body.classList.add('ios');
}

var hash = window.location.hash;

if (
    hash == '#mobilewallets' ||
    hash == '#multicurrencywallet' ||
    hash == '#get-coins' ||
    hash == '#article-bounty' ||
    hash == '#video-bounty' ||
    hash == '#cpc-model' ||
    hash == '#buy'
) {
    window.location.hash = '';
}

$(function() {
    // Adding youtube api script to DOM
    if (!document.querySelector(
            'script[src="https://www.youtube.com/iframe_api"]'
        ) &&
        ($('.promo__video').length || $('.videobox').length)
    ) {
        var scriptElement = document.createElement('script');
        var firstScriptElement = document.body.getElementsByTagName('script')[0];

        scriptElement.src = 'https://www.youtube.com/iframe_api';
        firstScriptElement.parentNode.insertBefore(
            scriptElement,
            firstScriptElement
        );
    }

    // Load youtube iframe
    window.onYouTubeIframeAPIReady = function() {
        var $promoVideo = $('.promo__video');

        $promoVideo.each(function() {
            initPromoPlayer(this);
        });

        if ($('.videobox').length) initVideobox();
    };

    function initPromoPlayer(element) {
        var player = element.querySelector('.promo__video-iframe');
        var button = element.querySelector('.promo__video-btn');
        var id = element.getAttribute('data-id');
        var ytplayer = new YT.Player(player, {
            playerVars: {
                autoplay: 0,
                modestbranding: 1,
                controls: 0,
                rel: 0,
                showinfo: 0
            },
            videoId: id
        });

        button.addEventListener('click', function() {
            switch (ytplayer.getPlayerState()) {
                case 1:
                    ytplayer.stopVideo();
                    element.classList.remove('_active');
                    break;
                default:
                    ytplayer.playVideo();
                    element.classList.add('_active');
                    break;
            }
        });
    }

    function initYTPlayer(element) {
        var player = element.querySelector('.videobox__iframe');
        var button = element.querySelector('.videobox__link');
        var id = element.getAttribute('data-id');
        var ytplayer = new YT.Player(player, {
            playerVars: {
                autoplay: 0,
                modestbranding: 1,
                rel: 0
            },
            videoId: id
        });

        button.addEventListener('click', function(event) {
            element.classList.add('_inited');
            ytplayer.playVideo();

            event.preventDefault();
        });
    }

    // Video tabs
    function initVideobox() {
        $('.videobox').each(function() {
            var $container = $(this);
            var $items = $container.find('.videobox__item');
            var videos = [];

            $items.each(function(index) {
                var $item = $(this);

                videos[index] = {
                    item: $item,
                    button: $item.find('.videobox__link'),
                    player: initVideoboxPlayer($item[0]),
                    tab: $container.find('a[href="#' + $item.attr('id') + '"]')
                };
            });

            videos.forEach(function(video) {
                video.button.on('click', function(event) {
                    event.preventDefault();

                    video.item.addClass('_inited');
                    video.player.playVideo();
                });

                video.tab.on('click', function(event) {
                    event.preventDefault();

                    var $tab = $(this);

                    if ($tab.hasClass('_active')) return;

                    var $activeTab = $tab.siblings('._active');
                    var $activeItem = $container.find('.videobox__item._active');

                    $activeTab.removeClass('_active');
                    $activeItem.removeClass('_active');
                    videos.forEach(function(video) {
                        if (video.player.getPlayerState() == 1) video.player.stopVideo();
                    });

                    video.tab.addClass('_active');
                    video.item.addClass('_active _inited');
                    video.player.playVideo();

                    if (
                        $(window).width() < 700 &&
                        video.item.offset().top - $('header').outerHeight() <
                        $(document).scrollTop()
                    ) {
                        $('html, body').animate({
                                scrollTop: video.item.offset().top - $('header').outerHeight()
                            },
                            500
                        );
                    } else if (
                        $(window).width() < 900 &&
                        video.item.offset().top < $(document).scrollTop()
                    ) {
                        $('html, body').animate({
                                scrollTop: video.item.offset().top
                            },
                            500
                        );
                    }
                });
            });

            function initVideoboxPlayer(element) {
                var player = element.querySelector('.videobox__iframe');
                var id = element.getAttribute('data-video-id');

                return new YT.Player(player, {
                    playerVars: {
                        autoplay: 0,
                        modestbranding: 1,
                        rel: 0
                    },
                    videoId: id
                });
            }
        });
    }

    // Partners slider
    $('.partners').each(function() {
        var $partners = $(this);
        var $container = $partners.find('.partners__container');
        var $wrapper = $partners.find('.partners__wrapper');
        var $slides = $partners.find('.partners__item');
        var windowWidth = $(window).width();
        var partnersSwiper;

        $partners.append('<div class="partners__pagination"></div>');

        var $pagination = $partners.find('.partners__pagination');

        if (windowWidth <= 599) swiperInit();

        $(window).on('resize', function() {
            if (windowWidth <= 599 && $(window).width() > 599) swiperDestroy();

            if (windowWidth > 599 && $(window).width() <= 599) swiperInit();

            windowWidth = $(window).width();
        });

        function swiperInit() {
            $container.addClass('swiper-container');
            $wrapper.addClass('swiper-wrapper');
            $slides.addClass('swiper-slide');

            partnersSwiper = new Swiper($container, {
                slidesPerView: 'auto',
                simulateTouch: false,
                pagination: {
                    el: $pagination,
                    bulletClass: 'partners__bullet',
                    bulletActiveClass: '_active',
                    clickable: true
                }
            });
        }

        function swiperDestroy() {
            $container.removeClass('swiper-container');
            $wrapper.removeClass('swiper-wrapper');
            $slides.removeClass('swiper-slide');

            partnersSwiper.destroy();
        }
    });

    // Services slider
    $('.services').each(function() {
        var $services = $(this);
        var $thumbs = $services.find('.services__thumbs');
        var $content = $services.find('.services__content');
        var $thumbsSlides = $thumbs.find('.swiper-slide');
        var activeSlideIndex = $thumbs.find('.swiper-slide._active').index();

        if (activeSlideIndex < 0) {
            activeSlideIndex = 0;
        }

        $thumbs.after(
            '<button class="services__arrow _type_prev"></button><button class="services__arrow _type_next"></button>'
        );
        $thumbsSlides[0].classList.add('_active');

        var $prevBtn = $services.find('.services__arrow._type_prev');
        var $nextBtn = $services.find('.services__arrow._type_next');

        var contentSwiper = new Swiper($content, {
            initialSlide: activeSlideIndex,
            simulateTouch: false,
            navigation: {
                prevEl: $prevBtn,
                nextEl: $nextBtn
            },
            autoHeight: true
        });

        var thumbsSwiper = new Swiper($thumbs, {
            initialSlide: activeSlideIndex,
            simulateTouch: false,
            slidesPerView: 'auto',
            on: {
                slideChange: function() {}
            }
        });

        contentSwiper.on('slideChange', function() {
            var currentIndex = contentSwiper.activeIndex;

            thumbsSwiper.slideTo(currentIndex);
            $thumbsSlides.removeClass('_active');
            $thumbsSlides[currentIndex].classList.add('_active');
        });

        thumbsSwiper.on('slideChange', function() {
            var currentIndex = thumbsSwiper.activeIndex;

            contentSwiper.slideTo(currentIndex);
            $thumbsSlides.removeClass('_active');
            $thumbsSlides[currentIndex].classList.add('_active');
        });

        $thumbsSlides.on('click', function() {
            var $clickedSlide = $(this);

            if (!$clickedSlide.hasClass('_active')) {
                $thumbsSlides.removeClass('_active');
                $clickedSlide.addClass('_active');
                contentSwiper.slideTo($clickedSlide.index());
            }
        });
    });

    // Gallery
    $('.gallery').each(function() {
        var $gallery = $(this);
        var $elements = $gallery.find('[data-fancybox]');

        $elements.fancybox({
            loop: true,
            animationEffect: 'fade',
            transitionEffect: 'slide',
            buttons: ['close']
        });
    });

    // Channels Slider
    $('.channels').each(function() {
        var $container = $(this);
        var $list = $container.find('.channels__list');

        $list.after('<div class="channels__pagination"></div>');

        var $pagination = $container.find('.channels__pagination');

        new Swiper($list, {
            simulateTouch: false,
            slidesPerView: 'auto',
            pagination: {
                el: $pagination,
                bulletClass: 'channels__bullet',
                bulletActiveClass: '_active',
                clickable: true
            }
        });
    });

    // History slider
    $('.history').each(function() {
        var $holder = $(this);
        var $container = $holder.find('.history__container');
        var lastSlideIndex = $container.find('.swiper-slide').length - 1;

        $container.after(
            '<button class="history__arrow _type_prev"></button><button class="history__arrow _type_next"></button>'
        );

        var $prevBtn = $holder.find('.history__arrow._type_prev');
        var $nextBtn = $holder.find('.history__arrow._type_next');

        new Swiper($container, {
            simulateTouch: false,
            initialSlide: lastSlideIndex,
            reverseDirection: true,
            slidesPerView: 'auto',
            navigation: {
                nextEl: $nextBtn,
                prevEl: $prevBtn
            }
        });
    });

    // Filter select
    filterInit();

    // Clients
    $('.clients').each(function() {
        var $clients = $(this);
        var $slider = $clients.find('.clients__slider');
        var $toggles = $clients.find('.clients__link._toggle');
        var $contentsWrapper = $clients.find('.clients__contents-wrapper');
        var clientsItemsQuantity = $clients.find('.clients__item').length;

        $slider.after(
            '<button class="clients__arrow _type_prev"></button><button class="clients__arrow _type_next"></button>'
        );

        var $prevBtn = $clients.find('.clients__arrow._type_prev');
        var $nextBtn = $clients.find('.clients__arrow._type_next');

        var contentSwiper = new Swiper($slider, {
            init: false,
            simulateTouch: false,
            slidesPerView: 'auto',
            navigation: {
                prevEl: $prevBtn,
                nextEl: $nextBtn
            },
            on: {
                init: toggleArrows,
                slideChange: function() {
                    var $activeItem = $clients.find('.clients__item._active');
                    var $activeContent = $clients.find('.clients__content._active');

                    if ($activeItem.length && $activeContent.length) {
                        slideUpContent($activeItem, $activeContent);
                    }
                },
                resize: toggleArrows
            }
        });

        contentSwiper.init();

        $toggles.each(function() {
            var $toggle = $(this);
            var $toggleHolder = $toggle.parent('.clients__item');
            var id = $toggle.attr('href');
            var $content = $(id);
            var $newsline = $content.find('.newsline');
            var newslineItemsQuantity = $newsline.find('.newsline__item').length;
            var newslineSlider;
            var $newslinePagination;

            if ($newsline.length) {
                $newsline.append('<div class="newsline__pagination"></div>');
                $newslinePagination = $newsline.find('.newsline__pagination');
            }

            $toggle.on('click', function(event) {
                if ($toggleHolder.hasClass('_active')) {
                    slideUpContent($toggleHolder, $content);
                } else {
                    if ($(window).width() < 600) {
                        $('html, body').animate({
                            scrollTop: $clients.offset().top - 34
                        });
                    }

                    slideDownContent($toggleHolder, $content);

                    if ($newsline.length) {
                        if (!newslineSlider) {
                            newslineSlider = new Swiper($newsline, {
                                slidesPerView: 'auto',
                                slidesPerGroup: 4,
                                simulateTouch: false,
                                pagination: {
                                    el: $newslinePagination,
                                    clickable: true,
                                    bulletClass: 'newsline__bullet',
                                    bulletActiveClass: '_active'
                                },
                                breakpoints: {
                                    599: {
                                        slidesPerGroup: 1
                                    },
                                    899: {
                                        slidesPerGroup: 2
                                    },
                                    1189: {
                                        slidesPerGroup: 3
                                    }
                                }
                            });
                        } else {
                            newslineSlider.update();
                        }

                        togglePagination($newslinePagination, newslineItemsQuantity);
                    }
                }

                event.preventDefault();
            });

            $(window).on('resize', function() {
                if ($newsline.length && $newsline.is(':visible'))
                    togglePagination($newslinePagination, newslineItemsQuantity);
            });
        });

        function toggleArrows() {
            if (
                ($(window).width() < 692 && clientsItemsQuantity < 2) ||
                ($(window).width() < 920 && clientsItemsQuantity < 3) ||
                ($(window).width() < 1148 && clientsItemsQuantity < 4) ||
                ($(window).width() < 1376 && clientsItemsQuantity < 5) ||
                ($(window).width() >= 1376 && clientsItemsQuantity < 6)
            ) {
                $prevBtn.addClass('_hidden');
                $nextBtn.addClass('_hidden');
            } else {
                $prevBtn.removeClass('_hidden');
                $nextBtn.removeClass('_hidden');
            }
        }

        function slideDownContent($item, $content) {
            var $activeContent = $content.siblings('.clients__content._active');
            var $activeItem = $item.siblings('.clients__item._active');
            var oldHeight = $activeContent.outerHeight() || 0;

            $contentsWrapper.css('height', oldHeight);
            $activeItem.removeClass('_active');
            $activeContent.removeClass('_active');
            $item.addClass('_active');
            $content.addClass('_active');

            var newHeight = $content.outerHeight();

            setTimeout(function() {
                $contentsWrapper.css('height', newHeight);
            }, 0);

            setTimeout(function() {
                $contentsWrapper.css('height', '');
                $(document).trigger('showClientNews');
            }, 200);
        }

        function slideUpContent($item, $content) {
            var contentHeight = $content.outerHeight();

            $contentsWrapper.css('height', contentHeight);
            $item.removeClass('_active');

            setTimeout(function() {
                $contentsWrapper.css('height', 0);
            }, 0);

            setTimeout(function() {
                $content.removeClass('_active');
                $contentsWrapper.css('height', '');
                $(document).trigger('showClientNews');
            }, 200);
        }

        function togglePagination($el, quantity) {
            if (
                quantity < 2 ||
                (quantity < 3 && $(window).width() > 599) ||
                (quantity < 4 && $(window).width() > 899) ||
                (quantity < 5 && $(window).width() > 1189)
            ) {
                $el.addClass('_hidden');
            } else {
                $el.removeClass('_hidden');
            }
        }
    });

    // Staff slider
    $('.staff').each(function() {
        var $staff = $(this);
        var slidesQuantity = $staff.find('.swiper-slide').length;
        var windowWidth = $(window).width();
        var staffSlider;

        $staff.append(
            '<div class="staff__nav"><button class="staff__arrow _type_prev"></button><button class="staff__arrow _type_next"></button></div>'
        );

        var $nav = $staff.find('.staff__nav');
        var $prevButton = $staff.find('.staff__arrow._type_prev');
        var $nextButton = $staff.find('.staff__arrow._type_next');

        if (slidesQuantity < 2) $nav.addClass('_hidden');

        initStaffSlider();

        $(window).on('resize', function() {
            initStaffSlider();

            windowWidth = $(window).width();
        });

        function initStaffSlider() {
            if (
                (windowWidth > 768 && $(window).width() <= 768) ||
                (!staffSlider && $(window).width() <= 768)
            ) {
                staffSlider = new Swiper($staff, {
                    slidesPerView: 1,
                    simulateTouch: false,
                    navigation: {
                        prevEl: $prevButton,
                        nextEl: $nextButton
                    }
                });
            } else if (windowWidth <= 768 && $(window).width() > 768) {
                staffSlider.destroy();
            }
        }
    });

    // Latest news
    $('.latestNews').each(function() {
        var $latestNews = $(this);
        var $latestNewsWrapper = $latestNews.find('.swiper-wrapper');
        var slidesQuantity = $latestNews.find('.swiper-slide').length;
        var $latestNewsImages = $latestNews.find('img');
        var loadedImages = 0;

        $latestNews.append('<div class="latestNews__pagination"></div>');

        var $pagination = $latestNews.find('.latestNews__pagination');

        var latestNewsSlider = new Swiper($latestNews, {
            init: false,
            slidesPerView: 'auto',
            simulateTouch: false,
            pagination: {
                el: $pagination,
                clickable: true,
                bulletClass: 'latestNews__bullet',
                bulletActiveClass: '_active'
            },
            on: {
                init: function() {
                    setSliderHeight(latestNewsSlider, $latestNewsWrapper);
                    togglePaginationVisibility($pagination, slidesQuantity);
                },
                slideChange: function() {
                    setSliderHeight(latestNewsSlider, $latestNewsWrapper);
                },
                resize: function() {
                    setSliderHeight(latestNewsSlider, $latestNewsWrapper);
                    togglePaginationVisibility($pagination, slidesQuantity);
                }
            }
        });

        $latestNewsImages.each(function() {
            var image = this;

            if (image.complete) {
                loadedImages++;

                if (loadedImages === $latestNewsImages.length) latestNewsSlider.init();
            } else {
                $(image).on('load', function() {
                    loadedImages++;

                    if (loadedImages === $latestNewsImages.length)
                        latestNewsSlider.init();
                });
            }
        });
    });

    // Accents
    $('.accents').each(function() {
        var $accents = $(this);
        var $accentsWrapper = $accents.find('.swiper-wrapper');
        var slidesQuantity = $accents.find('.swiper-slide').length;
        var $accentsImages = $accents.find('img');

        $accents.append('<div class="accents__pagination"></div>');

        var $pagination = $accents.find('.accents__pagination');

        var accentsSlider = new Swiper($accents, {
            init: false,
            slidesPerView: 3,
            slidesPerGroup: 3,
            simulateTouch: false,
            pagination: {
                el: $pagination,
                clickable: true,
                bulletClass: 'accents__bullet',
                bulletActiveClass: '_active'
            },
            breakpoints: {
                991: {
                    slidesPerView: 2,
                    slidesPerGroup: 2
                },
                519: {
                    slidesPerView: 1,
                    slidesPerGroup: 1
                }
            },
            on: {
                init: function() {
                    setSliderHeight(accentsSlider, $accentsWrapper);
                    togglePaginationVisibility($pagination, slidesQuantity);
                },
                slideChange: function() {
                    setSliderHeight(accentsSlider, $accentsWrapper);
                    console.log('slide change');
                },
                resize: function() {
                    setSliderHeight(accentsSlider, $accentsWrapper);
                    togglePaginationVisibility($pagination, slidesQuantity);
                }
            }
        });

        initSliderAfterLoadAllImages(accentsSlider, $accentsImages);
    });

    function initSliderAfterLoadAllImages(slider, $images) {
        var loadedImages = 0;

        if ($images.length == 0) {
            slider.init();
            return;
        }

        $images.each(function() {
            var image = this;

            if (image.complete) {
                loadedImages++;

                if (loadedImages === $images.length) slider.init();
            } else {
                $(image).on('load', function() {
                    loadedImages++;

                    if (loadedImages === $images.length) slider.init();
                });
            }
        });
    }

    function setSliderHeight(slider, $wrapper) {
        var activeSlide = slider.slides[slider.activeIndex];
        var nextSlide = slider.slides[slider.activeIndex + 1];
        var nextNextSlide = slider.slides[slider.activeIndex + 2];
        var newSliderHeight = activeSlide.offsetHeight;

        if ($(window).width() >= 992 && slider.slides.length >= 3) {
            newSliderHeight = Math.max(
                activeSlide.offsetHeight,
                nextSlide.offsetHeight,
                nextNextSlide.offsetHeight
            );
        } else if (
            $(window).width() >= 520 &&
            $(window).width() < 992 &&
            slider.slides.length >= 2
        ) {
            newSliderHeight = Math.max(
                activeSlide.offsetHeight,
                nextSlide.offsetHeight
            );
        }
        $wrapper.css('height', newSliderHeight);
    }

    function togglePaginationVisibility($pagination, quantity) {
        if (
            ($(window).width() < 520 && quantity < 2) ||
            ($(window).width() < 992 && quantity < 3) ||
            ($(window).width() >= 992 && quantity < 4)
        ) {
            $pagination.addClass('_hidden');
        } else {
            $pagination.removeClass('_hidden');
        }
    }

    // Promo
    $('.promo').each(function() {
        var $promo = $(this);
        var $promoSliderContainer = $promo.find('.promo__slider');
        var slidesQuantity = $promoSliderContainer.find('.swiper-slide').length;

        if (slidesQuantity > 1) {
            $promo.append('<div class="promo__pagination"></div>');

            var $pagination = $promo.find('.promo__pagination');

            var promoSlider = new Swiper($promoSliderContainer, {
                simulateTouch: false,
                autoHeight: true,
                pagination: {
                    el: $pagination,
                    clickable: true,
                    bulletClass: 'promo__bullet',
                    bulletActiveClass: '_active'
                },
                on: {
                    slideChange: function() {
                        var isVideo = promoSlider.slides[
                            promoSlider.previousIndex
                        ].querySelector('.promo__video');

                        if (isVideo) {
                            isVideo.classList.remove('_active');
                            YT.get(isVideo.querySelector('iframe').id).stopVideo();
                        }
                    }
                }
            });
        }
    });

    // Tabs
    $('.tabs').each(function() {
        var $tabs = $(this);
        var $tabsList = $tabs.find('.tabs__list');
        var $tabsSlider = $tabs.find('.tabs__contents');
        var $tabsItems = $tabs.find('.tabs__item');
        var $tabsLinks = $tabs.find('.tabs__link');

        $tabsSlider.append('<div class="tabs__pagination"></div>');

        if (!$tabs.find('.tabs__item._active').length) {
            $tabsItems[0].classList.add('_active');
        }

        var $tabsPagination = $tabs.find('.tabs__pagination');

        var tabsSwiper = new Swiper($tabsSlider, {
            init: false,
            autoHeight: true,
            speed: 0,
            simulateTouch: false,
            pagination: {
                el: $tabsPagination,
                clickable: true,
                bulletClass: 'tabs__bullet',
                bulletActiveClass: '_active'
            },
            breakpoints: {
                899: {
                    speed: 300
                }
            },
            on: {
                init: function() {
                    hideFirstSlide();
                    setTabsSliderHeight();
                },
                resize: function() {
                    hideFirstSlide();
                    setTabsSliderHeight();
                },
                slideChange: function() {
                    hideFirstSlide();
                    changeActiveTab();
                    setTabsSliderHeight();
                }
            }
        });

        tabsSwiper.init();

        $tabsLinks.on('click', function() {
            var $tabsItem = $(this).parent('.tabs__item');
            var newIndex = $tabsItem.index();

            tabsSwiper.slideTo(newIndex);
            return false;
        });

        $(document).on('showClientNews', setTabsSliderHeight);

        function setTabsSliderHeight() {
            var $activeSlide = $(tabsSwiper.slides[tabsSwiper.activeIndex]);

            $tabsSlider.css('height', $activeSlide.outerHeight());
        }

        function changeActiveTab() {
            var currentIndex = tabsSwiper.activeIndex;
            var $newActiveTab = $($tabsItems[currentIndex]);
            var $oldActiveTab = $newActiveTab.siblings('.tabs__item._active');

            $oldActiveTab.removeClass('_active');
            $newActiveTab.addClass('_active');
        }

        function hideFirstSlide() {
            if (!$tabs.hasClass('_skip_first')) return;

            if ($(window).width() < 900) {
                if (tabsSwiper.activeIndex <= 1) {
                    tabsSwiper.allowSlidePrev = false;
                } else {
                    tabsSwiper.allowSlidePrev = true;
                }

                if (tabsSwiper.activeIndex == 0) tabsSwiper.slideNext();
            }

            if ($(window).width() >= 900) {
                tabsSwiper.allowSlidePrev = true;
            }
        }
    });

    // Intro
    $('.intro').each(function() {
        var $intro = $(this);
        var $btn = $intro.find('.intro__more-btn');
        var $link = $intro.find('.intro__more-link');
        var $hidden = $intro.find('.intro__hidden-2');
        var $coinsLink = $intro.find('.intro__coins-link');

        $btn.on('click', function() {
            $intro.addClass('_open');
        });

        $link.on('click', function() {
            $intro.toggleClass('_open');
            $hidden.slideToggle(400);

            return false;
        });

        $coinsLink.on('click', function() {
            var $coins = $('#get-coins');
            var verticalOffset;

            if ($coins.length) {
                verticalOffset =
                    $(window).width() >= 700 ?
                    $coins.offset().top :
                    $coins.offset().top - 75;
                $coins.addClass('_open');
                $('html, body').animate({
                        scrollTop: verticalOffset
                    },
                    500
                );
            }

            return false;
        });
    });

    // Join our telegram
    $('.join-telegram').each(function() {
        var $this = $(this);
        var $closeButton = $this.find('.join-telegram__close');
        var $footer = $('.footer');

        if (localStorage.getItem('doNotShowJoinTelegram') != 'true') {
            $('body').addClass('_visible_telegram');

            $(window).on('scroll resize', function() {
                if (
                    $(document).scrollTop() + $(window).height() >
                    $footer.offset().top + 46
                ) {
                    $this.addClass('_absolute');
                } else {
                    $this.removeClass('_absolute');
                }
            });

            $closeButton.on('click', function() {
                $('body').removeClass('_visible_telegram');
                localStorage.setItem('doNotShowJoinTelegram', 'true');
            });
        }
    });

    // Animate elements
    $('.animate-it').each(function() {
        var el = this;

        checkViewport();

        $(window).on('scroll resize', checkViewport);

        function checkViewport() {
            if (!el.classList.contains('_animated')) {
                var animateOffset = $(window).width() >= 600 ? -120 : -60;

                if (
                    inViewport(el, {
                        offset: animateOffset
                    })
                )
                    el.classList.add('_animated');
            }
        }
    });

    // Docs
    $('.docs').each(function() {
        var $docs = $(this);
        var $docsToggle = $docs.find('.docs__toggle, .docs__submenu-toggle');

        $docsToggle.on('click', function() {
            var $toggle = $(this);
            var $holder = $toggle.parent();
            var $submenu = $toggle.siblings('.docs__submenu');

            if ($holder.hasClass('_active')) {
                $submenu.slideUp(300);

                setTimeout(function() {
                    $holder.removeClass('_active');
                }, 300);
            } else {
                $submenu.slideDown(300);
                $holder.addClass('_active');
            }
        });
    });

    // Solution
    $('.solution').each(function() {
        var $solution = $(this);
        var $toggle = $solution.find('.solution__details');
        var $info = $solution.find('.solution__info');

        $toggle.on('click', function() {
            $toggle.slideUp(400);
            $info.slideDown(400);

            return false;
        });
    });

    // Show More Button
    $('.show-more-button').on('click', function() {
        $(this).slideUp(400);
        $(this)
            .next('.hidden')
            .slideDown(400);
    });

    // Services dropdown
    $('.services-dd').each(function() {
        var $holder = $(this);
        var $toggle = $holder.find('.services-dd__btn');
        var $closeBtn = $holder.find('.services-dd__close');

        $toggle.on('click', function() {
            $holder.toggleClass('_open');
        });

        $closeBtn.on('click', function() {
            $holder.removeClass('_open');
        });

        $(document).on('click', function(event) {
            if (!$(event.target).parents('.services-dd').length &&
                $holder.hasClass('_open')
            ) {
                $holder.removeClass('_open');
            }
        });
    });

    // Others toggle items
    $('.others').each(function() {
        var $holder = $(this);
        var $toggle = $holder.find('.others__more-link');
        var $hidden = $holder.find('.others__hidden');

        $toggle.on('click', function() {
            var toggleText = $toggle.text();

            if ($holder.hasClass('_open')) {
                $hidden.css('height', $hidden.outerHeight());

                setTimeout(function() {
                    $hidden.css('height', 0);

                    setTimeout(function() {
                        $hidden.css('height', '');
                        $holder.removeClass('_open');
                    }, 400);
                }, 10);
            } else {
                var newHeight = $hidden.outerHeight();

                $hidden.css('height', 0);

                setTimeout(function() {
                    $holder.addClass('_open');
                    $hidden.css('height', newHeight);

                    setTimeout(function() {
                        $hidden.css('height', '');
                    }, 400);
                }, 10);
            }

            $toggle.text($toggle.data('alt-text'));
            $toggle.data('alt-text', toggleText);

            return false;
        });
    });

    // Blockchain services
    $('.b-services__slider').each(function() {
        var $services = $(this);
        var $servicesWrapper = $services.find('.swiper-wrapper');
        var slidesQuantity = $services.find('.swiper-slide').length;
        var $servicesImages = $services.find('img');

        $services.append('<div class="b-services__pagination"></div>');

        var $pagination = $services.find('.b-services__pagination');

        var servicesSlider = new Swiper($services, {
            init: false,
            slidesPerView: 3,
            slidesPerGroup: 3,
            simulateTouch: false,
            pagination: {
                el: $pagination,
                clickable: true,
                bulletClass: 'b-services__bullet',
                bulletActiveClass: '_active'
            },
            breakpoints: {
                991: {
                    slidesPerView: 2,
                    slidesPerGroup: 2
                },
                519: {
                    slidesPerView: 1,
                    slidesPerGroup: 1
                }
            },
            on: {
                init: function() {
                    setSliderHeight(servicesSlider, $servicesWrapper);
                    togglePaginationVisibility($pagination, slidesQuantity);
                },
                slideChange: function() {
                    setSliderHeight(servicesSlider, $servicesWrapper);
                },
                resize: function() {
                    setSliderHeight(servicesSlider, $servicesWrapper);
                    togglePaginationVisibility($pagination, slidesQuantity);
                }
            }
        });

        initSliderAfterLoadAllImages(servicesSlider, $servicesImages);
    });

    // Customers
    $('.customers').each(function() {
        var $customers = $(this);
        var $customersWrapper = $customers.find('.swiper-wrapper');
        var slidesQuantity = $customers.find('.swiper-slide').length;
        var $customersImages = $customers.find('img');

        $customers.append('<div class="customers__pagination"></div>');

        var $pagination = $customers.find('.customers__pagination');

        var customersSlider = new Swiper($customers, {
            init: false,
            slidesPerView: 2,
            slidesPerGroup: 2,
            simulateTouch: false,
            pagination: {
                el: $pagination,
                clickable: true,
                bulletClass: 'customers__bullet',
                bulletActiveClass: '_active'
            },
            breakpoints: {
                991: {
                    slidesPerView: 1,
                    slidesPerGroup: 1
                }
            },
            on: {
                init: function() {
                    setCustomersSliderHeight(customersSlider, $customersWrapper);
                    toggleCustomersPaginationVisibility($pagination, slidesQuantity);
                },
                slideChange: function() {
                    setCustomersSliderHeight(customersSlider, $customersWrapper);
                },
                resize: function() {
                    setCustomersSliderHeight(customersSlider, $customersWrapper);
                    toggleCustomersPaginationVisibility($pagination, slidesQuantity);
                }
            }
        });

        initSliderAfterLoadAllImages(customersSlider, $customersImages);
    });

    function setCustomersSliderHeight(slider, $wrapper) {
        var activeSlide = slider.slides[slider.activeIndex];
        var nextSlide = slider.slides[slider.activeIndex + 1];
        var newSliderHeight = activeSlide.offsetHeight;

        if ($(window).width() >= 992 && slider.slides.length >= 2) {
            newSliderHeight = Math.max(
                activeSlide.offsetHeight,
                nextSlide.offsetHeight
            );
        }

        $wrapper.css('height', newSliderHeight);
    }

    function toggleCustomersPaginationVisibility($pagination, quantity) {
        if (
            ($(window).width() < 992 && quantity < 2) ||
            ($(window).width() >= 992 && quantity < 3)
        ) {
            $pagination.addClass('_hidden');
        } else {
            $pagination.removeClass('_hidden');
        }
    }

    // Float placeholder
    $('.form__group').each(function() {
        var $holder = $(this);
        var $entry = $holder.find('.form__entry');

        if ($entry.val() != '') {
            $holder.addClass('_filled');
        }

        $entry.on('focus', function() {
            $holder.addClass('_filled');
        });

        $entry.on('blur', function() {
            if ($entry.val() == '') {
                $holder.removeClass('_filled');
            }
        });
    });

    // Feedback
    $('.feedback').each(function() {
        var $holder = $(this);
        var $header = $holder.find('.feedback__header');
        var $toggle = $holder.find('.feedback__toggle');
        var $body = $holder.find('.feedback__body');
        var $form = $holder.find('.feedback__form');

        $toggle.on('click', function() {
            $header.slideUp(400);
            $body.slideDown(400);

            setTimeout(function() {
                var scrollOffset =
                    $(window).width() >= 700 ?
                    $body.offset().top :
                    $body.offset().top - 75;

                $('html, body').animate({
                        scrollTop: scrollOffset
                    },
                    400
                );
            }, 400);
        });
    });

    // Services filter
    $('.js-services-filter').each(function() {
        var $holder = $(this);
        var $links = $holder.find('.js-services-filter-link');
        var $items = $holder.find('.js-services-filter-item');

        $links.on('click', function(event) {
            var $link = $(this);
            var id = $link.attr('href').substr(1);
            var buttonText = $link.find('.js-services-filter-text').text();
            var $wrapper = $link.parents('.services-dd');
            var $buttonText = $wrapper.find('.services-dd__btn-text');

            $items.removeClass('_animated');
            $wrapper.removeClass('_open');
            $buttonText.text(buttonText);

            setTimeout(function() {
                if (id == 'all') {
                    $items.removeClass('_hidden');
                } else {
                    var $activeItem = $('#' + id);
                    var $siblingsItems = $activeItem.siblings('.js-services-filter-item');

                    $activeItem.removeClass('_hidden');
                    $siblingsItems.addClass('_hidden');
                    $siblingsItems.removeClass('_animated');
                }

                $(window).scroll();
            }, 400);

            return false;
        });
    });

    // Wallets
    $('.js-wallets').each(function() {
        var $wallets = $(this);
        var $toggleLink = $wallets.find('.js-wallets-toggle-link');

        $toggleLink.on('click', function() {
            var $group = $(this).parents('.js-wallets-group');
            var $toggle = $group.find('.js-wallets-toggle');
            var $body = $group.find('.js-wallets-body');

            $toggle.slideUp(400);
            $body.slideDown(400);

            return false;
        });
    });

    // Mobile Wallets Scroll to Id
    if (hash == '#mobilewallets') {
        setTimeout(function() {
            window.scrollTo(0, 0);
        }, 1);

        $('.animate-it').each(function(index, value) {
            this.classList.add('_animated');
        });

        var $group = $('.js-wallets-group._type_mobile');
        var $toggle = $group.find('.js-wallets-toggle');
        var $body = $group.find('.js-wallets-body');

        $toggle.css('display', 'none');
        $body.css('display', 'block');

        setTimeout(function() {
            if ($('header').css('position') == 'fixed') {
                $('html, body').animate({
                        scrollTop: $(hash).offset().top -
                            parseInt($('header').css('height'), 10) -
                            20
                    },
                    1000
                );
            } else {
                $('html, body').animate({
                    scrollTop: $(hash).offset().top - 20
                }, 1000);
            }
        }, 1000);
    }

    // Get Coins Scroll to Id
    if (hash == '#get-coins') {
        setTimeout(function() {
            window.scrollTo(0, 0);
        }, 1);

        $('.animate-it').each(function(index, value) {
            this.classList.add('_animated');
        });

        var $getCoins = $(hash);
        var $getCoinsHeader = $getCoins.find('.feedback__header');
        var $getCoinsBody = $getCoins.find('.feedback__body');

        $getCoinsHeader.css('display', 'none');
        $getCoinsBody.css('display', 'block');

        setTimeout(function() {
            if ($('header').css('position') == 'fixed') {
                $('html, body').animate({
                        scrollTop: $(hash).offset().top -
                            parseInt($('header').css('height'), 10) -
                            20
                    },
                    1000
                );
            } else {
                $('html, body').animate({
                    scrollTop: $(hash).offset().top - 20
                }, 1000);
            }
        }, 1000);
    }

    // Multicurrency Wallet Scroll to Id
    if (hash == '#multicurrencywallet') {
        setTimeout(function() {
            window.scrollTo(0, 0);
        }, 1);

        $('.animate-it').each(function(index, value) {
            this.classList.add('_animated');
        });

        setTimeout(function() {
            if ($('header').css('position') == 'fixed') {
                $('html, body').animate({
                        scrollTop: $(hash).offset().top -
                            parseInt($('header').css('height'), 10) -
                            20
                    },
                    1000
                );
            } else {
                $('html, body').animate({
                    scrollTop: $(hash).offset().top - 20
                }, 1000);
            }
        }, 1000);
    }

    // benefits steps two
    if (hash == '#buy') {
        setTimeout(function() {
            window.scrollTo(0, 0);
        }, 1);

        $('.animate-it').each(function(index, value) {
            this.classList.add('_animated');
        });

        setTimeout(function() {
            if ($('header').css('position') == 'fixed') {
                $('html, body').animate({
                        scrollTop: $(hash).offset().top -
                            30 -
                            parseInt($('header').css('height'), 10) -
                            20
                    },
                    1000
                );
            } else {
                $('html, body').animate({
                    scrollTop: $(hash).offset().top - 50
                }, 1000);
            }
        }, 1000);
    }

    // Bounty Page
    if (
        hash == '#article-bounty' ||
        hash == '#video-bounty' ||
        hash == '#cpc-model'
    ) {
        setTimeout(function() {
            window.scrollTo(0, 0);
        }, 1);

        $('.animate-it').each(function(index, value) {
            this.classList.add('_animated');
        });

        setTimeout(function() {
            if ($('header').css('position') == 'fixed') {
                $('html, body').animate({
                        scrollTop: $(hash).offset().top - parseInt($('header').css('height'), 10)
                    },
                    1000
                );
            } else {
                $('html, body').animate({
                    scrollTop: $(hash).offset().top
                }, 1000);
            }
        }, 1000);
    }

    // Bounty Page Anchor Box Scroll on Click
    $('.anchor-box__link').click(function(event) {
        var anchor = $(this).attr('href');

        if ($('header').css('position') == 'fixed') {
            $('html, body').animate({
                    scrollTop: $(anchor).offset().top - parseInt($('header').css('height'), 10)
                },
                1000
            );
        } else {
            $('html, body').animate({
                scrollTop: $(anchor).offset().top
            }, 1000);
        }
    });

    // Tooltip
    $('.js-tooltip').each(function() {
        var $holder = $(this);
        var tooltipText = $holder.attr('title');
        var tooltip;
        var tooltipArrow;
        var tooltipCloseBtn;

        $holder.on('mouseenter', function() {
            if ($('body').hasClass('mobile')) return;

            showTooltip();
        });

        $holder.on('mouseleave', function() {
            if ($('body').hasClass('mobile')) return;

            hideTooltip();
        });

        $holder.on('click', function(event) {
            if (!$('body').hasClass('mobile')) return;

            event.preventDefault();

            if (tooltip == undefined) {
                showTooltip();
            } else if (tooltip.parentNode) {
                hideTooltip();
            } else {
                showTooltip();
            }
        });

        function showTooltip() {
            $holder.removeAttr('title');
            tooltip = document.createElement('div');
            tooltipArrow = document.createElement('div');
            tooltipCloseBtn = document.createElement('button');
            tooltip.classList.add('tooltip');
            tooltipArrow.classList.add('tooltip-arrow');
            tooltipCloseBtn.classList.add('tooltip__close');
            tooltip.innerHTML = tooltipText;
            tooltip.appendChild(tooltipCloseBtn);
            document.body.appendChild(tooltip);
            document.body.appendChild(tooltipArrow);

            tooltip.style.top = $holder.offset().top + 'px';
            tooltipArrow.style.top = $holder.offset().top + 'px';
            tooltipArrow.style.left =
                $holder.offset().left + $holder.outerWidth() / 2 + 'px';

            if (
                tooltip.offsetWidth / 2 +
                $holder.outerWidth() / 2 +
                $holder.offset().left >
                $(window).width()
            ) {
                tooltip.style.right = 0;
            } else if (
                $holder.offset().left + $holder.outerWidth() / 2 <
                tooltip.offsetWidth / 2
            ) {
                tooltip.style.left = 0;
            } else {
                tooltip.style.left =
                    $holder.offset().left + $holder.outerWidth() / 2 + 'px';
            }

            if ($holder.hasClass('js-tooltip_large-left')) {
                tooltip.classList.add('tooltip_large-left');
                tooltip.style.left =
                    $holder.offset().left -
                    tooltip.offsetWidth +
                    $holder.width() +
                    parseInt($holder.css('right'), 10) +
                    'px';
            }

            setTimeout(function() {
                tooltip.classList.add('_visible');
                tooltipArrow.classList.add('_visible');
            }, 1);

            $(tooltipCloseBtn).on('click', hideTooltip);
        }

        function hideTooltip() {
            document.body.removeChild(tooltip);
            document.body.removeChild(tooltipArrow);
            $holder.attr('title', tooltipText);
        }
    });

    // Show more
    $('.js-show-more').each(function() {
        var $holder = $(this);
        var $body = $holder.find('.js-show-more-outer');
        var $innerBody = $holder.find('.js-show-more-inner');
        var $showBtn = $holder.find('.js-show-more-button');
        var $footer = $holder.find('.js-show-more-footer');

        $showBtn.on('click', function() {
            $body.css('height', $body.outerHeight());
            $holder.addClass('_open');

            setTimeout(function() {
                $body.css('height', $innerBody.outerHeight());
                $footer.slideUp(400);

                setTimeout(function() {
                    $body.css('height', '');
                    $(window).scroll();
                    setNewHeightToSlider();
                }, 400);
            }, 1);
        });

        function setNewHeightToSlider() {
            var $slider = $holder.parents('.tabs__contents');
            var $slide = $holder.parents('.tabs__content');

            if ($slider.length) {
                $slider.css('height', $slide.outerHeight());
            }
        }
    });

    // Popup init
    popup();

    //  Modals
    $('.fancybox-modal').on('click', function() {
        var dataSrc = $(this).attr('data-modal-id');

        $.fancybox.open({
            src: '#' + dataSrc,
            type: 'inline',
            autoFocus: false,
            animationDuration: 600,
            // hideScrollbar: false,
            opts: {
                beforeClose: function(instance, slide) {
                    $('#intercom-container').removeClass('hidden');
                    if (slide.$slide.find('.feedback')) {
                        slide.$slide
                            .find('.feedback')
                            .removeClass('_success')
                            .find('.feedback__form')[0]
                            .reset();

                        slide.$slide.find('._error').removeClass('_error');
                        slide.$slide.find('.form__error').remove();

                        slide.$slide.find('input, textarea').each(function() {
                            $(this).trigger('blur');
                        });
                    }
                    if (slide.$slide.find('.select-custom__toggle').hasClass('_active')) {
                        slide.$slide.find('.select-custom__dropdown-items').slideUp('400');
                    }
                    if (slide.$slide.find('.select-custom__toggle')) {
                        var defaultText = slide.$slide
                            .find('.select-custom__toggle-text')
                            .attr('data-default-text');

                        slide.$slide
                            .find('.select-custom__toggle')
                            .removeClass('_active')
                            .find('.select-custom__toggle-text')
                            .html(defaultText);
                    }
                    if (slide.$slide.find('.attach-file-custom')) {
                        var defaultFileText = slide.$slide
                            .find('.attach-file-custom__name')
                            .attr('data-default-text');

                        slide.$slide
                            .find('.attach-file-custom')
                            .removeClass('_active')
                            .find('.attach-file-custom__name')
                            .html(defaultFileText);

                        slide.$slide.find('.attach-file-custom__input').val('');
                    }
                },
                beforeLoad: function(instance, slide) {
                    $('#intercom-container').addClass('hidden');
                },
                afterLoad: function(instance, slide) {
                    if (slide.$slide.find('.feedback')) {
                        slide.$slide.click(function name(event) {
                            if (
                                slide.$slide
                                .find('.select-custom__toggle')
                                .hasClass('_active') &&
                                !$(event.target).hasClass('select-custom__toggle') &&
                                !$(event.target).hasClass('select-custom__toggle-text') &&
                                !$(event.target).hasClass('select-custom')
                            ) {
                                slide.$slide
                                    .find('.select-custom__dropdown-items')
                                    .slideUp('400');

                                slide.$slide
                                    .find('.select-custom__toggle')
                                    .removeClass('_active');
                            }
                        });
                    }
                }
            }
        });
    });

    // Form Custom Add File
    $('.attach-file-custom').each(function() {
        var holder = this;
        var input = holder.querySelector('.attach-file-custom__input');
        var name = holder.querySelector('.attach-file-custom__name');
        var resetButton = holder.querySelector('.attach-file-custom__reset-button');
        var placeholder = name.innerHTML;

        input.addEventListener('change', updateFileName);

        resetButton.addEventListener('click', function() {
            input.type = '';
            input.type = 'file';

            updateFileName();
        });

        function updateFileName() {
            var fileName = input.files[0] ? input.files[0].name : undefined;

            if (fileName) {
                name.innerHTML = fileName;
                holder.classList.add('_active');

                var nameNextElem = name.nextElementSibling;
                var namePrevElem = name.previousElementSibling;

                if (nameNextElem && nameNextElem.classList.contains('form__error')) {
                    nameNextElem.remove();
                }

                if (namePrevElem && namePrevElem.classList.contains('_error')) {
                    console.log('error');
                    namePrevElem.classList.remove('_error');
                }
            } else {
                name.innerHTML = placeholder;
                holder.classList.remove('_active');
            }
        }
    });

    // Form Custom Dropdown
    $('.select-custom__toggle').click(function(event) {
        event.preventDefault();
        $(this)
            .next('.select-custom__dropdown')
            .find('.select-custom__dropdown-items')
            .slideToggle('400');
        $(this).toggleClass('_active');
    });

    $('.select-custom__dropdown-item-link').click(function(event) {
        event.preventDefault();

        var selectValue = $(this).html();
        var selectDataId = $(this).attr('data-id');
        var toogler = $(this)
            .closest('.select-custom__dropdown')
            .prev('.select-custom__toggle');

        toogler.find('.select-custom__toggle-text').html(selectValue);

        if (
            $(this)
            .closest('.select-custom__dropdown')
            .next()
            .hasClass('form__error')
        ) {
            console.log(this);
            $(this)
                .closest('.select-custom__dropdown')
                .next('.form__error')
                .remove();
        }

        toogler
            .toggleClass('_active')
            .next('.select-custom__dropdown')
            .find('.select-custom__dropdown-items')
            .slideToggle('400');

        toogler
            .prev('.select-custom__hidden-select')
            .removeClass('_error')
            .removeAttr('selected')
            .find('option[value="' + selectDataId + '"]')
            .prop('selected', true);
    });

    // Worklog
    $('.js-worklog').each(function() {
        var $holder = $(this);
        var $filter = $holder.find('.js-worklog-filter');
        var $filterWrapper = $holder.find('.js-worklog-filter-wrapper');
        var $filterSlides = $holder.find('.js-worklog-filter-slide');
        var $yearsSlider = $holder.find('.js-worklog-years-slider');
        var $yearsSliderWrapper = $holder.find('.js-worklog-years-slider-wrapper');
        var $yearsSlides = $holder.find('.js-worklog-years-slide');
        var $eventsSlider = $holder.find('.js-worklog-events-slider');
        var $eventsSliderWrapper = $holder.find(
            '.js-worklog-events-slider-wrapper'
        );
        var $eventsSlides = $eventsSlider.find('.js-worklog-events-slide');
        var $eventsHolders = $holder.find('.js-worklog-events-holder');
        var $eventsLists = $holder.find('.js-worklog-events-list');
        var $events = $holder.find('.js-worklog-event');
        var $tabs = $holder.find('.js-worklog-tab');
        var $moreLinks = $holder.find('.js-worklog-more-link');
        var $prevBtn = $holder.find('.js-worklog-prev-button');
        var $nextBtn = $holder.find('.js-worklog-next-button');
        var $yearsPrevInfo = $holder.find('.js-worklog-prev-info');
        var $yearsNextInfo = $holder.find('.js-worklog-next-info');
        var initialIndex = 0;
        var windowWidth = $(window).width();
        var activeYear;
        var yearsSwiper;
        var eventsSwiper;
        var filterSwiper;

        if (windowWidth < 600) initFilterSwiper();
        initSwipers();

        $(window).on('resize', function() {
            var newWindowWidth = $(window).width();

            if (
                (newWindowWidth >= 900 && windowWidth < 900) ||
                (newWindowWidth < 900 && windowWidth >= 900)
            ) {
                initSwipers();
            }

            if (newWindowWidth < 600 && windowWidth >= 600) initFilterSwiper();
            if (newWindowWidth >= 600 && windowWidth < 600) destroyFilterSwiper();

            windowWidth = newWindowWidth;
        });

        $tabs.on('click', function() {
            var $tab = $(this);
            var $activeTab = $holder.find('.js-worklog-tab._active');

            if (!$tab.hasClass('_active')) {
                $activeTab.removeClass('_active');
                $tab.addClass('_active');

                activeYear = +$holder
                    .find('.js-worklog-events-slide._active')
                    .data('year');

                $holder.addClass('_changing');
                setTimeout(function() {
                    initSwipers();
                    $holder.removeClass('_changing');
                }, 400);
            }

            return false;
        });

        $(document).on('click', '.js-worklog-years-slide', function() {
            var $yearsSlide = $(this);
            var slideIndex = $yearsSlide.index();

            eventsSwiper.slideTo(slideIndex);
        });

        $moreLinks.on('click', function() {
            var $eventsHolder = $(this).parents('.js-worklog-events-holder');

            if ($eventsHolder.hasClass('_open')) {
                slideUpEvents($eventsHolder);
            } else {
                slideDownEvents($eventsHolder);
            }

            return false;
        });

        function initFilterSwiper() {
            $filter.addClass('swiper-container');
            $filterWrapper.addClass('swiper-wrapper');
            $filterSlides.each(function() {
                var $filterSlide = $(this);

                $filterSlide.css('width', $filterSlide.outerWidth());
                $filterSlide.addClass('swiper-slide');
            });

            filterSwiper = new Swiper($filter, {
                slidesPerView: 'auto',
                freeMode: true,
                spaceBetween: 15
            });
        }

        function destroyFilterSwiper() {
            $filter.removeClass('swiper-container');
            $filterWrapper.removeClass('swiper-wrapper');
            $filterSlides.each(function() {
                var $filterSlide = $(this);

                $filterSlide.css('width', '');
                $filterSlide.removeClass('swiper-slide');
            });

            filterSwiper.destroy();
        }

        function initSwipers() {
            var yearsSwiperDirection =
                $(window).width() >= 900 ? 'vertical' : 'horizontal';
            var eventsSwiperEffect = $(window).width() >= 900 ? 'fade' : 'slide';

            filterEvents();

            if ($(window).width() < 900) {
                reverseSlidesOrder($yearsSliderWrapper);
                reverseSlidesOrder($eventsSliderWrapper);
                initialIndex =
                    $eventsSlider.find('.js-worklog-events-slide').length -
                    1 -
                    initialIndex;
            }

            yearsSwiper = new Swiper($yearsSlider, {
                init: false,
                initialSlide: initialIndex,
                direction: yearsSwiperDirection,
                slideActiveClass: '_active',
                slideNextClass: '_next',
                slidePrevClass: '_prev',
                speed: 800,
                on: {
                    init: fillYearsInfo,
                    slideChangeTransitionStart: fillYearsInfo
                }
            });

            eventsSwiper = new Swiper($eventsSlider, {
                init: false,
                initialSlide: initialIndex,
                simulateTouch: false,
                autoHeight: true,
                effect: eventsSwiperEffect,
                slideActiveClass: '_active',
                slideNextClass: '_next',
                slidePrevClass: '_prev',
                speed: 800,
                navigation: {
                    prevEl: $prevBtn,
                    nextEl: $nextBtn,
                    disabledClass: '_disabled'
                },
                on: {
                    slideChange: function() {
                        var $openEventsHolder = $holder.find(
                            '.js-worklog-events-holder._open'
                        );

                        yearsSwiper.slideTo(eventsSwiper.activeIndex);
                        if ($openEventsHolder.length)
                            slideUpEvents($openEventsHolder, true);
                    }
                }
            });

            yearsSwiper.init();
            eventsSwiper.init();
        }

        function reverseSlidesOrder($wrapper) {
            var $slides = $wrapper.children();

            $wrapper.append($slides.get().reverse());
        }

        function destroySwipers() {
            var $openEventsHolder = $holder.find('.js-worklog-events-holder._open');

            yearsSwiper.destroy();
            eventsSwiper.destroy();

            if ($openEventsHolder.length) slideUpEvents($openEventsHolder, true);

            $yearsSliderWrapper.remove('.js-worklog-years-slide');
            $eventsSliderWrapper.remove('.js-worklog-events-slide');

            $yearsSlides.each(function() {
                var $yearsSlide = $(this);

                $yearsSliderWrapper.append($yearsSlide);
            });

            $eventsSlides.each(function() {
                var $eventsSlide = $(this);

                $eventsSliderWrapper.append($eventsSlide);
            });
        }

        function filterEvents() {
            var $activeTab = $holder.find('.js-worklog-tab._active');
            var type = $activeTab.data('type');

            if (yearsSwiper && eventsSwiper) destroySwipers();

            $events.each(function() {
                var $event = $(this);

                $event.removeClass('_inactive');
                if (type != 'all' && $event.data('type') != type)
                    $event.addClass('_inactive');
            });

            collapseEvents();
            initialIndex = getSwiperActiveIndex();
        }

        function collapseEvents() {
            var $eventsHolders = $holder.find('.js-worklog-events-holder');

            $eventsHolders.each(function() {
                var $eventsHolder = $(this);
                var $eventsSlide = $eventsHolder.parents('.js-worklog-events-slide');
                var $yearsSlide = $(
                    $holder.find('.js-worklog-years-slide')[$eventsSlide.index()]
                );
                var $events = $eventsHolder.find('.js-worklog-event');
                var $activeEvents = $eventsHolder.find(
                    '.js-worklog-event:not("._inactive")'
                );
                var $more = $eventsHolder.find('.js-worklog-more');

                $events.removeClass('_hidden');

                if (!$activeEvents.length) {
                    $eventsSlide.remove();
                    $yearsSlide.remove();
                } else if ($activeEvents.length > 6) {
                    for (var i = 6; i < $activeEvents.length; i++) {
                        $($activeEvents[i]).addClass('_hidden');
                        $more.removeClass('_hidden');
                    }
                } else {
                    $more.addClass('_hidden');
                }
            });
        }

        function getSwiperActiveIndex() {
            var $eventsSlides = $holder.find('.js-worklog-events-slide');
            var $lastEventsSlide = $($eventsSlides[$eventsSlides.length - 1]);
            var maxYear = +$eventsSlides[0].getAttribute('data-year');
            var newInitialIndex;

            if (activeYear >= maxYear || activeYear == undefined) {
                newInitialIndex = 0;
            } else if ($lastEventsSlide.data('year') > activeYear) {
                newInitialIndex = $lastEventsSlide.index();
            } else {
                $eventsSlides.each(function() {
                    var $eventsSlide = $(this);
                    var eventsSlideYear = +$eventsSlide.data('year');

                    if (eventsSlideYear == activeYear) {
                        newInitialIndex = $eventsSlide.index();
                    } else if (
                        eventsSlideYear < activeYear &&
                        newInitialIndex == undefined
                    ) {
                        newInitialIndex = $eventsSlide.index() - 1;
                    }
                });
            }

            return newInitialIndex;
        }

        function slideDownEvents($eventsHolder) {
            var $eventsSlide = $eventsHolder.parents('.js-worklog-events-slide');
            var $eventsWrapper = $eventsHolder.find('.js-worklog-events-wrapper');
            var $eventsList = $eventsHolder.find('.js-worklog-events-list');
            var $moreLink = $eventsHolder.find('.js-worklog-more-link');
            var $moreText = $moreLink.find('.js-worklog-more-text');
            var moreText = $moreText.text();

            $eventsWrapper.css('height', $eventsWrapper.outerHeight());
            $eventsHolder.addClass('_open');

            setTimeout(function() {
                $eventsSlide.css(
                    'height',
                    $eventsSlide.outerHeight() +
                    $eventsList.outerHeight() -
                    $eventsWrapper.outerHeight()
                );
                $eventsWrapper.css('height', $eventsList.outerHeight());
                eventsSwiper.updateAutoHeight(800);

                setTimeout(function() {
                    $eventsWrapper.css('height', '');
                }, 800);
            }, 1);

            $moreText.text($moreLink.data('alt-text'));
            $moreLink.data('alt-text', moreText);
        }

        function slideUpEvents($eventsHolder, instantly) {
            var $eventsSlide = $eventsHolder.parents('.js-worklog-events-slide');
            var $eventsWrapper = $eventsHolder.find('.js-worklog-events-wrapper');
            var $activeEvents = $eventsHolder.find(
                '.js-worklog-event:not("._inactive")'
            );
            var $moreLink = $eventsHolder.find('.js-worklog-more-link');
            var $moreText = $moreLink.find('.js-worklog-more-text');
            var moreText = $moreText.text();
            var newWrapperHeight = 0;

            if (instantly) {
                $eventsHolder.removeClass('_open');
                $eventsWrapper.css('height', '');
                $eventsSlide.css('height', '');
            } else {
                for (var i = 0; i < 6; i++) {
                    newWrapperHeight += $($activeEvents[i]).outerHeight();
                }

                $eventsWrapper.css('height', $eventsWrapper.outerHeight());

                setTimeout(function() {
                    $eventsSlide.css(
                        'height',
                        $eventsSlide.outerHeight() +
                        newWrapperHeight -
                        $eventsWrapper.outerHeight()
                    );
                    $eventsWrapper.css('height', newWrapperHeight);

                    eventsSwiper.updateAutoHeight(800);

                    setTimeout(function() {
                        $eventsHolder.removeClass('_open');
                        $eventsWrapper.css('height', '');
                    }, 800);
                }, 1);
            }

            $moreText.text($moreLink.data('alt-text'));
            $moreLink.data('alt-text', moreText);
        }

        function fillYearsInfo() {
            var $activeYear = $yearsSliderWrapper.find(
                '.js-worklog-years-slide._active'
            );
            var $nextYear = $activeYear.next();
            var $prevYear = $activeYear.prev();

            $holder.addClass('_year-changing');

            setTimeout(function() {
                if ($nextYear.length) {
                    $yearsNextInfo.text($nextYear.text());
                } else {
                    $yearsNextInfo.text('');
                }

                if ($prevYear.length) {
                    $yearsPrevInfo.text($prevYear.text());
                } else {
                    $yearsPrevInfo.text('');
                }

                $holder.removeClass('_year-changing');
            }, 400);
        }
    });

    // Textarea autosizing
    $('.entry._textarea').each(function() {
        var textarea = this;

        autosize(textarea);
    });
});

function filterInit() {
    $('.filter').each(function() {
        var $filter = $(this);
        var $links = $filter.find('.filter__link');

        $links.on('click', function(event) {
            var $link = $(this);

            if ($link.hasClass('_active')) {
                if ($(window).width() < 1100) {
                    $filter.toggleClass('_open');
                }

                event.preventDefault();
            }
        });

        $(document).on('click', function(event) {
            if (!$(event.target).closest('.filter._open').length) {
                $filter.removeClass('_open');
            }
        });
    });
}

// Popup
function popup() {
    $('.js-popup').each(function() {
        var popup = this;
        var popupCloseButtons = popup.querySelectorAll('.js-popup-close-button');

        if (popup.parentNode != document.body) {
            popup.parentNode.removeChild(popup);
            document.body.appendChild(popup);
        }

        Array.from(popupCloseButtons).forEach(function(popupCloseButton) {
            popupCloseButton.addEventListener('click', closePopup);
        });

        popup.addEventListener('click', function(event) {
            if (!event.target.closest('.js-popup-body')) {
                closePopup();
            }
        });

        window.addEventListener('keydown', function(event) {
            if (event.keyCode === 27 && popup.classList.contains('_active')) {
                closePopup();
            }
        });
    });

    $('.js-popup-open-button').each(function() {
        var button = this;
        var popupId = !!button.dataset.popup ?
            button.dataset.popup :
            button.getAttribute('href');

        button.addEventListener('click', function(event) {
            openPopup(popupId);
            event.preventDefault();
        });
    });

    function openPopup(popupId) {
        var popup = document.querySelector(popupId);
        var ytVideo = popup.querySelector('.js-popup-yt-video');

        closePopup();

        popup.classList.add('_active');

        setTimeout(function() {
            popup.classList.add('_visible');

            if (ytVideo)
                ytVideo.contentWindow.postMessage(
                    '{"event":"command","func":"' + 'playVideo' + '","args":""}',
                    '*'
                );
        }, 0);

        overlay().show();
    }

    function closePopup() {
        var activePopup = document.querySelector('.js-popup._active');

        if (!activePopup) return;

        var ytVideo = activePopup.querySelector('.js-popup-yt-video');

        activePopup.classList.remove('_visible');

        if (ytVideo)
            ytVideo.contentWindow.postMessage(
                '{"event":"command","func":"' + 'pauseVideo' + '","args":""}',
                '*'
            );

        setTimeout(function() {
            activePopup.classList.remove('_active');

            if (activePopup.id == 'btu__result') {
                document.querySelector('[name=indent]').value = '';
                activePopup.querySelector('.result').innerHTML = '';
            }
        }, 200);

        overlay().hide();
    }

    return {
        open: openPopup,
        close: closePopup
    };
}

function overlay() {
    var html = document.documentElement;
    var body = document.body;
    var overlay = document.querySelector('.overlay');

    function showOverlay() {
        addOverlay();

        if (!overlay.classList.contains('_visible')) {
            overlay.classList.add('_visible');
            fixViewport();
        }
    }

    function hideOverlay() {
        overlay.classList.remove('_visible');
        unfixViewport();
    }

    function addOverlay() {
        if (overlay) return;

        overlay = document.createElement('div');
        overlay.classList.add('overlay');
        document.body.appendChild(overlay);
    }

    function fixViewport() {
        var scrollY = window.scrollY || document.documentElement.scrollTop;

        if (window.innerWidth > document.body.clientWidth)
            html.classList.add('has-scrollbar');

        body.style.marginTop = -scrollY + 'px';
        html.classList.add('fixed');
    }

    function unfixViewport() {
        var newScrollTop = -body.style.marginTop.slice(0, -2);

        html.classList.remove('fixed');
        html.classList.remove('has-scrollbar');
        body.style.marginTop = '';
        window.scrollTo(0, newScrollTop);
    }

    return {
        show: showOverlay,
        hide: hideOverlay
    };
}