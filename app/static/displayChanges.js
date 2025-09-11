// Manage Display Changes checkbox

function initDisplayChanges({
    displayChangesId,
    url
}) {

    document.getElementById(displayChangesId).addEventListener("change", function () {
        const displayChangesUrl = url;
        const params = new URLSearchParams({
            display_changes : document.getElementById(displayChangesId).checked,
        });
        fetch(`${displayChangesUrl}?${params.toString()}`)
            .then(res => res.text())
            .then(responseText => {
                showUpdatePopup(responseText);
            });
    });

    function getDisplayChangesState() {
        return document.getElementById(displayChangesId).checked;
    }

    return { getDisplayChangesState }
}
