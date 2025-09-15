// Manage Display Changes checkbox

function initDisplayChanges({
    checkbox,
    url
}) {

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
