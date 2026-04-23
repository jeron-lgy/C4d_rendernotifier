const TEXT = {
  noTask: "\u5f53\u524d\u6ca1\u6709\u6e32\u67d3\u4efb\u52a1",
  running: "\u8fd0\u884c\u4e2d",
  stopped: "\u5df2\u505c\u6b62",
  machine: "\u673a\u5668",
  project: "\u5de5\u7a0b",
  time: "\u65f6\u95f4",
  status: "\u72b6\u6001",
  renderMode: "\u6e32\u67d3\u6a21\u5f0f",
  outputPath: "\u8f93\u51fa\u8def\u5f84",
  startedAt: "\u5f00\u59cb\u65f6\u95f4",
  renderCompleted: "\u6e32\u67d3\u5b8c\u6210",
  renderTimeout: "\u8d85\u65f6\u63d0\u9192",
  testMessage: "\u6d4b\u8bd5\u6d88\u606f",
  configTest: "\u914d\u7f6e\u6d4b\u8bd5",
  manualRender: "\u624b\u52a8\u6e32\u67d3",
  queueRender: "\u6e32\u67d3\u961f\u5217",
  idle: "\u7a7a\u95f2",
  noNotification: "\u6682\u65e0\u901a\u77e5",
  noHistory: "\u6682\u65e0\u5386\u53f2\u8bb0\u5f55",
  noHistoryHint: "\u6267\u884c\u6e32\u67d3\u6216\u6d4b\u8bd5\u53d1\u9001\u540e\uff0c\u8fd9\u91cc\u4f1a\u51fa\u73b0\u6700\u65b0\u901a\u77e5\u3002",
  noHistoryPage: "\u6682\u65e0\u901a\u77e5\u5386\u53f2\u3002<br/>\u6267\u884c\u6e32\u67d3\u6216\u6d4b\u8bd5\u53d1\u9001\u540e\uff0c\u8fd9\u91cc\u4f1a\u663e\u793a\u771f\u5b9e\u8bb0\u5f55\u3002",
  noLogs: "\u5f53\u524d\u8fd8\u6ca1\u6709\u65e5\u5fd7\u6587\u4ef6\u3002<br/>\u542f\u52a8 watcher \u6216\u6267\u884c\u4e00\u6b21\u6e32\u67d3\u540e\uff0c\u8fd9\u91cc\u4f1a\u51fa\u73b0\u65e5\u5fd7\u5185\u5bb9\u3002",
  noLogPreview: "\u6682\u65e0\u65e5\u5fd7\u9884\u89c8\u3002<br/>\u6267\u884c\u6e32\u67d3\u3001\u6d4b\u8bd5\u53d1\u9001\u6216 watcher \u64cd\u4f5c\u540e\uff0c\u8fd9\u91cc\u4f1a\u663e\u793a\u6700\u8fd1\u65e5\u5fd7\u3002",
  unnamedSlot: "\u672a\u4f7f\u7528\u69fd\u4f4d",
  unnamedProject: "\u672a\u77e5\u5de5\u7a0b",
  unnamedMachine: "\u672a\u547d\u540d\u673a\u5668",
  notConfigured: "\u5c1a\u672a\u914d\u7f6e\u901a\u77e5\u901a\u9053",
  enabled: "\u5df2\u542f\u7528",
  disabled: "\u5df2\u505c\u7528",
  channelsNone: "\u5f53\u524d\u6ca1\u6709\u914d\u7f6e\u901a\u9053",
  channelsNoneEnabled: "\u5f53\u524d\u6ca1\u6709\u542f\u7528\u901a\u9053",
  autostartOn: "\u5f00\u542f",
  autostartOff: "\u5173\u95ed",
  autostartOnNote: "\u6258\u76d8\u4e0e\u5f00\u673a\u542f\u52a8\u5df2\u542f\u7528",
  autostartOffNote: "\u5f53\u524d\u4e3a\u624b\u52a8\u542f\u52a8",
  watcherLoop: "Watcher \u5faa\u73af",
  trayState: "\u6258\u76d8\u72b6\u6001",
  pluginLink: "\u63d2\u4ef6\u8fde\u63a5",
  everyPoll: "\u6bcf {0} \u79d2\u8f6e\u8be2\u4e00\u6b21",
  trayReadyOn: "\u6258\u76d8\u4e0e\u5f00\u673a\u81ea\u542f\u5df2\u5f00\u542f",
  trayReadyOff: "\u6258\u76d8\u53ef\u7528\uff0c\u5f53\u524d\u672a\u5f00\u542f\u81ea\u542f",
  ready: "\u5c31\u7eea",
  pluginUpdating: "runtime_state \u6b63\u5728\u6301\u7eed\u66f4\u65b0",
  waitingHeartbeat: "\u7b49\u5f85\u63d2\u4ef6\u5fc3\u8df3",
  linked: "\u5df2\u8fde\u63a5",
  empty: "\u7a7a\u95f2",
  watcherRunningHint: "Watcher \u6b63\u5728\u8fd0\u884c\uff0c\u5e76\u6301\u7eed\u8f6e\u8be2\u6e32\u67d3\u72b6\u6001\u3002",
  watcherStoppedHint: "Watcher \u5f53\u524d\u5df2\u505c\u6b62\uff0c\u542f\u52a8\u540e\u624d\u4f1a\u81ea\u52a8\u53d1\u9001\u901a\u77e5\u3002",
  saved: "\u914d\u7f6e\u5df2\u4fdd\u5b58\u3002",
  channelSaved: "\u901a\u9053\u5df2\u4fdd\u5b58\u3002",
  channelDeleted: "\u901a\u9053\u5df2\u5220\u9664\u3002",
  testSent: "\u6d4b\u8bd5\u6d88\u606f\u5df2\u53d1\u9001\u3002",
  tickDone: "\u5df2\u6267\u884c\u4e00\u6b21\u8f6e\u8be2\u3002",
  watcherStarted: "Watcher \u5df2\u542f\u52a8\u3002",
  watcherStopped: "Watcher \u5df2\u505c\u6b62\u3002",
  watcherRefreshed: "Watcher \u72b6\u6001\u5df2\u5237\u65b0\u3002",
  resetDone: "\u5f53\u524d\u6a21\u677f\u5df2\u6062\u590d\u9ed8\u8ba4\u3002",
  chooseField: "\u8bf7\u81f3\u5c11\u9009\u62e9\u4e00\u4e2a\u901a\u77e5\u5b57\u6bb5",
  pluginLog: "\u63d2\u4ef6\u65e5\u5fd7",
  watcherLog: "Watcher \u65e5\u5fd7",
  readFromLocal: "\u5df2\u4ece\u672c\u5730\u65e5\u5fd7\u6587\u4ef6\u8bfb\u53d6",
  noContent: "\u5f53\u524d\u65e0\u5185\u5bb9",
  noLogContent: "\u6682\u65e0\u65e5\u5fd7\u5185\u5bb9\u3002",
  blankLogLine: "\u7a7a\u767d\u65e5\u5fd7\u884c",
  channelNameRequired: "\u901a\u9053\u540d\u79f0\u4e0d\u80fd\u4e3a\u7a7a\u3002",
  endpointRequired: "Webhook \u5730\u5740\u6216 SendKey \u4e0d\u80fd\u4e3a\u7a7a\u3002",
};

