"""Generate the HTML pages and BOM files for SafeASP (USBasp V6, USB-C). Run from the repo root:
    python -X utf8 -I tools/gen_docs.py
Writes docs/bom.html, wiring-by-section.html, schematic-sections.html, pcb-floorplan.html (same look as the TankPilot pages),
docs/images/pcb-floorplan.svg and hardware/bom/*. All connections are PLANNED (no EasyEDA schematic exists yet)."""
import os, sys, csv, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D
import layout as PL
import sheets as SH
import pinguides as PG

e = html.escape
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
os.makedirs(os.path.join(DOCS, "images"), exist_ok=True)
os.makedirs(os.path.join(ROOT, "hardware", "bom"), exist_ok=True)


CSS = """:root{--bg:#f4f6fb;--card:#fff;--ink:#16202f;--fg:#16202f;--mut:#64748b;--mute:#64748b;--line:#e2e8f0;--acc:#2563eb;--board:#e8efe4}
@media (prefers-color-scheme:dark){:root{--bg:#0b1220;--card:#131c2e;--ink:#e6edf7;--fg:#e6edf7;--mut:#93a3b8;--mute:#93a3b8;--line:#243049;--acc:#60a5fa;--board:#16251d}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,Segoe UI,Roboto,sans-serif}
header{padding:36px 16px 70px;background:linear-gradient(120deg,#0f172a,#1e3a8a 55%,#0e7490);color:#fff}
.wrap{max-width:1100px;margin:0 auto;padding:0 16px}
header h1{margin:0 0 6px;font-size:clamp(24px,4vw,36px)}
header p{margin:0;opacity:.85}
header nav a{color:#fff;background:#ffffff22;padding:5px 12px;border-radius:99px;margin:10px 8px 0 0;text-decoration:none;font-size:13.5px;display:inline-block}
header nav a.on{background:#fff;color:#0f172a;font-weight:700}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-top:-48px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;box-shadow:0 6px 20px rgba(0,0,0,.08)}
.stat b{display:block;font-size:26px}.stat span{color:var(--mut);font-size:13px}
.top{margin-top:-48px}
.bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:22px 0 8px}
.bar input[type=search],.bar input[type=number]{padding:9px 12px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--ink);font:inherit}
.bar input[type=search]{flex:1;min-width:200px}.bar input[type=number]{width:80px}
button{padding:9px 14px;border:0;border-radius:10px;background:var(--acc);color:#fff;font:inherit;cursor:pointer}
button.ghost{background:transparent;color:var(--acc);border:1px solid var(--acc)}
.prog{height:8px;border-radius:99px;background:var(--line);overflow:hidden;margin:6px 0 20px}
.prog i{display:block;height:100%;width:0;background:linear-gradient(90deg,#10b981,#22d3ee);transition:width .3s}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;margin:0 0 18px;overflow:hidden}
.card>h2{margin:0;padding:12px 16px;font-size:17px;color:#fff;background:var(--c,#475569);display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}
.card>*:not(h2){margin-left:16px;margin-right:16px}.card>h2+*{margin-top:12px}.card>*:last-child{margin-bottom:16px}
.card>h2 .cnt,.card>h2 label{color:#fff}.cnt{font-weight:400;font-size:13px;opacity:.92}
h3{font-size:1rem;margin:16px 0 6px}
.scroll{overflow-x:auto}
table{width:100%;border-collapse:collapse;min-width:640px;font-size:14px}
th,td{padding:8px 10px;text-align:left;border-top:1px solid var(--line);vertical-align:top}
th{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);border-top:0;white-space:nowrap}
td.num,td.n{text-align:right;white-space:nowrap}
tr.ok,tr.done{opacity:.5}tr.ok td,.step.ok span{text-decoration:line-through}
input.ck{width:18px;height:18px}
.mpn{display:block;font-family:ui-monospace,Consolas,monospace;font-size:13px}
.note{display:block;color:var(--mut);font-size:12.5px;margin-top:2px}.mut{color:var(--mut);font-size:13px}
a{color:var(--acc)}
.tag{display:inline-block;padding:1px 8px;border-radius:99px;font-size:11.5px;font-weight:600;background:#dcfce7;color:#166534}
.tag.LISTING{background:#fef3c7;color:#92400e}.tag.opt{background:#e2e8f0;color:#334155}.tag.VERIFIED{background:#dcfce7;color:#166534}
@media (prefers-color-scheme:dark){.tag{background:#14532d;color:#bbf7d0}.tag.LISTING{background:#78350f;color:#fde68a}.tag.opt{background:#334155;color:#e2e8f0}}
.warn{background:var(--card);border-left:5px solid #dc2626;border-radius:8px;padding:8px 12px;margin:16px 0;font-size:13px;border-top:1px solid var(--line);border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.rec{border-left:4px solid #10b981;padding:6px 12px;background:rgba(16,185,129,.1);border-radius:6px;margin:12px 0}
.chips{position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:5;display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:14px}
.chips a,.chip{padding:4px 10px;border-radius:14px;color:#fff;text-decoration:none;font-size:12px;font-weight:700}
.pbar{height:8px;background:var(--line);border-radius:5px;overflow:hidden;min-width:140px}.pbar div{height:100%;background:#10b981;width:0}
ul.rules li,ol.steps li{margin:5px 0}.step{display:flex;gap:10px;padding:6px 0;border-bottom:1px dashed var(--line)}
svg.plan,svg.dia{max-width:100%;height:auto}svg.dia text{fill:var(--ink);font-family:system-ui,Segoe UI,sans-serif}.ref{font-size:12px;font-weight:700}.role{font-size:10.5px;fill:var(--mut)!important}.lab{font-size:9.5px;fill:var(--mut)!important}
.pin{font-size:11px}.net{font-size:11px;font-weight:700}.flag{font-size:10px;font-weight:700;fill:#10151c!important}.pill{font-size:11px;font-weight:700;fill:#fff!important}
.bx{cursor:pointer}.bx.ok{opacity:.35}
.w{cursor:pointer;transition:opacity .15s}svg.hl .w{opacity:.15}svg.hl .w.on{opacity:1}.w.done line{stroke-dasharray:4 4}.pt{cursor:pointer}.pt.ok rect{fill-opacity:.1;stroke-dasharray:.6 .6}.pt.ok text{opacity:.4}
.legend{margin:12px 0}.legend span{display:inline-block;margin-right:12px;font-size:12px;color:var(--mut)}.legend i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:5px;vertical-align:middle}
footer{color:var(--mut);font-size:13px;padding:10px 0 40px}
@media print{header{background:#fff;color:#000}.bar,button,.chips{display:none}}"""


NAV = [("index.html", "Home"), ("bom.html", "BOM"), ("wiring-by-section.html", "Wiring"), ("schematic-sections.html", "Schematic"), ("pcb-floorplan.html", "PCB floorplan")]
HEAD_SUB = "USB-C AVR ISP programmer &middot; ATmega8A + USBasp firmware &middot; 1.8-5.5 V level shifting &middot; LCSC listings read 2026-11-13 &middot; Sheet N here = Sheet N on every page"


def head(title, sub, nav="", active="bom.html", stats=""):
    nv = "".join(f'<a class="{"on" if f == active else ""}" href="{f}">{n}</a>' for f, n in NAV)
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><style>{CSS}</style></head><body>'
            f'<header><div class="wrap"><h1>{e(title)}</h1><p>{sub}</p><nav>{nv}</nav></div></header><div class="wrap">' + stats +
            '<div class="warn"><b>Design stage.</b> Planned design, not a finished schematic or PCB and not built yet: nets come from tools/data.py, pin numbers of U1, U4, U5 were read from the datasheets, but every symbol and footprint must still be checked in EasyEDA.</div>' + nav)


def links():
    return ('<footer>Generated by <code>tools/gen_docs.py</code>. Prices are the first LCSC tier shown and change daily; stock is from the check date. '
            'Repo: <a href="https://github.com/ElectroIoT/SafeASP">github.com/ElectroIoT/SafeASP</a>. Hardware and docs: CC BY-SA 4.0.</footer>')


