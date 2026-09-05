"use strict";

/* =========================================================
   THINKIX MANAGEMENT DASHBOARD
   REGISTRATION + PERSISTENT DEVICE HISTORY
========================================================= */

/* =========================================================
   FORM ELEMENTS
========================================================= */

const form = document.getElementById("deviceForm");
const description = document.getElementById("description");
const characterCount = document.getElementById("characterCount");
const successMessage = document.getElementById("successMessage");
const loadingBox = document.getElementById("loadingBox");
const resetButton = document.getElementById("resetButton");

/* =========================================================
   DASHBOARD ELEMENTS
========================================================= */

const totalDevicesElement = document.getElementById("totalDevices");
const onlineDevicesElement = document.getElementById("onlineDevices");
const alertCountElement = document.getElementById("alertCount");

const deviceList = document.querySelector(".device-list");
const emailHistory = document.querySelector(".email-history");

const trafficSummary = document.querySelectorAll(".traffic-summary strong");

const trafficLine = document.querySelector(".traffic-line");

const trafficArea = document.querySelector(".traffic-area");

/* =========================================================
   VERIFIED LAB VALUES (2 Sep 2026 GNS3 verification pass)

   These 4 devices are the real nodes shown directly inside
   management.html, sourced from the project evidence log —
   not simulated.

   iot-sensor-vlan10  (online, mTLS verified)
   plc1-robotics      (revoked via CRL, rejected by broker)
   Mosquitto-Broker   (active, TLS 1.3 + mTLS)
   Suricata-IDS       (monitoring, 2 signatures live)
========================================================= */

const SIMULATED_LAB_DEVICE_COUNT = 4;
const SIMULATED_ONLINE_COUNT = 3;

let registeredDeviceCount = 0;

let totalDevices = SIMULATED_LAB_DEVICE_COUNT;

let onlineDevices = SIMULATED_ONLINE_COUNT;

let securityAlerts = 2;
let mqttMessages = 4;

/* =========================================================
   CHANGE OLD "DEMO" WORDING
========================================================= */

function updateSimulationLabels() {
  document.querySelectorAll(".demo-badge").forEach((badge) => {
    const text = badge.textContent.trim().toUpperCase();

    if (text === "DEMO DATA") {
      badge.textContent = "SIMULATION ENVIRONMENT";
    }
  });

  document.querySelectorAll(".live-badge").forEach((badge) => {
    const text = badge.textContent.trim().toUpperCase();

    if (text.includes("DEMO LIVE")) {
      badge.textContent = "● SIMULATION MODE";
    }
  });
}

/* =========================================================
   HISTORY HELPERS
========================================================= */

function getDeviceHistory() {
  try {
    return JSON.parse(localStorage.getItem("thinkixDeviceHistory") || "[]");
  } catch (error) {
    console.error("Unable to read ThinkiX device history:", error);

    return [];
  }
}

function saveDeviceHistory(history) {
  localStorage.setItem("thinkixDeviceHistory", JSON.stringify(history));
}

/* =========================================================
   ERROR FUNCTIONS
========================================================= */

function showError(fieldId, message) {
  const field = document.getElementById(fieldId);

  const error = document.getElementById(`${fieldId}Error`);

  if (field) {
    field.classList.add("invalid");
  }

  if (error) {
    error.textContent = message;
  }
}

function clearError(fieldId) {
  const field = document.getElementById(fieldId);

  const error = document.getElementById(`${fieldId}Error`);

  if (field) {
    field.classList.remove("invalid");
  }

  if (error) {
    error.textContent = "";
  }
}

/* =========================================================
   VALIDATION HELPERS
========================================================= */

function validEmail(email) {
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  return pattern.test(email);
}

function validIp(ip) {
  const parts = ip.split(".");

  if (parts.length !== 4) {
    return false;
  }

  return parts.every((part) => {
    if (!/^\d+$/.test(part)) {
      return false;
    }

    const number = Number(part);

    return number >= 0 && number <= 255;
  });
}

function validMac(mac) {
  const pattern = /^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$/;

  return pattern.test(mac);
}

/* =========================================================
   FORM VALIDATION
========================================================= */