const state = {
  currentPage: "overview",
  config: null,
  history: [],
  selectedChannelIndex: -1,
  watcherRunning: false,
  busy: false,
  notificationTemplate: "render_completed",
  notificationDirty: false,
  notificationDefaults: null,
};

const NOTIFICATION_FIELDS = [
  { key: "event_type", label: TEXT.status, samples: { render_completed: TEXT.renderCompleted, render_timeout: TEXT.renderTimeout, test: TEXT.testMessage } },
  { key: "machine_name", label: TEXT.machine, samples: { render_completed: "home", render_timeout: "home", test: "home" } },
  { key: "project_name", label: TEXT.project, samples: { render_completed: "\u5e95\u5ea7.c4d", render_timeout: "\u5e95\u5ea7.c4d", test: TEXT.configTest } },
  { key: "sent_time", label: TEXT.time, samples: { render_completed: "18:30:15", render_timeout: "18:30:15", test: "18:30:15" } },
  { key: "render_mode", label: TEXT.renderMode, samples: { render_completed: TEXT.manualRender, render_timeout: TEXT.queueRender, test: TEXT.manualRender } },
  { key: "output_path", label: TEXT.outputPath, samples: { render_completed: "D:/renders/\u5e95\u5ea7_####.png", render_timeout: "D:/renders/\u5e95\u5ea7_####.png", test: "D:/renders/test.png" } },
  { key: "started_at", label: TEXT.startedAt, samples: { render_completed: "2026/04/23 18:20:00", render_timeout: "2026/04/23 18:20:00", test: "2026/04/23 18:20:00" } },
];