NETCOL = {"GND": "#8a93a3", "+5V": "#fb8c00", "VBUS": "#fb8c00", "+3V3": "#f4b400", "VTGT": "#0891b2", "VTGT_SUP": "#0891b2"}
RAILS = ("+5V", "VBUS", "+3V3", "VTGT")
D_RAILS = set(RAILS)


def ncol(n):
    if n in NETCOL: return NETCOL[n]
    if n.startswith(("USB_", "CC")): return "#8e24aa"
    if n.endswith("_M"): return "#00bcd4"
    if n.endswith("_T"): return "#16a34a"
    if n == "BUSY_N": return "#dc2626"
    return "#a66cff"


# ------------------------------------------------------------------ BOM files
def write_bom():
    rows = D.bom_rows()
    with open(os.path.join(ROOT, "hardware/bom/usbasp-v6-bom.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Refs", "Qty", "Function", "LCSC #", "MPN", "Manufacturer", "Stock", "Unit price USD", "Tier", "Status", "Line total USD"])
        for refs, q, name, c, mpn, mk, st, pr, tier, status, sub in rows:
            w.writerow([refs, q, name, c, mpn, mk, st, pr, tier, status, f"{sub:.4f}"])
    return rows


def bom_md():
    o = ["| Refs | Qty | Function | LCSC | MPN | Unit $ (tier) |", "|---|---|---|---|---|---|"]
    for refs, q, name, c, mpn, mk, st, pr, tier, status, sub in D.bom_rows():
        o.append(f"| {refs} | {q} | {name} | [{c}](https://www.lcsc.com/product-detail/{c}.html) | {mpn} | {pr:.4f} ({tier}) |")
    o.append(f"\n**{D.TOTAL_PIECES} pieces, about USD {D.totals():.2f} per board** (first LCSC price tier, PCB not included). Plus 2 jumper caps (2.54 mm) for JP1 and JP2.")
    return "\n".join(o)


# ------------------------------------------------------------------ wiring diagrams
def gnd_sym(x, y, c, right=True):
    s = 1 if right else -1
    return (f'<line x1="{x}" y1="{y}" x2="{x+12*s}" y2="{y}" stroke="{c}" stroke-width="2"/>'
            f'<line x1="{x+12*s}" y1="{y-7}" x2="{x+12*s}" y2="{y+7}" stroke="{c}" stroke-width="2"/>'
            f'<line x1="{x+16*s}" y1="{y-4}" x2="{x+16*s}" y2="{y+4}" stroke="{c}" stroke-width="2"/>'
            f'<line x1="{x+20*s}" y1="{y-2}" x2="{x+20*s}" y2="{y+2}" stroke="{c}" stroke-width="2"/>')


def section_svg(sid):
    parts = [p for p in D.PARTS if p[1] == sid]
    PXR = 300
    y = 16
    boxes, pinpos = [], []
    for ref, s, name, c, q, pins in parts:
        pl = D.pins_of(ref)
        h = 34 + 16 * len(pl)
        boxes.append((ref, name, c, pl, y, h))
        for k, (pin, net) in enumerate(pl):
            pinpos.append((ref, pin, net, y + 40 + 16 * k))
        y += h + 14
    lanes = []
    for ref, pin, net, py in pinpos:
        if net and net not in D_RAILS and net != "GND" and net not in lanes:
            lanes.append(net)
    lx = {n: 520 + 24 * i for i, n in enumerate(lanes)}
    Wd, Ht = 520 + 24 * len(lanes) + 30, y + 20
    o = [f'<svg viewBox="0 0 {Wd} {Ht}" width="{Wd}" height="{Ht}" class="dia" data-sec="{sid}">']
    for ref, name, c, pl, by, bh in boxes:
        o.append(f'<g class="bx" data-ref="{ref}"><rect x="8" y="{by}" width="{PXR-8}" height="{bh}" rx="7" fill="var(--card)" stroke="var(--line)" stroke-width="2"/>'
                 f'<text x="16" y="{by+14}" class="ref">{e(ref)}</text><text x="{16+8*len(ref)+8}" y="{by+14}" class="role">{e(name[:44])}</text><text x="16" y="{by+27}" class="lab">[{c}]</text></g>')
    for ref, pin, net, py in pinpos:
        o.append(f'<text x="{PXR-14}" y="{py+3.5}" text-anchor="end" class="pin">{e(pin)}</text>')
        if not net:
            o.append(f'<g class="w"><line x1="{PXR}" y1="{py}" x2="{PXR+10}" y2="{py}" stroke="#9aa5b5" stroke-width="2"/><line x1="{PXR+10}" y1="{py-4}" x2="{PXR+16}" y2="{py+4}" stroke="#9aa5b5" stroke-width="2"/><line x1="{PXR+16}" y1="{py-4}" x2="{PXR+10}" y2="{py+4}" stroke="#9aa5b5" stroke-width="2"/><text x="{PXR+22}" y="{py+3.5}" class="lab">no connect</text></g>')
            continue
        c = ncol(net)
        if net == "GND":
            o.append(f'<g class="w" data-net="GND">{gnd_sym(PXR, py, c)}<text x="{PXR+28}" y="{py+3.5}" class="net" fill="{c}">GND</text></g>')
        elif net in D_RAILS:
            wd = 7 * len(net) + 10
            o.append(f'<g class="w" data-net="{e(net)}"><line x1="{PXR}" y1="{py}" x2="{PXR+14}" y2="{py}" stroke="{c}" stroke-width="3"/><rect x="{PXR+14}" y="{py-8}" width="{wd}" height="16" rx="4" fill="{c}"/><text x="{PXR+19}" y="{py+3.5}" class="flag">{e(net)}</text></g>')
        else:
            x2 = lx[net]
            pw = 6.6 * len(net) + 14
            o.append(f'<g class="w" data-net="{e(net)}"><line x1="{PXR}" y1="{py}" x2="{x2}" y2="{py}" stroke="{c}" stroke-width="2"/><circle cx="{PXR}" cy="{py}" r="3" fill="{c}"/><circle cx="{x2}" cy="{py}" r="2.6" fill="{c}"/><rect x="{PXR+14}" y="{py-9}" width="{pw:.0f}" height="18" rx="9" fill="{c}"/><text x="{PXR+22}" y="{py+4}" class="pill">{e(net)}</text></g>')
    for net in lanes:
        ys = [py for _, _, n, py in pinpos if n == net]
        if len(ys) > 1:
            o.append(f'<g class="w" data-net="{e(net)}"><line x1="{lx[net]}" y1="{min(ys)}" x2="{lx[net]}" y2="{max(ys)}" stroke="{ncol(net)}" stroke-width="2"/></g>')
    o.append("</svg>")
    return "".join(o)


def tagcls(status):
    return "VERIFIED" if status.startswith("VERIFIED") else "LISTING"


def sheet_color(secs):
    return D.SEC[secs[0]][2]


