
// Manages form submission for both Find Words and Show Summaries

function initFormHandler({ 
    form, 
    url, 
    gatherValues,
    resultsElement, 
    formHistory,
    displayChanges,
    postSubmitCallbacks = [],
    buttonLabels = { first: "Submit", after: "Update" }
}) {
    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const storageKey = `state:${form.id}`;

        const submitButton = form.querySelector("input[type='submit']");
        const isFirstSubmit = submitButton.value === buttonLabels.first;
        submitButton.value = buttonLabels.after;

        const valuesAndLabels = gatherValues();
        saveCurrentState(storageKey, valuesAndLabels);

        const displayChangesChecked = displayChanges.getDisplayChangesState();
        const changes = getChanges(storageKey, valuesAndLabels);
        const historyIndex = formHistory.getHistoryIndex(pluck(valuesAndLabels, "value"));

        console.log( // sanity check
            `${form.id} - displayChangesChecked: ${displayChangesChecked}, changes.length: ${changes.length}, isFirstSubmit: ${isFirstSubmit}, dirtyFlag: ${formHistory.getDirtyFlag()}, historyIndex: ${historyIndex}`
        );

        if (!isFirstSubmit && displayChangesChecked) {
            showChanges(changes);
        }

        if (isFirstSubmit || changes.length || formHistory.getDirtyFlag()) {
            if (historyIndex >= 0) {
                doFetchFromHistory(historyIndex);
            } else {
                const params = new URLSearchParams(pluck(valuesAndLabels, "value"));
                doFetch(url, params, resultsElement, postSubmitCallbacks);
            }
        }
    });
}

function doFetchFromHistory(historyIndex) {
    resultsElement.innerHTML = formHistory.getHistoryResults(historyIndex);
    postSubmitCallbacks.forEach( fn => fn() );
    formHistory.setDirtyFlag(false);
}

function doFetch (url, params, resultsElement, postSubmitCallbacks) {
    fetch(`${url}?${params.toString()}`)
        .then(res => res.text())
        .then(html => {
            resultsElement.innerHTML = `
                <div class="mt-3 bg-light results">
                    ${html}
                </div>`;
            postSubmitCallbacks.forEach( fn => fn() );
        });
    formHistory.setDirtyFlag(false);
}


function saveCurrentState (storageKey, currentValuesAndLabels) {
    const currentState = pluck(currentValuesAndLabels, "value");
    localStorage.setItem(storageKey, JSON.stringify(currentState));
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
    return changes;
}