const DEFAULT_NOTIFICATION_TEMPLATES = {
  render_completed: {
    fields: ["event_type", "machine_name", "project_name"],
    separator: " | ",
    show_labels: false,
  },
  render_timeout: {
    fields: ["event_type", "machine_name", "project_name", "render_mode", "sent_time"],
    separator: " | ",
    show_labels: false,
  },
  test: {
    fields: ["event_type", "machine_name", "project_name"],
    separator: " | ",
    show_labels: false,
  },
};

const byId = (id) => document.getElementById(id);

function parseDate(value) {
  if (!value) return null;
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? null : date;
}

function formatDisplayTime(value, withSeconds = false) {
  const date = parseDate(value);
  if (!date) return withSeconds ? "--:--:--" : "--:--";
  return new Intl.DateTimeFormat("zh-CN", {
    hour: "2-digit",
    minute: "2-digit",
    ...(withSeconds ? { second: "2-digit" } : {}),
    hour12: false,
  }).format(date);
}

function formatDisplayDateTime(value) {
  const date = parseDate(value);
  if (!date) return "\u672a\u77e5\u65f6\u95f4";
  return new Intl.DateTimeFormat("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(date);
}

function localizeEventType(value) {
  const labels = {
    render_completed: TEXT.renderCompleted,
    render_timeout: TEXT.renderTimeout,
    test: TEXT.testMessage,
    config_test: TEXT.configTest,
  };
  return labels[value] || value || "\u672a\u77e5\u4e8b\u4ef6";
}

function localizeChannelType(value) {
  const labels = {
    feishu_webhook: "Feishu Webhook",
    serverchan: "ServerChan",
    generic_webhook: "Generic Webhook",
  };
  return labels[value] || value || "\u672a\u8bbe\u7f6e";
}

function localizeRenderMode(value) {
  if (value === "manual") return TEXT.manualRender;
  if (value === "queue") return TEXT.queueRender;
  return TEXT.idle;
}

function defaultNotificationTemplate(eventType) {
  return JSON.parse(JSON.stringify(DEFAULT_NOTIFICATION_TEMPLATES[eventType] || DEFAULT_NOTIFICATION_TEMPLATES.render_completed));
}

function ensureNotificationConfig() {
  if (!state.config.notification || typeof state.config.notification !== "object") {
    state.config.notification = {};
  }
  if (!state.config.notification.templates || typeof state.config.notification.templates !== "object") {
    state.config.notification.templates = {};
  }

  ["render_completed", "render_timeout", "test"].forEach((eventType) => {
    const fallback = defaultNotificationTemplate(eventType);
    const current = state.config.notification.templates[eventType];
    if (!current || typeof current !== "object") {
      state.config.notification.templates[eventType] = { ...fallback };
      return;
    }
    if (!Array.isArray(current.fields) || !current.fields.length) {
      current.fields = [...fallback.fields];
    }
    if (!current.separator) {
      current.separator = fallback.separator;
    }
    current.show_labels = !!current.show_labels;
  });

  if (!state.config.notification.default_template) {
    state.config.notification.default_template = "render_completed";
  }
  if (!["render_completed", "render_timeout", "test"].includes(state.notificationTemplate)) {
    state.notificationTemplate = state.config.notification.default_template;
  }
}

function currentNotificationTemplate() {
  ensureNotificationConfig();
  return state.config.notification.templates[state.notificationTemplate];
}

function buildNotificationPreview() {
  const template = currentNotificationTemplate();
  const labels = Object.fromEntries(NOTIFICATION_FIELDS.map((item) => [item.key, item.label]));
  const parts = template.fields
    .map((field) => {
      const def = NOTIFICATION_FIELDS.find((item) => item.key === field);
      if (!def) return "";
      const sample = def.samples[state.notificationTemplate] || def.samples.render_completed;
      return template.show_labels ? `${labels[field]}: ${sample}` : sample;
    })
    .filter(Boolean);
  return parts.join(template.separator || " | ");
}

function setNotificationDirty(value) {
  state.notificationDirty = value;
  const badge = byId("notificationDirtyBadge");
  if (badge) badge.classList.toggle("show", value);
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json") ? await response.json() : await response.text();
  if (!response.ok) {
    throw new Error(payload.message || payload || `Request failed: ${response.status}`);
  }
  return payload;
}

function setPage(page) {
  state.currentPage = page;
  document.querySelectorAll(".page").forEach((el) => el.classList.toggle("active", el.id === `${page}-page`));
  document.querySelectorAll(".nav-item").forEach((el) => el.classList.toggle("active", el.dataset.page === page));
}

function setBusy(busy) {
  state.busy = busy;
  ["watcherBtn", "testSendBtn", "tickBtn", "saveConfigBtn", "saveChannelBtn", "deleteChannelBtn", "newChannelBtn", "notificationSaveBtn"].forEach((id) => {
    const el = byId(id);
    if (el) el.disabled = busy;
  });
}

let toastTimer = null;
function showToast(message) {
  const toast = byId("toast");
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add("show");
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => toast.classList.remove("show"), 2200);
}

