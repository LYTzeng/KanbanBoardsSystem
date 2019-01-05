$("#owner-input").tagit({
    fieldName: "owner",
    autocomplete: {delay: 0, minLength: 4, source: projUserID},
    showAutocompleteOnFocus: false,
    singleField: true,
    tagLimit: 1,
    caseSensitive: true,
    allowDuplicates: false,
});
$("#owner-input").data("ui-tagit").tagInput.addClass('uk-input');
$("#owner-input").data("ui-tagit").tagInput.attr('placeholder', '請輸入負責人帳號');
$("#owner-input").data("ui-tagit").tagInput.attr('required');
$("#owner-input").data("ui-tagit").tagInput.attr('id', 'card-owner');
$("#owner-input").data("ui-tagit").tagInput.attr('name', 'owner');
$("#owner-input").data("ui-tagit").tagInput.attr('type', 'text');
