import $ from './globals';

/* ============================================
    Quick Links
 */
var quickLinks = function() {

    var $trigger            = $('.site-header__quick-links-button'),
        $siteContainer      = $('.site-container'),
        siteContainerPush   = 'site-container--push',
        displayBuffer       = 10,
        state               = {
            open    : false,
            busy    : false
        };

    function open() {
        if( !state.busy ){
            state.busy = true;
            
            setTimeout(function(){
                $siteContainer.addClass(siteContainerPush);
                state.open = true;
                state.busy = false;
            }, displayBuffer );
        }
    }

    function close() {
        if( !state.busy ){
            state.busy = true;

            setTimeout(function(){
                $siteContainer.removeClass(siteContainerPush);
                state.open = false;
                state.busy = false;
            }, displayBuffer );
        }
    }

    function toggle(){
        if( state.open ) {
            close();
        } else {
            open();
        }
    }

    $trigger.on( 'click', function() {
        toggle();
    });

};

quickLinks();