function setSignal(el, value) {
  if (!el) return;
  el.style.width = `${Math.max(0, Math.min(100, value))}%`;
}

function makeRuntimeRow(item) {
  const row = document.createElement("div");
  row.className = "runtime-item";
  row.innerHTML = `
    <div>
      <strong>${item.title}</strong>
      <p>${item.subtitle}</p>
    </div>
    <span class="badge ${item.tone}">${item.badge}</span>
  `;
  return row;
}

function renderOverview(status) {
  const runtime = status.state || {};
  const channels = state.config?.channels || [];

  byId("heroProject").textContent = runtime.project_name || TEXT.noTask;
  byId("heroStatus").textContent = status.watcher_running ? TEXT.running : TEXT.stopped;
  byId("metricMachine").textContent = runtime.machine_name || "-";
  byId("metricMode").textContent = localizeRenderMode(runtime.render_mode);
  byId("metricTimeout").textContent = runtime.timeout_seconds ? `${runtime.timeout_seconds} \u79d2` : "-";
  byId("metricRuntime").textContent = runtime.status || "\u672a\u5199\u5165";

  byId("summaryChannels").textContent = String(status.enabled_channel_count || 0);
  byId("summaryChannelsNote").textContent = channels.length
    ? channels.filter((channel) => channel.enabled).map((channel) => localizeChannelType(channel.type)).slice(0, 3).join(" / ") || TEXT.channelsNoneEnabled
    : TEXT.channelsNone;
  byId("summaryAutostart").textContent = status.autostart_enabled ? TEXT.autostartOn : TEXT.autostartOff;
  byId("summaryAutostartNote").textContent = status.autostart_enabled ? TEXT.autostartOnNote : TEXT.autostartOffNote;

  const lastEvent = status.last_event;
  if (lastEvent) {
    byId("summaryLastTime").textContent = formatDisplayTime(lastEvent.time, true);
    byId("summaryLastNote").textContent = localizeEventType(lastEvent.event_type);
  } else {
    byId("summaryLastTime").textContent = "--:--:--";
    byId("summaryLastNote").textContent = TEXT.noNotification;
  }

  setSignal(byId("signalHeartbeat"), runtime.last_heartbeat_at ? 92 : 12);
  setSignal(byId("signalWatcher"), status.watcher_running ? 88 : 24);
  setSignal(byId("signalOutput"), runtime.output_path ? 74 : 18);

  const runtimeList = byId("runtimeList");
  runtimeList.innerHTML = "";
  [
    {
      title: TEXT.watcherLoop,
      subtitle: TEXT.everyPoll.replace("{0}", String(state.config?.watcher?.poll_interval_seconds || 2)),
      badge: status.watcher_running ? TEXT.running : TEXT.stopped,
      tone: status.watcher_running ? "green" : "dark",
    },
    {
      title: TEXT.trayState,
      subtitle: status.autostart_enabled ? TEXT.trayReadyOn : TEXT.trayReadyOff,
      badge: TEXT.ready,
      tone: "dark",
    },
    {
      title: TEXT.pluginLink,
      subtitle: runtime.last_heartbeat_at ? TEXT.pluginUpdating : TEXT.waitingHeartbeat,
      badge: runtime.last_heartbeat_at ? TEXT.linked : TEXT.empty,
      tone: runtime.last_heartbeat_at ? "green" : "dark",
    },
  ].forEach((item) => runtimeList.appendChild(makeRuntimeRow(item)));

  const channelStatusList = byId("channelStatusList");
  channelStatusList.innerHTML = "";
  const previewChannels = channels.slice(0, 3);
  while (previewChannels.length < 3) previewChannels.push({ name: TEXT.unnamedSlot, type: "", enabled: false });

  previewChannels.forEach((channel, index) => {
    const row = document.createElement("div");
    row.className = "channel-row";
    row.innerHTML = `
      <div class="avatar ${index === 0 ? "green" : index === 1 ? "blush" : "dark"}">${(channel.name || TEXT.unnamedSlot).slice(0, 1).toUpperCase()}</div>
      <div>
        <strong>${channel.name || TEXT.unnamedSlot}</strong>
        <p>${channel.type ? `${localizeChannelType(channel.type)} | ${channel.enabled ? TEXT.enabled : TEXT.disabled}` : TEXT.notConfigured}</p>
      </div>
      <span class="toggle ${channel.enabled ? "on" : ""}"></span>
    `;
    channelStatusList.appendChild(row);
  });

  const timelineList = byId("timelineList");
  timelineList.innerHTML = "";
  const recent = [...state.history].slice(-6).reverse();
  if (!recent.length) {
    timelineList.innerHTML = `
      <div class="timeline-item">
        <span class="dot mute"></span>
        <div>
          <strong>${TEXT.noHistory}</strong>
          <p>${TEXT.noHistoryHint}</p>
        </div>
        <time>--:--</time>
      </div>
    `;
  } else {
    recent.forEach((item, index) => {
      const row = document.createElement("div");
      row.className = "timeline-item";
      row.innerHTML = `
        <span class="dot ${item.success ? "done" : index === 0 ? "alert" : "mute"}"></span>
        <div>
          <strong>${localizeEventType(item.event_type)}</strong>
          <p>${item.project_name || TEXT.unnamedProject}</p>
        </div>
        <time>${formatDisplayTime(item.time, true)}</time>
      `;
      timelineList.appendChild(row);
    });
  }
}

