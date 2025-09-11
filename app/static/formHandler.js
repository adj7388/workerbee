
// Manages form submission for both Find Words and Show Summaries

function initFormHandler({ 
    formId, 
    url, 
    gatherValues,
    submitButtonId,
    resultsId, 
    formHistory,
    displayChangesId,
    storageKey,
    postSubmitCallbacks = [],
    buttonLabels = { first: "Submit", after: "Update" }
}) {
    document.getElementById(formId).addEventListener('submit', function (e) {
        e.preventDefault();
        console.log(submitButtonId);

        const submitButton = document.getElementById(submitButtonId);
        const isFirstSubmit = submitButton.value === buttonLabels.first;
        submitButton.value = buttonLabels.after;

        const valuesAndLabels = gatherValues();

        const displayChanges = document.getElementById(displayChangesId).checked;
        const changes = getChanges(storageKey, valuesAndLabels);

        console.log(
            `${formId} - displayChanges: ${displayChanges}, changes.length: ${changes.length}, isFirstSubmit: ${isFirstSubmit}, dirtyFlag: ${formHistory.getDirtyFlag()}`
        );

        if (!isFirstSubmit && displayChanges) {
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
