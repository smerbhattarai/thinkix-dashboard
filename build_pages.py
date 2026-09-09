#!/usr/bin/env python3
"""Builds the sidebar-shell dashboard pages using gen_site.render_page()."""
import pathlib
from gen_site import render_page

ROOT = pathlib.Path(__file__).parent

# =====================================================================
# DASHBOARD (clean — devices + a thin stat row, nothing else combined in)
# =====================================================================

dashboard_content = """
          <section class="dash2-stat-row">
            <a href="#connected-devices" class="dashboard-stat-card">
              <div class="dash2-stat-icon">&#9673;</div>
              <div>
                <p>Connected Devices</p>
                <h2 id="totalDevices">4</h2>
              </div>
            </a>

            <a href="#connected-devices" class="dashboard-stat-card">
              <div class="dash2-stat-icon ok">&#9679;</div>
              <div>
                <p>Online Devices</p>
                <h2 id="onlineDevices">3</h2>
              </div>
            </a>

            <a href="alerts.html" class="dashboard-stat-card">
              <div class="dash2-stat-icon warn">&#9888;</div>
              <div>
                <p>Security Alerts</p>
                <h2 id="alertCount">2</h2>
              </div>
            </a>

            <a href="event-log.html" class="dashboard-stat-card">
              <div class="dash2-stat-icon info">&#9776;</div>
              <div>
                <p>Event Log Entries</p>
                <h2>3</h2>
              </div>
            </a>
          </section>

          <section class="dash2-panel" id="connected-devices">
            <div class="dash2-panel-head">
              <div>
                <h2>Connected Devices</h2>
                <p>Live-verified against the GNS3 lab evidence pass &middot; 2 Sep 2026</p>
              </div>
              <a href="zone-map.html" class="dash2-chip">View zone map &rarr;</a>
            </div>

            <div class="device-list">
              <div class="device-row" id="sensorLiveDeviceRow">
                <span class="device-status online" id="sensorLiveDot"></span>
                <div class="device-info">
                  <strong>iot-sensor-vlan10</strong>
                  <small>10.10.10.12 &bull; mTLS verified</small>
                  <span class="device-zone-tag" style="--zc:#34d399" id="sensorLiveSubline">Live-checked from Monitoring node</span>
                </div>
                <span class="status-label online-text" id="sensorLiveStatusLabel">ONLINE</span>
              </div>

              <div class="device-row">
                <span class="device-status offline"></span>
                <div class="device-info">
                  <strong>plc1-robotics</strong>
                  <small>Cert serial 1000 &bull; CRL revoked</small>
                  <span class="device-zone-tag" style="--zc:#fb923c">VLAN 20 &mdash; Robotics / PLC</span>
                </div>
                <span class="status-label offline-text">REVOKED</span>
              </div>

              <div class="device-row">
                <span class="device-status online"></span>
                <div class="device-info">
                  <strong>Mosquitto-Broker</strong>
                  <small>10.10.30.11 &bull; Port 8883 (TLS 1.3)</small>
                  <span class="device-zone-tag" style="--zc:#38bdf8">VLAN 30 &mdash; Broker / Firewall</span>
                </div>
                <span class="status-label online-text">ACTIVE</span>
              </div>

              <div class="device-row">
                <span class="device-status online"></span>
                <div class="device-info">
                  <strong>Suricata-IDS</strong>
                  <small>10.10.40.11 &bull; 2 signatures live</small>
                  <span class="device-zone-tag" style="--zc:#a78bfa">VLAN 40 &mdash; Monitoring</span>
                </div>
                <span class="status-label online-text">MONITORING</span>
              </div>
            </div>
          </section>
"""

dashboard_html = render_page(
    active_key="dashboard",
    title_tag="Dashboard",
    eyebrow="&#9679; Industrial IoT Security &mdash; ThinkiX Manufacturing",
    title="Dashboard",
    subtitle="Every device connected across the five segmented VLANs, live-verified against the project evidence log.",
    right_html='<span class="live-badge">&#9679; LAST VERIFIED 2 SEP 2026</span>',
    content=dashboard_content,
)
(ROOT / "management.html").write_text(dashboard_html)


# =====================================================================
# ZONE MAP
# =====================================================================