function renderChannels() {
  if (!state.config) return;
  ensureNotificationConfig();

  byId("machineNameInput").value = state.config.machine_name || "";
  byId("timeoutInput").value = state.config.timeout_seconds || 1800;
  byId("pollInput").value = state.config.watcher?.poll_interval_seconds || 2;
  byId("autostartInput").checked = !!state.config.watcher?.start_with_windows;

  const typeSelect = byId("channelTypeInput");
  if (!typeSelect.dataset.ready) {
    Object.entries({
      feishu_webhook: "Feishu Webhook",
      serverchan: "ServerChan",
      generic_webhook: "Generic Webhook",
    }).forEach(([value, label]) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = label;
      typeSelect.appendChild(option);
    });
    typeSelect.dataset.ready = "1";
  }

  const box = byId("channelListBox");
  box.innerHTML = "";
  (state.config.channels || []).forEach((channel, index) => {
    const item = document.createElement("button");
    item.className = `channel-list-item ${state.selectedChannelIndex === index ? "active" : ""}`;
    item.textContent = `${channel.name || "\u672a\u547d\u540d"} | ${channel.enabled ? TEXT.enabled : TEXT.disabled}`;
    item.onclick = () => selectChannel(index);
    box.appendChild(item);
  });

  if (state.selectedChannelIndex >= 0 && state.config.channels[state.selectedChannelIndex]) {
    const channel = state.config.channels[state.selectedChannelIndex];
    byId("channelNameInput").value = channel.name || "";
    byId("channelTypeInput").value = channel.type || "feishu_webhook";
    byId("channelEndpointInput").value = channel.endpoint || "";
    byId("channelEnabledInput").checked = !!channel.enabled;
  } else {
    byId("channelNameInput").value = "";
    byId("channelTypeInput").value = "feishu_webhook";
    byId("channelEndpointInput").value = "";
    byId("channelEnabledInput").checked = true;
  }

  renderNotificationEditor();
}

