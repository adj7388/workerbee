// Manage Display Changes checkbox

function initDisplayChanges({
    checkboxId,
    url
}) {
    const checkbox = document.getElementById(checkboxId);

    checkbox.addEventListener("change", function () {
        const params = new URLSearchParams({
            display_changes : checkbox.checked,
        });
        fetch(`${url}?${params.toString()}`)
            .then(res => res.text())
            .then(responseText => {
                showUpdatePopup(responseText);
            });
    });

    function getState() {
        return checkbox.checked;
    }

    return { getState }
}
