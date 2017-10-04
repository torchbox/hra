import Pikaday from 'pikaday';

function datepicker() {

    const dateFrom = new Pikaday({
        field: document.getElementById('date_from'),
        format: 'DD/MM/YYYY',
    });

    const dateTo = new Pikaday({
        field: document.getElementById('date_to'),
        format: 'DD/MM/YYYY',
    });
}

export default datepicker;
