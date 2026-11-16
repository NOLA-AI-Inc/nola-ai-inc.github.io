#!/usr/bin/env python3
"""Generate a website celebrating how awesome Lauren is.

Usage:
    python3 generate_lauren.py               # writes lauren/index.html
    python3 generate_lauren.py --name Lauren --out lauren

Add or edit reasons in REASONS below and re-run. The output is a single
self-contained HTML file (no dependencies), served by GitHub Pages at /lauren/.
"""
import argparse
import html
import json
from pathlib import Path

REASONS = [
    "Is super nice to everyone she meets",
    "Is super friendly and makes people feel welcome",
    "Is very kind, all the way through",
    "Is very helpful and always ready to pitch in",
    "Loves spending time with and caring for people with intellectual disabilities and autistic people",
    "Brings patience and warmth to everyone she looks after",
    "Makes every room brighter just by walking into it",
    "Shows up for the people she cares about, every time",
    "Has a laugh that's genuinely contagious",
    "Is, quite simply, awesome",
]

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} Is Awesome</title>
<style>
  :root {{ --bg1:#ff9a9e; --bg2:#fad0c4; --bg3:#a18cd1; --ink:#2b1d3a; --card:rgba(255,255,255,.75); }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; min-height:100vh; font-family:system-ui,-apple-system,"Segoe UI",sans-serif;
         color:var(--ink); background:linear-gradient(135deg,var(--bg1),var(--bg2),var(--bg3));
         background-size:300% 300%; animation:shift 12s ease infinite; overflow-x:hidden; }}
  @keyframes shift {{ 0%,100%{{background-position:0% 50%}} 50%{{background-position:100% 50%}} }}
  main {{ max-width:760px; margin:0 auto; padding:64px 16px; text-align:center; position:relative; z-index:1; }}
  h1 {{ font-size:clamp(2.6rem,9vw,5.5rem); line-height:1; margin:0 0 12px; letter-spacing:-.02em; }}
  h1 span {{ display:inline-block; margin-right:.25em; animation:pop 1.6s ease-in-out infinite; }}
  @keyframes pop {{ 0%,100%{{transform:scale(1)}} 50%{{transform:scale(1.08)}} }}
  .sub {{ font-size:1.25rem; margin:0 0 40px; opacity:.85; }}
  #reason {{ background:var(--card); border-radius:20px; padding:32px 24px; font-size:clamp(1.2rem,4vw,1.7rem);
            min-height:130px; display:flex; align-items:center; justify-content:center;
            box-shadow:0 10px 40px rgba(43,29,58,.15); transition:opacity .3s; }}
  button {{ margin-top:24px; font:inherit; font-weight:700; font-size:1.1rem; padding:14px 28px; border:0;
           border-radius:999px; background:var(--ink); color:#fff; cursor:pointer; transition:transform .15s; }}
  button:hover {{ transform:translateY(-2px) scale(1.04); }}
  ol {{ text-align:left; background:var(--card); border-radius:20px; padding:24px 24px 24px 48px;
       margin-top:48px; line-height:1.8; font-size:1.05rem; }}
  .count {{ margin-top:16px; font-weight:600; }}
  .heart {{ position:fixed; top:-40px; pointer-events:none; font-size:24px; animation:fall linear forwards; z-index:0; }}
  @keyframes fall {{ to {{ transform:translateY(110vh) rotate(360deg); opacity:.2; }} }}
  @media (prefers-reduced-motion: reduce) {{ *{{animation:none!important}} }}
</style>
</head>
<body>
<main>
  <h1><span>{name}</span> is awesome</h1>
  <p class="sub">This is a scientifically verified fact.</p>
  <div id="reason">Click the button for a reason.</div>
  <button id="more">Another reason &#10024;</button>
  <p class="count" id="count"></p>
  <ol>{items}</ol>
</main>
<script>
  const reasons = {reasons_json};
  const box = document.getElementById("reason"), count = document.getElementById("count");
  let seen = 0, last = -1;
  function next() {{
    let i; do {{ i = Math.floor(Math.random() * reasons.length); }} while (reasons.length > 1 && i === last);
    last = i; seen++;
    box.style.opacity = 0;
    setTimeout(() => {{ box.textContent = reasons[i]; box.style.opacity = 1; }}, 200);
    count.textContent = `Awesomeness confirmed ${{seen}} time${{seen === 1 ? "" : "s"}}.`;
    burst(12);
  }}
  function burst(n) {{
    const icons = ["\\u2764\\ufe0f","\\u2728","\\u{{1F496}}","\\u2b50","\\u{{1F389}}"];
    for (let k = 0; k < n; k++) {{
      const h = document.createElement("div");
      h.className = "heart";
      h.textContent = icons[Math.floor(Math.random() * icons.length)];
      h.style.left = Math.random() * 100 + "vw";
      h.style.animationDuration = 3 + Math.random() * 3 + "s";
      document.body.appendChild(h);
      setTimeout(() => h.remove(), 6500);
    }}
  }}
  document.getElementById("more").addEventListener("click", next);
  burst(20);
</script>
</body>
</html>
"""


def build(name: str, reasons: list[str]) -> str:
    items = "".join(f"<li>{html.escape(r)}</li>" for r in reasons)
    # Escape "</" so a reason can never close the <script> tag early.
    reasons_json = json.dumps(reasons).replace("</", "<\\/")
    return TEMPLATE.format(name=html.escape(name), items=items, reasons_json=reasons_json)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--name", default="Lauren")
    p.add_argument("--out", default="lauren", help="output directory")
    args = p.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "index.html"
    path.write_text(build(args.name, REASONS), encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