zonemap_content = """
          <section class="dash2-panel" id="zone-map">
            <div class="dash2-panel-head">
              <div>
                <h2>Network Zone Map</h2>
                <p>IEC 62443-style zone &amp; conduit segmentation, enforced by pfSense</p>
              </div>
              <span class="dash2-chip">5 zones &middot; deny-by-default</span>
            </div>

            <div class="zm-hub">
              <div class="zm-hub-core">
                <div class="zm-hub-icon">&#129521;</div>
                <div>
                  <strong>pfSense &mdash; Zone &amp; Conduit Firewall</strong>
                  <small>Every inter-zone packet is inspected and explicitly allowed</small>
                </div>
              </div>
            </div>

            <p class="zm-conduit-label">&#9662; nothing crosses a zone boundary unless a rule below explicitly allows it &#9662;</p>

            <div class="zm-zones">
              <div class="zm-zone" style="--zc:#34d399">
                <span class="zm-zone-vlan">VLAN 10</span>
                <h3>IoT Sensors</h3>
                <p>Field sensors, mTLS to the broker only.</p>
                <div class="zm-zone-foot">
                  <span>1 device</span>
                  <span class="zm-status zm-status--ok">ONLINE</span>
                </div>
              </div>

              <div class="zm-zone" style="--zc:#fb923c">
                <span class="zm-zone-vlan">VLAN 20</span>
                <h3>Robotics / PLC</h3>
                <p>Controllers with certificate-based access control.</p>
                <div class="zm-zone-foot">
                  <span>1 device</span>
                  <span class="zm-status zm-status--warn">CRL REVOKED</span>
                </div>
              </div>

              <div class="zm-zone" style="--zc:#38bdf8">
                <span class="zm-zone-vlan">VLAN 30</span>
                <h3>Broker / Firewall</h3>
                <p>Mosquitto MQTT broker, TLS 1.3 + mutual auth.</p>
                <div class="zm-zone-foot">
                  <span>1 device</span>
                  <span class="zm-status zm-status--ok">ACTIVE</span>
                </div>
              </div>

              <div class="zm-zone" style="--zc:#a78bfa">
                <span class="zm-zone-vlan">VLAN 40</span>
                <h3>Monitoring</h3>
                <p>Suricata IDS with automated quarantine response.</p>
                <div class="zm-zone-foot">
                  <span>1 device</span>
                  <span class="zm-status zm-status--info">MONITORING</span>
                </div>
              </div>

              <div class="zm-zone" style="--zc:#f472b6">
                <span class="zm-zone-vlan">VLAN 50</span>
                <h3>Management</h3>
                <p>Admin access to this dashboard &mdash; restricted zone.</p>
                <div class="zm-zone-foot">
                  <span>Restricted</span>
                  <span class="zm-status zm-status--ok">SECURE</span>
                </div>
              </div>
            </div>

            <div class="dash2-rules">
              <div class="dash2-rules-row head">
                <span>Source zone</span>
                <span>Destination zone</span>
                <span>Protocol / port</span>
                <span>Purpose</span>
                <span>Rule</span>
              </div>
              <div class="dash2-rules-row">
                <span class="mono">VLAN 10 &mdash; Sensors</span>
                <span class="mono">VLAN 30 &mdash; Broker</span>
                <span class="mono">TCP/8883 (MQTT+TLS)</span>
                <span>Sensor telemetry publish</span>
                <span class="dash2-rule-pill allow">ALLOW</span>
              </div>
              <div class="dash2-rules-row">
                <span class="mono">VLAN 40 &mdash; Monitoring</span>
                <span class="mono">VLAN 10 &mdash; Sensors</span>
                <span class="mono">ICMP</span>
                <span>Live reachability check</span>
                <span class="dash2-rule-pill allow">ALLOW</span>
              </div>
              <div class="dash2-rules-row">
                <span class="mono">VLAN 40 &mdash; Monitoring</span>
                <span class="mono">pfSense (local)</span>
                <span class="mono">syslog (local0)</span>
                <span>Automated quarantine trigger</span>
                <span class="dash2-rule-pill allow">ALLOW</span>
              </div>
              <div class="dash2-rules-row">
                <span class="mono">Any zone</span>
                <span class="mono">Any zone</span>
                <span class="mono">any</span>
                <span>Everything not explicitly listed above</span>
                <span class="dash2-rule-pill deny">DENY</span>
              </div>
              <div class="dash2-rules-row">
                <span class="mono">Any zone</span>
                <span class="mono">WAN / Internet</span>
                <span class="mono">any</span>
                <span>Lab isolation &mdash; no public route</span>
                <span class="dash2-rule-pill deny">DENY</span>
              </div>
            </div>
          </section>
"""

zonemap_html = render_page(
    active_key="zonemap",
    title_tag="Zone Map",
    eyebrow="Network Architecture",
    title="Network Zone Map",
    subtitle="The IEC 62443 zone &amp; conduit model this project implements &mdash; five VLANs, one deny-by-default firewall.",
    right_html='<span class="dash2-chip dash2-chip--ok">&#9679; LAST VERIFIED 2 SEP 2026</span>',
    content=zonemap_content,
)
(ROOT / "zone-map.html").write_text(zonemap_html)