function validateForm() {
  let valid = true;

  const deviceName = document.getElementById("deviceName").value.trim();

  const deviceId = document.getElementById("deviceId").value.trim();

  const deviceType = document.getElementById("deviceType").value;

  const vlan = document.getElementById("vlan").value;

  const ipAddress = document.getElementById("ipAddress").value.trim();

  const macAddress = document.getElementById("macAddress").value.trim();

  const ownerName = document.getElementById("ownerName").value.trim();

  const email = document.getElementById("email").value.trim();

  const descriptionValue = description.value.trim();

  const agreement = document.getElementById("agreement");

  /* DEVICE NAME */

  if (deviceName.length < 3) {
    showError("deviceName", "Enter a valid device name.");

    valid = false;
  } else {
    clearError("deviceName");
  }

  /* DEVICE ID */

  if (deviceId.length < 3) {
    showError("deviceId", "Enter a valid device ID.");

    valid = false;
  } else {
    clearError("deviceId");
  }

  /* DEVICE TYPE */

  if (!deviceType) {
    showError("deviceType", "Select a device type.");

    valid = false;
  } else {
    clearError("deviceType");
  }

  /* VLAN */

  if (!vlan) {
    showError("vlan", "Select a VLAN.");

    valid = false;
  } else {
    clearError("vlan");
  }

  /* IP ADDRESS */

  if (!validIp(ipAddress)) {
    showError("ipAddress", "Enter a valid IPv4 address.");

    valid = false;
  } else {
    clearError("ipAddress");
  }

  /* MAC ADDRESS */

  if (!validMac(macAddress)) {
    showError("macAddress", "Format: 00:1A:2B:3C:4D:5E");

    valid = false;
  } else {
    clearError("macAddress");
  }

  /* OWNER */

  if (ownerName.length < 2) {
    showError("ownerName", "Enter the device owner.");

    valid = false;
  } else {
    clearError("ownerName");
  }

  /* EMAIL */

  if (!validEmail(email)) {
    showError("email", "Enter a valid email.");

    valid = false;
  } else {
    clearError("email");
  }

  /* DESCRIPTION */

  if (descriptionValue.length < 10) {
    showError("description", "Enter at least 10 characters.");

    valid = false;
  } else {
    clearError("description");
  }

  /* SECURITY AGREEMENT */

  if (!agreement.checked) {
    document.getElementById("agreementError").textContent =
      "Please confirm the security policy.";

    valid = false;
  } else {
    document.getElementById("agreementError").textContent = "";
  }

  return valid;
}

/* =========================================================
   DESCRIPTION COUNTER
========================================================= */

if (description && characterCount) {
  description.addEventListener("input", () => {
    characterCount.textContent = `${description.value.length} / 300 characters`;
  });
}

/* =========================================================
   COUNTER ANIMATION
========================================================= */

function animateCounter(element, start, end, duration) {
  if (!element) {
    return;
  }

  let startTime = null;

  function animation(currentTime) {
    if (!startTime) {
      startTime = currentTime;
    }

    const progress = Math.min((currentTime - startTime) / duration, 1);

    const value = Math.floor(progress * (end - start) + start);

    element.textContent = value;

    if (progress < 1) {
      requestAnimationFrame(animation);
    }
  }

  requestAnimationFrame(animation);
}

/* =========================================================
   FORMAT DEVICE TYPE
========================================================= */

function formatDeviceType(type) {
  const types = {
    temperature: "Temperature Sensor",

    pressure: "Pressure Sensor",

    vibration: "Vibration Sensor",

    plc: "PLC Controller",

    robotic: "Robotic Arm",

    monitoring: "Monitoring Server",
  };

  return types[type] || type || "Industrial IoT Device";
}

/* =========================================================
   CREATE REGISTERED DEVICE CARD

   IMPORTANT:
   Registered does NOT mean online.
   GNS3 must verify the device later.
========================================================= */

