// Manage Display Changes checkbox

function initDisplayChanges(config) {
    const checkbox = document.getElementById(config.changesCheckboxId);
    const changesContainer = document.getElementById(config.changesContainerId);

    checkbox.addEventListener("change", function () {
        const params = new URLSearchParams({
            display_changes : checkbox.checked,
        });
        fetch(`${config.updateSessionUrl}?${params.toString()}`)
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
