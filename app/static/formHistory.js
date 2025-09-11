
function initFormHistory({
    formId,
    backBtnId,
    forwardBtnId,
    indexDisplayId,
    saveHistoryBtnId,
    resultsHtmlId
  })
  {

  console.log(`${formId} ${backBtnId} ${forwardBtnId} ${indexDisplayId} ${saveHistoryBtnId} ${resultsHtmlId}`);
  const form = document.getElementById(formId);
  const backBtn = document.getElementById(backBtnId);
  const forwardBtn = document.getElementById(forwardBtnId);
  const indexDisplay = document.getElementById(indexDisplayId);
  const saveHistoryBtn = document.getElementById(saveHistoryBtnId);
  const resultsDiv = document.getElementById(resultsHtmlId);

  let history = [];
  let index = -1;
  let dirtyFlag = false;

  displayIndex(index);

  function setDirtyFlag(state) {
    dirtyFlag = state;
  }

  function getDirtyFlag() {
    return dirtyFlag;
  }


  function saveState() {
    const searchParams = {};
    // Collect searchParams of all form elements
    for ( const el of form.elements ) {
      if ( !el.name ) continue;

      if ( el.type === "checkbox" ) {
        if ( !searchParams[el.name] ) searchParams[el.name] = [];
        if ( el.checked ) searchParams[el.name].push(el.value);
      } else if ( el.type === "radio" ) {
        if ( el.checked ) searchParams[el.name] = el.value;
      } else {
        searchParams[el.name] = el.value;
      }
    }

    const historyEntry = {
      search : searchParams,
      results : resultsDiv.innerHTML
    } 

    if ( arrayIncludesNestedObject(history, "search", searchParams) ) {
      showUpdatePopup("Query already saved");
    } else {
      history.push(historyEntry);
      index = history.length - 1;
      displayIndex(index);
      localStorage.setItem(`history:${formId}`, JSON.stringify(history));
    }
  }

  function restoreState(historyEntry) {
    for (const el of form.elements) {
      if (!el.name || !(el.name in historyEntry.search)) continue;

      if (el.type === "checkbox") {
        el.checked = historyEntry.search[el.name].includes(el.value);
      } else if (el.type === "radio") {
        el.checked = historyEntry.search[el.name] === el.value;
      } else {
        el.value = historyEntry.search[el.name];
      }
    }
    resultsDiv.innerHTML = "";

    // Keep form UI updated - shotgun approach 
    for (const el of form.elements) {
      el.dispatchEvent(new Event("change", { bubbles: true }));
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

  backBtn.addEventListener("click", () => {
    if (index > 0) {
      index--;
      displayIndex(index);
      restoreState(history[index]);
      setDirtyFlag(true);
    }
  });

  forwardBtn.addEventListener("click", () => {
    if (index < history.length - 1) {
      index++;
      displayIndex(index);
      restoreState(history[index]);
      setDirtyFlag(true);
    }
  });

  saveHistoryBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    saveState();
  });

  return { setDirtyFlag, getDirtyFlag };

}
