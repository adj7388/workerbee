
// Manages form submission for both Find Words and Show Summaries

function initFormHandler({ 
    form, 
    resultsElement,
    displayChanges,
}) {
    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const storageKey = `state:${form.id}`;

        const submitButton = form.querySelector("input[type='submit']");
        const isFirstSubmit = submitButton.value === form.buttonLabels.first;
        submitButton.value = form.buttonLabels.after;

        const valuesAndLabels = form.gatherValues();
        const changes = getChanges(storageKey, valuesAndLabels);
        saveCurrentState(storageKey, valuesAndLabels);
        const historyIndex = form.formHistory.getHistoryIndex(pluck(valuesAndLabels, "value"));

        console.log( // sanity check
            `${form.id} - changes.length: ${changes.length}, isFirstSubmit: ${isFirstSubmit}, dirtyFlag: ${form.formHistory.getDirtyFlag()}, historyIndex: ${historyIndex}`
        );

        if (!isFirstSubmit && displayChanges.getDisplayChangesState()) {
            showChanges(changes);
        }

        if (isFirstSubmit || changes.length || form.formHistory.getDirtyFlag()) {
            if (historyIndex >= 0) {
                doFetchFromHistory(historyIndex);
            } else {
                doFetch(valuesAndLabels);
            }
        }
    });

    function doFetchFromHistory(historyIndex) {
        resultsElement.innerHTML = form.formHistory.getHistoryResults(historyIndex);
        form.postSubmitCallbacks.forEach( fn => fn() );
        form.formHistory.setDirtyFlag(false);
    }

    function doFetch (valuesAndLabels) {
        const params = new URLSearchParams(pluck(valuesAndLabels, "value"));
        fetch(`${form.url}?${params.toString()}`)
            .then(res => res.text())
            .then(html => {
                resultsElement.innerHTML = `
                    <div class="mt-3 bg-light results">
                        ${html}
                    </div>`;
                form.postSubmitCallbacks.forEach( fn => fn() );
            });
        form.formHistory.setDirtyFlag(false);
    }

    function saveCurrentState (storageKey, valuesAndLabels) {
        const currentState = pluck(valuesAndLabels, "value");
        localStorage.setItem(storageKey, JSON.stringify(currentState));
    }

    function getChanges(storageKey, valuesAndLabels) {
        const currentState = pluck(valuesAndLabels, "value");
        const labels = pluck(valuesAndLabels, "label");

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
}

