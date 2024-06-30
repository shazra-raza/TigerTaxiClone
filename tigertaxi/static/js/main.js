/***********************************************************************
* main.js
* Authors: Jude Muriithi, Shazra Raza
* Description: Defines JQuery and other JS functions used across the
* entire application
***********************************************************************/

// Convert all given timestamps from the SQLAlchemy format to local time
function dateConvert(dates) {
    // Convert their timestamps to local time and set their HTML
    // accordingly
    for (let date of dates) {
        // SQLAlchemy timestamp -> Correctly formatted UTC timestamp
        let UTCTimestamp = $(date).html()
            .trim().replace(" ", "T") + "Z";

        let curr = new Date(UTCTimestamp);

        // Get human-readable date from JS Date class methods
        // (returns info for local time)
        weekday = curr.toLocaleString('en-US', {weekday: "long"});
        month = curr.toLocaleString('en-US', {month: "long"});
        day = curr.toLocaleString('en-US', {day:"numeric"});
        year = curr.toLocaleString('en-US', {year: "numeric"});
        time = curr.toLocaleString('en-US', {timeStyle: "short"});

        localTimestamp = `${weekday}, ${month} ${day}, ${year} at ` +
            `${time}`;

        $(date).html(localTimestamp);
    }
}

// Disable submit buttons after submit to prevent duplicate form
// submissions
function disableSubmit() {
    $("[type='submit']").attr("disabled", "true");
    $("[value='submit']").attr("disabled", "true");

    // Restore buttons after 2 seconds
    setTimeout(() => {
        $("[type='submit']").removeAttr('disabled');
        $("[value='submit']").removeAttr('disabled');
    }, 2000);
}

function setupMain() {
    // Convert all dates that exist when the page is loaded
    dateConvert($(".tt-date"));
}

$(document).ready(setupMain);
