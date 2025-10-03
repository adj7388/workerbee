// Manage Display Changes checkbox

function initDisplayChanges({
    checkboxId,
    changesContainerId,
    updateSessionUrl
}) {
    const checkbox = document.getElementById(checkboxId);
    const changesContainer = document.getElementById(changesContainerId);

    checkbox.addEventListener("change", function () {
        const params = new URLSearchParams({
            display_changes : checkbox.checked,
        });
        fetch(`${updateSessionUrl}?${params.toString()}`)
            .then(res => res.text())
            .then(responseText => {
                showMessage(responseText);
            });
        if (!checkbox.checked) changesContainer.innerHTML = "";
    });

    function getState() {
        return checkbox.checked;
    }

    function showChanges(changes) {
        const changesString = changes.length > 0
            ? changes.join('<br>')
            : "Nothing changed";
        changesContainer.innerHTML = changesString;
    }

    return { getState, showChanges }
}
