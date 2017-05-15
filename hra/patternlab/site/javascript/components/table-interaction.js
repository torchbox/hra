import $ from '../globals';

function tableInteraction() {

    const $tablePinned      = $('.table--pinned'),
        $tableBody          = $('.table--pinned tbody'),
        $navigateLeft       = $('.js-table-left'),
        $navigateRight      = $('.js-table-right'),
        clickDistance       = '200px',
        speed               = 300,
        displayBuffer       = 10;

    let state       = {
        open    : false,
        busy    : false
    };

    function scrollLeft() {

        // Check if scrolling left is possible
        if ($tableBody.scrollLeft() > 0) {
            $tableBody.animate({
                scrollLeft: '-='+ clickDistance +''
            }, speed);
        }
    }

    function scrollRight() {
        let scrollWidth         = $tableBody[0].scrollWidth,
            tableWidth          = $tableBody.outerWidth(),
            scrollPosition      = $tableBody.scrollLeft(),
            offset              = (scrollWidth - tableWidth) - scrollPosition;

        // Check if scrolling right is possible
        if (offset !== 0) {
            $tableBody.animate({
                scrollLeft: '+='+ clickDistance +''
            }, speed);
        }
    }

    function scroll(direction) {

        // Scroll right
        if (direction === 'right') {
            if(!state.busy) {
                state.busy = true;
                setTimeout(() => {
                    scrollRight();
                    state.open = false;
                    state.busy = false;
                }, displayBuffer);
            }
        } 

        // Scroll left
        else {
            if(!state.busy) {
                state.busy = true;
                setTimeout(() => {
                    scrollLeft();
                    state.open = false;
                    state.busy = false;
                }, displayBuffer);
            }
        }
    }

    function bindEvents(){
        if ( $tablePinned.length ) {
            $navigateLeft.on('click', () => scroll('left'));
            $navigateRight.on('click', () => scroll('right'));
        }
    }

    bindEvents();
}

export default tableInteraction;