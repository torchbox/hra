import $ from '../globals';

function mobileMenu() {

    const $menuTrigger          = $('.js-mobile-menu-trigger'),
        $menu                   = $('.js-mobile-menu'),
        menuOpen                = 'site-header__right--open',
        displayBuffer           = 10;

    let state       = {
        open    : false,
        busy    : false
    };

    function open(){
        if(!state.busy){
            state.busy = true;
            setTimeout(() => {
                $menu.addClass(menuOpen);
                state.open = true;
                state.busy = false;
            }, displayBuffer);
        }
    }

    function close(){
        if(!state.busy){
            state.busy = true;
            setTimeout(() => {
                $menu.removeClass(menuOpen);
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

    
    function bindEvents(){

        // Toggle tab on click
        $menuTrigger.on('click', () => toggle());

    }

    bindEvents();
}

export default mobileMenu;