function customConfirm(message) {
  return new Promise((resolve) => {
    const modal = document.getElementById("custom-confirm");
    const messageEl = document.getElementById("confirm-message");
    const yesBtn = document.getElementById("confirm-yes");
    const noBtn = document.getElementById("confirm-no");

    messageEl.textContent = message;
    modal.classList.add("show"); // show modal

    function cleanup() {
      modal.classList.remove("show"); // hide modal
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
async function myConfirm(message) {
  return await customConfirm(message);
}