# =====================================================================
# ALERTS
# =====================================================================

alerts_content = """
          <section class="dash2-strip">
            <div class="dash2-strip-item bad"><strong>1</strong><span>High severity</span></div>
            <div class="dash2-strip-item warn"><strong>1</strong><span>Medium severity</span></div>
            <div class="dash2-strip-item ok"><strong>1</strong><span>Verified normal</span></div>
            <div class="dash2-strip-item"><strong>0</strong><span>Manual interventions</span></div>
          </section>

          <section class="dash2-panel" id="security-alerts">
            <div class="dash2-panel-head">
              <div>
                <h2>Security Alerts</h2>
                <p>Suricata detections on the Monitoring node, cross-checked against pfSense's quarantine table</p>
              </div>
              <span class="dash2-chip dash2-chip--warn">2 Alerts</span>
            </div>

            <div class="dash2-alert-list">
              <div class="dash2-alert" style="--ac:#f43f5e">
                <div class="dash2-alert-icon">&#9888;</div>
                <div>
                  <div class="dash2-alert-top">
                    <strong>Unexpected TCP Connection &mdash; Auto-Quarantined</strong>
                  </div>
                  <p>Suricata sid 1000002 fired on 10.10.40.1; pfSense added the source to the quarantine table automatically, zero manual steps.</p>
                  <div class="dash2-alert-meta">
                    <span><b>03:19 UTC</b></span>
                    <span>Severity: <b>HIGH</b></span>
                    <span>Action: <b>Auto-quarantined</b></span>
                  </div>
                </div>
              </div>

              <div class="dash2-alert" style="--ac:#f59e0b">
                <div class="dash2-alert-icon">!</div>
                <div>
                  <div class="dash2-alert-top">
                    <strong>ICMP Probe Detected</strong>
                  </div>
                  <p>Suricata sid 1000001 fired on cross-host ping traffic to the Monitoring node.</p>
                  <div class="dash2-alert-meta">
                    <span><b>03:16 UTC</b></span>
                    <span>Severity: <b>MEDIUM</b></span>
                    <span>Action: <b>Logged</b></span>
                  </div>
                </div>
              </div>

              <div class="dash2-alert" style="--ac:#22c55e">
                <div class="dash2-alert-icon">&#10003;</div>
                <div>
                  <div class="dash2-alert-top">
                    <strong>Cross-Zone MQTT Delivery Verified</strong>
                  </div>
                  <p>VLAN10 sensor &rarr; VLAN30 broker delivered over the 8883 conduit with mutual TLS, end to end.</p>
                  <div class="dash2-alert-meta">
                    <span><b>2 Sep 2026</b></span>
                    <span>Severity: <b>NORMAL</b></span>
                    <span>Action: <b>Verified</b></span>
                  </div>
                </div>
              </div>
            </div>
          </section>
"""

alerts_html = render_page(
    active_key="alerts",
    title_tag="Security Alerts",
    eyebrow="Threat Detection",
    title="Security Alerts",
    subtitle="Every Suricata detection from the verification pass, with the pfSense response that followed it.",
    right_html='<span class="dash2-chip dash2-chip--ok">&#9679; LAST VERIFIED 2 SEP 2026</span>',
    content=alerts_content,
)
(ROOT / "alerts.html").write_text(alerts_html)


# =====================================================================
# INTERFACES
# =====================================================================

interfaces_content = """
          <section class="dash2-panel">
            <div class="dash2-panel-head">
              <div>
                <h2>Interface Status</h2>
                <p>Live-verified state of every enforcement point in the segmented network</p>
              </div>
              <span class="dash2-chip dash2-chip--ok">6 / 6 healthy</span>
            </div>

            <div class="dash2-iface-grid">
              <div class="dash2-iface-row">
                <div>
                  <strong>pfSense WAN</strong>
                  <small>Internet Gateway</small>
                </div>
                <span class="dash2-iface-up">&#9679; UP</span>
              </div>

              <div class="dash2-iface-row">
                <div>
                  <strong>pfSense LAN</strong>
                  <small>Industrial Network</small>
                </div>
                <span class="dash2-iface-up">&#9679; UP</span>
              </div>

              <div class="dash2-iface-row">
                <div>
                  <strong>MQTT Broker</strong>
                  <small>TCP 8883 &bull; TLS 1.3 + mutual auth</small>
                </div>
                <span class="dash2-iface-up">&#9679; ACTIVE</span>
              </div>

              <div class="dash2-iface-row">
                <div>
                  <strong>Suricata IDS</strong>
                  <small>Security Monitoring</small>
                </div>
                <span class="dash2-iface-mon">&#9679; MONITORING</span>
              </div>

              <div class="dash2-iface-row">
                <div>
                  <strong>CRL Enforcement</strong>
                  <small>Revoked certs rejected at handshake</small>
                </div>
                <span class="dash2-iface-up">&#9679; ACTIVE</span>
              </div>

              <div class="dash2-iface-row">
                <div>
                  <strong>Automated Quarantine</strong>
                  <small>Suricata &rarr; syslog &rarr; pf table</small>
                </div>
                <span class="dash2-iface-up">&#9679; ACTIVE</span>
              </div>
            </div>
          </section>
"""