def page_bom():
    tot = D.totals()
    stats = ('<div class="stats top">'
             f'<div class="stat"><b>{D.TOTAL_PIECES}</b><span>parts per board</span></div>'
             f'<div class="stat"><b>{len(D.PAGES)}</b><span>schematic sheets</span></div>'
             f'<div class="stat"><b id="cost">${tot:.2f}</b><span>parts cost, 1st price tier</span></div>'
             '<div class="stat"><b id="ticked">0%</b><span>ticked off</span></div></div>')
    o = [head("SafeASP - Bill of materials", HEAD_SUB, "", "bom.html", stats)]
    o.append('<div class="bar"><input type="search" id="q" placeholder="Search ref, MPN, C-number, function..."><label>Boards <input type="number" id="boards" min="1" value="1"></label>'
             '<button id="copy">Copy all C-numbers</button><button class="ghost" id="reset">Clear ticks</button></div><div class="prog"><i id="pbar"></i></div>')
    o.append('<div class="rec"><b>Whole board about USD %.2f</b> (%d pieces). PCB, 2 jumper caps (2.54 mm, for JP1 and JP2) and the ISP ribbon cable are not included. '
             'U4 (74LVC8T245PW) is only in other-supplier stock at LCSC (3-5 day lead time); the TI SN74LVC8T245PWR (C27643) has the same pinout.</div>' % (tot, D.TOTAL_PIECES))
    for n, (pid, ptitle, secs) in enumerate(D.PAGES, 1):
        parts = [p for p in D.PARTS if p[1] in secs]
        cost = sum(p[4] * D.INFO[p[3]][3] for p in parts)
        o.append(f'<section class="card" id="{pid}" style="--c:{sheet_color(secs)}"><h2>{e(ptitle)}<span class="cnt">{len(parts)} lines, {sum(p[4] for p in parts)} pieces, about ${cost:.2f}</span></h2>')
        o.append('<div class="scroll"><table><thead><tr><th></th><th>Ref</th><th>Function</th><th>Part</th><th>LCSC #</th><th>Qty</th><th>Stock</th><th>$ each</th></tr></thead><tbody>')
        for sid in secs:
            o.append(f'<tr><td colspan="8" style="background:{D.SEC[sid][2]}22"><b>{e(D.SEC[sid][1])}</b></td></tr>')
            for ref, s, name, c, q, pins in D.PARTS:
                if s != sid:
                    continue
                mpn, mk, st, pr, tier, status = D.INFO[c]
                o.append(f'<tr data-ref="{ref}" data-sub="{q*pr:.4f}" data-c="{c}" data-q="{q}"><td><input type="checkbox" class="ck" data-k="{ref}"></td><td class="ref"><b>{ref}</b></td>'
                         f'<td class="f">{e(name)}</td><td><span class="mpn">{e(mpn)}</span><span class="note">{e(mk)}</span><span class="tag {tagcls(status)}">{e(status.split(";")[0].split(" ")[0])}</span><span class="note">{e(status)}</span></td>'
                         f'<td><a href="https://www.lcsc.com/product-detail/{c}.html" target="_blank" rel="noopener">{c}</a></td><td class="n">{q}</td><td class="n">{st}</td><td class="n">{pr:.4f} <span class="note">{tier}</span></td></tr>')
        o.append("</tbody></table></div></section>")
    o.append(links() + """<script>
const K='usbasp6-bom-ticks';let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
const rows=[...document.querySelectorAll('tr[data-ref]')],cks=[...document.querySelectorAll('.ck')];
function money(){const b=Math.max(1,+document.getElementById('boards').value||1);let s=0;rows.forEach(r=>{s+=+r.dataset.sub});document.getElementById('cost').textContent='$'+(s*b).toFixed(2)}
function upd(){const n=cks.filter(c=>c.checked).length;document.getElementById('ticked').textContent=Math.round(100*n/cks.length)+'%';document.getElementById('pbar').style.width=(100*n/cks.length)+'%';
 rows.forEach(r=>r.classList.toggle('done',r.querySelector('.ck').checked));try{localStorage.setItem(K,JSON.stringify(Object.fromEntries(cks.filter(c=>c.checked).map(c=>[c.dataset.k,1]))))}catch(e){}}
cks.forEach(c=>{c.checked=!!st[c.dataset.k];c.addEventListener('change',upd)});
document.getElementById('reset').onclick=()=>{cks.forEach(c=>c.checked=false);upd()};
document.getElementById('boards').oninput=money;
document.getElementById('q').oninput=ev=>{const v=ev.target.value.toLowerCase();rows.forEach(r=>r.style.display=r.innerText.toLowerCase().includes(v)?'':'none')};
document.getElementById('copy').onclick=()=>{const b=Math.max(1,+document.getElementById('boards').value||1),m={};
 rows.forEach(r=>{m[r.dataset.c]=(m[r.dataset.c]||0)+(+r.dataset.q)*b});
 const t=Object.entries(m).map(([c,q])=>c+','+q).join('\\n');const btn=document.getElementById('copy');
 (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>{btn.textContent='Copied '+Object.keys(m).length+' lines (C#,qty)'},()=>{prompt('Copy:',t)})};
upd();money();
</script></div></body></html>""")
    return "".join(o)


EXTERNAL = [
 ("USB-C (J1)", "Any USB-C cable to a PC: USB-C to USB-C works too, because CC1 and CC2 each have their own 5.1 k pull-down. The board draws about 20 mA plus the target."),
 ("10-pin ISP (J2)", "Standard AVR 10-pin ribbon: 1 MOSI, 2 VCC, 3 NC, 4/6/8/10 GND, 5 RST, 7 SCK, 9 MISO. The box header key stops a reversed plug."),
 ("6-pin ISP (J3)", "Standard AVR 6-pin (Arduino ICSP): 1 MISO, 2 VCC, 3 SCK, 4 MOSI, 5 RST, 6 GND. Use J2 OR J3, not both at once."),
 ("Target supply (JP1)", "Jumper 1-2 = we send 5 V, 2-3 = we send 3.3 V, none = the target has its own supply. The level shifter always follows the voltage on ISP pin 2, so the target pin 2 MUST have power (ours or its own) or the outputs stay off."),
 ("Never", "Never fit JP1 when the target has its own supply (two supplies fighting). Never feed more than 5.5 V on ISP pin 2."),
 ("Slow SCK (JP2)", "Fit for a target running below 1.5 MHz (for example a new ATmega with CKDIV8 on 1 MHz internal clock), or use avrdude -B 32."),
 ("Self-programming (J4)", "Only to flash the ATmega8A of this board with another programmer. Unplug USB-C first; the other programmer supplies 5 V on pin 2."),
]


def page_wiring():
    o = [head("SafeASP - Wiring by section", HEAD_SUB.replace("LCSC listings read 2026-11-13 &middot; ", ""), "", "wiring-by-section.html")]
    o.append('<p class="legend"><span><i style="background:#fb8c00"></i>5 V / VBUS</span><span><i style="background:#f4b400"></i>3.3 V</span><span><i style="background:#0891b2"></i>target supply (VTGT)</span><span><i style="background:#8a93a3"></i>GND</span><span><i style="background:#8e24aa"></i>USB</span><span><i style="background:#00bcd4"></i>ISP, 5 V side (_M)</span><span><i style="background:#16a34a"></i>ISP, target side (_T)</span><span><i style="background:#dc2626"></i>BUSY_N / OE#</span><span><i style="background:#a66cff"></i>MCU control</span></p>')
    o.append('<section class="card" style="--c:#1e3a8a"><h2>System wiring (connection map)</h2>' + map_body() + '</section>')
    o.append('<section class="card" style="--c:#dc2626"><h2>External wiring (what you connect by hand)</h2><div class="scroll"><table><thead><tr><th>Connection</th><th>How</th></tr></thead><tbody>'
             + "".join(f"<tr><td><b>{a}</b></td><td>{b}</td></tr>" for a, b in EXTERNAL) + '</tbody></table></div></section>')
    o.append('<div class="bar"><progress id="pg" value="0" max="1" style="width:240px"></progress><span id="pt" class="mut"></span><button class="ghost" id="rs">Clear ticks</button></div><p class="mut">Pin-to-net per section: each box is a part; the flag on a pin is the net name, put the same net label in EasyEDA and the pins join. Hover a wire to highlight its net, click to mark it wired (saved in this browser).</p>')
    for n, (pid, ptitle, secs) in enumerate(D.PAGES, 1):
        o.append(f'<section class="card" id="{pid}" style="--c:{sheet_color(secs)}"><h2>{e(ptitle)}</h2>')
        for sid in secs:
            _, title, col, desc = D.SEC[sid]
            o.append(f'<div data-sec="{sid}" class="sec"><h3 style="color:{col}">{e(title)} <span class="mut secprog"></span></h3><p class="mut">{e(desc)}</p><div class="scroll">{section_svg(sid)}</div></div>')
        o.append("</section>")
    o.append(links() + """<script>
const K='usbasp6-wiring-ticks';let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
const svgs=[...document.querySelectorAll('svg.dia')];
function nets(svg){return [...new Set([...svg.querySelectorAll('.w[data-net]')].map(w=>w.dataset.net))]}
function apply(){let done=0,total=0;svgs.forEach(svg=>{const sid=svg.dataset.sec,ns=nets(svg);let d=0;
 svg.querySelectorAll('.w[data-net]').forEach(w=>w.classList.toggle('done',!!st[sid+'|'+w.dataset.net]));ns.forEach(n=>{if(st[sid+'|'+n])d++});
 svg.closest('.sec').querySelector('.secprog').textContent=d+' / '+ns.length+' nets wired';done+=d;total+=ns.length});
 document.getElementById('pg').max=total;document.getElementById('pg').value=done;document.getElementById('pt').textContent=done+' / '+total+' nets wired';try{localStorage.setItem(K,JSON.stringify(st))}catch(e){}}
svgs.forEach(svg=>{const sid=svg.dataset.sec;svg.querySelectorAll('.w[data-net]').forEach(w=>{
 w.addEventListener('mouseenter',()=>{svg.classList.add('hl');svg.querySelectorAll('.w[data-net="'+w.dataset.net+'"]').forEach(x=>x.classList.add('on'))});
 w.addEventListener('mouseleave',()=>{svg.classList.remove('hl');svg.querySelectorAll('.w.on').forEach(x=>x.classList.remove('on'))});
 w.addEventListener('click',()=>{const k=sid+'|'+w.dataset.net;if(st[k])delete st[k];else st[k]=1;apply()})})});
document.getElementById('rs').onclick=()=>{if(confirm('Clear all net ticks?')){st={};apply()}};apply();
</script></div></body></html>""")
    return "".join(o)


