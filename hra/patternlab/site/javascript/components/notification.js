import $ from '../globals';

function notification() {

    const $notification         = $('.notification'),
        $closeButton            = $('.notification__close'),
        notificationHeight      = $notification.outerHeight(),
        notificationDarken      = 'notification--darken',
        notificationHide        = 'notification--hide',
        notificationClose       = 'notification--close';

    function darken(){
        $notification.addClass(notificationDarken);
    }

    function lighten(){
        $notification.removeClass(notificationDarken);
    }

    function close(){

        // Reduce opacity
        $notification.addClass(notificationHide);

        // Move out of viewport
        $notification.css({
            'margin-top' : -notificationHeight
        });

        // Remove entirely
        setTimeout(() => {
            $notification.addClass(notificationClose);
        }, 500);
    }

    function bindEvents(){

        // Visual feedback when hovering on close button
        $closeButton.mouseenter(darken).mouseleave(lighten);

        // Close notification entirely
        $closeButton.on('click', () => close());
    }

    bindEvents();
}

export default notification;