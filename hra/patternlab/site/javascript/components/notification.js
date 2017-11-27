import $ from '../globals';

function notification() {

    const $notification         = $('.notification').not('.notification--footer'),
        $closeButton            = $('.notification__close'),
        $html                   = $('html'),
        notificationHeight      = $notification.outerHeight(),
        notificationTime        = $notification.data('updatedAt'),
        notificationStorageKey  = 'notification-bar',
        notificationDarken      = 'notification--darken',
        notificationHide        = 'notification--hide',
        notificationClose       = 'notification--close',
        withFooter              = 'with-footer';

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

    function closeFooter(){
        $html.removeClass(withFooter);
    }

    function openFooter() {
        $html.addClass(withFooter);
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
            openFooter();
        }, 500);
    }

    function init() {
        const latestNotificationTime = localStorage.getItem(notificationStorageKey);

        if (!latestNotificationTime || notificationTime > latestNotificationTime) {
            localStorage.removeItem(notificationStorageKey);
            closeFooter();
            openWithAnimation();
        } else {
            // Notification should be closed by default (should contain the `notification--close` class).
            // Otherwise the notification bar will flash to the users who have decided to close the notification.
            close();
            openFooter();
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
