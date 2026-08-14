async function api(url, options = {}) {
  const response = await fetch(url, {
    credentials: 'same-origin',
    headers: { 'content-type': 'application/json', ...(options.headers || {}) },
    ...options,
  });
  const text = await response.text();
  let body = null;
  try { body = text ? JSON.parse(text) : null; } catch { body = text; }
  if (!response.ok) throw new Error(body?.error || body?.message || `Request failed (${response.status})`);
  return body;
}

function showError(form, message) {
  const node = form.querySelector('.form-error');
  if (!node) return;
  node.hidden = false;
  node.textContent = message;
  node.focus?.();
}

const loginForm = document.querySelector('#login-form');
if (loginForm) {
  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    try {
      await api('/api/login', {
        method: 'POST',
        body: JSON.stringify({
          email: loginForm.email.value,
          password: loginForm.password.value,
        }),
      });
      window.location.assign('/dashboard');
    } catch (error) {
      showError(loginForm, error.message);
    }
  });
}

document.querySelector('[data-action="logout"]')?.addEventListener('click', async () => {
  await api('/api/logout', { method: 'POST', body: '{}' });
  window.location.assign('/login');
});

document.querySelectorAll('[data-toggle="customer-form"]').forEach((button) => {
  button.addEventListener('click', () => {
    const form = document.querySelector('#customer-form');
    if (!form) return;
    form.hidden = !form.hidden;
    if (!form.hidden) form.querySelector('input')?.focus();
  });
});

const customerForm = document.querySelector('#customer-form');
if (customerForm) {
  customerForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    try {
      await api('/api/customers', {
        method: 'POST',
        body: JSON.stringify({
          name: customerForm.name.value,
          email: customerForm.email.value,
          phone: customerForm.phone.value,
        }),
      });
      window.location.reload();
    } catch (error) {
      showError(customerForm, error.message);
    }
  });
}

const orderForm = document.querySelector('#new-order');
if (orderForm) {
  orderForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    try {
      await api('/api/work-orders', {
        method: 'POST',
        body: JSON.stringify({
          customerId: orderForm.customerId.value,
          title: orderForm.title.value,
          priority: orderForm.priority.value,
        }),
      });
      window.location.reload();
    } catch (error) {
      showError(orderForm, error.message);
    }
  });
}

document.querySelectorAll('[data-work-order][data-next-status]').forEach((button) => {
  button.addEventListener('click', async () => {
    button.disabled = true;
    try {
      await api(`/api/work-orders/${encodeURIComponent(button.dataset.workOrder)}/status`, {
        method: 'POST',
        body: JSON.stringify({ status: button.dataset.nextStatus }),
      });
      window.location.reload();
    } catch (error) {
      button.disabled = false;
      window.alert(error.message);
    }
  });
});

document.querySelector('#checkout-button')?.addEventListener('click', async () => {
  const result = document.querySelector('#checkout-result');
  try {
    const payload = await api('/api/billing/checkout', { method: 'POST', body: '{}' });
    result.textContent = `Checkout intent ${payload.reference} created. Access remains governed by the reconciled entitlement.`;
  } catch (error) {
    result.textContent = error.message;
  }
});

const importForm = document.querySelector('#import-form');
if (importForm) {
  importForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    try {
      const payload = await api('/api/import', {
        method: 'POST',
        body: JSON.stringify({ batchKey: importForm.batchKey.value, csv: importForm.csv.value }),
      });
      document.querySelector('#import-result').textContent = JSON.stringify(payload, null, 2);
    } catch (error) {
      showError(importForm, error.message);
    }
  });
}
