import $ from '../globals';

function glossaryBorder() {

    const $glossaryResult   = $('.glossary__result'),
        $glossaryHeading    = $('.glossary__result-heading'),
        $glossaryBorder     = $('.glossary__result-border');

    function setResultBorder(){
        $glossaryResult.each(function() {
            var headingWidth = $(this).closest('li').find($glossaryHeading).width();

            $(this).closest('li').find($glossaryBorder).css({
                width : headingWidth
            })
        });
    }

    function bindEvents(){
        $(window).on('load', function(){
            if ($('.glossary__result').length) {
                setResultBorder()
            }
        });
    }

    bindEvents();
}

export default glossaryBorder;