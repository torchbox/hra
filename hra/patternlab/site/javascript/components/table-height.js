import $ from '../globals';

function tableHeight() {

    var $bodyCell   = $('.table--pinned td, .table--pinned th'),
        tallestCell = null,
        cellHeights = [];

    // Get tallest heading height
    function getTallest() {
        $('.table thead tr th, .table thead tr td').each(function () {
            cellHeights.push($(this).outerHeight());
        });

        tallestCell = Math.max.apply(Math, cellHeights);
    }

    // Update CSS
    function setHeights(item) {
        $(item).css({
            'height' : tallestCell
        });
    }

    // Apply height
    function targetElements() {
        getTallest();

        $bodyCell.each(function () {
            let item = $(this);
            setHeights(item);
        });
    }

    function bindEvents(){
        $(window).on('load', () => targetElements());
    }

    bindEvents();
}

export default tableHeight;
