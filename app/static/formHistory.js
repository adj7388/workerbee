
function initFormHistory({
    formId,
    backId,
    forwardId,
    indexId,
    saveId,
    resultsContainerId
  })
  {

  const form = document.getElementById(formId);
  const backBtn = document.getElementById(backId);
  const forwardBtn = document.getElementById(forwardId);
  const indexDisplay = document.getElementById(indexId);
  const saveHistoryBtn = document.getElementById(saveId);
  const resultsContainer = document.getElementById(resultsContainerId);

  let history = [];
  let index = -1;
  let dirtyFlag = false;
  const storageKey = `history:${formId}`;

  // Load saved history (if any)
  const saved = localStorage.getItem(storageKey);
  if (saved) {
    history = JSON.parse(saved);
    index = history.length - 1;
    if (index >= 0) restoreFormState(history[index]);
  }
  updateHistoryUI();

  function setDirtyFlag(state) {
    dirtyFlag = state;
  }

  function getDirtyFlag() {
    return dirtyFlag;
  }

  function getFormValues() {
    const formValues = {};
    for ( const el of form.elements ) {
      if ( !el.name ) continue;
      if ( el.type === "checkbox" ) {
        formValues[el.name] = el.checked;
      } else if ( el.type === "radio" ) {
        if ( el.checked ) formValues[el.name] = el.value;
      } else {
        formValues[el.name] = el.value;
      }
    }
    return formValues;
  }

  function getHistoryIndex(formValues) {
    return arrayIndexOfNestedObject(history, "search", formValues);
  }

  function getHistoryResults(historyIndex) {
    return historyIndex >= 0 ? `${history[historyIndex].results}` : null;
  }

  function saveFormState() {
    const formValues = getFormValues();
    if ( arrayIncludesNestedObject(history, "search", formValues) ) {
      showUpdatePopup("Query already saved");
    } else { 
      history.push({
        search : formValues,
        results : resultsContainer.innerHTML
      });
      index = history.length - 1;
      updateHistoryUI();
      localStorage.setItem(storageKey, JSON.stringify(history));
    }
  }

  function restoreFormState(historyEntry) {
    for (const el of form.elements) {
      if (!el.name || !(el.name in historyEntry.search)) continue;

      if (el.type === "checkbox") {
        el.checked = historyEntry.search[el.name];
      } else if (el.type === "radio") {
        el.checked = historyEntry.search[el.name] === el.value;
      } else {
        el.value = historyEntry.search[el.name];
      }
    }

    // Keep form UI updated - shotgun approach 
    for (const el of form.elements) {
      el.dispatchEvent(new Event("change", { bubbles: true }));
    }
  }

  function updateHistoryUI() {
    indexDisplay.textContent = `${index + 1}/${history.length}`;
    forwardBtn.disabled = (index >= history.length - 1);
    backBtn.disabled = (index <= 0);
  }


  ////////// listeners //////////
  function restoreAndSubmit() {
      restoreFormState(history[index]);
      setDirtyFlag(true);
      updateHistoryUI();
      form.requestSubmit();
  }

  backBtn.addEventListener("click", () => {
    if (index > 0) {
      index--;
      restoreAndSubmit();
    }
  });

  forwardBtn.addEventListener("click", () => {
    if (index < history.length - 1) {
      index++;
      restoreAndSubmit();
    }
  });

  saveHistoryBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    saveFormState();
  });

  return { setDirtyFlag, getDirtyFlag, getHistoryIndex, getHistoryResults };

}
