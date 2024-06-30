/***********************************************************************
* createride.js
* Authors: Kwasi Oppong-Badu, Shazra Raza, Jude Muriithi, Aatmik Gupta
* Description: Defines JS functions used across the Create a Ride page
***********************************************************************/

const handleDateTimeInputFocus = (input) => {
    input.type = 'datetime-local';
    if (!input.value) {
        // Show local time for date preview
        curr = new Date();

        // Increment hour by 1
        curr.setHours(curr.getHours() + 1);

        year = curr.toLocaleString("en-US", {year: "numeric"});
        month = curr.toLocaleString("en-US", {month: "2-digit"});
        day = curr.toLocaleString('en-US', {day:"2-digit"});
        // Needs to be British to prevent the time returning as
        // '24:XX' around midnight
        time = curr.toLocaleString('en-GB', {timeStyle:"short",
            hour12: false});

        input.value = `${year}-${month}-${day}T${time}`;
    }
}

const handleDateTimeInputBlur = (input) => {
    if (!input.value) {
        input.type = 'text';
    }
}

// Set value of hidden timezone offset input
$(document).ready(function () {
    $("#utc_offset").attr("value", new Date().getTimezoneOffset());
});

function validateOriginDestLabel() {
    let toFromInput = $("#locationSelect").children("option:selected").val();

    /* if from princeton is selected, change label to dest */
    if (toFromInput == "From") {
        if (!$('#location').attr('placeholder','Destination'))
            $('#location').attr('placeholder','Destination');
    }
    else
        $('#location').attr('placeholder','Origin');
}

function setupCreateRide() {
    $("#locationSelect").on('change', validateOriginDestLabel);
}

$(document).ready(setupCreateRide);

/* Google Maps Autocomplete *******************************************/
function initMapCreate() {
  let input = document.getElementById("location");
  let options = {
    componentRestrictions: { country: "us" }, fields: ["name"]
  };
  let autocomplete = new google.maps.places.Autocomplete(input, options);

  // Truncate location name for UX
  google.maps.event.addListener(autocomplete, 'place_changed', () => {
    let name = autocomplete.getPlace()['name'];
    input.value = name.split(',')[0];
  });
}

