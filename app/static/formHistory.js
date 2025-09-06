
function initFormHistory(formId, backBtnId, forwardBtnId, indexDisplayId) {
  const form = document.getElementById(formId);
  const backBtn = document.getElementById(backBtnId);
  const forwardBtn = document.getElementById(forwardBtnId);
  const indexDisplay = document.getElementById(indexDisplayId);

  if (!form || !backBtn || !forwardBtn) return; // safety check

  let history = [];
  let index = -1;

  function saveState() {
    const values = {};

    // Collect form element values
    for (const el of form.elements) {
      if (!el.name) continue;

      if (el.type === "checkbox") {
        if (!values[el.name]) values[el.name] = [];
        if (el.checked) values[el.name].push(el.value);
      } else if (el.type === "radio") {
        if (el.checked) values[el.name] = el.value;
        console.log(el);
        console.log(el.checked);
      } else {
        values[el.name] = el.value;
      }
    }

    history.push(values);
    index = history.length - 1;
    displayIndex(index);
    localStorage.setItem(`history:${formId}`, JSON.stringify(history));
  }

  function restoreState(values) {
    for (const el of form.elements) {
      if (!el.name || !(el.name in values)) continue;

      if (el.type === "checkbox") {
        el.checked = values[el.name].includes(el.value);
      } else if (el.type === "radio") {
        el.checked = values[el.name] === el.value;
      } else {
        el.value = values[el.name];
      }
    }
  }

  function displayIndex(index) {
    indexDisplay.textContent = index + 1;
    forwardBtn.disabled = (index >= history.length - 1);
    backBtn.disabled = (index <= 0);
  }

  // Load saved history (if any)
  const saved = localStorage.getItem(`history:${formId}`);
  if (saved) {
    history = JSON.parse(saved);
    index = history.length - 1;
    displayIndex(index);
    if (index >= 0) restoreState(history[index]);
  }

  form.addEventListener("submit", e => {
    e.preventDefault();
    saveState();
  });

  backBtn.addEventListener("click", () => {
    if (index > 0) {
      index--;
      displayIndex(index);
      restoreState(history[index]);
    }
  });

  forwardBtn.addEventListener("click", () => {
    if (index < history.length - 1) {
      index++;
      displayIndex(index);
      restoreState(history[index]);
    }
  });
}
