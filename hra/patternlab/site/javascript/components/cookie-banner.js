import $ from '../globals';

function cookieBanner() {

    const $cookieBanner         = $('#cookie-banner'),
        $html                   = $('html'),
        $acceptButton           = $('#cookie-banner #accept-button'),
        bannerHeight            = $cookieBanner.outerHeight(),
        notificationHide        = 'notification--hide',
        notificationClose       = 'notification--close',
        withFooter              = 'with-footer';

    function openWithAnimation() {
        $cookieBanner.css({ 'margin-top': -bannerHeight });

        setTimeout(() => {
            $cookieBanner.removeClass(notificationClose);
            setTimeout(() => {
                $cookieBanner.removeClass(notificationHide);
                $cookieBanner.css({ 'margin-top': 0 });
            }, 300);
        }, 300);
    }

    function close(){
        $cookieBanner.addClass(notificationClose);
    }

    function closeWithAnimation(){
        // Reduce opacity
        $cookieBanner.addClass(notificationHide);

        // Move out of viewport
        $cookieBanner.css({ 'margin-top' : -bannerHeight });

        // Remove entirely but only after a delay to allow for css animation
        setTimeout(() => close(), 500);
    }

    function closeFooter(){
        $html.removeClass(withFooter);
    }

    function openFooter() {
        $html.addClass(withFooter);
    }

    function init() {
        const cookies = document.cookie.split(';');
        const cookiePreferences = cookies.find(item => item.trim().startsWith(`cookie-preferences_measurement`));
        
        if (!cookiePreferences) {
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
        $acceptButton.on('click', () => {
            if (window.allowMeasurementCookies) {
                window.allowMeasurementCookies();
            }
            closeWithAnimation();
            openFooter();
        });
    }

    init();
    bindEvents();
}

export default cookieBanner;
