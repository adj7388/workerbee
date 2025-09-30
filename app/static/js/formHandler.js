
// Manages form submission for both Find Words and Show Summaries

function initFormHandler({
    formId,
    url,
    buttonLabels,
    postSubmitCallbacks,
    formHistory,
    resultsContainerId,
    displayChanges,
}) {

    const form = document.getElementById(formId);
    const resultsContainer = document.getElementById(resultsContainerId);
    
    function runCallbacks() {
        postSubmitCallbacks.forEach( (fn) => {
            if ( typeof fn !== 'function' ) {
                console.warn(`${fnKey} is not a function`, fn);
                return;
            }
            fn();
        });
    }
 
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const storageKey = `state:${form.id}`;

        const submitButton = form.querySelector("input[type='submit']");
        const isFirstSubmit = submitButton.value === buttonLabels.first;
        submitButton.value = buttonLabels.after;

        const valuesAndLabels = getFormValues(form, getLabels=true);
        const changes = getChanges(storageKey, valuesAndLabels);
        saveCurrentState(storageKey, valuesAndLabels);
        const historyIndex = formHistory.getHistoryIndex(pluck(valuesAndLabels, "value"));

        console.log( // sanity check
            `${form.id} - changes.length: ${changes.length}, isFirstSubmit: ${isFirstSubmit}, dirtyFlag: ${formHistory.getDirtyFlag()}, historyIndex: ${historyIndex}`
        );

        if ( displayChanges.getState() && (!isFirstSubmit || formHistory.getDirtyFlag()) ) {
            showChanges(changes);
        }

        if (isFirstSubmit || changes.length || formHistory.getDirtyFlag()) {
            if (historyIndex >= 0) {
                doFetchFromHistory(historyIndex);
            } else {
                doFetchFromServer(valuesAndLabels);
            }
        }
    });

    function doFetchFromHistory(historyIndex) {
        resultsContainer.innerHTML = formHistory.getHistoryResults(historyIndex);
        runCallbacks();
        formHistory.setDirtyFlag(false);
    }

    function doFetchFromServer (valuesAndLabels) {
        const params = new URLSearchParams(pluck(valuesAndLabels, "value"));
        fetch(`${url}?${params.toString()}`)
            .then(res => res.text())
            .then(html => {
                resultsContainer.innerHTML = `
                    <div class="mt-3 bg-light results">
                        ${html}
                    </div>`;
                runCallbacks();
            });
        formHistory.setDirtyFlag(false);
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
