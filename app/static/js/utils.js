function showMessage(message = "Updated") {
    let popup = document.createElement('div');
    popup.className = 'showMessagePopup';
    popup.innerHTML = message;
    popup.style.display = "block";
    document.body.appendChild(popup);

    requestAnimationFrame(() => popup.classList.add('show'));

    let removed = false;
    const finishRemove = () => popup.remove();
    // start fade-out, remove after transition ends
    popup.addEventListener('transitionend', finishRemove, { once: true });

    const removePopup = () => {
        if (removed) return;
        removed = true;

        popup.classList.remove('show');

        window.removeEventListener('scroll', removePopup);
        window.removeEventListener('keydown', removePopup);
        window.removeEventListener('click', removePopup);
    };

   setTimeout(() => {
        window.addEventListener('scroll', removePopup, { once: true });
        window.addEventListener('keydown', removePopup, { once: true });
        window.addEventListener('click', removePopup, { once: true });
   }, 0);
}

const getInputLabelOrLegend = (input, { combine = false } = {}) => {
    const legend = input.closest('fieldset')?.querySelector('legend')?.textContent.trim();
    const label  = input.labels?.[0]?.textContent.trim();

    if (combine && legend && label) return `${legend}: ${label}`;
    return legend || label || null;
};

function getFormValues(form, { getLabels = false } = {} ) {
    const returnObj = {};
    let thisValue = undefined;

    for (const el of form.elements) {
        if (!el.name) continue; // skip unnamed
        switch (el.type) {
            case "checkbox":
                thisValue = el.checked;
                break;
            case "radio":
                if (el.checked) thisValue = el.value;
                break;
            default:
                thisValue = el.value;
        }
        if (getLabels) {
            returnObj[el.name] = {
                value: thisValue,
                label: getInputLabelOrLegend(el),
            };
        } else {
            returnObj[el.name] = thisValue
        }
    }
    return returnObj;
}

function setFormValues(form, historyObject) {
    for (const el of form.elements) {
        if (!el.name || !(el.name in historyObject.formValues)) continue;
        switch (el.type) {
            case "checkbox":            
                el.checked = historyObject.formValues[el.name];
                break;
            case "radio":
                el.checked = historyObject.formValues[el.name] === el.value;
                break;
            default:
                el.value = historyObject.formValues[el.name];
        }
    }
}

function extract(key, obj) {
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