function renderNotificationEditor() {
  ensureNotificationConfig();
  const template = currentNotificationTemplate();
  const fieldsBox = byId("notificationFields");
  if (!fieldsBox) return;
  if (!template || !Array.isArray(template.fields)) {
    fieldsBox.innerHTML = `<div class="records-empty">通知模板读取失败，请刷新页面后重试。</div>`;
    return;
  }
  const selectedOrder = [...template.fields];
  const orderedFields = [
    ...selectedOrder.map((key) => NOTIFICATION_FIELDS.find((item) => item.key === key)).filter(Boolean),
    ...NOTIFICATION_FIELDS.filter((item) => !selectedOrder.includes(item.key)),
  ];

  byId("notificationTemplateInput").value = state.notificationTemplate;
  byId("notificationSeparatorInput").value = template.separator || " | ";
  byId("notificationShowLabelsInput").checked = !!template.show_labels;

  fieldsBox.innerHTML = "";
  orderedFields.forEach((item) => {
    const enabled = selectedOrder.includes(item.key);
    const selectedIndex = selectedOrder.indexOf(item.key);
    const row = document.createElement("div");
    row.className = "notification-field-row";
    row.innerHTML = `
      <div class="notification-field-main">
        <label class="checkbox-row">
          <input type="checkbox" data-field-toggle="${item.key}" ${enabled ? "checked" : ""}>
          ${item.label}
        </label>
        <span>${item.samples[state.notificationTemplate] || item.samples.render_completed}</span>
      </div>
      <div class="notification-field-actions">
        <button class="icon-btn" data-field-up="${item.key}" ${!enabled || selectedIndex <= 0 ? "disabled" : ""}>↑</button>
        <button class="icon-btn" data-field-down="${item.key}" ${!enabled || selectedIndex === selectedOrder.length - 1 ? "disabled" : ""}>↓</button>
      </div>
    `;
    fieldsBox.appendChild(row);
  });

  byId("notificationPreview").textContent = buildNotificationPreview() || TEXT.chooseField;
  setNotificationDirty(state.notificationDirty);
}

function markNotificationDirty() {
  setNotificationDirty(true);
}

function changeNotificationTemplate(templateKey) {
  ensureNotificationConfig();
  state.notificationTemplate = templateKey;
  renderNotificationEditor();
}

function toggleNotificationField(field, enabled) {
  const template = currentNotificationTemplate();
  const fields = template.fields.filter((item) => item !== field);
  if (enabled) fields.push(field);
  template.fields = fields.length ? fields : ["event_type"];
  markNotificationDirty();
  renderNotificationEditor();
}

function moveNotificationField(field, direction) {
  const template = currentNotificationTemplate();
  const order = [...template.fields];
  const index = order.indexOf(field);
  const nextIndex = index + direction;
  if (index < 0 || nextIndex < 0 || nextIndex >= order.length) return;
  [order[index], order[nextIndex]] = [order[nextIndex], order[index]];
  template.fields = order;
  markNotificationDirty();
  renderNotificationEditor();
}

function renderHistory() {
  const container = byId("historyText");
  container.innerHTML = "";
  if (!state.history.length) {
    container.innerHTML = `<div class="records-empty">${TEXT.noHistoryPage}</div>`;
    return;
  }
  [...state.history].reverse().forEach((item) => {
    const block = document.createElement("div");
    block.className = "record-item";
    block.innerHTML = `
      <strong>${localizeEventType(item.event_type)}</strong>
      <div class="meta">${formatDisplayDateTime(item.time)} | ${item.project_name || TEXT.unnamedProject} | ${item.success ? "\u53d1\u9001\u6210\u529f" : "\u53d1\u9001\u5931\u8d25"}</div>
      <pre>${item.message || ""}</pre>
    `;
    container.appendChild(block);
  });
}

