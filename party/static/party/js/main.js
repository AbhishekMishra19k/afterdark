// ---- Countdown ----
function startCountdown(targetIso) {
  const target = new Date(targetIso).getTime();
  const els = {
    d: document.getElementById("cd-days"),
    h: document.getElementById("cd-hours"),
    m: document.getElementById("cd-minutes"),
    s: document.getElementById("cd-seconds"),
  };
  if (!els.d) return;

  function tick() {
    const now = Date.now();
    let diff = target - now;
    if (diff <= 0) {
      els.d.textContent = els.h.textContent = els.m.textContent = els.s.textContent = "00";
      clearInterval(timer);
      return;
    }
    const days = Math.floor(diff / 86400000);
    const hours = Math.floor((diff % 86400000) / 3600000);
    const mins = Math.floor((diff % 3600000) / 60000);
    const secs = Math.floor((diff % 60000) / 1000);
    els.d.textContent = String(days).padStart(2, "0");
    els.h.textContent = String(hours).padStart(2, "0");
    els.m.textContent = String(mins).padStart(2, "0");
    els.s.textContent = String(secs).padStart(2, "0");
  }
  tick();
  const timer = setInterval(tick, 1000);
}

// ---- Tabs ----
function initTabs() {
  const buttons = document.querySelectorAll(".tab-btn");
  const panels = document.querySelectorAll(".tab-panel");
  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      buttons.forEach((b) => b.classList.remove("active"));
      panels.forEach((p) => p.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById(btn.dataset.tab).classList.add("active");
      window.scrollTo({ top: document.querySelector(".tabs").offsetTop - 80, behavior: "smooth" });
    });
  });

  // Allow #book, #reviews, #upcoming, #contact deep links
  const hash = window.location.hash.replace("#", "");
  if (hash) {
    const target = document.querySelector(`.tab-btn[data-tab="${hash}"]`);
    if (target) target.click();
  }
}

// ---- Entry type -> price display ----
function initEntryTypePricing() {
  const select = document.querySelector('select[name="entry_type"]');
  const priceLabel = document.getElementById("selected-price");
  if (!select || !priceLabel) return;
  const prices = JSON.parse(document.getElementById("price-data").textContent);
  function update() {
    priceLabel.textContent = "₹" + (prices[select.value] || "--");
  }
  select.addEventListener("change", update);
  update();
}

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initEntryTypePricing();
});