# ------------------------------------------------------------------ connection map
def box(x, y, w, h, col, title, lines, dash=False):
    d = ' stroke-dasharray="7 5"' if dash else ""
    s = f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{col}" fill-opacity=".09" stroke="{col}" stroke-width="2"{d}/><rect x="{x}" y="{y}" width="{w}" height="26" rx="12" fill="{col}" fill-opacity=".9"/><text x="{x+12}" y="{y+18}" font-size="13" font-weight="700" fill="#fff">{e(title)}</text>'
    for i, l in enumerate(lines):
        s += f'<text x="{x+12}" y="{y+46+i*17}" font-size="12" fill="currentColor">{e(l)}</text>'
    return s + "</g>"


def arrow(pts, col, label="", lx=None, ly=None):
    d = " ".join(("M" if i == 0 else "L") + f"{a},{b}" for i, (a, b) in enumerate(pts))
    mid = pts[len(pts) // 2]
    s = f'<path d="{d}" fill="none" stroke="{col}" stroke-width="3" marker-end="url(#ah{col[1:]})"/>'
    if label:
        s += f'<text x="{lx if lx is not None else mid[0]+6}" y="{ly if ly is not None else mid[1]-6}" font-size="11" font-weight="700" fill="{col}">{e(label)}</text>'
    return s


def map_body():
    cols = ["#fb8c00", "#f4b400", "#8e24aa", "#00bcd4", "#16a34a", "#0891b2", "#dc2626"]
    s = ['<svg viewBox="0 0 1240 560" width="1240" class="dia" style="color:var(--fg)"><defs>']
    for c in cols:
        s.append(f'<marker id="ah{c[1:]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
    s.append("</defs>")
    s.append(box(20, 20, 270, 150, "#4895ef", "USB-C (J1)", ["R1 / R2 5.1 k on CC1 / CC2", "U2 USBLC6 ESD on D+ / D-", "F1 PTC 500 mA -> +5V", "C1 10 uF, C2 100 nF"]))
    s.append(box(20, 210, 270, 150, "#8e24aa", "V-USB INTERFACE", ["R3 / R4 68 R series", "D1 / D2 3.6 V zener clamps", "R5 2.2 k D- pull-up", "low-speed USB 1.1"]))
    s.append(box(350, 20, 300, 340, "#a66cff", "ATMEGA8A + USBasp FIRMWARE", ["U1 ATmega8A-AU, 5 V, Y1 12 MHz", "PB0 = D-, PB1 + PD2/INT0 = D+", "PB3 MOSI, PB4 MISO, PB5 SCK", "PB2 = target RST", "PC1 = red LED + BUSY_N (OE#)", "PC0 = green LED (USB ready)", "PC2 = JP2 slow SCK", "J4 = flash this chip", "firmware: USBasp 2011-05-28,", "unchanged (same pins)"]))
    s.append(box(710, 20, 300, 230, "#00bcd4", "LEVEL SHIFTER", ["U4 74LVC8T245: MOSI, SCK, RST out", "  A side 5 V, B side = VTGT", "  OE# = BUSY_N: Hi-Z when idle", "U5 74LVC1T45: MISO in (B to A)", "R10 OE# pull-up, R11-13 pull-downs", "works for 1.8 to 5.5 V targets"]))
    s.append(box(710, 290, 300, 180, "#ff9f43", "TARGET POWER", ["U3 AP2112K 3.3 V LDO", "JP1: 5 V / 3.3 V / off", "F2 PTC 200 mA -> VTGT", "LED3 yellow = we power the target"]))
    s.append(box(1060, 20, 160, 450, "#2fbf71", "ISP OUT", ["J2 10-pin box", "J3 6-pin", "", "MOSI_T", "SCK_T", "RST_T", "MISO_T", "VTGT (pin 2)", "GND"]))
    s.append(arrow([(155, 170), (155, 210)], cols[2], "D+ D-", lx=162, ly=196))
    s.append(arrow([(290, 285), (350, 285)], cols[2], "USB_DP/DN", lx=292, ly=278))
    s.append(arrow([(290, 60), (350, 60)], cols[0], "+5V", lx=300, ly=52))
    s.append(arrow([(650, 120), (710, 120)], cols[3], "_M nets", lx=654, ly=112))
    s.append(arrow([(650, 200), (710, 200)], cols[6], "BUSY_N", lx=654, ly=192))
    s.append(arrow([(1010, 120), (1060, 120)], cols[4], "_T nets", lx=1012, ly=112))
    s.append(arrow([(1010, 380), (1060, 380)], cols[5], "VTGT", lx=1016, ly=372))
    s.append(arrow([(860, 290), (860, 250)], cols[5], "VTGT", lx=866, ly=276))
    s.append(arrow([(500, 360), (500, 400), (710, 400)], cols[0], "+5V", lx=600, ly=394))
    s.append("</svg>")
    io = [("PB0 (12)", "USB_DN", "D- via R4, D2; R5 pull-up"), ("PB1 (13), PD2/INT0 (32)", "USB_DP", "D+ via R3, D1"), ("PB2 (14)", "RST_M", "U4 A3 -> RST_T"), ("PB3 (15)", "MOSI_M", "U4 A1 -> MOSI_T; J4 pin 4"),
          ("PB4 (16)", "MISO_M", "U5 A <- MISO_T; J4 pin 1"), ("PB5 (17)", "SCK_M", "U4 A2 -> SCK_T; J4 pin 3"), ("PC0 (23)", "LED_G_K", "LED2 green (low = on)"), ("PC1 (24)", "BUSY_N", "LED1 red + U4 OE# (low while programming)"),
          ("PC2 (25)", "SLOW_SCK", "JP2 to GND"), ("PC6 RESET (29)", "MCU_RST", "R6 10 k, J4 pin 5"), ("PB6 / PB7 (7 / 8)", "XTAL1 / XTAL2", "Y1 12 MHz, C3 / C4 22 pF")]
    tab = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in io)
    return (f'<div class="scroll" style="background:var(--card);border-radius:12px;padding:8px">{"".join(s)}</div>'
            f'<h3>Pin assignment (ATmega8A, TQFP-32 pin numbers)</h3><div class="scroll"><table><thead><tr><th>Pin</th><th>Net</th><th>Goes to</th></tr></thead><tbody>{tab}</tbody></table></div>'
            '<p class="mut">These are exactly the pins the USBasp 2011-05-28 firmware uses (usbasp.h: red LED PC1, green PC0; isp.h: RST PB2, MOSI PB3, MISO PB4, SCK PB5; usbconfig.h: D- PB0, D+ PB1; main.c: slow SCK on PC2 with pull-up). No firmware change is needed.</p>')


# ------------------------------------------------------------------ schematic guide
PAGE_STEPS = {
 "p1": [
  ("J1 USB-C (C165948): VBUS pins (A4B9, B4A9) to <b>VBUS</b>, GND pins and the 4 shell tabs to GND, A5 CC1 to R1 5.1 k to GND, B5 CC2 to R2 5.1 k to GND (two separate resistors!), SBU1 / SBU2 No-Connect.", "usb"),
  ("D+ pins A6 and B6 joined = <b>USB_DP_J</b>, D- pins A7 and B7 joined = <b>USB_DN_J</b>. U2 USBLC6: pins 1 and 6 to USB_DP_J, pins 3 and 4 to USB_DN_J, pin 5 VBUS, pin 2 GND. C2 100 nF on VBUS.", "usb"),
  ("F1 PTC 500 mA from VBUS to <b>+5V</b>. C1 10 uF on +5V.", "usb"),
  ("R3 68 R from USB_DP_J to <b>USB_DP</b>, R4 68 R from USB_DN_J to <b>USB_DN</b>. D1 zener: cathode USB_DP, anode GND. D2 zener: cathode USB_DN, anode GND. R5 2.2 k from +5V to USB_DN.", "vusb"),
  ("U3 AP2112K: pin 1 VIN and pin 3 EN to +5V, pin 2 GND, pin 5 VOUT to <b>+3V3</b>, pin 4 No-Connect. C8 10 uF on +5V, C9 10 uF on +3V3.", "tpwr"),
  ("JP1 1x3: pin 1 +5V, pin 2 <b>VTGT_SUP</b>, pin 3 +3V3. F2 PTC 200 mA from VTGT_SUP to <b>VTGT</b>. R9 1 k from VTGT_SUP to LED3 (yellow) anode, cathode to GND.", "tpwr"),
 ],
 "p2": [
  ("Place U1 ATmega8A-AU (C16190). Pins 4, 6 and 18 (AVCC) to +5V, pins 3, 5, 21 to GND. C5, C6, C7 100 nF, one next to each supply pin.", "mcu"),
  ("Crystal: pin 7 <b>XTAL1</b>, pin 8 <b>XTAL2</b> to Y1 pads 1 and 3; Y1 pads 2 and 4 to GND; C3 22 pF XTAL1-GND, C4 22 pF XTAL2-GND.", "mcu"),
  ("Pin 29 RESET = <b>MCU_RST</b> with R6 10 k to +5V.", "mcu"),
  ("USB: pin 12 PB0 = <b>USB_DN</b>; pin 13 PB1 AND pin 32 PD2 = <b>USB_DP</b> (both pins on the same net).", "mcu"),
  ("ISP (5 V side): pin 14 PB2 = <b>RST_M</b>, pin 15 PB3 = <b>MOSI_M</b>, pin 16 PB4 = <b>MISO_M</b>, pin 17 PB5 = <b>SCK_M</b>.", "mcu"),
  ("LEDs: R7 1 k from +5V to LED1 (red) anode, LED1 cathode to pin 24 PC1 = <b>BUSY_N</b>. R8 1 k from +5V to LED2 (green) anode, cathode to pin 23 PC0 = <b>LED_G_K</b>.", "mcu"),
  ("JP2 1x2: pin 1 to pin 25 PC2 = <b>SLOW_SCK</b>, pin 2 GND. J4 2x3: 1 MISO_M, 2 +5V, 3 SCK_M, 4 MOSI_M, 5 MCU_RST, 6 GND.", "mcu"),
  ("No-Connect flags on pins 1, 2, 9, 10, 11, 19, 20, 22, 26, 27, 28, 30, 31.", "mcu"),
 ],
 "p3": [
  ("U4 74LVC8T245PW (C458788): pin 1 VCCA and pin 2 DIR to +5V (DIR high = A to B). Pins 23 and 24 VCCB to <b>VTGT</b>. Pins 11, 12, 13 GND.", "shift"),
  ("U4 A side: pin 3 A1 = MOSI_M, pin 4 A2 = SCK_M, pin 5 A3 = RST_M, pins 6-10 (A4-A8) to GND. B side: pin 21 B1 = <b>MOSI_T</b>, pin 20 B2 = <b>SCK_T</b>, pin 19 B3 = <b>RST_T</b>, pins 14-18 No-Connect.", "shift"),
  ("U4 pin 22 OE# = <b>BUSY_N</b> (the red-LED line) with R10 10 k to +5V.", "shift"),
  ("U5 74LVC1T45GW (C478004): pin 1 VCCA +5V, pin 2 GND, pin 3 A = MISO_M, pin 4 B = <b>MISO_T</b>, pin 5 DIR to GND (B to A), pin 6 VCCB = VTGT.", "shift"),
  ("C10 / C12 100 nF on +5V at U4 / U5, C11 / C13 100 nF on VTGT at U4 / U5. R11, R12, R13 100 k from MOSI_M, SCK_M, RST_M to GND.", "shift"),
  ("J2 2x5 box header: 1 MOSI_T, 2 VTGT, 3 No-Connect, 4/6/8/10 GND, 5 RST_T, 7 SCK_T, 9 MISO_T. J3 2x3: 1 MISO_T, 2 VTGT, 3 SCK_T, 4 MOSI_T, 5 RST_T, 6 GND.", "isp"),
 ],
}
PAGE_NOTES = {
 "p1": ["Nets leaving this page: +5V, +3V3, VTGT, GND, USB_DP, USB_DN.", "Zener orientation: the bar (cathode) on the data line. The USB-C shell must go to GND."],
 "p2": ["Every _M net here appears again on sheet 3 (U4 / U5). BUSY_N is used three times: PC1, LED1 cathode, U4 OE# (+ R10).", "Pin numbers are TQFP-32 numbers, not the DIP-28 numbers of the old v4 / v5 boards."],
 "p3": ["Target-side nets end in _T. VTGT is both the target supply (when JP1 is fitted) and the level-shifter supply: no voltage on ISP pin 2 = outputs off.", "Both VCC pins of U4 (23, 24) must be connected."],
}
SETUP = ["Open EasyEDA Pro (web), new project SafeASP (USBasp V6) with one schematic and one PCB.", "Make 3 schematic sheets named as above (1_USB_POWER, 2_MCU, 3_SHIFT_ISP).",
         "Place parts by searching the LCSC number (C#) in the library search; set the Designator to the Ref in the table.", "Use net labels for every connection that leaves a page; use the same name on both pages. Names are case-sensitive.",
         "Run the schematic check after each page and fix every warning."]
FINAL = ["Every net label is used at least twice. One GND, one +5V, one +3V3, one VTGT.", "Compare the part count with the BOM page (%d pieces)." % D.TOTAL_PIECES,
         "Compare every footprint with its datasheet before the layout: C165948 USB-C, TQFP-32 (0.8 mm pitch), TSSOP-24, SC-88, 3225 crystal, box header key position.",
         "Check USB_DP is on BOTH U1 pin 13 and pin 32.", "Export the schematic PDF and send it for a check."]


def sheet_parts_table(secs):
    groups, order = {}, []
    for ref, s, name, c, q, pins in D.PARTS:
        if s in secs:
            if c not in groups:
                groups[c] = [[], 0, name]
                order.append(c)
            groups[c][0].append(ref)
            groups[c][1] += q
    body = ""
    for c in order:
        refs, q, name = groups[c]
        mpn = D.INFO[c][0]
        fn = name if len(refs) == 1 else " / ".join(dict.fromkeys(D.BYREF[r][2].split(",")[0] for r in refs))
        body += (f'<tr><td><b>{e(", ".join(refs))}</b></td><td class="n">{q}</td><td>{e(fn)}</td><td><span class="mpn">{e(mpn)}</span></td>'
                 f'<td><a href="https://www.lcsc.com/product-detail/{c}.html" target="_blank" rel="noopener">{c}</a></td></tr>')
    return f'<div class="scroll"><table><thead><tr><th>Ref</th><th>Qty</th><th>Function</th><th>Part</th><th>LCSC</th></tr></thead><tbody>{body}</tbody></table></div>'


def page_schem():
    total = sum(len(v) for v in PAGE_STEPS.values()) + len(SETUP) + len(FINAL)
    o = [head("SafeASP - Schematic by section", "Three sheets, simplified symbols, with the parts of each sheet; the same Sheet 1, 2, 3 as on the BOM and Wiring pages. Draw the real schematic in EasyEDA.",
              "", "schematic-sections.html")]
    o.append('<p class="mut">Jump to: <a href="#u1pins">U1 ATmega8A pin guide</a> &middot; <a href="#u4pins">U4 / U5 level-shifter pins</a> &middot; <a href="#j1pins">J1 USB-C pins</a></p><div class="warn"><b>Planning drawing.</b> Symbols are simplified: draw the real schematic in EasyEDA from this page and the Wiring page. Check all pin numbers in the EasyEDA symbols.</div>')
    o.append(f'<div class="bar"><progress id="pg" value="0" max="{total}" style="width:240px"></progress><span id="pt" class="mut"></span><button class="ghost" id="rs">Clear ticks</button></div>')
    o.append('<section class="card" id="setup" style="--c:#475569"><h2>Setup in EasyEDA</h2>' + "".join(f'<div class="step"><input type="checkbox" class="ck" data-k="setup{i}"><span><b>{i}.</b> {e(s)}</span></div>' for i, s in enumerate(SETUP, 1)) + "</section>")
    for n, (pid, ptitle, secs) in enumerate(D.PAGES, 1):
        col = D.SEC[secs[0]][2]
        o.append(f'<section class="card" id="{pid}" style="--c:{col}"><h2>{e(ptitle)}</h2><div class="scroll">{SH.SHEETS[pid]()}</div>')
        for tx in PAGE_NOTES[pid]:
            o.append(f'<p class="mut">{e(tx)}</p>')
        o.append('<h3>Parts of this sheet</h3>' + sheet_parts_table(secs))
        o.append('<details open><summary><b>Build steps</b> (tick as you draw this sheet)</summary>')
        for i, (txt, sec) in enumerate(PAGE_STEPS[pid], 1):
            o.append(f'<div class="step"><input type="checkbox" class="ck" data-k="{pid}-s{i}"><span><b>{i}.</b> {txt}</span></div>')
        o.append("</details></section>")
    o.append('<section class="card" id="u1pins" style="--c:#7c3aed"><h2>Pin guide: U1 ATmega8A-AU (TQFP-32, all 32 pins)</h2>'
             '<p class="mut">Top view as the footprint sits on the PCB: dot = pin 1 corner, pins 1-8 down the left, 9-16 along the bottom, 17-24 up the right, 25-32 along the top. Pin names and numbers from the Microchip ATmega8A datasheet, figure 1-1. '
             '<b style="color:#dc2626">Red X = place a No-Connect flag.</b></p><div class="scroll">' + PG.u1_svg() + '</div><h3>What to do on each pin</h3>' + PG.u1_table() + '</section>')
    o.append('<section class="card" id="u4pins" style="--c:#00bcd4"><h2>Pin guide: U4 74LVC8T245PW and U5 74LVC1T45GW</h2>'
             '<p class="mut">From the Nexperia datasheets (pin description and function tables): U4 DIR high = A to B, OE# high = all outputs Hi-Z; U5 DIR low = B to A. If either supply is 0 V, both parts go to suspend mode (all pins Hi-Z).</p>'
             '<h3>U4</h3>' + PG.pin_table("U4") + '<h3>U5</h3>' + PG.pin_table("U5") + '</section>')
    o.append('<section class="card" id="j1pins" style="--c:#4895ef"><h2>Pin guide: J1 USB-C (TYPE-C-31-M-12)</h2>' + PG.pin_table("J1") + '</section>')
    o.append('<section class="card" id="final" style="--c:#10b981"><h2>Final checks</h2>' + "".join(f'<div class="step"><input type="checkbox" class="ck" data-k="final{i}"><span><b>{i}.</b> {e(s)}</span></div>' for i, s in enumerate(FINAL, 1)) + "</section>")
    o.append(links() + """<script>
const K='usbasp6-schem-ticks';let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
const cks=[...document.querySelectorAll('.ck')];
function upd(){const n=cks.filter(c=>c.checked).length;document.getElementById('pg').value=n;document.getElementById('pt').textContent=n+' / '+cks.length+' done';cks.forEach(c=>{const r=c.closest('.step');if(r)r.classList.toggle('ok',c.checked)});try{localStorage.setItem(K,JSON.stringify(Object.fromEntries(cks.filter(c=>c.checked).map(c=>[c.dataset.k,1]))))}catch(e){}}
cks.forEach(c=>{c.checked=!!st[c.dataset.k];c.addEventListener('change',upd)});document.getElementById('rs').onclick=()=>{cks.forEach(c=>c.checked=false);upd()};upd();
</script></div></body></html>""")
    return "".join(o)


# ------------------------------------------------------------------ PCB guide
BW, BH = PL.BOARD_W, PL.BOARD_H
BLK = {b[0]: b for b in PL.BLOCKS}
REF_NAME = {p[0]: p[2] for p in D.PARTS}
REF_C = {p[0]: p[3] for p in D.PARTS}
BLOCK_NOTES = {
 "usb": ["J1 USB-C on the left edge, opening flush with the board edge, shell tabs to GND. R1 / R2 right at the CC pins.", "D+ / D- as a short pair from J1 through U2 to R3 / R4; no vias if possible."],
 "vusb": ["R3, R4 and the zeners D1, D2 in a straight line between U2 and U1 pins 12 / 13 / 32. R5 pull-up next to R4.", "C1 10 uF bulk on +5V right after F1."],
 "mcu": ["U1 in the middle; Y1 and C3 / C4 as close as possible to pins 7 / 8, short loop to GND.", "C5, C6, C7 next to pins 4, 6, 18. LEDs on the top edge so they are visible; J4 and JP2 on the bottom edge."],
 "shift": ["U4 between the MCU and the headers: A side (pins 1-12) faces U1, B side (13-24) faces J2 / J3. C10 at pin 1, C11 at pins 23 / 24.", "U5 and C12 / C13 next to the MISO lines; R10-R13 in the free column."],
 "tpwr": ["U3 with C8 / C9 close by; JP1 easy to reach with silkscreen 5V | OUT | 3V3; LED3 visible from the top.", "F2 between JP1 pin 2 and the VTGT net."],
 "isp": ["J2 box header on the right edge with the key facing outwards (cable leaves to the right); J3 6-pin beside it.", "Silkscreen pin 1 on both headers and the pin names MISO / SCK / RST / MOSI / VCC / GND."],
}
NETS = [("+5V, VBUS", "0.5 mm", "Board + target up to about 0.25 A."), ("VTGT, VTGT_SUP, +3V3", "0.4 mm", "Target supply up to 200 mA (F2)."),
        ("GND", "pour on both layers", "Stitching vias around the USB pair and the crystal."), ("USB_DP / USB_DN (and _J)", "0.25 mm pair", "Low-speed USB: short and together, no stubs."),
        ("XTAL1 / XTAL2", "0.25 mm", "As short as possible, GND pour around, nothing else under Y1."), ("_M, _T, BUSY_N, others", "0.25 mm", "Plain signals; keep SCK_T away from MISO_T on the way to the headers.")]
STEPS = [f"In EasyEDA PCB draw the outline {BW:.0f} x {BH:.0f} mm, 2 mm corners, two 3.2 mm non-plated holes at " + ", ".join(f"({x:g},{y:g})" for x, y in PL.HOLES) + " mm.",
         "Import the schematic (Design > Update/Convert Schematic to PCB). Check every footprint against its datasheet first.", "Place block by block with the X / Y tables, ticking each part here.",
         "Draw one rectangle per block on the Top Silkscreen layer with its title (the dashed boxes).", "Route the USB pair and the crystal first, then power, then the ISP lines. Pour GND on both layers.",
         "Run DRC. Add silkscreen: SafeASP, JP1 5V | 3V3, JP2 SLOW, J4 SELF-PROG, LED names (BUSY, USB, TGT PWR), ISP pin names.", "Export Gerber, BOM and pick-and-place."]


def rect_of(v):
    x, y, w, h, r = v
    if r in (90, 270):
        w, h = h, w
    return x, y, w, h


def part_svg(ref, dim=False):
    x, y, w, h = rect_of(PL.L[ref])
    col = BLK[PL.REF_BLOCK[ref]][2]
    f = 1.5 if min(w, h) > 3.2 else 1.0
    rot = f' transform="rotate(-90 {x:.2f} {-y:.2f})"' if h > 1.6 * w and h > 4 else ""
    return (f'<g class="pt" data-ref="{ref}" opacity="{".22" if dim else "1"}"><title>{e(ref)}: {e(REF_NAME[ref])} [{e(REF_C[ref])}] x={x:.1f} y={y:.1f} mm</title>'
            f'<rect x="{x-w/2:.2f}" y="{-(y+h/2):.2f}" width="{w:.2f}" height="{h:.2f}" rx="0.3" fill="{col}" fill-opacity=".30" stroke="{col}" stroke-width="0.18"/>'
            f'<text x="{x:.2f}" y="{-y+f/3:.2f}" text-anchor="middle" font-size="{f}" font-weight="700" fill="var(--fg)"{rot} style="pointer-events:none">{e(ref)}</text></g>')


def board_inner(full, active=None):
    o = [f'<rect x="0" y="{-BH}" width="{BW}" height="{BH}" rx="2" fill="var(--board)" stroke="var(--fg)" stroke-width="0.3"/>']
    for gx in range(10, int(BW), 10):
        o.append(f'<line x1="{gx}" y1="{-BH}" x2="{gx}" y2="0" stroke="var(--line)" stroke-width="0.08" stroke-dasharray="0.5 1"/>')
        if full: o.append(f'<text x="{gx}" y="{-BH-0.8}" text-anchor="middle" font-size="1.4" fill="#5b6677">{gx}</text>')
    for gy in range(10, int(BH), 10):
        o.append(f'<line x1="0" y1="{-gy}" x2="{BW}" y2="{-gy}" stroke="var(--line)" stroke-width="0.08" stroke-dasharray="0.5 1"/>')
        if full: o.append(f'<text x="-0.8" y="{-gy+0.5}" text-anchor="end" font-size="1.4" fill="#5b6677">{gy}</text>')
    for (hx, hy) in PL.HOLES:
        o.append(f'<circle cx="{hx}" cy="{-hy}" r="3.2" fill="none" stroke="#9aa5b5" stroke-width="0.2" stroke-dasharray="0.6 0.4"/><circle cx="{hx}" cy="{-hy}" r="1.6" fill="var(--board)" stroke="#9aa5b5" stroke-width="0.2"/>')
    for b in PL.BLOCKS:
        bx = b[4]
        dim = active is not None and b[0] != active
        tw = len(b[1]) * 0.8 + 1.0
        tx, ty = bx[0] + 0.8, -bx[3] + 0.45
        o.append(f'<g opacity="{".35" if dim else "1"}"><rect x="{bx[0]:.2f}" y="{-bx[3]:.2f}" width="{bx[2]-bx[0]:.2f}" height="{bx[3]-bx[1]:.2f}" rx="0.6" fill="none" stroke="{b[2]}" stroke-width="0.22" stroke-dasharray="1.0 0.6"/><rect x="{tx-0.3:.2f}" y="{ty-1.0:.2f}" width="{tw:.2f}" height="1.3" fill="var(--board)"/><text x="{tx:.2f}" y="{ty:.2f}" font-size="1.15" font-weight="700" fill="{b[2]}">{e(b[1])}</text></g>')
    for ref in PL.L:
        o.append(part_svg(ref, dim=(active is not None and PL.REF_BLOCK[ref] != active)))
    return "".join(o)


def board_svg(view=None, active=None, width_px=900):
    vx0, vy0, vx1, vy1 = view or (-3, -3, BW + 3, BH + 3)
    w, h = vx1 - vx0, vy1 - vy0
    return (f'<svg viewBox="{vx0:.2f} {-vy1:.2f} {w:.2f} {h:.2f}" width="{width_px:.0f}" height="{width_px*h/w:.0f}" class="plan" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,Segoe UI,sans-serif">{board_inner(view is None, active)}</svg>')


def parts_table(block):
    refs = sorted(block[3], key=lambda r: (r[0] != "U", r[0] != "J", r.rstrip("0123456789"), int("".join(c for c in r if c.isdigit()) or 0)))
    t = '<div class="scroll"><table><thead><tr><th></th><th>Ref</th><th>Part</th><th>LCSC</th><th>X mm</th><th>Y mm</th><th>Rot</th><th>Size mm (est.)</th></tr></thead><tbody>'
    for r in refs:
        x, y, w, h, rot = PL.L[r]
        t += f'<tr data-ref="{r}"><td><input type="checkbox" class="ck" data-k="{r}"></td><td><b>{r}</b></td><td>{e(REF_NAME[r])}</td><td>{e(REF_C[r])}</td><td class="num">{x:.1f}</td><td class="num">{y:.1f}</td><td class="num">{rot}&deg;</td><td>{w:.1f} x {h:.1f}</td></tr>'
    return t + "</tbody></table></div>"


def page_pcb():
    total = len(PL.L)
    used = sum(v[2] * v[3] for v in PL.L.values())
    o = [head(f"SafeASP - PCB floorplan {BW:.0f} x {BH:.0f} mm", f"{BW:.0f} x {BH:.0f} mm, 2 layers. Signal flow left to right: USB-C, V-USB, ATmega8A, level shifter, ISP headers. One zoomed drawing, one dashed silkscreen box and one X / Y table per block; tick each part as you place it in EasyEDA (saved in this browser).",
              '<div class="chips"><a style="background:#607d8b" href="#size">Board size</a><a style="background:#607d8b" href="#plan">Floor plan</a>' + "".join(f'<a style="background:{b[2]}" href="#{b[0]}">{e(b[1])}</a>' for b in PL.BLOCKS) + f'<a style="background:#607d8b" href="#nets">Nets</a><a style="background:#607d8b" href="#steps">Steps</a><span class="mut">placed <b id="tot">0</b> / {total}</span><div class="pbar"><div id="barfill"></div></div><button class="ghost" id="reset">Reset ticks</button></div>', "pcb-floorplan.html")]
    o.append(f'<section class="card" id="size"><h2>Board size: {BW:.0f} x {BH:.0f} mm</h2><div class="rec"><b>2 layers, 1.6 mm FR-4, 1 oz copper, {BW:.0f} x {BH:.0f} mm, 2 mm corners, two M3 holes (3.2 mm, non-plated) on the USB end.</b> Parts add up to about {used:.0f} mm&sup2; of {BW*BH:.0f} mm&sup2; ({used/(BW*BH/100):.0f} %). '
             'The v5 board was 68 x 31 mm; V6 is longer because of the level shifter, the target-power block and the second ISP header. It stays far below 100 x 100 mm (cheapest PCB price tier).</div>'
             f'<h3>Outline and holes</h3><div class="scroll"><table><thead><tr><th>Item</th><th>X mm</th><th>Y mm</th><th>Size</th></tr></thead><tbody><tr><td>Board outline</td><td class="num">0 - {BW:.0f}</td><td class="num">0 - {BH:.0f}</td><td>{BW:.0f} x {BH:.0f}, corner radius 2 mm</td></tr>'
             + "".join(f'<tr><td>MH{i} M3 hole</td><td class="num">{hx:.1f}</td><td class="num">{hy:.1f}</td><td>3.2 mm, non-plated</td></tr>' for i, (hx, hy) in enumerate(PL.HOLES, 1))
             + '</tbody></table></div><h3>Edge plan</h3><ul class="rules"><li><b>Left edge:</b> J1 USB-C.</li><li><b>Right edge:</b> J2 10-pin box header (key outwards), J3 6-pin next to it.</li><li><b>Top edge:</b> LED1 / LED2 (MCU), LED3 and JP1 (target power).</li><li><b>Bottom edge:</b> J4 self-programming header and JP2 slow-SCK jumper.</li></ul>'
             '<p class="mut">The checker (tools/layout.py) confirmed: no overlaps, every part inside its own silkscreen box, no box touching another box or a mounting hole.</p></section>')
    o.append('<section class="card" id="plan"><h2>Floor plan<span class="cnt">dashed boxes = silkscreen boxes; click a part to tick it</span></h2><div class="scroll">' + board_svg() + '</div></section>')
    for b in PL.BLOCKS:
        bx = b[4]
        crop = (max(bx[0] - 2, -2), max(bx[1] - 2, -2), min(bx[2] + 2, BW + 2), min(bx[3] + 2, BH + 2))
        wpx = int(min(900, max(480, (crop[2] - crop[0]) * 24)))
        o.append(f'<section class="card" id="{b[0]}" style="--c:{b[2]}"><h2>{e(b[1])}<span class="cnt"><span class="done">0</span> / {len(b[3])} placed &middot; box x {bx[0]:.1f} to {bx[2]:.1f}, y {bx[1]:.1f} to {bx[3]:.1f} mm</span></h2><ul class="rules">' + "".join(f"<li>{e(t)}</li>" for t in BLOCK_NOTES[b[0]]) + f'</ul><div class="scroll">{board_svg(view=crop, active=b[0], width_px=wpx)}</div>{parts_table(b)}</section>')
    o.append('<section class="card" id="nets"><h2>Nets and trace widths<span class="cnt">1 oz copper, with margin</span></h2><div class="scroll"><table><thead><tr><th>Net</th><th>Width</th><th>Notes</th></tr></thead><tbody>' + "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td></tr>" for a, b, c in NETS) + '</tbody></table></div></section>')
    o.append('<section class="card" id="steps"><h2>Order of work</h2><ol class="steps">' + "".join(f"<li>{e(t)}</li>" for t in STEPS) + "</ol></section>" + links())
    o.append("""<script>
const K='usbasp6-pcb-ticks';let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
function apply(){const total=document.querySelectorAll('#plan .pt').length;document.querySelectorAll('.pt').forEach(g=>g.classList.toggle('ok',!!st[g.dataset.ref]));
 document.querySelectorAll('tr[data-ref]').forEach(r=>{const on=!!st[r.dataset.ref];r.classList.toggle('ok',on);r.querySelector('.ck').checked=on});
 const n=Object.keys(st).length;document.getElementById('tot').textContent=n;document.getElementById('barfill').style.width=(100*n/total)+'%';
 document.querySelectorAll('section.card[id]').forEach(sec=>{const rows=sec.querySelectorAll('tr[data-ref]');if(!rows.length)return;const d=[...rows].filter(r=>st[r.dataset.ref]).length;const c=sec.querySelector('.done');if(c)c.textContent=d});
 try{localStorage.setItem(K,JSON.stringify(st))}catch(e){}}
function tog(r){if(st[r])delete st[r];else st[r]=1;apply()}
document.querySelectorAll('.pt').forEach(g=>g.addEventListener('click',()=>tog(g.dataset.ref)));document.querySelectorAll('input.ck').forEach(c=>c.addEventListener('change',()=>tog(c.dataset.k)));
document.getElementById('reset').onclick=()=>{st={};apply()};apply();
</script></div></body></html>""")
    return "".join(o)