function renderLogs(logs) {
  const plugin = logs.plugin_log || "";
  const watcher = logs.watcher_log || "";
  const logsContainer = byId("logsText");
  const debugEl = byId("logDebug");
  const consoleEl = byId("logConsole");

  logsContainer.innerHTML = "";
  debugEl.textContent = "";
  consoleEl.innerHTML = "";

  if (!plugin && !watcher) {
    logsContainer.innerHTML = `<div class="records-empty">${TEXT.noLogs}</div>`;
  } else {
    [
      { title: TEXT.pluginLog, content: plugin },
      { title: TEXT.watcherLog, content: watcher },
    ].forEach((section) => {
      const block = document.createElement("div");
      block.className = "record-item";
      block.innerHTML = `
        <strong>${section.title}</strong>
        <div class="meta">${section.content ? TEXT.readFromLocal : TEXT.noContent}</div>
        <pre>${section.content || TEXT.noLogContent}</pre>
      `;
      logsContainer.appendChild(block);
    });
  }

  const previewLines = [...plugin.split("\n").filter(Boolean).slice(-3), ...watcher.split("\n").filter(Boolean).slice(-5)];
  if (!previewLines.length) {
    consoleEl.innerHTML = `<div class="log-empty">${TEXT.noLogPreview}</div>`;
    return;
  }
  previewLines.slice(-10).forEach((line) => {
    const row = document.createElement("div");
    row.className = "log-line";
    row.innerHTML =
      line.replace(/^\[(.*?)\]\s*/, (_match, stamp) => `<span class="time">[${stamp}]</span> `) ||
      `<span class="muted">${TEXT.blankLogLine}</span>`;
    consoleEl.appendChild(row);
  });
}

function clearChannelForm() {
  state.selectedChannelIndex = -1;
  byId("channelNameInput").value = "";
  byId("channelTypeInput").value = "feishu_webhook";
  byId("channelEndpointInput").value = "";
  byId("channelEnabledInput").checked = true;
  document.querySelectorAll(".channel-list-item").forEach((item) => item.classList.remove("active"));
}

function selectChannel(index) {
  state.selectedChannelIndex = index;
  renderChannels();
}

async function refreshAll() {
  let defaults = state.notificationDefaults || JSON.parse(JSON.stringify(DEFAULT_NOTIFICATION_TEMPLATES));
  try {
    defaults = await api("/api/notification-defaults");
  } catch (_error) {
    defaults = state.notificationDefaults || JSON.parse(JSON.stringify(DEFAULT_NOTIFICATION_TEMPLATES));
  }

  const [status, cfg, history, logs] = await Promise.all([
    api("/api/status"),
    api("/api/config"),
    api("/api/history"),
    api("/api/logs"),
  ]);

  state.config = cfg;
  state.history = history;
  state.watcherRunning = !!status.watcher_running;
  state.notificationDefaults = defaults;
  ensureNotificationConfig();

  renderOverview(status);
  renderChannels();
  renderHistory();
  renderLogs(logs);

  byId("watcherBtn").textContent = status.watcher_running ? "\u505c\u6b62 Watcher" : "\u542f\u52a8 Watcher";
  byId("topbarStatus").textContent = status.watcher_running ? TEXT.watcherRunningHint : TEXT.watcherStoppedHint;
}

async function saveConfig() {
  setBusy(true);
  ensureNotificationConfig();
  state.config.notification.default_template = state.notificationTemplate;

  const payload = {
    machine_name: byId("machineNameInput").value.trim(),
    timeout_seconds: Number(byId("timeoutInput").value || 0),
    channels: state.config.channels || [],
    notification: state.config.notification,
    watcher: {
      poll_interval_seconds: Number(byId("pollInput").value || 2),
      start_with_windows: byId("autostartInput").checked,
    },
  };

  try {
    await api("/api/config", { method: "POST", body: JSON.stringify(payload) });
    state.config = payload;
    setNotificationDirty(false);
    await refreshAll();
    showToast(TEXT.saved);
  } finally {
    setBusy(false);
  }
}

function collectChannelForm() {
  return {
    name: byId("channelNameInput").value.trim(),
    type: byId("channelTypeInput").value,
    endpoint: byId("channelEndpointInput").value.trim(),
    enabled: byId("channelEnabledInput").checked,
  };
}

