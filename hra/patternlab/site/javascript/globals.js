import jQuery from './vendor/jquery';
import pluralize from './vendor/pluralize';

// We have to manually make jQuery a global variable.
// By default it will be in a closure and renamed to lowercase.
window.jQuery = jQuery;

export { pluralize, jQuery };
export default jQuery;
