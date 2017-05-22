import $ from '../globals';

function searchFilter() {

    const $searchForm = $('.js-main-search-form');

    function bindEvents(){
        $searchForm.find('input[type="checkbox"]').on('change', function () {
            $searchForm.submit();
        });

        $searchForm.find('select').on('change', function () {
            $searchForm.submit();
        });
    }

    bindEvents();
}

export default searchFilter;