function createRegisteredDeviceRow(device) {
  if (!deviceList) {
    return;
  }

  /* Prevent duplicate rendering */

  if (
    device.registrationId &&
    deviceList.querySelector(
      `[data-registration-id="${device.registrationId}"]`,
    )
  ) {
    return;
  }

  const deviceRow = document.createElement("div");

  deviceRow.className = "device-row registered-device-row";

  if (device.registrationId) {
    deviceRow.dataset.registrationId = device.registrationId;
  }

  /* A device only shows as (simulated) online once device-status.html
     has run its simulated GNS3 confirmation for it. Until then it stays
     the original honest "registered but unverified" yellow state. */

  const isSimulatedOnline = device.gns3Status === "Confirmed (Simulated)";

  const dotColor = isSimulatedOnline ? "#4ade80" : "#facc15";
  const dotGlow = isSimulatedOnline
    ? "rgba(74,222,128,.7)"
    : "rgba(250,204,21,.7)";
  const subLineColor = isSimulatedOnline ? "#4ade80" : "#facc15";
  const subLineText = isSimulatedOnline
    ? "GNS3 Verified (Simulated)"
    : "GNS3 Pending";
  const badgeColor = isSimulatedOnline ? "#4ade80" : "#fde047";
  const badgeText = isSimulatedOnline ? "ONLINE (SIMULATED)" : "REGISTERED";

  deviceRow.innerHTML = `

    <span
      class="device-status"
      style="
        background:${dotColor};
        box-shadow:0 0 10px ${dotGlow};
      "
    ></span>

    <div class="device-info">

      <strong>
        ${device.deviceName || "Unknown Device"}
      </strong>

      <small>
        ${device.ipAddress || "No IP"}
        •
        ${device.vlan ? `VLAN ${device.vlan}` : "No VLAN"}
      </small>

      <small
        style="
          color:${subLineColor};
          margin-top:4px;
        "
      >
        ${formatDeviceType(device.deviceType)}
        • ${subLineText}
      </small>

    </div>

    <span
      class="status-label"
      style="color:${badgeColor};"
    >
      ${badgeText}
    </span>

  `;

  deviceList.prepend(deviceRow);

  deviceRow.animate(
    [
      {
        opacity: 0,
        transform: "translateY(-12px)",
      },

      {
        opacity: 1,
        transform: "translateY(0)",
      },
    ],
    {
      duration: 400,
      easing: "ease",
    },
  );
}

/* =========================================================
   LOAD REGISTERED DEVICES FROM HISTORY

   This is what makes devices remain after page refresh.
========================================================= */

function loadRegisteredDevices() {
  const history = getDeviceHistory();

  registeredDeviceCount = history.length;

  history
    .slice()
    .reverse()
    .forEach((device) => {
      createRegisteredDeviceRow(device);
    });

  /* ---------------------------------------------------------
     TOTAL DEVICES

     Existing lab devices = 4
     Registered devices = history count

     ONLINE DEVICES starts at 3 (the real lab devices) and only
     gains a registered device once device-status.html has run
     its simulated GNS3 confirmation for it — a plain registration
     is NOT considered live until that (simulated) confirmation.
  --------------------------------------------------------- */

  const simulatedOnlineCount = history.filter(
    (device) => device.gns3Status === "Confirmed (Simulated)",
  ).length;

  totalDevices = SIMULATED_LAB_DEVICE_COUNT + registeredDeviceCount;

  onlineDevices = SIMULATED_ONLINE_COUNT + simulatedOnlineCount;

  if (totalDevicesElement) {
    totalDevicesElement.textContent = totalDevices;
  }

  if (onlineDevicesElement) {
    onlineDevicesElement.textContent = onlineDevices;
  }
}

/* =========================================================
   VERIFIED CHECKS CHART

   This dashboard shows a real, hands-on verification pass,
   not a live telemetry feed (the lab is intentionally
   isolated behind pfSense — see the Lab Integration panel
   below). The random live-updating simulation that used to
   run here has been removed so the numbers on screen match
   the evidence log exactly instead of drifting.
========================================================= */

function randomTraffic(minimum, maximum) {
  return (Math.random() * (maximum - minimum) + minimum).toFixed(1);
}

function updateTrafficNumbers() {
  // Intentionally inert — see comment above. Kept as a stub in case
  // a future phase (SIEM/Phase 7) wires this to a real polled source.
}

let trafficPoints = [190, 160, 175, 110, 135, 75, 120, 85, 140, 95, 115];

function updateTrafficGraph() {
  // Intentionally inert — see comment above.
}

/* =========================================================
   CURRENT TIME
========================================================= */

function getCurrentTime() {
  const now = new Date();

  return now.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}

/* =========================================================
   MANAGEMENT ACTIVITY ENTRY
========================================================= */

