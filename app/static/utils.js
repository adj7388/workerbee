function showUpdatePopup(message = "Updated") {
    let popup = document.createElement('div');
    popup.className = 'updatePopup';
    popup.innerHTML = message;
    popup.style.display = "block";
    document.body.appendChild(popup);

    // fade in
    requestAnimationFrame(() => popup.classList.add('show'));

    // remove popup when transition ends
    popup.addEventListener('transitionend', () => popup.remove(), { once: true });

    let removed = false;
    const removePopup = () => {
        if (removed) return;   // guard so it only runs once
        removed = true;
        popup.classList.remove('show');  // triggers fade-out

        window.removeEventListener('scroll', removePopup);
        window.removeEventListener('keydown', removePopup);
        window.removeEventListener('click', removePopup);
    };

    // remove on scroll, key press, or click
    window.addEventListener('scroll', removePopup);
    window.addEventListener('keydown', removePopup);
    window.addEventListener('click', removePopup);
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

const stableStringify = obj => {
    return JSON.stringify(obj, Object.keys(obj).sort());
}

const objsAreEqual = (obj1, obj2) => 
    stableStringify(obj1) === stableStringify(obj2);

const arrayIncludesObject = (arr, obj) =>
  arr.some(item => objsAreEqual(item, obj));

const arrayIncludesNestedObject = (arr, key, obj) =>
  arr.some(item => objsAreEqual(item[key], obj));

const arrayIndexOfObject = (arr, obj) => {
  const objStr = stableStringify(obj);
  return arr.findIndex(item => stableStringify(item) === objStr);
}

const arrayIndexOfNestedObject = (arr, key, obj) => {
  const objStr = stableStringify(obj);
  return arr.findIndex(item => stableStringify(item[key]) === objStr);
}

// initFormHistory helpers
function inputValue(id, labelOverride = null) {
    const el = document.getElementById(id);
    return { 
        value: el.value, 
        label: labelOverride || getInputLabelOrLegend(el) 
    };
}

function checkboxValue(id, labelOverride = null) {
    const el = document.getElementById(id);
    return { 
        value: el.checked, 
        label: labelOverride || getInputLabelOrLegend(el) 
    };
}

function radioValue(name, labelOverride = null) {
    const el = document.querySelector(`input[name="${name}"]:checked`);
    return { 
        value: el.value, 
        label: labelOverride || getInputLabelOrLegend(el) 
    };
}