interfaces_html = render_page(
    active_key="interfaces",
    title_tag="Interfaces",
    eyebrow="Network Health",
    title="Interface Status",
    subtitle="Every enforcement point pfSense and the Monitoring node reported healthy during the verification pass.",
    right_html='<span class="dash2-chip dash2-chip--ok">&#9679; LAST VERIFIED 2 SEP 2026</span>',
    content=interfaces_content,
)
(ROOT / "interfaces.html").write_text(interfaces_html)


# =====================================================================
# EVIDENCE
# =====================================================================

evidence_content = """
          <section class="dash2-panel">
            <div class="dash2-panel-head">
              <div>
                <h2>GNS3 Lab Evidence</h2>
                <p>Why this page shows verified figures instead of a live feed</p>
              </div>
            </div>

            <div class="dash2-gns3">
              <div class="dash2-gns3-icon">&#9673;</div>
              <div>
                <h3>Not wired to a public live feed, by design</h3>
                <p>
                  The lab's VLANs sit behind pfSense with no route to the public
                  internet &mdash; that isolation is the whole point of the
                  architecture, so this site doesn't poll it directly. Every
                  figure across this dashboard instead comes from a hands-on
                  verification pass inside GNS3 (console/VNC access only, no
                  SSH used anywhere in the lab), captured 2 Sep 2026.
                </p>
              </div>
            </div>

            <div class="dash2-node-tags">
              <span>iot-sensor-vlan10</span>
              <span>plc1-robotics</span>
              <span>pfSense</span>
              <span>Suricata</span>
              <span>Mosquitto</span>
            </div>
          </section>

          <section class="dash2-panel">
            <div class="dash2-panel-head">
              <div>
                <h2>Verified Security Checks</h2>
                <p>Counted directly during the verification pass, by project phase</p>
              </div>
            </div>

            <div class="dash2-stat-row" style="margin-bottom:18px">
              <div class="dashboard-stat-card" style="cursor:default">
                <div class="dash2-stat-icon">&#128274;</div>
                <div><p>TLS 1.3 Handshakes</p><h2>5</h2></div>
              </div>
              <div class="dashboard-stat-card" style="cursor:default">
                <div class="dash2-stat-icon info">&#128196;</div>
                <div><p>Device Certs Issued</p><h2>4</h2></div>
              </div>
              <div class="dashboard-stat-card" style="cursor:default">
                <div class="dash2-stat-icon ok">&#9993;</div>
                <div><p>MQTT Messages Delivered</p><h2>4</h2></div>
              </div>
              <div class="dashboard-stat-card" style="cursor:default">
                <div class="dash2-stat-icon warn">&#9873;</div>
                <div><p>Quarantine Triggers</p><h2>1</h2></div>
              </div>
            </div>

            <div class="dash2-checklist">
              <div class="dash2-checklist-item"><span class="n">5</span><p>Phase 2 &mdash; Segmentation checks</p></div>
              <div class="dash2-checklist-item"><span class="n">6</span><p>Phase 3 &mdash; PKI / TLS checks</p></div>
              <div class="dash2-checklist-item"><span class="n">2</span><p>Phase 4 &mdash; IDS checks</p></div>
              <div class="dash2-checklist-item"><span class="n">3</span><p>Phase 5 &mdash; Quarantine checks</p></div>
            </div>
          </section>
"""

evidence_html = render_page(
    active_key="evidence",
    title_tag="Evidence",
    eyebrow="Project Evidence",
    title="GNS3 Lab Evidence",
    subtitle="The hands-on verification pass behind every figure on this site &mdash; not simulated traffic.",
    right_html='<span class="dash2-chip dash2-chip--ok">&#9679; LAST VERIFIED 2 SEP 2026</span>',
    content=evidence_content,
)
(ROOT / "evidence.html").write_text(evidence_html)


# =====================================================================
# EVENT LOG
# =====================================================================

