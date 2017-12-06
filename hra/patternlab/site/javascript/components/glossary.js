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

        const response = fetch(apiURL + qs, { credentials: 'same-origin' })
            .then(response => response.json());

        response.then(json => {
            history.pushState(
                { startswith, json },
                document.title,
                document.location.pathname + (startswith ? `#${startswith}` : '')
            );
        });

        return response;
    }

    function loadSearchListing(searchQuery) {
        let qs = `?search=${searchQuery}`;

        const response = fetch(apiURL + qs, { credentials: 'same-origin' })
            .then(response => response.json());

        response.then(json => {
            history.pushState(
                { searchQuery, json },
                document.title,
                document.location.pathname + qs
            );
        });

        return response;
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
            <div class="glossary__result">
                <dt class="glossary__result-heading">
                    <dfn>${item.name}</dfn>
                    ${item.is_noun ? '<span class="glossary__noun">Noun</span>' : ''}
                </dt>
                <dd class="glossary__result-content">${item.description}</dd>
            </div>`;
        });

        $resultsContainer.html(resultList);
    }

    function renderResultHeader(totalCount) {
        $resultsHeading.text(`Found ${totalCount} ${pluralize('result', totalCount)}`);
    }

    function renderActiveLetter(startswith = null) {
        $keyboardLetters.removeClass(keyboardLettersActiveClass);
        if (startswith) {
            $keyboardLetters.filter(`[data-keyboard-letter='${startswith}']`).addClass(keyboardLettersActiveClass);
        }
    }

    function renderLetters(count_per_letter) {
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
    }

    function renderDefaultListing(searchQuery = null, startswith = null) {
        let response;
        if (searchQuery) {
            response = loadSearchListing(searchQuery);
        } else {
            response = loadListing(startswith);
        }

        renderListingResponse(response);
        response
            .then(json => json.meta.count_per_letter)
            .then(renderLetters)
            .then(() => {
                renderActiveLetter(startswith);
            });
    }

    function getSearchQuery() {
        return $searchInput.val().trim();
    }

    // https://gist.github.com/anaibol/b511550e0d6faed05bf777a50ed37e59 seems legit
    function debounce(func, wait, immediate = false) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                timeout = null;
                if (!immediate) func.apply(this, args);
            }, wait);
            if (immediate && !timeout) func.apply(this, [...args]);
        }
    }

    function bindEvents() {
        // Initial screen
        $(document).ready(() => {
            renderDefaultListing(
                getSearchQuery(),
                document.location.hash && document.location.hash.slice(1, 2)
            );
        });

        // Search functionality
        $searchInput.on('keyup', debounce(() => {
            const searchQuery = getSearchQuery();

            if (searchQuery.length >= 1) {
                if (searchQuery !== previousSearchQuery) {
                    const response = loadSearchListing(searchQuery);
                    renderListingResponse(response);
                    response.then(() => {
                        renderActiveLetter();
                    });

                    previousSearchQuery = searchQuery;
                }
            } else {
                renderDefaultListing();
            }
        }, 250));

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
                renderActiveLetter(letter);

                // Cleanup the search field
                $searchInput.val('');
            }
        });

        window.addEventListener('popstate', event => {
            const { searchQuery, startswith, json } = event.state || {};
            if (json) {
                renderResultItems(json.items);
                renderResultHeader(json.meta.total_count);
                renderLetters(json.meta.count_per_letter);
                renderActiveLetter(startswith);
                $searchInput.val(searchQuery || '');
            }
        });
    }

    if ($container.length > 0) {
        bindEvents();
    }
}

export default glossary;