function addEmailHistory(title, message) {
  if (!emailHistory) {
    return;
  }

  const row = document.createElement("div");

  row.className = "email-row";

  row.innerHTML = `

    <div
      class="email-icon-small"
    >
      ✉
    </div>

    <div>

      <strong>
        ${title}
      </strong>

      <p>
        ${message}
      </p>

      <small>
        ${getCurrentTime()}
      </small>

    </div>

    <span
      class="email-sent"
    >
      RECORDED
    </span>

  `;

  emailHistory.prepend(row);

  row.animate(
    [
      {
        opacity: 0,
        transform: "translateX(-15px)",
      },

      {
        opacity: 1,
        transform: "translateX(0)",
      },
    ],
    {
      duration: 450,
      easing: "ease",
    },
  );
}

/* =========================================================
   FLASH DASHBOARD CARD
========================================================= */

function flashElement(element) {
  if (!element) {
    return;
  }

  const card = element.closest(".dashboard-stat-card");

  if (!card) {
    return;
  }

  card.animate(
    [
      {
        boxShadow: "0 0 0 rgba(56,189,248,0)",
      },

      {
        boxShadow: "0 0 35px rgba(56,189,248,.35)",
      },

      {
        boxShadow: "0 0 0 rgba(56,189,248,0)",
      },
    ],
    {
      duration: 850,
    },
  );
}

/* =========================================================
   REGISTER DEVICE
========================================================= */

if (form) {
  form.addEventListener("submit", (event) => {
    event.preventDefault();

    if (successMessage) {
      successMessage.classList.remove("show");
    }

    if (loadingBox) {
      loadingBox.classList.remove("show");
    }

    if (!validateForm()) {
      return;
    }

    if (loadingBox) {
      loadingBox.classList.add("show");
    }

    setTimeout(() => {
      if (loadingBox) {
        loadingBox.classList.remove("show");
      }

      if (successMessage) {
        successMessage.classList.add("show");
      }

      /* =====================================
             COLLECT DEVICE INFORMATION
          ====================================== */

      const deviceName = document.getElementById("deviceName").value.trim();

      const deviceId = document.getElementById("deviceId").value.trim();

      const deviceType = document.getElementById("deviceType").value;

      const vlan = document.getElementById("vlan").value;

      const ipAddress = document.getElementById("ipAddress").value.trim();

      const macAddress = document.getElementById("macAddress").value.trim();

      const ownerName = document.getElementById("ownerName").value.trim();

      const email = document.getElementById("email").value.trim();

      const deviceDescription = document
        .getElementById("description")
        .value.trim();

      const tlsEnabled = document.getElementById("tlsEnabled").checked;

      const certificateInstalled = document.getElementById(
        "certificateInstalled",
      ).checked;

      const monitoringEnabled =
        document.getElementById("monitoringEnabled").checked;

      /* =====================================
             CREATE DEVICE RECORD
          ====================================== */

      const formData = {
        registrationId: `REG-${Date.now()}`,

        registeredAt: new Date().toLocaleString(),

        deviceName,
        deviceId,
        deviceType,
        vlan,
        ipAddress,
        macAddress,
        ownerName,
        email,

        description: deviceDescription,

        tlsEnabled,

        certificateInstalled,

        monitoringEnabled,

        registrationStatus: "Processing",

        securityProfile: "Preparing",

        monitoringStatus: "Preparing",

        gns3Status: "Pending",

        liveStatus: "Not Verified",

        overallStatus: "Awaiting Live Network Connection",
      };

      console.log("ThinkiX Device Registration:", formData);

      /* =====================================
             CURRENT DEVICE FOR STATUS PAGE
          ====================================== */

      sessionStorage.setItem(
        "thinkixRegisteredDevice",
        JSON.stringify(formData),
      );

      /* =====================================
             SAVE PERMANENT BROWSER HISTORY
          ====================================== */

      const history = getDeviceHistory();

      history.unshift(formData);

      saveDeviceHistory(history);

      /* =====================================
             SHOW REGISTERED DEVICE ON DASHBOARD

             NOTE:
             It is NOT marked online.
          ====================================== */

      createRegisteredDeviceRow(formData);

      /* =====================================
             UPDATE ONLY TOTAL COUNT

             DO NOT increase onlineDevices.
          ====================================== */

      const previousTotal = totalDevices;

      totalDevices++;

      registeredDeviceCount++;

      animateCounter(totalDevicesElement, previousTotal, totalDevices, 450);

      flashElement(totalDevicesElement);

      /*
            IMPORTANT:

            onlineDevices stays unchanged.

            The device cannot be considered online
            until GNS3 confirms it.
          */

      /* =====================================
             MANAGEMENT ACTIVITY
          ====================================== */

      addEmailHistory(
        "Device Registration Received",
        `${deviceName} (${ipAddress}) registered for VLAN ${vlan}. GNS3 verification pending.`,
      );

      /* =====================================
             SHOW SUCCESS
          ====================================== */

      if (successMessage) {
        successMessage.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      }

      /* =====================================
             GO TO DEVICE STATUS PAGE
          ====================================== */

      setTimeout(() => {
        window.location.href = "device-status.html";
      }, 1400);
    }, 1200);
  });
}

