import { TinyDatePicker } from '../globals';

function datepicker() {

    const datepickers = document.querySelectorAll('.js-datepicker');

    for (let i = 0; i < datepickers.length; i++) {
        TinyDatePicker(datepickers[i], {
            format(date) {
                return date.toLocaleDateString('en-GB');
            },
        });
    }
}

export default datepicker;
