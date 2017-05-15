import $ from '../globals';

function resultsBorder() {

    const $resultsResult    = $('.js-border-result'),
        $resultsHeading     = $('.js-border-result__heading'),
        $resultsImage       = $('.js-border-result__image'),
        $resultsBorder      = $('.js-border-result__border');

    function setResultBorder(){
        $resultsResult.each(function() {
            const $closestBorder = $(this).closest('li').find($resultsBorder),
                headingWidth = $(this).closest('li').find($resultsHeading).width(),
                imageAndHeadingWidth = headingWidth + 105;

            // Set larger border width if image is present
            if ($resultsImage.length) {
                $closestBorder.css({
                    width : imageAndHeadingWidth
                });
            } else {
                $closestBorder.css({
                    width : headingWidth
                });
            }
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