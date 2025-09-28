function confirmDialog(message) {
  return new Promise((resolve) => {
    const modal = document.getElementById("confirm-dialog");
    const messageEl = document.getElementById("confirm-message");
    const yesBtn = document.getElementById("confirm-yes");
    const noBtn = document.getElementById("confirm-no");

    messageEl.textContent = message;
    modal.classList.add("show");

    function cleanup() {
      modal.classList.remove("show");
      yesBtn.removeEventListener("click", onYes);
      noBtn.removeEventListener("click", onNo);
    }

    function onYes() {
      cleanup();
      resolve(true);
    }

    function onNo() {
      cleanup();
      resolve(false);
    }

    yesBtn.addEventListener("click", onYes);
    noBtn.addEventListener("click", onNo);
  });
}

// Convenience wrapper
async function confirm(message) {
  return await confirmDialog(message);
}
