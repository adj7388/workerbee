function showUpdatePopup(message = "Updated") {
    let popup = document.createElement('div');
    popup.className = 'updatePopup bg-primary text-white shadow';
    popup.textContent = message;
    document.body.appendChild(popup);

    // fade in
    requestAnimationFrame(() => popup.classList.add('show'));

    // handler to remove the popup
    const removePopup = () => {
        popup.classList.remove('show');
        popup.addEventListener('transitionend', () => popup.remove());
        window.removeEventListener('scroll', removePopup);
        window.removeEventListener('keydown', removePopup);
        window.removeEventListener('click', removePopup);
    };

    // remove on scroll, key press, or click
    window.addEventListener('scroll', removePopup);
    window.addEventListener('keydown', removePopup);
    window.addEventListener('click', removePopup);
}

function getUpdateDiff(currentState, storageKey = 'searchFormState') {
    const prevStateJSON = localStorage.getItem(storageKey);
    const prevState = prevStateJSON ? JSON.parse(prevStateJSON) : null;
    const changes = [];
    if (prevState) {
        for (const [key, value] of Object.entries(currentState)) {
            if (prevState[key] !== value) {
                changes.push(`${prevState[key]} changed to ${value}`);
            }
        }
    }
    localStorage.setItem(storageKey, JSON.stringify(currentState));
    return changes;
}
