function showUpdatePopup(message = "Updated") {
    let popup = document.createElement('div');
    popup.className = 'updatePopup';
    popup.innerHTML = message;
    popup.style.display = "block";
    document.body.appendChild(popup);

    // fade in
    requestAnimationFrame(() => popup.classList.add('show'));

    // handler to remove the popup
    const removePopup = () => {
        popup.addEventListener('transitionend', () => popup.remove(), { once: true });
        popup.classList.remove('show');

        window.removeEventListener('scroll', removePopup);
        window.removeEventListener('keydown', removePopup);
        window.removeEventListener('click', removePopup);
    };

    // remove on scroll, key press, or click
    window.addEventListener('scroll', removePopup);
    window.addEventListener('keydown', removePopup);
    window.addEventListener('click', removePopup);
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
                    `<span style="font-style: italic">${currentValue}</span>` +
                    ` <span style="font-weight: bold">was</span> ` +
                    `<span style="font-style: italic">${previousState[key]}</span> `
                );

            }
        }
    }
    localStorage.setItem(storageKey, JSON.stringify(currentState));
    return changes;
}

function showChanges(changes) {
    const message = changes.length > 0
        ? changes.join('<br>')
        : "Nothing changed";

    showUpdatePopup(message);
}

const getInputLabelOrLegend = (input, { combine = false } = {}) => {
    const legend = input.closest('fieldset')?.querySelector('legend')?.textContent.trim();
    const label  = input.labels?.[0]?.textContent.trim();

    if (combine && legend && label) return `${legend}: ${label}`;
    return legend || label || null;
};

function pluck(obj, key) {
    return Object.fromEntries(
        Object.entries(obj).map(([k, v]) => [k, v[key]])
    );
}