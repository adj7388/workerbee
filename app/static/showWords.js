
// Manage the Show Words checkbox and its dependent radio buttons on Show Summaries form
// - gray out radio buttons when Show Words not selected
// - show/hide words in the show summaries table depending on checkbox

function initShowWords ({showWordsId, alphabeticallyId, byWordLengthId}) {

    // gray out word sort radios when showWords is not checked
    const showWordsCheckbox = document.getElementById(showWordsId);
    const radios = [
        document.getElementById(alphabeticallyId),
        document.getElementById(byWordLengthId)
    ];

    function toggleSortRadios() {
        const enabled = showWordsCheckbox.checked;
        radios.forEach(radio => {
            radio.disabled = !enabled;

            // find the label for this radio and make it really gray
            const label = document.querySelector(`label[for="${radio.id}"]`);
            if (label) {
                label.classList.toggle("text-muted", !enabled);   // dim when disabled
                label.classList.toggle("opacity-50", !enabled);   // extra fade
            }
        });
    }

    // toggle between showing words and not
    function toggleWordRows() {
        const enabled = showWordsCheckbox.checked;
        const rows = document.querySelectorAll('tr[data-words]');
        rows.forEach(row => {
            if ( !enabled ) {
                row.classList.add('hide-words')
            }
            else {
                row.classList.remove('hide-words');
            }
        });
    }

    // enable/disable word sort radio buttons when showWordsCheckbox changes 
    showWordsCheckbox.addEventListener(
        "change", toggleSortRadios
    );

    // show/hide word rows when showWordsCheckbox changes
    showWordsCheckbox.addEventListener(
        "change", toggleWordRows
    );

    toggleSortRadios(); // run on load
}