/* =========================================================
   RESET FORM
========================================================= */

if (resetButton) {
  resetButton.addEventListener("click", () => {
    setTimeout(() => {
      document.querySelectorAll(".invalid").forEach((field) => {
        field.classList.remove("invalid");
      });

      document.querySelectorAll(".error-message").forEach((error) => {
        error.textContent = "";
      });

      if (characterCount) {
        characterCount.textContent = "0 / 300 characters";
      }

      if (successMessage) {
        successMessage.classList.remove("show");
      }

      if (loadingBox) {
        loadingBox.classList.remove("show");
      }
    }, 0);
  });
}

/* =========================================================
   PANEL ENTRANCE EFFECT
========================================================= */

const panels = document.querySelectorAll(".dashboard-panel");

panels.forEach((panel, index) => {
  panel.style.animationDelay = `${index * 0.08}s`;
});

/* =========================================================
   INITIALISE DASHBOARD
========================================================= */

window.addEventListener("load", () => {
  updateSimulationLabels();

  /*
      Load devices saved from previous registrations.
    */

  loadRegisteredDevices();

  /*
      Animate counters after history has been loaded.
    */

  animateCounter(totalDevicesElement, 0, totalDevices, 900);

  animateCounter(onlineDevicesElement, 0, onlineDevices, 1100);

  animateCounter(alertCountElement, 0, securityAlerts, 1300);
});

/* =========================================================
   LIVE STATUS FEED (Phase 8 — real live pipeline)

   Every ~30 seconds the Monitoring node in the actual GNS3
   lab pushes a small JSON snapshot (real Suricata alert
   count over the last 5 minutes + the anomaly detector's
   current status) to a dedicated `live-data` branch of this
   repo via the GitHub API. This function polls that file
   directly — genuinely live data from the running lab, not
   simulated. If the lab is offline (e.g. between demos) the
   fetch simply fails silently and the static, evidence-based
   values already on the page stay as they are.
========================================================= */

const LIVE_STATUS_URL =
  "https://raw.githubusercontent.com/smerbhattarai/thinkix-dashboard/live-data/status.json";

/* The Monitoring node pushes its timestamp as UTC (e.g.
   "2026-09-03 13:54:22 UTC") — that's the right way to store it.
   For display we convert it to Australian Eastern time. We use the
   Australia/Brisbane zone specifically because it never observes
   daylight saving, so the label always reads "AEST" (Sydney/
   Melbourne would flip to "AEDT" for part of the year). */

function formatLiveTimestampAEST(rawTimestamp) {
  if (!rawTimestamp) {
    return rawTimestamp;
  }

  const isoUtc = rawTimestamp.replace(" UTC", "Z").replace(" ", "T");
  const date = new Date(isoUtc);

  if (isNaN(date.getTime())) {
    return rawTimestamp;
  }

  const parts = new Intl.DateTimeFormat("en-AU", {
    timeZone: "Australia/Brisbane",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
    timeZoneName: "short",
  }).formatToParts(date);

  const get = (type) => parts.find((p) => p.type === type)?.value || "";

  return `${get("year")}-${get("month")}-${get("day")} ${get("hour")}:${get("minute")}:${get("second")} ${get("timeZoneName")}`;
}

