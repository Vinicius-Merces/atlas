const body = document.body;
const toggle = document.querySelector(".menu-toggle");
const nav = document.querySelector("#primary-nav");

if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!open));
    body.classList.toggle("menu-open", !open);
    toggle.querySelector(".menu-label").textContent = open ? "Abrir menu" : "Fechar menu";
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && body.classList.contains("menu-open")) {
      toggle.setAttribute("aria-expanded", "false");
      toggle.querySelector(".menu-label").textContent = "Abrir menu";
      body.classList.remove("menu-open");
      toggle.focus();
    }
  });
  nav.addEventListener("click", (event) => {
    if (event.target.closest("a")) {
      toggle.setAttribute("aria-expanded", "false");
      toggle.querySelector(".menu-label").textContent = "Abrir menu";
      body.classList.remove("menu-open");
    }
  });
}

function track(event) {
  const payload = JSON.stringify({ event, path: location.pathname });
  if (navigator.sendBeacon) navigator.sendBeacon("/api/analytics", new Blob([payload], { type: "application/json" }));
  else fetch("/api/analytics", { method: "POST", headers: { "content-type": "application/json" }, body: payload, keepalive: true }).catch(() => {});
}

track(location.pathname.startsWith("/residencias/") ? "residence_view" : "page_view");

const form = document.querySelector("#visit-form");
if (form) {
  const status = document.querySelector("#form-status");
  status.tabIndex = -1;
  const submit = form.querySelector("button[type=submit]");
  let started = false;
  let idempotencyKey = crypto.randomUUID().replaceAll("-", "_");

  form.addEventListener("input", () => {
    if (!started) { started = true; track("lead_form_start"); }
  }, { once: true });

  function clearErrors() {
    form.querySelectorAll(".field-error").forEach((element) => { element.textContent = ""; });
    form.querySelectorAll("[aria-invalid=true]").forEach((element) => { element.removeAttribute("aria-invalid"); element.removeAttribute("aria-describedby"); });
    status.className = "form-status";
    status.textContent = "";
  }

  function showErrors(errors) {
    const first = Object.keys(errors).find((key) => form.elements[key]);
    for (const [key, message] of Object.entries(errors)) {
      const output = document.querySelector(`#${CSS.escape(key)}-error`);
      const field = form.elements[key];
      if (output) output.textContent = message;
      if (field) {
        const inputs = field instanceof RadioNodeList ? [...form.querySelectorAll(`[name="${CSS.escape(key)}"]`)] : [field];
        inputs.forEach((input) => { input.setAttribute("aria-invalid", "true"); input.setAttribute("aria-describedby", `${key}-error`); });
      }
    }
    if (first) {
      const target = form.elements[first] instanceof RadioNodeList ? form.querySelector(`[name="${CSS.escape(first)}"]`) : form.elements[first];
      target?.focus();
    }
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearErrors();
    const data = new FormData(form);
    const payload = {
      name: data.get("name"), email: data.get("email"), phone: data.get("phone"), interest: data.get("interest"), budget: data.get("budget"), visitDate: data.get("visitDate"), company: data.get("company"), consent: data.get("consent") === "on",
    };
    submit.disabled = true;
    submit.setAttribute("aria-busy", "true");
    submit.querySelector("span").textContent = "Confirmando…";
    status.textContent = "Enviando sua solicitação com segurança.";
    try {
      const response = await fetch("/api/leads", { method: "POST", headers: { "content-type": "application/json", "idempotency-key": idempotencyKey }, body: JSON.stringify(payload) });
      const result = await response.json();
      if (response.ok && result.ok) {
        status.className = "form-status form-status--success";
        status.innerHTML = `<strong>Solicitação confirmada.</strong><span>${result.message}</span><small>Protocolo ${result.leadId}</small>`;
        form.querySelectorAll(".field-row, fieldset, .field, .consent, .submit-button, .form-note").forEach((element) => { if (!element.classList.contains("form-status")) element.hidden = true; });
        status.focus();
        return;
      }
      if (result.errors) showErrors(result.errors);
      status.className = "form-status form-status--error";
      status.textContent = result.message || "Não foi possível confirmar. Revise os dados e tente novamente.";
    } catch {
      status.className = "form-status form-status--error";
      status.textContent = "A conexão foi interrompida antes da confirmação. Tente novamente; o mesmo protocolo evitará duplicidade.";
    } finally {
      if (!status.classList.contains("form-status--success")) {
        submit.disabled = false;
        submit.removeAttribute("aria-busy");
        submit.querySelector("span").textContent = "Tentar novamente";
      }
    }
  });
}
