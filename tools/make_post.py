"""Build the 1080x1350 Instagram image from the same spec JSON used by make_short.py.
Usage: python3 make_post.py spec.json out.jpg
Spec scenes used: first "hook" (tag/title/tamil), first "code" (code), "step" scenes (en/tamil)."""
import json, sys, html
from playwright.sync_api import sync_playwright

spec = json.load(open(sys.argv[1], encoding="utf-8")); out = sys.argv[2]
sc = spec["scenes"]; e = html.escape
hook = next(s for s in sc if s["type"] == "hook")
code = next((s for s in sc if s["type"] == "code"), None)
steps = [s for s in sc if s["type"] == "step"]
title = e(hook["title"]).replace("[[", "<span>").replace("]]", "</span>")
code_html = f"<div class='formula'><small>{e(code.get('en','')).upper()}</small>{e(code['code'])}</div>" if code else ""
steps_html = "".join(f"<div class='step'><div class='n'>{e(s['n'])}</div><div><div class='en'>{e(s['en'])}</div>"
                     f"<div class='t'>{e(s['tamil'])}</div></div></div>" for s in steps)
doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;background:#0f172a;font-family:'FreeSans',sans-serif;color:#f8fafc;position:relative;overflow:hidden}}
.bar{{position:absolute;top:0;left:0;right:0;height:14px;background:linear-gradient(90deg,#ef4444,#f97316)}}
.wrap{{padding:80px 72px}}
.tag{{display:inline-block;background:#ef4444;color:#fff;font-weight:bold;font-size:30px;padding:10px 26px;border-radius:40px}}
h1{{font-size:76px;line-height:1.1;margin:36px 0 18px;font-weight:bold}} h1 span{{color:#f97316}}
.ta{{font-size:40px;color:#cbd5e1;line-height:1.5}}
.formula{{margin:44px 0;background:#1e293b;border:3px solid #22c55e;border-radius:22px;padding:30px 36px;
 font-family:'DejaVu Sans Mono',monospace;font-size:36px;color:#4ade80;overflow-wrap:break-word;line-height:1.4}}
.formula small{{display:block;font-family:'FreeSans';font-size:26px;color:#94a3b8;margin-bottom:12px;letter-spacing:2px}}
.step{{display:flex;gap:28px;margin:28px 0;align-items:flex-start}}
.n{{flex:0 0 66px;height:66px;border-radius:50%;background:#f97316;color:#0f172a;font-weight:bold;font-size:36px;display:flex;align-items:center;justify-content:center}}
.en{{font-size:36px;font-weight:bold}} .t{{font-size:31px;color:#cbd5e1;margin-top:6px;line-height:1.4}}
.foot{{position:absolute;bottom:0;left:0;right:0;background:#1e293b;padding:30px 72px;display:flex;justify-content:space-between;font-size:30px}}
.foot b{{color:#f97316}}
</style></head><body><div class="bar"></div><div class="wrap">
<div class="tag">{e(hook['tag'])}</div><h1>{title}</h1><div class="ta">{e(hook['tamil'])}</div>
{code_html}{steps_html}</div>
<div class="foot"><span>Follow <b>@bh_arath1843</b></span><span>Daily AI &amp; automation tips · தமிழ்</span></div>
</body></html>"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
    pg.set_content(doc); pg.wait_for_timeout(300)
    h = pg.evaluate("document.querySelector('.wrap').scrollHeight")
    if h > 1250: print("WARNING: content too tall, shorten text", h)
    pg.screenshot(path=out, type="jpeg", quality=90); b.close()
print(out)
