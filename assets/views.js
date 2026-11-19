// Optional enhancement: a control for choosing which views of the message blocks to show.
// One view checked works like tabs, several show side by side. The choice is kept in localStorage
// and applied as :root[data-views="words bits"]; style.css does the showing and hiding.
// Without this script, the views are a closed <details> under each block.
(() => {
  const views = ["words", "symbols", "math", "chunks", "bits"];
  const blocks = document.querySelectorAll("details[data-views]");
  if (blocks.length === 0) return;
  const available = views.filter((view) => document.querySelector(`details[data-views] th[data-view="${view}"]`));

  let shown = ["words"];
  try {
    const stored = JSON.parse(localStorage.getItem("cl-views"));
    if (Array.isArray(stored)) shown = available.filter((view) => stored.includes(view));
  } catch {}
  if (shown.length === 0) shown = ["words"];

  const apply = () => {
    document.documentElement.dataset.views = shown.join(" ");
    try { localStorage.setItem("cl-views", JSON.stringify(shown)); } catch {}
  };

  const control = document.createElement("fieldset");
  control.dataset.viewControl = "";
  const legend = document.createElement("legend");
  legend.textContent = "Show";
  control.append(legend);
  for (const view of available) {
    const label = document.createElement("label");
    const box = document.createElement("input");
    box.type = "checkbox";
    box.value = view;
    box.checked = shown.includes(view);
    label.append(box, view);
    control.append(label);
  }
  control.addEventListener("change", (event) => {
    const checked = Array.from(control.querySelectorAll("input:checked"), (box) => box.value);
    // At least one view stays on.
    if (checked.length === 0) { event.target.checked = true; return; }
    shown = available.filter((view) => checked.includes(view));
    apply();
  });

  for (const details of blocks) details.open = true;
  document.body.append(control);
  apply();
})();
