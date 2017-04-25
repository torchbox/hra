import $ from '../globals';

function disableTransition() {

    let transitionElements   = $('.site-header__right'),
        disabledClass        = 'disable-transition',
        delaySpeed           = 300;

    transitionElements.addClass(disabledClass);

    setTimeout(() => {
        transitionElements.removeClass(disabledClass);
    }, delaySpeed);
}

$(window).resize(() => {
    disableTransition();
});

export default disableTransition;