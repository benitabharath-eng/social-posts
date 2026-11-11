"""Build a 1080x1920 YouTube Short from a JSON spec of scenes.
Usage: python3 make_short.py spec.json out.mp4
"""
import json, subprocess, sys, os, html
from playwright.sync_api import sync_playwright

spec = json.load(open(sys.argv[1], encoding="utf-8"))
out = sys.argv[2]
work = os.path.join(os.path.dirname(os.path.abspath(out)), "frames")
os.makedirs(work, exist_ok=True)

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;background:#0f172a;font-family:'FreeSans',sans-serif;color:#f8fafc;
 display:flex;flex-direction:column;justify-content:center;padding:0 90px;position:relative;overflow:hidden}
.bar{position:absolute;top:0;left:0;right:0;height:18px;background:linear-gradient(90deg,#ef4444,#f97316)}
.tag{align-self:flex-start;background:#ef4444;color:#fff;font-weight:bold;font-size:40px;padding:14px 34px;border-radius:50px;margin-bottom:50px}
h1{font-size:110px;line-height:1.08;font-weight:bold;margin-bottom:50px}
h1 em{font-style:normal;color:#f97316}
.ta{font-size:56px;color:#cbd5e1;line-height:1.5}
.en{font-size:70px;font-weight:bold;line-height:1.2;margin-bottom:36px}
.code{background:#1e293b;border:5px solid #22c55e;border-radius:30px;padding:50px 46px;font-family:'DejaVu Sans Mono',monospace;
 font-size:52px;color:#4ade80;line-height:1.5;margin:40px 0;overflow-wrap:break-word;white-space:pre-line}
.num{width:150px;height:150px;border-radius:50%;background:#f97316;color:#0f172a;font-weight:bold;font-size:84px;
 display:flex;align-items:center;justify-content:center;margin-bottom:50px}
.foot{position:absolute;bottom:140px;left:90px;right:90px;font-size:44px;color:#94a3b8;text-align:center}
.foot b{color:#f97316}
"""

def page(body):
    return f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='bar'></div>{body}" \
           f"<div class='foot'>Follow <b>@bh_arath1843</b> · English + தமிழ்</div></body></html>"

def scene_html(s):
    t = s["type"]
    e = lambda k: html.escape(s.get(k, ""))
    if t == "hook":
        title = e("title").replace("[[", "<em>").replace("]]", "</em>")
        return page(f"<div class='tag'>{e('tag')}</div><h1>{title}</h1><div class='ta'>{e('tamil')}</div>")
    if t == "code":
        return page(f"<div class='en'>{e('en')}</div><div class='code'>{e('code')}</div><div class='ta'>{e('tamil')}</div>")
    if t == "step":
        return page(f"<div class='num'>{e('n')}</div><div class='en'>{e('en')}</div><div class='ta'>{e('tamil')}</div>")
    if t == "cta":
        return page(f"<h1>{e('en')}</h1><div class='ta'>{e('tamil')}</div>")
    raise ValueError(t)

pngs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    for i, s in enumerate(spec["scenes"]):
        pg.set_content(scene_html(s)); pg.wait_for_timeout(200)
        f = os.path.join(work, f"s{i:02d}.png"); pg.screenshot(path=f); pngs.append((f, s.get("secs", 3)))
    b.close()

# Voice-over (ffmpeg flite, English) per scene; scene length stretches to fit narration.
def dur(f):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],
                                capture_output=True,text=True).stdout)
voice = spec.get("voice", "slt")
here = os.path.dirname(os.path.abspath(__file__))
def speak(lang, text, wav):
    """Google voice (en/ta) if reachable, else offline flite (English only)."""
    mp3 = wav[:-4] + ".mp3"
    try:
        subprocess.run([sys.executable, os.path.join(here, "tts.py"), lang, text, mp3], check=True, capture_output=True, timeout=60)
        subprocess.run(["ffmpeg","-y","-loglevel","error","-i",mp3,"-af","atempo=1.22,aresample=44100","-ac","2",wav], check=True)
        return True
    except Exception:
        if lang != "en": return False
        txt = text.replace("'", "").replace(":", " ")
        subprocess.run(["ffmpeg","-y","-loglevel","error","-f","lavfi","-i",f"flite=text='{txt}':voice={voice}",
                        "-af","atempo=1.05,aresample=44100","-ac","2",wav], check=True)
        return True
scenes = []
for i, ((f, d), s) in enumerate(zip(pngs, spec["scenes"])):
    pieces = []
    for lang, key in (("en", "say"), ("ta", "say_ta")):
        if s.get(key):
            w = os.path.join(work, f"v{i:02d}{lang}.wav")
            if speak(lang, s[key], w): pieces.append(w)
    vw = None
    if pieces:
        vw = os.path.join(work, f"v{i:02d}.wav")
        if len(pieces) == 1: subprocess.run(["cp", pieces[0], vw], check=True)
        else:
            subprocess.run(["ffmpeg","-y","-loglevel","error","-i",pieces[0],"-i",pieces[1],"-filter_complex",
                            "[0:a]apad=pad_dur=0.25[a0];[a0][1:a]concat=n=2:v=0:a=1[o]","-map","[o]",vw], check=True)
        d = max(d, dur(vw) + 0.6)
    scenes.append((f, round(d, 2), vw))

clips = []; vparts = []
for i, (f, d, vw) in enumerate(scenes):
    c = os.path.join(work, f"c{i:02d}.mp4"); fr = int(d * 30)
    vf = (f"scale=1188:2112,zoompan=z='1+0.0006*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps=30,"
          f"fade=t=in:st=0:d=0.3,fade=t=out:st={d-0.3}:d=0.3,format=yuv420p")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-i",f,"-t",str(d),"-vf",vf,"-c:v","libx264",
                    "-preset","veryfast","-crf","23",c], check=True)
    clips.append(c)
    a = os.path.join(work, f"a{i:02d}.wav")  # voice padded to scene length, starting 0.3s in
    src = ["-i", vw] if vw else ["-f","lavfi","-i","anullsrc=r=44100:cl=stereo"]
    subprocess.run(["ffmpeg","-y","-loglevel","error",*src,"-af",f"adelay=300|300,apad","-t",str(d),"-ar","44100","-ac","2",a], check=True)
    vparts.append(a)

lst = os.path.join(work, "list.txt"); open(lst, "w").write("".join(f"file '{c}'\n" for c in clips))
vid = os.path.join(work, "video.mp4")
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",lst,"-c","copy",vid], check=True)
alst = os.path.join(work, "alist.txt"); open(alst, "w").write("".join(f"file '{a}'\n" for a in vparts))
voicewav = os.path.join(work, "voice.wav")
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",alst,"-c","copy",voicewav], check=True)
total = sum(d for _, d, _ in scenes)
musicwav = os.path.join(work, "music.wav")
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "music.py"), str(total + 0.5),
                musicwav, str(spec.get("music_seed", 0))], check=True, capture_output=True)
# Mix: music ducks under the voice (sidechain), then loudness-normalise for YouTube.
fc = ("[2:a]volume=0.35[m];[1:a]asplit[v1][v2];[m][v1]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400[md];"
      "[md][v2]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5[a]")
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",vid,"-i",voicewav,"-i",musicwav,"-filter_complex",fc,
                "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",out], check=True)
print(out, round(total, 1), "sec")
