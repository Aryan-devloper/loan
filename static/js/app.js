document.addEventListener("DOMContentLoaded", () => {
  const input = document.querySelector("#quick-fill-input");
  const button = document.querySelector("#quick-fill-button");
  const status = document.querySelector("#quick-fill-status");
  if (!input || !button || !status) return;

  button.addEventListener("click", () => {
    const entries = input.value.split(/[\n,]+/).map((entry) => entry.trim()).filter(Boolean);
    let filled = 0;
    let skipped = 0;
    entries.forEach((entry) => {
      const separator = entry.indexOf("=");
      if (separator < 1) {
        skipped += 1;
        return;
      }
      const name = entry.slice(0, separator).trim();
      const value = entry.slice(separator + 1).trim();
      const field = document.querySelector(`[name="${CSS.escape(name)}"]`);
      if (!field) {
        skipped += 1;
        return;
      }
      field.value = value;
      field.dispatchEvent(new Event("change", { bubbles: true }));
      field.classList.add("quick-filled");
      setTimeout(() => field.classList.remove("quick-filled"), 900);
      filled += 1;
    });
    status.textContent = skipped ? `${filled} field(s) filled, ${skipped} skipped.` : `${filled} field(s) filled.`;
    status.className = filled ? "quick-fill-success" : "quick-fill-error";
  });
});
