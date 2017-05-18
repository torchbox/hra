import $ from '../globals';

function notification() {

    const $notification         = $('.notification'),
        $closeButton            = $('.notification__close'),
        notificationHeight      = $notification.outerHeight(),
        notificationTime        = $notification.data('updatedAt'),
        notificationStorageKey  = 'notification-bar',
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
        $notification.addClass(notificationClose);
    }

    function open() {
        $notification.removeClass(notificationClose);
    }

    function closeWithAnimation(){

        localStorage.setItem(notificationStorageKey, notificationTime);

        // Reduce opacity
        $notification.addClass(notificationHide);

        // Move out of viewport
        $notification.css({
            'margin-top' : -notificationHeight
        });

        // Remove entirely
        setTimeout(() => {
            close();
        }, 500);
    }

    function init() {
        const latestNotificationTime = localStorage.getItem(notificationStorageKey);

        if (!latestNotificationTime || notificationTime > latestNotificationTime) {
            localStorage.removeItem(notificationStorageKey);
            open();
        } else {
            // Should be closed by default
            close();
        }
    }

    function bindEvents(){

        // Visual feedback when hovering on close button
        $closeButton.mouseenter(darken).mouseleave(lighten);

        // Close notification entirely
        $closeButton.on('click', () => closeWithAnimation());
    }

    init();
    bindEvents();
}

export default notification;