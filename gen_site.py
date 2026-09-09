#!/usr/bin/env python3
"""Generates the sidebar-shell HTML pages for the ThinkiX dashboard v3.
Reads the logo base64 from logo_b64.txt so the huge string is only
stored once, and templates every page from a shared shell so the
sidebar / watermark / topbar stay identical across the whole site.
"""
import pathlib

ROOT = pathlib.Path(__file__).parent
LOGO_B64 = (ROOT / "logo_b64.txt").read_text().strip()
LOGO_DATA_URI = f"data:image/png;base64,{LOGO_B64}"
LOGO_MARK_B64 = (ROOT / "logo_mark_b64.txt").read_text().strip()
LOGO_MARK_DATA_URI = f"data:image/png;base64,{LOGO_MARK_B64}"

ICONS = {
    "dashboard": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="2.5" y="2.5" width="6" height="6" rx="1.5"/><rect x="11.5" y="2.5" width="6" height="6" rx="1.5"/><rect x="2.5" y="11.5" width="6" height="6" rx="1.5"/><rect x="11.5" y="11.5" width="6" height="6" rx="1.5"/></svg>',
    "zonemap": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="10" cy="10" r="2.3"/><circle cx="3" cy="3" r="1.6"/><circle cx="17" cy="3" r="1.6"/><circle cx="3" cy="17" r="1.6"/><circle cx="17" cy="17" r="1.6"/><line x1="8.3" y1="8.3" x2="4.2" y2="4.2"/><line x1="11.7" y1="8.3" x2="15.8" y2="4.2"/><line x1="8.3" y1="11.7" x2="4.2" y2="15.8"/><line x1="11.7" y1="11.7" x2="15.8" y2="15.8"/></svg>',
    "alerts": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"><path d="M10 3 L18 17 L2 17 Z"/><line x1="10" y1="8" x2="10" y2="11.5"/><circle cx="10" cy="14" r="0.9" fill="currentColor" stroke="none"/></svg>',
    "interfaces": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M7 2v4M13 2v4M5 6h10v3a5 5 0 0 1-10 0V6z"/><path d="M10 14v4"/></svg>',
    "evidence": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"><path d="M10 2l7 3v5c0 4.5-3 7.5-7 8-4-.5-7-3.5-7-8V5l7-3z"/><path d="M7 10l2 2 4-4.5"/></svg>',
    "eventlog": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="12" height="15" rx="1.5"/><line x1="7" y1="7.5" x2="13" y2="7.5"/><line x1="7" y1="11" x2="13" y2="11"/><line x1="7" y1="14.5" x2="10.5" y2="14.5"/></svg>',
    "simulation": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><line x1="4" y1="17" x2="4" y2="3"/><line x1="10" y1="17" x2="10" y2="3"/><line x1="16" y1="17" x2="16" y2="3"/><circle cx="4" cy="7" r="1.8" fill="currentColor" stroke="none"/><circle cx="10" cy="13" r="1.8" fill="currentColor" stroke="none"/><circle cx="16" cy="9" r="1.8" fill="currentColor" stroke="none"/></svg>',
    "register": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="7" r="3"/><path d="M2.5 17c.5-3.5 3-5.5 5.5-5.5s5 2 5.5 5.5"/><line x1="15.5" y1="5" x2="15.5" y2="10"/><line x1="13" y1="7.5" x2="18" y2="7.5"/></svg>',
    "devicestatus": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><polyline points="2,10 6,10 8,4 12,16 14,10 18,10"/></svg>',
    "history": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="10" cy="11" r="7"/><polyline points="10,7 10,11 13,13"/><path d="M6 2.5 L3 4.5"/></svg>',
    "logout": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h4"/><polyline points="12,6 16,10 12,14"/><line x1="16" y1="10" x2="7" y2="10"/></svg>',
}

NAV_GROUPS = [
    ("Overview", [("dashboard", "Dashboard", "management.html")]),
    ("Network & Security", [
        ("zonemap", "Zone Map", "zone-map.html"),
        ("alerts", "Security Alerts", "alerts.html"),
        ("interfaces", "Interfaces", "interfaces.html"),
        ("evidence", "Evidence", "evidence.html"),
        ("eventlog", "Event Log", "event-log.html"),
    ]),
    ("Simulation", [("simulation", "Live Simulation", "simulation.html")]),
    ("Device Management", [
        ("register", "Register Device", "register.html"),
        ("history", "History", "history.html"),
    ]),
]


def render_sidebar(active_key: str) -> str:
    groups_html = []
    for group_label, items in NAV_GROUPS:
        links = []
        for key, label, href in items:
            cls = "active" if key == active_key else ""
            links.append(
                f'<a href="{href}" class="{cls}">{ICONS[key]}<span>{label}</span></a>'
            )
        groups_html.append(
            f'<div class="dash2-sidenav-group"><span>{group_label}</span>{"".join(links)}</div>'
        )

    return f"""
    <div class="dash2-watermark"></div>
    <div class="dash2-shell">
      <aside class="dash2-sidebar">
        <div class="dash2-sidebar-brand">
          <img src="{LOGO_DATA_URI}" alt="ThinkiX logo" />
          <div>
            <h1>ThinkiX</h1>
            <span>Industrial IoT Security</span>
          </div>
        </div>

        <nav class="dash2-sidenav">
          {"".join(groups_html)}
        </nav>

        <div class="dash2-sidebar-foot">
          <span class="dash2-online-pill"><i></i><span>SYSTEM ONLINE</span></span>
          <a href="index.html" class="dash2-logout">{ICONS['logout']}<span>Logout</span></a>
        </div>
      </aside>

      <div class="dash2-content">
"""


SHELL_CLOSE = """
      </div>
    </div>
"""


def render_topbar(eyebrow: str, title: str, subtitle: str, right_html: str = "") -> str:
    return f"""
        <header class="dash2-topbar">
          <div>
            <p class="dash2-eyebrow">{eyebrow}</p>
            <h1>{title}</h1>
            <p>{subtitle}</p>
          </div>
          <div class="dash2-topbar-right">{right_html}</div>
        </header>
"""


def render_page(active_key: str, title_tag: str, eyebrow: str, title: str, subtitle: str,
                 right_html: str, content: str, extra_head: str = "") -> str:
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <title>ThinkiX | {title_tag}</title>

    <link rel="stylesheet" href="dashboard.css" />
    <style>
      :root {{
        --logo-url: url('{LOGO_DATA_URI}');
        --logo-mark-url: url('{LOGO_MARK_DATA_URI}');
      }}
    </style>
    {extra_head}
  </head>

  <body class="dash2">
    {render_sidebar(active_key)}
        {render_topbar(eyebrow, title, subtitle, right_html)}

        <main class="dash2-page">
{content}
        </main>

        <footer class="dash2-footer">
          <p>ThinkiX Manufacturing &bull; Secure Industrial IoT Management Platform &bull; BN304 Evidence Log</p>
        </footer>
    {SHELL_CLOSE}
    <script src="script.js"></script>
  </body>
</html>
"""


if __name__ == "__main__":
    print("logo bytes:", len(LOGO_B64))