async function saveChannel() {
  setBusy(true);
  const item = collectChannelForm();
  if (!item.name) {
    setBusy(false);
    alert(TEXT.channelNameRequired);
    return;
  }
  if (!item.endpoint) {
    setBusy(false);
    alert(TEXT.endpointRequired);
    return;
  }

  const channels = [...(state.config.channels || [])];
  if (state.selectedChannelIndex >= 0) channels[state.selectedChannelIndex] = item;
  else {
    channels.push(item);
    state.selectedChannelIndex = channels.length - 1;
  }
  state.config.channels = channels;

  try {
    await saveConfig();
    showToast(TEXT.channelSaved);
  } finally {
    setBusy(false);
  }
}

async function deleteChannel() {
  if (state.selectedChannelIndex < 0) return;
  setBusy(true);
  state.config.channels.splice(state.selectedChannelIndex, 1);
  state.selectedChannelIndex = -1;
  try {
    await saveConfig();
    showToast(TEXT.channelDeleted);
  } finally {
    setBusy(false);
  }
}

async function toggleWatcher() {
  setBusy(true);
  const isRunning = state.watcherRunning;
  byId("watcherBtn").textContent = isRunning ? "\u505c\u6b62\u4e2d..." : "\u542f\u52a8\u4e2d...";
  try {
    const result = await api(isRunning ? "/api/watcher/stop" : "/api/watcher/start", { method: "POST" });
    await refreshAll();
    showToast(!isRunning && result.running ? TEXT.watcherStarted : isRunning && !result.running ? TEXT.watcherStopped : TEXT.watcherRefreshed);
  } catch (error) {
    await refreshAll();
    alert(error.message);
  } finally {
    setBusy(false);
  }
}

async function testSend() {
  setBusy(true);
  try {
    await api("/api/test-send", { method: "POST" });
    showToast(TEXT.testSent);
  } catch (error) {
    alert(error.message);
  } finally {
    setBusy(false);
  }
  await refreshAll();
}

async function runTick() {
  setBusy(true);
  try {
    await api("/api/watcher/tick", { method: "POST" });
    await refreshAll();
    showToast(TEXT.tickDone);
  } finally {
    setBusy(false);
  }
}

function bindEvents() {
  document.querySelectorAll(".nav-item").forEach((item) => {
    item.addEventListener("click", () => setPage(item.dataset.page));
  });

  byId("saveConfigBtn").addEventListener("click", saveConfig);
  byId("notificationSaveBtn").addEventListener("click", saveConfig);
  byId("saveChannelBtn").addEventListener("click", saveChannel);
  byId("deleteChannelBtn").addEventListener("click", deleteChannel);
  byId("newChannelBtn").addEventListener("click", clearChannelForm);
  byId("watcherBtn").addEventListener("click", toggleWatcher);
  byId("testSendBtn").addEventListener("click", testSend);
  byId("tickBtn").addEventListener("click", runTick);
  byId("reloadLogsBtn").addEventListener("click", refreshAll);
  byId("notificationResetBtn").addEventListener("click", () => {
    ensureNotificationConfig();
    const fallback = state.notificationDefaults?.[state.notificationTemplate] || defaultNotificationTemplate(state.notificationTemplate);
    state.config.notification.templates[state.notificationTemplate] = JSON.parse(JSON.stringify(fallback));
    markNotificationDirty();
    renderNotificationEditor();
    showToast(TEXT.resetDone);
  });

  document.addEventListener("change", (event) => {
    const field = event.target.dataset.fieldToggle;
    if (field) {
      toggleNotificationField(field, event.target.checked);
      return;
    }
    if (event.target.id === "notificationTemplateInput") {
      changeNotificationTemplate(event.target.value);
      return;
    }
    if (event.target.id === "notificationSeparatorInput") {
      currentNotificationTemplate().separator = event.target.value;
      markNotificationDirty();
      renderNotificationEditor();
      return;
    }
    if (event.target.id === "notificationShowLabelsInput") {
      currentNotificationTemplate().show_labels = event.target.checked;
      markNotificationDirty();
      renderNotificationEditor();
    }
  });

  document.addEventListener("click", (event) => {
    const upField = event.target.dataset.fieldUp;
    const downField = event.target.dataset.fieldDown;
    if (upField) {
      moveNotificationField(upField, -1);
      return;
    }
    if (downField) {
      moveNotificationField(downField, 1);
    }
  });
}

bindEvents();
refreshAll();
setInterval(() => {
  if (state.currentPage === "channels" || state.busy) return;
  refreshAll();
}, 3000);
