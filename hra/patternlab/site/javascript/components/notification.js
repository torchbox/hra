import $ from '../globals';

function notification() {

    const $notification         = $('.notification').not('.notification--footer').not('#cookie-banner'),
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

    function openWithAnimation() {

        $notification.css({
            'margin-top': -notificationHeight,
        });

        setTimeout(() => {
            open();

            setTimeout(() => {
                $notification.removeClass(notificationHide);

                $notification.css({
                    'margin-top': 0
                });
            }, 300);

        }, 300);
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
            openWithAnimation();
        } else {
            // Notification should be closed by default (should contain the `notification--close` class).
            // Otherwise the notification bar will flash to the users who have decided to close the notification.
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
