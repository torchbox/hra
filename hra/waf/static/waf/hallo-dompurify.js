// based on https://github.com/bergie/hallo/blob/master/src/plugins/cleanhtml.coffee
// which is (c) 2012 Henri Bergius, IKS Consortium
// Hallo may be freely distributed under the MIT license
(function() {
  (function(jQuery) {
    var rangyMessage;
    rangyMessage = 'The dompurify plugin requires the selection save and\
    restore module from Rangy';
    return jQuery.widget('IKS.dompurify', {
      _create: function() {
        var editor,
          _this = this;
        editor = this.element;
        return editor.bind('paste', this, function(event) {
          var lastContent, lastRange, widget;
          if (rangy.saveSelection === void 0) {
            throw new Error(rangyMessage);
            return;
          }
          widget = event.data;
          widget.options.editable.getSelection().deleteContents();
          lastRange = rangy.saveSelection();
          lastContent = editor.html();
          editor.html('');
          return setTimeout(function() {
            var cleanPasted, error, pasted, range;
            pasted = editor.html();
            cleanPasted = DOMPurify.sanitize(pasted, _this.options);
            editor.html(lastContent);
            rangy.restoreSelection(lastRange);
            if (cleanPasted !== '') {
              try {
                return document.execCommand('insertHTML', false, cleanPasted);
              } catch (_error) {
                error = _error;
                range = widget.options.editable.getSelection();
                return range.insertNode(range.createContextualFragment(cleanPasted));
              }
            }
          }, 4);
        });
      }
    });
  })(jQuery);
}).call(this);
