"use strict";

const $ = (selector) => document.querySelector(selector);
const severityNames = ["critical", "high", "medium", "low", "info"];

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[char]);
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Request failed.");
  return data;
}

async function loadHealth() {
  try {
    await fetchJson("/api/health");
    $("#health-label").textContent = "System operational";
  } catch {
    $("#health-label").textContent = "Service unavailable";
  }
}

async function loadSummary() {
  const data = await fetchJson("/api/summary");
  $("#count-total").textContent = data.total;
  $("#count-critical").textContent = data.critical;
  $("#count-high").textContent = data.high;
  $("#count-medium").textContent = data.medium;
  $("#count-other").textContent = data.low + data.info;
}

function formatTimestamp(value) {
  if (!value) return "—";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? escapeHtml(value) : escapeHtml(date.toLocaleString());
}

async function loadEvents() {
  const params = new URLSearchParams({
    q: $("#search-input").value.trim(),
    severity: $("#severity-filter").value,
    limit: "100"
  });
  const data = await fetchJson(`/api/events?${params}`);
  const body = $("#events-body");
  if (!data.events.length) {
    body.innerHTML = '<tr><td colspan="4" class="empty">No matching events found.</td></tr>';
  } else {
    body.innerHTML = data.events.map((event) => {
      const severity = severityNames.includes(String(event.severity).toLowerCase())
        ? String(event.severity).toLowerCase() : "info";
      return `<tr>
        <td><span class="severity ${severity}">${severity}</span></td>
        <td>${escapeHtml(event.message || event.event || event.description || "—")}</td>
        <td>${escapeHtml(event.source || event.ip || "—")}</td>
        <td>${formatTimestamp(event.timestamp)}</td>
      </tr>`;
    }).join("");
  }
  $("#events-count").textContent = `Showing ${data.events.length} of ${data.total} matching events`;
}

async function refreshDashboard() {
  try {
    await Promise.all([loadHealth(), loadSummary(), loadEvents()]);
  } catch (error) {
    $("#events-body").innerHTML = `<tr><td colspan="4" class="empty">${escapeHtml(error.message)}</td></tr>`;
  }
}

$("#analyze-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = $("#analyze-button");
  const result = $("#analysis-result");
  button.disabled = true;
  button.textContent = "Analyzing…";
  result.hidden = true;
  try {
    const data = await fetchJson("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ log: $("#log-input").value })
    });
    result.hidden = false;
    result.innerHTML = `<strong class="${escapeHtml(data.severity)}">${escapeHtml(data.severity)}</strong>
      ${escapeHtml(data.explanation)}<p>${escapeHtml(data.disclaimer)}</p>`;
  } catch (error) {
    result.hidden = false;
    result.textContent = error.message;
  } finally {
    button.disabled = false;
    button.innerHTML = 'Analyze event <span aria-hidden="true">↗</span>';
  }
});

let searchDebounce;
$("#search-input").addEventListener("input", () => {
  clearTimeout(searchDebounce);
  searchDebounce = setTimeout(() => loadEvents().catch((e) => {
    $("#events-body").innerHTML = `<tr><td colspan="4" class="empty">${escapeHtml(e.message)}</td></tr>`;
  }), 180);
});
$("#severity-filter").addEventListener("change", () => loadEvents().catch(() => {}));

refreshDashboard();
