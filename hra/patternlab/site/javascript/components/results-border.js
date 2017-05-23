import $ from '../globals';

function resultsBorder() {

    function setResultBorder(){

        const $resultsResult    = $('.js-border-result'),
            $resultsHeading     = $('.js-border-result__heading'),
            $resultsImage       = $('.js-border-result__image'),
            $resultsBorder      = $('.js-border-result__border'),
            animationSpeed      = 250;

        $resultsResult.each(function() {

            let $closestBorder = $(this).closest('li').find($resultsBorder),
                headingWidth = $(this).closest('li').find($resultsHeading).width(),
                imageAndHeadingWidth = headingWidth + 105;

            // Set larger border width if image is present
            if ($resultsImage.length) {
                $closestBorder.animate({
                    width : imageAndHeadingWidth,
                    opacity: 1
                }, animationSpeed);
            } else {
                $closestBorder.animate({
                    width : headingWidth,
                    opacity: 1
                }, animationSpeed);
            }
        });
    }

    function bindEvents(){
        $(window).on('load refresh-results-border', function(){
            setTimeout(function() {
                setResultBorder();
            }, 150);
        });
    }

    bindEvents();
}

export default resultsBorder;