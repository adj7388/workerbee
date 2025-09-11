
// Manages form submission for both Find Words and Show Summaries

function initFormHandler({ 
    formId, 
    url, 
    gatherValues,
    submitButtonId,
    resultsId, 
    formHistory,
    displayChangesId,
    postSubmitCallbacks = [],
    buttonLabels = { first: "Submit", after: "Update" }
}) {
    document.getElementById(formId).addEventListener('submit', function (e) {
        e.preventDefault();

        const submitButton = document.getElementById(submitButtonId);
        const isFirstSubmit = submitButton.value === buttonLabels.first;
        submitButton.value = buttonLabels.after;

        const valuesAndLabels = gatherValues();

        const displayChangesChecked = document.getElementById(displayChangesId).checked;
        const changes = getChanges(`state:${formId}`, valuesAndLabels);

        console.log(
            `${formId} - displayChangesChecked: ${displayChangesChecked}, changes.length: ${changes.length}, isFirstSubmit: ${isFirstSubmit}, dirtyFlag: ${formHistory.getDirtyFlag()}`
        );

        if (!isFirstSubmit && displayChangesChecked) {
            showChanges(changes);
        }

        if (isFirstSubmit || changes.length || formHistory.getDirtyFlag()) {
            const params = new URLSearchParams(pluck(valuesAndLabels, "value"));
            fetch(`${url}?${params.toString()}`)
                .then(res => res.text())
                .then(html => {
                    document.getElementById(resultsId).innerHTML = `
                        <div class="mt-3 bg-light results">
                            ${html}
                        </div>`;
                    postSubmitCallbacks.forEach( fn => fn() );
                });
            formHistory.setDirtyFlag(false);
        }
    });
}

function getChanges(storageKey, currentValuesAndLabels) {
    const currentState = pluck(currentValuesAndLabels, "value");
    const labels = pluck(currentValuesAndLabels, "label");

    const previousStateJSON = localStorage.getItem(storageKey);
    const previousState = previousStateJSON ? JSON.parse(previousStateJSON) : null;

    const changes = [];
    if (previousState) {
        for (const [key, currentValue] of Object.entries(currentState)) {
            if (previousState[key] !== currentValue) {
                changes.push(
                    `<span style="font-weight: bold">${labels[key]}</span> ` +
                    `<span style="font-style: italic">${currentValue}</span> ` +
                    `(was <span style="font-style: italic">${previousState[key]}</span>)`
                );

            }
        }
    }
    localStorage.setItem(storageKey, JSON.stringify(currentState));
    return changes;
}

