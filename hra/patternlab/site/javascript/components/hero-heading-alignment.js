import $ from '../globals';

function heroHeadingAlignment() {

    let $bodyWrapper        = $('.standard-page-body__wrapper'),
        headingHeight       = $('.hero__heading').outerHeight(),
        defaultMargin       = 150,
        breakpoint          = 900;

    function setMargin() {
        if (headingHeight >= defaultMargin && $(window).width() >= breakpoint) {
            $bodyWrapper.css({
                '-webkit-transform': 'translate3d(0, -' + headingHeight + 'px, 0)',
                '-moz-transform': 'translate3d(0, -' + headingHeight + 'px, 0)',
                'transform': 'translate3d(0, -' + headingHeight + 'px, 0)'
            });
        }
    }

    function bindEvents(){
        $(window).on('load', () => setMargin());
    }

    bindEvents();
}

export default heroHeadingAlignment;