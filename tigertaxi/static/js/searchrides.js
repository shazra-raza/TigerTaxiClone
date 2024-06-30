/***********************************************************************
* searchrides.js
* Authors: Aatmik Gupta, Kwasi Oppong-Badu, Jude Muriithi
* Description: Defines JS for the functionality of the ride search page
***********************************************************************/

/* AJAX request handling **********************************************/

const queryData = {};
const fromPrincetonTab = document.querySelector('#from-princeton-tab')
const toPrincetonTab = document.querySelector("#to-princeton-tab")

const handleFromTabClick = () => {
    clearQueryData("#from-princeton");
    queryData['tab'] = "from";
    getData();
}

const handleToTabClick = () => {
    clearQueryData("#to-princeton");
    queryData['tab'] = "to";
    getData();
}

const clearQueryData = (tab) => {
    delete queryData['origin'];
    delete queryData['destination'];
    delete queryData['departure_date'];

    document.querySelectorAll(`${tab} .form-control`).forEach(
        (input) => {
            input.value = "";
            input.type = 'text';
        }
    );
}

const displayData = (html) => {
    if (fromPrincetonTab.className.includes("active")) {
        document.querySelector("#from-princeton-container").innerHTML = html;

        // Convert the dates within the newly loaded rows
        // (should only happen in the newly generated container)
        dateConvert($("#from-princeton-container .tt-date"));
    }
    else if (toPrincetonTab.className.includes("active")) {
        document.querySelector("#to-princeton-container").innerHTML = html;
        dateConvert($("#to-princeton-container .tt-date"));
    }
}

const getData = () => {
    if (!queryData["tab"]) {
        if (fromPrincetonTab.className.includes("active"))
            queryData['tab'] = "from";
        else
            queryData['tab'] = "to";
    }

    const queryString = Object.keys(queryData)
        .map(key => {
            let value = queryData[key].trim();
            let hasValue = !!value;
            if (hasValue)
                return `${key}=${encodeURIComponent(value)}`;
            else
                return '';
        })
        .filter(s => !!s).join('&');
    const rideSearchEndpoint = `/rides?${queryString}`;

    // get class data from server
    fetch(rideSearchEndpoint)
        .then(response => response.text())
        .then(displayData)
        .catch(console.error);
}

[...document.getElementsByClassName("form-control")].forEach(input => {
    input.addEventListener("input", () => {
        queryData[input.name] = input.value;
        getData();
    });
})

// Add utc_offset to form data
$(document).ready(function () {
    queryData['utc_offset'] =  String(new Date().getTimezoneOffset());
});

document.addEventListener("DOMContentLoaded", getData);

/* Date picker input events *******************************************/

const handleDateInputFocus = (input) => {
    input.type = 'date'

    // Show local time for date preview
    curr = new Date();
    year = curr.toLocaleString("en-US", {year: "numeric"});
    month = curr.toLocaleString("en-US", {month: "2-digit"});
    day = curr.toLocaleString('en-US', {day:"2-digit"});

    if (!input.value) {
        input.value = `${year}-${month}-${day}`;

        // Run a search for the newly filled in date (for UX
        // consistency)
        queryData['departure_date'] = input.value;
        getData();
    }
}

const handleDateInputBlur = (input) => {
    if (!input.value) {
        input.type = 'text';
    }
}
