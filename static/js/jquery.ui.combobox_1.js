/*
 * Combobox widget. This widget extends the jQuery UI autocomplete widget. 
 *  
 * usage:  $("#select_element").combox();
 *         $("#input_element").combox( {minLength: 2, delay: 200, source: anArray} );
 *  
 * For select elements, the source list is automatically generated from the option elements.
 * 
 * To configure a label decorator (i.e. "[admin]"), set the decoratorField when you 
 * initialize the combobox. The field corresponds to the object field, if the source is
 * an array of objects. Or it's the attribute in <option> if the source is a select drop-down menu. 
 */

(function($) {
    $.widget("ui.combobox", {
        _create : function() {
            var self = this;
            var select = this.element.hide(), selected = select
                    .children(":selected"), value = selected.val() ? selected
                    .text() : "";
            var input = $("<input />").insertAfter(select).val(value)
                    .autocomplete({
                        delay : 0,
                        minLength : 0,
                        source : function(request, response) {
                            var matcher = new RegExp($.ui.autocomplete
                                            .escapeRegex(request.term), "i");
                            response(select.children("option").map(function() {
                                var text = $(this).text();
                                if (this.value
                                        && (!request.term || matcher.test(text)))
                                    return {
                                        label : text
                                                .replace(
                                                        new RegExp(
                                                                "(?![^&;]+;)(?!<[^<>]*)("
                                                                        + $.ui.autocomplete
                                                                                .escapeRegex(request.term)
                                                                        + ")(?![^<>]*>)(?![^&;]+;)",
                                                                "gi"),
                                                        "<strong>$1</strong>"),
                                        value : text,
                                        option : this
                                    };
                            }));
                        },
                        select : function(event, ui) {
                            ui.item.option.selected = true;
                            self._trigger("selected", event, {
                                        item : ui.item.option
                                    });
                        },
                        change : function(event, ui) {
                            if (!ui.item) {
                                var matcher = new RegExp("^"
                                                + $.ui.autocomplete
                                                        .escapeRegex($(this)
                                                                .val()) + "$",
                                        "i"), valid = false;
                                select.children("option").each(function() {
                                            if (this.value.match(matcher)) {
                                                this.selected = valid = true;
                                                return false;
                                            }
                                        });
                                if (!valid) {
                                    // remove invalid value, as it didn't match
                                    // anything
                                    $(this).val("");
                                    select.val("");
                                    return false;
                                }
                            }
                        }
                    }).addClass("ui-widget ui-widget-content ui-corner-left");

            this.input = input;
            input.data("ui-autocomplete")._renderItem = function(ul, item) {
                return $("<li></li>").data("ui-autocomplete-item", item)
                        .append("<a>" + item.label + "</a>").appendTo(ul);
            };

            $("<button> </button>").attr("tabIndex", -1).attr("title",
                    "Show All Items").insertAfter(input).button({
                        icons : {
                            primary : "ui-icon-triangle-1-s"
                        },
                        text : false
                    }).removeClass("ui-corner-all")
                    .addClass("ui-corner-right ui-button-icon").click(
                            function() {
                                // close if already visible
                                if (input.autocomplete("widget").is(":visible")) {
                                    input.autocomplete("close");
                                    return;
                                }
                                // pass empty string as value to search for,
                                // displaying all results
                                input.autocomplete("search", "");
                                input.focus();
                            });
        },
        search : function(value) {
            this.input.autocomplete("search", value);
            this.input.focus();
        },
        destroy : function() {
            this.input.remove();
            this.button.remove();
            this.element.show();
            $.Widget.prototype.destroy.call(this);
        }
    });
})(jQuery);
