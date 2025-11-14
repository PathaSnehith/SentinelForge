const alertTableBody = document.querySelector("#alerts-table tbody");
const logTableBody = document.querySelector("#logs-table tbody");
const alertCountEl = document.querySelector("#alert-count");
const logCountEl = document.querySelector("#log-count");
const lastRefreshEl = document.querySelector("#last-refresh");
const ingestBtn = document.querySelector("#ingest-btn");
const datasetSelect = document.querySelector("#dataset-select");

async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(detail || res.statusText);
  }
  return res.json();
}

function renderAlerts(alerts) {
  alertTableBody.innerHTML = "";
  alerts.forEach((alert) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td class="severity-${alert.severity.toLowerCase()}">${alert.severity.toUpperCase()}</td>
      <td>${alert.rule_id}</td>
      <td>${alert.description}</td>
      <td>${alert.entities}</td>
      <td>${new Date(alert.created_at).toLocaleString()}</td>
    `;
    alertTableBody.appendChild(tr);
  });
  alertCountEl.textContent = alerts.length;
}

function renderLogs(logs) {
  logTableBody.innerHTML = "";
  logs.forEach((log) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${new Date(log.timestamp).toLocaleString()}</td>
      <td>${log.user}</td>
      <td>${log.action}</td>
      <td>${log.status}</td>
      <td>${log.device || "-"}</td>
      <td>${log.source_ip}</td>
    `;
    logTableBody.appendChild(tr);
  });
  logCountEl.textContent = logs.length;
}

async function refreshData() {
  try {
    const [alerts, logs] = await Promise.all([
      fetchJSON("/alerts"),
      fetchJSON("/logs?limit=100"),
    ]);
    renderAlerts(alerts);
    renderLogs(logs);
    lastRefreshEl.textContent = new Date().toLocaleTimeString();
  } catch (err) {
    console.error("Failed to refresh dashboard:", err);
  }
}

async function loadDatasets() {
  try {
    const { datasets } = await fetchJSON("/demo/datasets");
    datasetSelect.innerHTML = '<option value="">Select Dataset...</option>';
    datasets.forEach((ds) => {
      const option = document.createElement("option");
      option.value = ds.filename;
      option.textContent = `${ds.name} (${ds.event_count} events)`;
      datasetSelect.appendChild(option);
    });
  } catch (err) {
    console.error("Failed to load datasets:", err);
  }
}

async function ingestDataset() {
  const filename = datasetSelect.value;
  if (!filename) {
    alert("Please select a dataset first!");
    return;
  }
  ingestBtn.disabled = true;
  ingestBtn.textContent = "Ingesting...";
  try {
    const result = await fetchJSON(`/demo/ingest-dataset/${filename}`, { method: "POST" });
    alert(`Success! Ingested ${result.ingested} events, generated ${result.alerts_generated} alerts.`);
    await refreshData();
  } catch (err) {
    alert("Failed to ingest dataset: " + err.message);
  } finally {
    ingestBtn.disabled = false;
    ingestBtn.textContent = "Ingest Selected Dataset";
  }
}

ingestBtn.addEventListener("click", ingestDataset);
loadDatasets();
refreshData();
setInterval(refreshData, 15000);

