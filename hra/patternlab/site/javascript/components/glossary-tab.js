import $ from '../globals';

function glossaryTab() {

    const $glossaryTab          = $('.glossary-tab'),
        $glossaryLabel          = $('.glossary-tab__label'),
        $glossaryClose          = $('.glossary-tab__close'),
        tabOpen                 = 'glossary-tab--open',
        tabFixed                = 'glossary-tab--fixed',
        stickValue              = 600,
        displayBuffer           = 10;

    let state       = {
        open    : false,
        busy    : false
    };

    function open(){
        if(!state.busy){
            state.busy = true;
            setTimeout(() => {
                $glossaryTab.addClass(tabOpen);
                state.open = true;
                state.busy = false;
            }, displayBuffer);
        }
    }

    function close(){
        if(!state.busy){
            state.busy = true;
            setTimeout(() => {
                $glossaryTab.removeClass(tabOpen);
                $glossaryTab.blur();
                state.open = false;
                state.busy = false;
            }, displayBuffer);
        }
    }

    function toggle(){
        if (state.open) {
            close();
        } else {
            open();
        }
    }

    function stick(){
        if ($(document).scrollTop() >= stickValue){
            $glossaryTab.addClass(tabFixed);
        } else {
            $glossaryTab.removeClass(tabFixed);
        }
    }

    function outOfBounds(element){
        if (!$glossaryTab.is(element.target) && $glossaryTab.has(element.target).length === 0) {
            close();
        }
    }

    function focus(element){
        if (!$glossaryLabel.is(element.target) && $glossaryTab.has(element.target).length > 0) {
            if (!state.open) {
                open();
            }
        }
    }

    function bindEvents(){
        if ($(window).width() >= 800) {

            // Toggle tab on click
            $glossaryLabel.on('click', () => toggle());

            // Close tab on click
            $glossaryClose.on('click', () => close());

            // Stick tab on scroll
            $(document).on('scroll', () => stick());

            // Close tab on click outside
            $(document).on('mouseup', e => outOfBounds(e));

            // Open on focus (i.e. keyboard tab)
            $glossaryTab.on('focusin', e => focus(e));

        }
    }

    bindEvents();
}

export default glossaryTab;
