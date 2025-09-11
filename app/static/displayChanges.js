// Manage Display Changes checkbox

function initDisplayChanges({
    displayChangesCheckbox,
    url
}) {

    displayChangesCheckbox.addEventListener("change", function () {
        const params = new URLSearchParams({
            display_changes : displayChangesCheckbox.checked,
        });
        fetch(`${url}?${params.toString()}`)
            .then(res => res.text())
            .then(responseText => {
                showUpdatePopup(responseText);
            });
    });

    function getDisplayChangesState() {
        return displayChangesCheckbox.checked;
    }

    return { getDisplayChangesState }
}
