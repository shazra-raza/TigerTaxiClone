/***********************************************************************
* settings.js
* Author: Jude Muriithi
* Description: Defines JQuery which drives the interactive functionality
* of the settings page
***********************************************************************/

// Disables the submit button on the 'Display Name' field based on its
// value
function validateNameButton() {
    let nameInput = $('#displayName').val();
    let placeholder = $('#displayName').attr('placeholder');

    if (nameInput == "" || nameInput == placeholder) {
        if (!$('#name-btn').attr('disabled'))
            $('#name-btn').attr('disabled', true);
    }
    else
        $('#name-btn').removeAttr('disabled');
}

// Disables the submit button on the 'Phone Number' field based on its
// value
function validatePhoneButton() {
    let phoneInput = $('#phoneNumber').val();
    let placeholder = $('#phoneNumber').attr('placeholder');
    let phoneReg = new RegExp("^\\+?([0-2]{1})?((-?)|(.?)|( ?))\\(?" +
        "[0-9]{3}\\)?((-?)|(.?)|( ?))[0-9]{3}((-?)|(.?)|( ?))[0-9]" +
        "{4}$");

    if (phoneInput == "" || phoneInput == placeholder ||
        !phoneReg.test(phoneInput)) {
        if (!$('#phone-btn').attr('disabled'))
            $('#phone-btn').attr('disabled', true);
    }
    else
        $('#phone-btn').removeAttr('disabled');
}

// Disables the submit button on the 'Email Notifs' field based on its
// value
function validateEmailButton() {
    let emailInput = $("#emailSelect").children("option:selected").val();
    let placeholder = $("#chosenEmailPref").val();

    if (emailInput == "" || emailInput == placeholder) {
        if (!$('#email-btn').attr('disabled'))
            $('#email-btn').attr('disabled', true);
    }
    else
        $('#email-btn').removeAttr('disabled');
}

function setupSettings() {
    $('#displayName').on('input', validateNameButton);
    $('#phoneNumber').on('input', validatePhoneButton);
    $("#emailSelect").on('change', validateEmailButton);
}

$(document).ready(setupSettings);