# ------------------------------------------------------------------ home page
FEATURES = [
 ("USB-C", "16-pin USB 2.0 receptacle with separate 5.1 k on CC1 and CC2: works with USB-C to USB-C cables, laptops and phone chargers."),
 ("Safe 1.8 - 5.5 V targets", "74LVC8T245 + 74LVC1T45 level shifter powered from the target's own VCC: no more 5 V signals into a 3.3 V chip."),
 ("Pins released when idle", "The shifter outputs are only on while the red BUSY LED is lit, so the programmer does not fight the target's own use of MOSI / SCK / RST."),
 ("Protected target power", "Jumper for 5 V / 3.3 V / off, 200 mA PTC fuse and a yellow LED: a shorted target no longer resets the programmer or the PC port."),
 ("USB protection", "500 mA PTC on VBUS and a USBLC6 ESD diode array on D+ / D-."),
 ("10-pin AND 6-pin ISP", "Keyed box header for the standard 10-pin cable plus the 6-pin Arduino ICSP layout, as asked in the v5 comments."),
 ("Easy firmware update", "A separate 6-pin header (J4) to flash the board's own ATmega8A; no more jumper juggling on the ISP header."),
 ("Stock firmware", "Runs the original USBasp 2011-05-28 firmware unchanged and works with avrdude (-c usbasp) and the Arduino IDE."),
]


