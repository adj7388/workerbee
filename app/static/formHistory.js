
function initFormHistory({
    formId,
    backId,
    forwardId,
    indexId,
    saveId,
    resultsId
  })
  {

  const form = document.getElementById(formId);
  const backBtn = document.getElementById(backId);
  const forwardBtn = document.getElementById(forwardId);
  const indexDisplay = document.getElementById(indexId);
  const saveHistoryBtn = document.getElementById(saveId);
  const resultsDiv = document.getElementById(resultsId);

  let history = [];
  let index = -1;
  let dirtyFlag = false;
  let storageKey = `history:${formId}`;

  // Load saved history (if any)
  const saved = localStorage.getItem(storageKey);
  if (saved) {
    history = JSON.parse(saved);
    index = history.length - 1;
    if (index >= 0) restoreState(history[index]);
  }

  displayIndex();

  function setDirtyFlag(state) {
    dirtyFlag = state;
  }

  function getDirtyFlag() {
    return dirtyFlag;
  }

  function getSearchParams() {
    const searchParams = {};
    for ( const el of form.elements ) {
      if ( !el.name ) continue;
      if ( el.type === "checkbox" ) {
        searchParams[el.name] = el.checked;
      } else if ( el.type === "radio" ) {
        if ( el.checked ) searchParams[el.name] = el.value;
      } else {
        searchParams[el.name] = el.value;
      }
    }
    return searchParams;
  }

  function getHistoryIndex(searchParams) {
    return arrayIndexOfNestedObject(history, "search", searchParams);
  }

  function getHistoryResults(historyIndex) {
    return historyIndex >= 0 ? `<p>Greetings from history</p>${history[historyIndex].results}` : null;
  }

  function saveState() {
    const searchParams = getSearchParams();
    if ( arrayIncludesNestedObject(history, "search", searchParams) ) {
      showUpdatePopup("Query already saved");
    } else { 
      history.push({
        search : searchParams,
        results : resultsDiv.innerHTML
      });
      index = history.length - 1;
      displayIndex();
      localStorage.setItem(storageKey, JSON.stringify(history));
    }
  }

  function restoreState(historyEntry) {
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
    resultsDiv.innerHTML = "";

    // Keep form UI updated - shotgun approach 
    for (const el of form.elements) {
      el.dispatchEvent(new Event("change", { bubbles: true }));
    }
  }

  function displayIndex() {
    indexDisplay.textContent = `${index + 1}/${history.length}`;
    forwardBtn.disabled = (index >= history.length - 1);
    backBtn.disabled = (index <= 0);
  }


  ////////// listeners //////////
  backBtn.addEventListener("click", () => {
    if (index > 0) {
      index--;
      displayIndex();
      restoreState(history[index]);
      setDirtyFlag(true);
      form.requestSubmit();
    }
  });

  forwardBtn.addEventListener("click", () => {
    if (index < history.length - 1) {
      index++;
      displayIndex();
      restoreState(history[index]);
      setDirtyFlag(true);
      form.requestSubmit();
    }
  });

  saveHistoryBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    saveState();
  });

  return { setDirtyFlag, getDirtyFlag, getHistoryIndex, getHistoryResults };

}
