#!/usr/bin/env python3
"""Re-skins device-status.html and history.html with the v3 dash2 sidebar
shell (matching the other 8 pages), while leaving every id/class the
pages' own inline <script> depends on completely untouched. Only the
outer chrome (old .topbar header) is replaced; internal panel/content
markup, ids, and behavior are preserved byte-for-byte.
"""
import re
import pathlib
from gen_site import render_sidebar, render_topbar, SHELL_CLOSE, LOGO_DATA_URI, LOGO_MARK_DATA_URI

ROOT = pathlib.Path(__file__).parent


def extract(content, start_tag, end_tag, start_from=0):
    s = content.index(start_tag, start_from)
    e = content.index(end_tag, s) + len(end_tag)
    return content[s:e], s, e


def strip_top_level_rules(style_text, remove_selectors):
    """Parse style_text into top-level blocks (selector + braced body,
    braces balanced so @media blocks are captured whole) and drop any
    block whose selector line matches an entry in remove_selectors
    (exact string match after stripping whitespace)."""
    blocks = []
    i = 0
    n = len(style_text)
    while i < n:
        # skip leading whitespace
        while i < n and style_text[i].isspace():
            i += 1
        if i >= n:
            break
        sel_start = i
        depth = 0
        j = i
        # scan selector up to first '{'
        brace_pos = style_text.index('{', j)
        selector = style_text[sel_start:brace_pos].strip()
        # now find matching closing brace for this block (balanced)
        depth = 1
        k = brace_pos + 1
        while depth > 0:
            if style_text[k] == '{':
                depth += 1
            elif style_text[k] == '}':
                depth -= 1
            k += 1
        block_text = style_text[sel_start:k]
        blocks.append((selector, block_text))
        i = k
    kept = [b for sel, b in blocks if sel not in remove_selectors]
    return '\n\n      '.join(kept)


def convert(fname, active_key, title_tag, eyebrow, title, subtitle, remove_selectors,
            right_html_pattern=None):
    path = ROOT / fname
    content = path.read_text()

    style_block, _, _ = extract(content, '<style>', '</style>')
    style_inner = style_block[len('<style>'):-len('</style>')]

    header_block, _, _ = extract(content, '<header', '</header>')

    main_block, main_s, main_e = extract(content, '<main', '</main>')
    # the old page-heading section duplicates the title/subtitle the new
    # dash2-topbar now renders -- drop it so the heading isn't repeated
    main_block = re.sub(
        r'<section class="page-heading">.*?</section>\s*',
        '', main_block, count=1, flags=re.S,
    )

    script_block, script_s, _ = extract(content, '<script>', '</script>')
    # anything sitting between </main> and <script> (e.g. a modal dialog
    # that lives outside <main> in the original markup) must be preserved
    # too, or ids its own inline script depends on will vanish
    trailing_block = content[main_e:script_s].strip()
    # the old page had its own plain <footer> -- the new dash2-footer
    # replaces it, so drop the old one to avoid a duplicate
    trailing_block = re.sub(r'<footer>.*?</footer>\s*', '', trailing_block, flags=re.S)

    if trailing_block:
        main_block = main_block + "\n\n        " + trailing_block

    right_html = ""
    if right_html_pattern:
        m = re.search(right_html_pattern, header_block, re.S)
        if m:
            right_html = m.group(0)

    trimmed_style = strip_top_level_rules(style_inner, remove_selectors)

    new_html = f"""<!doctype html>
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

      {trimmed_style}
    </style>
  </head>

  <body class="dash2">
    {render_sidebar(active_key)}
        {render_topbar(eyebrow, title, subtitle, right_html)}

        {main_block}

        <footer class="dash2-footer">
          <p>ThinkiX Manufacturing &bull; Secure Industrial IoT Management Platform &bull; BN304 Evidence Log</p>
        </footer>
    {SHELL_CLOSE}
    {script_block}
  </body>
</html>
"""
    path.write_text(new_html)
    print(f"Converted: {fname}")


DEVICE_STATUS_REMOVE = {
    'body', '.topbar', '.brand', '.logo', '.logo img', '.topbar-nav',
    '.nav-tab', '.nav-tab:hover', '.nav-tab.active', '.topbar-right',
    '.logout-link', '.logout-link:hover', '@media (max-width: 900px)',
    '.brand h2', '.brand p',
}

HISTORY_REMOVE = {
    'body', '.topbar', '.brand', '.logo', '.logo img', '.brand h2',
    '.brand p', '.header-actions', '.header-button', '.header-button:hover',
    '.header-button.active',
}

if __name__ == "__main__":
    convert(
        'device-status.html',
        active_key='devicestatus',
        title_tag='Device Onboarding Status',
        eyebrow='Device Onboarding Workflow',
        title='Registering Industrial Device',
        subtitle='Processing the device information entered by management, preparing the security profile and attempting live network integration.',
        remove_selectors=DEVICE_STATUS_REMOVE,
        right_html_pattern=r'<div class="gns3-top-status".*?</div>',
    )
    convert(
        'history.html',
        active_key='history',
        title_tag='Registration History',
        eyebrow='Device Management Records',
        title='Registration History',
        subtitle='Review every industrial device that has been registered through the ThinkiX management workflow.',
        remove_selectors=HISTORY_REMOVE,
    )