eventlog_content = """
          <section class="dash2-panel" id="event-log">
            <div class="dash2-panel-head">
              <div>
                <h2>Security Event Log</h2>
                <p>Chronological record of certificate, onboarding and quarantine events</p>
              </div>
              <span class="dash2-chip">3 entries</span>
            </div>

            <div class="email-history">
              <div class="email-row">
                <div class="email-icon-small">&#9940;</div>
                <div>
                  <strong>Certificate Revoked</strong>
                  <p>plc1-robotics revoked via CRL; broker rejected it (error 23).</p>
                  <small>2 Sep 2026</small>
                </div>
                <span class="email-sent">LOGGED</span>
              </div>

              <div class="email-row">
                <div class="email-icon-small">&#10004;</div>
                <div>
                  <strong>Device Onboarded</strong>
                  <p>iot-sensor-vlan10 issued a device cert and verified onto VLAN 10.</p>
                  <small>2 Sep 2026</small>
                </div>
                <span class="email-sent">LOGGED</span>
              </div>

              <div class="email-row">
                <div class="email-icon-small">&#9888;</div>
                <div>
                  <strong>Source Auto-Quarantined</strong>
                  <p>10.10.40.1 blocked at pfSense following a Suricata detection.</p>
                  <small>2 Sep 2026</small>
                </div>
                <span class="email-sent">LOGGED</span>
              </div>
            </div>
          </section>
"""

eventlog_html = render_page(
    active_key="eventlog",
    title_tag="Event Log",
    eyebrow="Audit Trail",
    title="Security Event Log",
    subtitle="Every certificate, onboarding and quarantine event recorded during the verification pass.",
    right_html='<span class="dash2-chip dash2-chip--ok">&#9679; LAST VERIFIED 2 SEP 2026</span>',
    content=eventlog_content,
)
(ROOT / "event-log.html").write_text(eventlog_html)


# =====================================================================
# LIVE SIMULATION
# =====================================================================

simulation_content = """
          <section class="dash2-panel dash2-sim" id="live-sim">
            <div class="dash2-panel-head">
              <div>
                <h2>Live Simulation &mdash; Virtual Sensor</h2>
                <p>Same-browser demo via local storage &mdash; not a live connection into the isolated GNS3 lab</p>
              </div>
            </div>

            <div class="dash2-sim-grid">
              <div class="dash2-sim-card">
                <h3>Virtual Sensor Switch</h3>
                <p class="dash2-sim-desc">
                  Flip the switch, then open the virtual sensor view (link above) in
                  a second tab or window next to this one &mdash; it updates
                  instantly. Demonstrates the operator &rarr; actuator control
                  concept down to a device indicator.
                </p>

                <div class="dash2-sim-row">
                  <div>
                    <strong id="actuatorStateLabel">Sensor Indicator: OFF (Simulated)</strong>
                    <small>iot-sensor-vlan10 &bull; simulated, this browser only</small>
                  </div>
                  <label class="switch">
                    <input type="checkbox" id="actuatorToggle" />
                    <span class="slider"></span>
                  </label>
                </div>
              </div>

              <div class="dash2-sim-card">
                <h3>Virtual Temperature Reading</h3>
                <p class="dash2-sim-desc">
                  The slider lives on the virtual sensor view &mdash; move it there and
                  this reading updates here instantly, drifting slightly on its own
                  to imitate real sensor noise.
                </p>

                <div class="dash2-sim-row">
                  <div class="dash2-temp-value" id="tempReadoutValue">24.0&deg;C</div>
                  <div>
                    <strong id="tempStatusLabel">Live Reading</strong>
                    <small>iot-sensor-vlan10 &bull; simulated, this browser only</small>
                  </div>
                </div>

                <div class="dash2-temp-bar">
                  <div class="dash2-temp-bar-fill" id="tempBarFill"></div>
                </div>

                <div class="dash2-temp-labels">
                  <span>15&deg;C</span>
                  <span>45&deg;C</span>
                </div>
              </div>
            </div>
          </section>
"""

simulation_html = render_page(
    active_key="simulation",
    title_tag="Live Simulation",
    eyebrow="Interactive Demo",
    title="Live Simulation",
    subtitle="A same-browser demo of the operator &rarr; actuator control concept, tied to the virtual sensor view.",
    right_html='<a href="sensor.html" target="_blank" rel="noopener" class="dash2-sim-link">Open Sensor View &#8599;</a>',
    content=simulation_content,
)
(ROOT / "simulation.html").write_text(simulation_html)

print("Generated: management.html, zone-map.html, alerts.html, interfaces.html, evidence.html, event-log.html, simulation.html")
