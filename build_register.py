#!/usr/bin/env python3
import pathlib
from gen_site import render_page

ROOT = pathlib.Path(__file__).parent

content = """
          <section class="form-card dashboard-registration" id="registration">
            <div class="form-header">
              <div>
                <h2>Register New Industrial Device</h2>
                <p>Enter the device information and security configuration below.</p>
              </div>
              <div class="security-ring">&#128274;</div>
            </div>

            <form id="deviceForm" novalidate>
              <div class="form-grid">
                <div class="form-group">
                  <label for="deviceName">Device Name</label>
                  <input type="text" id="deviceName" placeholder="Temperature Sensor 01" />
                  <small class="error-message" id="deviceNameError"></small>
                </div>

                <div class="form-group">
                  <label for="deviceId">Device ID</label>
                  <input type="text" id="deviceId" placeholder="TEMP-SENSOR-001" />
                  <small class="error-message" id="deviceIdError"></small>
                </div>

                <div class="form-group">
                  <label for="deviceType">Device Type</label>
                  <select id="deviceType">
                    <option value="">Select device type</option>
                    <option value="temperature">Temperature Sensor</option>
                    <option value="pressure">Pressure Sensor</option>
                    <option value="vibration">Vibration Sensor</option>
                    <option value="plc">PLC Controller</option>
                    <option value="robotic">Robotic Arm</option>
                    <option value="monitoring">Monitoring Server</option>
                  </select>
                  <small class="error-message" id="deviceTypeError"></small>
                </div>

                <div class="form-group">
                  <label for="vlan">Network VLAN</label>
                  <select id="vlan">
                    <option value="">Select VLAN</option>
                    <option value="10">VLAN 10 &mdash; IoT Sensors</option>
                    <option value="20">VLAN 20 &mdash; Robotics / PLC</option>
                    <option value="30">VLAN 30 &mdash; Firewall</option>
                    <option value="40">VLAN 40 &mdash; Monitoring</option>
                    <option value="50">VLAN 50 &mdash; Management</option>
                  </select>
                  <small class="error-message" id="vlanError"></small>
                </div>

                <div class="form-group">
                  <label for="ipAddress">IP Address</label>
                  <input type="text" id="ipAddress" placeholder="192.168.10.10" />
                  <small class="error-message" id="ipAddressError"></small>
                </div>

                <div class="form-group">
                  <label for="macAddress">MAC Address</label>
                  <input type="text" id="macAddress" placeholder="00:1A:2B:3C:4D:5E" />
                  <small class="error-message" id="macAddressError"></small>
                </div>

                <div class="form-group">
                  <label for="ownerName">Device Owner</label>
                  <input type="text" id="ownerName" placeholder="Production Team" />
                  <small class="error-message" id="ownerNameError"></small>
                </div>

                <div class="form-group">
                  <label for="email">Owner Email</label>
                  <input type="email" id="email" placeholder="production@thinkix.com" />
                  <small class="error-message" id="emailError"></small>
                </div>
              </div>

              <div class="form-group full-width">
                <label for="description">Device Description</label>
                <textarea id="description" rows="5" maxlength="300" placeholder="Describe the device and its role in the industrial network..."></textarea>
                <small class="character-count" id="characterCount">0 / 300 characters</small>
                <small class="error-message" id="descriptionError"></small>
              </div>

              <div class="security-box">
                <div class="security-box-header">
                  <div>
                    <h3>Security Configuration</h3>
                    <p>Select the controls enabled for this device.</p>
                  </div>
                  <span class="shield">&#128737;&#65039;</span>
                </div>

                <label class="toggle-row">
                  <input type="checkbox" id="tlsEnabled" />
                  <span class="toggle"></span>
                  <span>MQTT over TLS</span>
                </label>

                <label class="toggle-row">
                  <input type="checkbox" id="certificateInstalled" />
                  <span class="toggle"></span>
                  <span>Device certificate installed</span>
                </label>

                <label class="toggle-row">
                  <input type="checkbox" id="monitoringEnabled" />
                  <span class="toggle"></span>
                  <span>Zeek &amp; Suricata monitoring</span>
                </label>
              </div>

              <label class="agreement-row">
                <input type="checkbox" id="agreement" />
                <span>I confirm that this device follows the approved security and network policy.</span>
              </label>

              <small class="error-message" id="agreementError"></small>

              <div class="button-group">
                <button type="reset" class="secondary-button" id="resetButton">Clear Form</button>
                <button type="submit" class="primary-button">
                  <span>Register Device</span>
                  <span class="button-arrow">&rarr;</span>
                </button>
              </div>
            </form>

            <div class="loading-box" id="loadingBox">
              <div class="loader"></div>
              <p>Validating secure device configuration...</p>
            </div>

            <div class="success-message" id="successMessage">
              <div class="success-icon">&#10003;</div>
              <div>
                <h3>Device Registration Successful</h3>
                <p>Device information passed front-end validation successfully.</p>
              </div>
            </div>
          </section>
"""

html = render_page(
    active_key="register",
    title_tag="Register Device",
    eyebrow="Device Onboarding",
    title="Register New Device",
    subtitle="Add a device to the industrial network with its security configuration.",
    right_html="",
    content=content,
)

# Full-screen registration loader: a direct child of <body> (not nested
# inside the panel/shell) so its position:fixed is never trapped by an
# ancestor's transform/animation, and it can truly cover everything.
LOADING_OVERLAY = """
    <div class="reg-loading-overlay" id="regLoadingOverlay" hidden>
      <div class="reg-loading-mark">
        <div class="reg-loading-ring"></div>
        <div class="reg-loading-logo"></div>
      </div>

      <div>
        <div class="reg-loading-heading" id="regLoadingHeading">Registering Device</div>
        <div class="reg-loading-count" id="regLoadingCount">STEP 1 OF 8</div>
      </div>

      <div class="reg-loading-status" id="regLoadingStatus">
        Loading the information submitted by management.
      </div>

      <div class="reg-loading-track">
        <div class="reg-loading-fill" id="regLoadingFill"></div>
      </div>
    </div>
"""

html = html.replace('<body class="dash2">', '<body class="dash2">\n' + LOADING_OVERLAY)

(ROOT / "register.html").write_text(html)
print("Generated: register.html")