def page_index():
    o = [head("SafeASP - USB-C AVR programmer", HEAD_SUB.replace("LCSC listings read 2026-11-13 &middot; Sheet N here = Sheet N on every page", "open hardware by ElectroIoT"), "", "index.html")]
    o.append('<section class="card" style="--c:#1e3a8a"><h2>What is new in V6</h2><div class="scroll"><table><tbody>' + "".join(f"<tr><td><b>{e(a)}</b></td><td>{e(b)}</td></tr>" for a, b in FEATURES) + '</tbody></table></div></section>')
    o.append('<section class="card" style="--c:#0e7490"><h2>Design pages</h2><ul class="rules">'
             f'<li><a href="bom.html"><b>Bill of materials</b></a>: {D.TOTAL_PIECES} parts, about USD {D.totals():.2f}, LCSC numbers, copy-all button.</li>'
             '<li><a href="wiring-by-section.html"><b>Wiring by section</b></a>: connection map, ATmega8A pin table, every pin-to-net per part.</li>'
             '<li><a href="schematic-sections.html"><b>Schematic by section</b></a>: three sheets, build steps, ATmega8A / level-shifter / USB-C pin guides.</li>'
             f'<li><a href="pcb-floorplan.html"><b>PCB floorplan</b></a>: {BW:.0f} x {BH:.0f} mm board, block boxes, X / Y position of every part.</li></ul></section>')
    o.append('<section class="card" style="--c:#475569"><h2>Floor plan preview</h2><div class="scroll">' + board_svg(width_px=900) + '</div></section>' + links() + '</div></body></html>')
    return "".join(o)


