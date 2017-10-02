import { TinyDatePicker } from '../globals';

function datepicker() {
    TinyDatePicker('.js-datepicker', {
        format(date) {
            return date.toLocaleDateString();
        },
    });
}

export default datepicker;
