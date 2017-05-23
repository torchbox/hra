// Note that the '../globals' module imports fetch polyfill
import {jQuery as $, pluralize} from '../globals';

function glossary() {

    const $glossary = $('.js-glossary'),
        $glossaryResultsHeading = $glossary.find('.glossary__results-heading'),
        $glossaryResultsContainer = $glossary.find('.glossary__results'),
        $glossarySearchInput = $glossary.find('.glossary__search'),
        $glossaryKeyboardLetters = $glossary.find('.keyboard__letter'),
        glossaryKeyboardLettersActiveClass = 'keyboard__letter--active',
        glossaryApiURL = $glossary.data('apiUrl');

    let previousSearchQuery = null;

    function loadListing(startswith = null) {
        let qs = '';
        if (startswith) {
            qs = `?term_startswith=${startswith}`;
        }

        return fetch(glossaryApiURL + qs)
            .then(response => response.json());
    }

    function loadSearchListing(searchQuery) {
        let qs = `?search=${searchQuery}`;

        return fetch(glossaryApiURL + qs)
            .then(response => response.json());
    }

    function renderListingResponse(response) {
        response.then(json => json.items)
            .then(renderResultItems);

        response.then(json => json.meta.total_count)
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

    function renderAllListing() {
        renderListingResponse(
            loadListing()
        );
    }

    function bindEvents() {
        // Initial screen
        $(document).ready(() => renderAllListing());

        // Search functionality
        $glossarySearchInput.on('keyup', () => {
            const searchQuery = $glossarySearchInput.val().trim();

            if (searchQuery.length >= 1) {
                if (searchQuery !== previousSearchQuery) {
                    renderListingResponse(
                        loadSearchListing(searchQuery)
                    );

                    previousSearchQuery = searchQuery;
                }
            } else {
                renderAllListing();
            }

        });

        // Browse by letter functionality
        $glossaryKeyboardLetters.on('click', (e) => {
            const $element = $(e.currentTarget);
            const letter = $element.data('keyboardLetter');

            // Request and render a listing for the given letter
            renderListingResponse(
                loadListing(letter)
            );

            // Deactivate other buttons and activate current button
            $glossaryKeyboardLetters.removeClass(glossaryKeyboardLettersActiveClass);
            $element.addClass(glossaryKeyboardLettersActiveClass);

            // Cleanup the search field
            $glossarySearchInput.val('')
        });
    }

    bindEvents();
}

export default glossary;
