import $ from '../globals';

function sidebarMenu() {

    const $sidebarMenu          = $('.site-sidebar__menu'),
        $sidebarMenuToggle      = $('.site-sidebar__label'),
        labelActive             = 'site-sidebar__label--active',
        slideSpeed              = 300,
        displayBuffer           = 10;

    let state       = {
        open    : false,
        busy    : false
    };

    function open(){
        if(!state.busy){
            state.busy = true;
            setTimeout(() => {
                $sidebarMenu.slideDown(slideSpeed);
                $sidebarMenuToggle.addClass(labelActive);
                state.open = true;
                state.busy = false;
            }, displayBuffer);
        }
    }

    function close(){
        if(!state.busy){
            state.busy = true;
            setTimeout(() => {
                $sidebarMenu.slideUp(slideSpeed);
                $sidebarMenuToggle.removeClass(labelActive);
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
        $sidebarMenuToggle.on('click', () => toggle());
    }

    bindEvents();
}

export default sidebarMenu;