function showUpdatePopup(message = "Updated") {
    let popup = document.createElement('div');
    popup.className = 'updatePopup bg-primary text-white shadow';
    popup.textContent = message;
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

function handleChanges(storageKey, currentState) {
    const prevStateJSON = localStorage.getItem(storageKey);
    const prevState = prevStateJSON ? JSON.parse(prevStateJSON) : null;

    const changes = [];
    if (prevState) {
        for (const [key, value] of Object.entries(currentState)) {
            if (prevState[key] !== value) {
                changes.push(`'${prevState[key]}' changed to '${value}'`);
            }
        }
    }
    localStorage.setItem(storageKey, JSON.stringify(currentState));
    return changes;
}

function showChanges(changes) {
    if (changes.length > 0) {
        showUpdatePopup(`Updated: \n${changes.join('\n')}`);
    } else {
        showUpdatePopup("No updates");
    }
}
