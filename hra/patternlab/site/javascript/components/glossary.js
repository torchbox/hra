// Note that the '../globals' module imports fetch polyfill
import {jQuery as $, pluralize} from '../globals';

function glossary() {

    const $container = $('.js-glossary'),
        $resultsHeading = $container.find('.glossary__results-heading'),
        $resultsContainer = $container.find('.glossary__results'),
        $searchInput = $container.find('.glossary__search'),
        $keyboardLetters = $container.find('.keyboard__letter'),
        keyboardLettersActiveClass = 'keyboard__letter--active',
        keyboardLettersDisabledClass = 'keyboard__letter--disabled',
        apiURL = $container.data('apiUrl');

    let previousSearchQuery = null;

    function loadListing(startswith = null) {
        let qs = '';
        if (startswith) {
            qs = `?term_startswith=${startswith}`;
        }

        return fetch(apiURL + qs)
            .then(response => response.json());
    }

    function loadSearchListing(searchQuery) {
        let qs = `?search=${searchQuery}`;

        return fetch(apiURL + qs)
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

        $resultsContainer.html(resultList);
    }

    function renderResultHeader(totalCount) {
        $resultsHeading.text(`Found ${totalCount} ${pluralize('result', totalCount)}`);
    }

    function renderDefaultListing(searchQuery = null) {
        let response;
        if (searchQuery) {
            response = loadSearchListing(searchQuery);
        } else {
            response = loadListing();
        }

        renderListingResponse(response);

        response.then(json => json.meta.count_per_letter)
            .then((count_per_letter) => {
                if (!count_per_letter) {
                    return;
                }

                $keyboardLetters.addClass(keyboardLettersDisabledClass);

                for (const letter in count_per_letter) {
                    if (!count_per_letter.hasOwnProperty(letter)) {
                        continue;
                    }

                    const letter_count = count_per_letter[letter];
                    if (letter_count >= 0) {
                        const lookup = `[data-keyboard-letter="${letter}"]`;

                        $keyboardLetters.closest(lookup).removeClass(keyboardLettersDisabledClass);
                    }
                }
            });
    }

    function getSearchQuery() {
        return $searchInput.val().trim();
    }

    function bindEvents() {
        // Initial screen
        $(document).ready(() => {
            renderDefaultListing(
                getSearchQuery()
            );
        });

        // Search functionality
        $searchInput.on('keyup', () => {
            const searchQuery = getSearchQuery();

            if (searchQuery.length >= 1) {
                if (searchQuery !== previousSearchQuery) {
                    renderListingResponse(
                        loadSearchListing(searchQuery)
                    );

                    previousSearchQuery = searchQuery;
                }
            } else {
                renderDefaultListing();
            }

            // Deactivate letter buttons
            $keyboardLetters.removeClass(keyboardLettersActiveClass);

            // Trigger border refresh
            $(window).trigger('refresh-results-border');
        });

        // Browse by letter functionality
        $keyboardLetters.on('click', (e) => {
            const $element = $(e.currentTarget);
            const letter = $element.data('keyboardLetter');

            // Only run if letter will return results
            if (!$element.hasClass('keyboard__letter--disabled')) {

                // Request and render a listing for the given letter
                renderListingResponse(
                    loadListing(letter)
                );

                // Deactivate other buttons and activate current button
                $keyboardLetters.removeClass(keyboardLettersActiveClass);
                $element.addClass(keyboardLettersActiveClass);

                // Cleanup the search field
                $searchInput.val('');

                // Trigger border refresh
                $(window).trigger('refresh-results-border');
            }
        });
    }

    bindEvents();
}

export default glossary;