def standalone_svg():
    inner = board_inner(True).replace("var(--fg)", "#1c2330").replace("var(--board)", "#e8efe4").replace("var(--line)", "#c9d1dc")
    leg = "".join(f'<rect x="{-2 + i * 14}" y="3.4" width="1.6" height="1.6" fill="{b[2]}"/><text x="{-2 + i * 14 + 2.2}" y="4.7" font-size="1.35" fill="#1c2330">{e(b[1])}</text>' for i, b in enumerate(PL.BLOCKS))
    vh = BH + 12
    return (f'<svg viewBox="-3 {-(BH+5)} {BW+6} {vh}" width="1000" height="{1000*vh/(BW+6):.0f}" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,Segoe UI,sans-serif"><rect x="-3" y="{-(BH+5)}" width="{BW+6}" height="{vh}" fill="#ffffff"/>'
            f'<text x="-2" y="{-(BH+2.5)}" font-size="2" font-weight="700" fill="#1c2330">SafeASP PCB floor plan - {BW:.0f} x {BH:.0f} mm, 2 layers, one silkscreen box per block (planning estimate)</text>{inner}{leg}</svg>')


def main():
    write_bom()
    pages = {"index.html": page_index(), "bom.html": page_bom(), "wiring-by-section.html": page_wiring(), "schematic-sections.html": page_schem(), "pcb-floorplan.html": page_pcb()}
    for f, html_ in pages.items():
        with open(os.path.join(DOCS, f), "w", encoding="utf-8") as fh:
            fh.write(html_)
    with open(os.path.join(DOCS, "images", "pcb-floorplan.svg"), "w", encoding="utf-8") as fh:
        fh.write(standalone_svg())
    with open(os.path.join(ROOT, "hardware", "bom", "bom-table.md"), "w", encoding="utf-8") as fh:
        fh.write(bom_md())
    pr = PL.check() + D.check()
    print("pages written; problems:", len(pr), "; pieces", D.TOTAL_PIECES, "; total USD", round(D.totals(), 2))
    for p in pr:
        print(" ", p)


if __name__ == "__main__":
    main()
