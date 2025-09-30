
// Manage the history tool

function initFormHistory({
    formId,
    backId,
    forwardId,
    indexId,
    saveId,
    deleteId,
    resultsContainerId
  })
  {

  const form = document.getElementById(formId);
  const backBtn = document.getElementById(backId);
  const forwardBtn = document.getElementById(forwardId);
  const indexDisplay = document.getElementById(indexId);
  const saveHistoryBtn = document.getElementById(saveId);
  const deleteHistoryBtn = document.getElementById(deleteId);
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

  function getHistoryIndex(formValues) {
    return arrayIndexOfNestedObject(history, "search", formValues);
  }

  function getHistoryResults(historyIndex) {
    return historyIndex >= 0 ? `${history[historyIndex].results}` : null;
  }

  function saveFormState() {
    const formValues = getFormValues(form);
    if ( arrayIncludesNestedObject(history, "search", formValues) ) {
      showUpdatePopup("Already in history");
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
    deleteHistoryBtn.disabled = (index < 0);
  }

  async function deleteHistory() {
      if (await confirm("Delete the entire history? This cannot be undone.")) {
        localStorage.removeItem(storageKey);
        index = -1;
        history = [];
        updateHistoryUI();
      }
    }

  function restoreAndSubmit() {
      restoreFormState(history[index]);
      setDirtyFlag(true);
      form.requestSubmit();
  }

  ////////// listeners //////////
  backBtn.addEventListener("click", () => {
    if (index > 0) {
      index--;
      restoreAndSubmit();
      updateHistoryUI();
    }
  });

  forwardBtn.addEventListener("click", () => {
    if (index < history.length - 1) {
      index++;
      restoreAndSubmit();
      updateHistoryUI();
    }
  });

  saveHistoryBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    saveFormState();
  });

  deleteHistoryBtn.addEventListener("click", () => {
    deleteHistory();
  });

  return { setDirtyFlag, getDirtyFlag, getHistoryIndex, getHistoryResults };

}