function updateLiveStatus(data) {
  if (alertCountElement && typeof data.recent_alerts_5min === "number") {
    const previous = securityAlerts;
    securityAlerts = data.recent_alerts_5min;
    animateCounter(alertCountElement, previous, securityAlerts, 500);
    flashElement(alertCountElement);
  }

  const heroBadge = document.querySelector(".live-badge");
  if (heroBadge && data.last_updated) {
    const anomalyNote =
      data.anomaly_status === "ANOMALY" ? " — ANOMALY DETECTED" : "";
    const displayTimestamp = formatLiveTimestampAEST(data.last_updated);
    heroBadge.textContent = `● LIVE — Monitoring node, ${displayTimestamp}${anomalyNote}`;
  }
}

function fetchLiveStatus() {
  fetch(`${LIVE_STATUS_URL}?t=${Date.now()}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Live status fetch failed: " + response.status);
      }
      return response.json();
    })
    .then((data) => updateLiveStatus(data))
    .catch((error) => {
      console.warn(
        "Live status feed unavailable — showing last verified evidence values instead:",
        error,
      );
    });
}

window.addEventListener("load", () => {
  fetchLiveStatus();
  setInterval(fetchLiveStatus, 30000);
});

/* =========================================================
   VIRTUAL ACTUATOR SWITCH (SIMULATED)

   Same-browser-only demo: this toggle writes to localStorage,
   and sensor.html (opened in another tab/window on this same
   site) reacts to it live via the "storage" event. There is no
   real connection into the GNS3 lab here — the lab's VLANs have
   no route to the public internet, by design.
========================================================= */

const ACTUATOR_KEY = "thinkixActuatorState";

const actuatorToggle = document.getElementById("actuatorToggle");
const actuatorStateLabel = document.getElementById("actuatorStateLabel");

function renderActuatorState(isOn) {
  if (actuatorToggle) {
    actuatorToggle.checked = isOn;
  }

  if (actuatorStateLabel) {
    actuatorStateLabel.textContent = `Sensor Indicator: ${
      isOn ? "ON" : "OFF"
    } (Simulated)`;
  }
}

if (actuatorToggle) {
  renderActuatorState(localStorage.getItem(ACTUATOR_KEY) === "on");

  actuatorToggle.addEventListener("change", () => {
    const isOn = actuatorToggle.checked;
    localStorage.setItem(ACTUATOR_KEY, isOn ? "on" : "off");
    renderActuatorState(isOn);
  });
}

/* =========================================================
   VIRTUAL TEMPERATURE SENSOR (SIMULATED)

   The slider lives on sensor.html; this page only displays
   whatever value is shared through localStorage, live. Same
   same-browser-only simulation as the actuator switch above —
   not a real reading from the physical GNS3 lab.
========================================================= */

const TEMP_KEY = "thinkixTemperatureValue";
const TEMP_MIN = 15;
const TEMP_MAX = 45;
const TEMP_DEFAULT = 24.0;

const tempReadoutValue = document.getElementById("tempReadoutValue");
const tempBarFill = document.getElementById("tempBarFill");

function readSharedTemperature() {
  const raw = parseFloat(localStorage.getItem(TEMP_KEY));
  return isNaN(raw) ? TEMP_DEFAULT : raw;
}

function renderTemperatureDisplay(value) {
  if (tempReadoutValue) {
    tempReadoutValue.textContent = `${value.toFixed(1)}°C`;
  }

  if (tempBarFill) {
    const pct = ((value - TEMP_MIN) / (TEMP_MAX - TEMP_MIN)) * 100;
    tempBarFill.style.width = `${Math.min(100, Math.max(0, pct))}%`;
  }
}

if (tempReadoutValue || tempBarFill) {
  renderTemperatureDisplay(readSharedTemperature());

  window.addEventListener("storage", (event) => {
    if (event.key === TEMP_KEY) {
      const value = parseFloat(event.newValue);
      if (!isNaN(value)) {
        renderTemperatureDisplay(value);
      }
    }
  });

  /* Fallback poll — picks up the ambient drift sensor.html pushes
     even in browsers/tabs where the storage event doesn't fire
     reliably (e.g. this tab was backgrounded). */
  setInterval(() => {
    renderTemperatureDisplay(readSharedTemperature());
  }, 2000);
}

/* =========================================================
   DEVELOPMENT INFORMATION
========================================================= */

console.log(
  "%cThinkiX Management Dashboard",
  "color:#38bdf8;font-size:18px;font-weight:bold",
);

console.log(
  "Registered devices persist in browser history. Registered devices remain GNS3 Pending until live network verification is available.",
);
