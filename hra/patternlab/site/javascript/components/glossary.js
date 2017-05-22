import {jQuery as $, pluralize} from '../globals';

// TODO: polyfill for fetch
function glossary() {

    const $glossary = $('.js-glossary'),
        $glossaryResultsHeading = $glossary.find('.glossary__results-heading'),
        $glossaryResultsContainer = $glossary.find('.glossary__results'),
        glossaryApiURL = $glossary.data('apiUrl');

    function loadData(startswith = null) {
        let data = {};
        if (startswith) {
            data['term_startswith'] = startswith;
        }

        return fetch(glossaryApiURL)
            .then(response => response.json());
    }

    function renderData(startswith = null) {
        const request = loadData(startswith);

        request.then(json => json.items)
            .then(renderResultItems);

        request.then(json => json.meta.total_count)
            .then(renderResultHeader);
    }

    function renderResultItems(items) {
        let resultList = '';
        items.forEach(item => {
            resultList += `
            <li class="glossary__result js-border-result">
                <div class="glossary__result-border js-border-result__border"></div>
                <div class="glossary__result-heading js-border-result__heading">
                    ${item.name}
                    ${item.is_noun ? '<span class="glossary__noun">Noun</span>' : ''}
                </div>
                <div class="glossary__result-content">${item.description}</div>
            </li>`;
        });

        $glossaryResultsContainer.html(resultList);
    }

    function renderResultHeader(totalCount) {
        $glossaryResultsHeading.text(`Found ${totalCount} ${pluralize('result', totalCount)}`);
    }

    function bindEvents() {
        $(document).ready(() => renderData('a'));
    }

    bindEvents();
}

export default glossary;
