import $ from '../globals';

function resultsBorder() {

    const $resultsResult   = $('.js-border-result'),
        $resultsHeading    = $('.js-border-result__heading'),
        $resultsBorder     = $('.js-border-result__border');

    function setResultBorder(){
        $resultsResult.each(function() {
            var headingWidth = $(this).closest('li').find($resultsHeading).width();

            $(this).closest('li').find($resultsBorder).css({
                width : headingWidth
            });
        });
    }

    function bindEvents(){
        $(window).on('load', function(){
            if ($('.js-border-result').length) {
                setResultBorder();
            }
        });
    }

    bindEvents();
}

export default resultsBorder;