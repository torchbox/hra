import $ from '../globals';

function searchFilter() {

    const $searchForm = $('.js-main-search-form');

    function bindEvents(){
        $searchForm.find('input[type="checkbox"]').on('click', function () {
            $searchForm.submit();
        });
    }

    bindEvents();
}

export default searchFilter;
