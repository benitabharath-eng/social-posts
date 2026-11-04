"""Google Translate TTS (no package needed). Usage: python3 tts.py lang "text" out.mp3"""
import sys, urllib.request, urllib.parse, re
lang, text, out = sys.argv[1], sys.argv[2], sys.argv[3]
# split into <=180-char chunks on sentence/comma boundaries
parts, cur = [], ""
for w in re.split(r'(?<=[.,!?।])\s+', text.strip()):
    if len(cur) + len(w) + 1 > 180 and cur: parts.append(cur); cur = w
    else: cur = (cur + " " + w).strip()
if cur: parts.append(cur)
data = b""
for i, p in enumerate(parts):
    q = urllib.parse.urlencode({"ie": "UTF-8", "q": p, "tl": lang, "client": "tw-ob", "total": len(parts), "idx": i, "textlen": len(p)})
    req = urllib.request.Request("https://translate.google.com/translate_tts?" + q, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://translate.google.com/"})
    data += urllib.request.urlopen(req, timeout=20).read()
open(out, "wb").write(data); print(out, len(data))
