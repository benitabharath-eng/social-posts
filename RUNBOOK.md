# Daily post runbook (Instagram + YouTube Shorts)

Owner: Bharath Kumar (@bh_arath1843). Metricool brand blogId **7498096**, timezone **Asia/Calcutta**.
Post DIRECTLY (no approval). Share the links with Bharath every time.

## 1. Topic (rotate by IST weekday)
- **Mon / Wed / Fri** – Excel or TallyPrime tip for accountants (formulas, shortcuts, GST, reconciliation, Power Query). Must be accurate. Check `videos/*/spec.json` so you never repeat a tip; number tips in sequence (EXCEL TIP #N).
- **Tue / Thu / Sat** – one AI news item from the last 48 h, confirmed by a reliable source (official blog, Reuters, The Verge, TechCrunch). Say why it matters for office/finance workers in India. Put the source in captions.
- **Sun** – a simple "automate your office work with AI" idea.

## 2. Spec
Create `videos/YYYY-MM-DD/spec.json` (copy the structure of `videos/2026-11-04/spec.json`):
- scenes: `hook` (tag, title with `[[orange words]]`, tamil, say, say_ta), optional `code` (en, code, tamil, say), 3× `step` (n, en, tamil, say_ta), `cta` (en, tamil, say, say_ta).
- Tamil = Tamil script, casual spoken Tamil with English tech words ("formula போடுங்க").
- Keep voice short so the Short is **≤ 35 s** (English on hook/code/cta, Tamil on steps). Use a different `music_seed` (0–2) each day.

## 3. Build
```
python3 tools/make_post.py  videos/DATE/spec.json videos/DATE/post.jpg
python3 tools/make_short.py videos/DATE/spec.json videos/DATE/short.mp4
```
Look at post.jpg (Read tool) and a frame of the video before publishing. If make_post warns "too tall", shorten text.
Voice uses translate.google.com (allowed domain). If it fails, make_short falls back to an offline English voice — still publish.
Commit and push to `main` (git identity: Bharath Kumar <benitabharath@gmail.com>).

Public URLs: `https://raw.githubusercontent.com/benitabharath-eng/social-posts/main/videos/DATE/post.jpg` and `.../short.mp4`

## 4. Schedule on Metricool (createScheduledPost, publish ~8 min from now, autoPublish true, draft false)
- **Instagram**: providers [instagram], media [post.jpg URL], instagramData {"type":"POST","showReelOnFeed":true,"isAiGenerated":false}. Caption: English, then "தமிழில்:" Tamil, save & follow @bh_arath1843, 8–12 hashtags.
- **YouTube** (separate post): providers [youtube], media [short.mp4 URL], youtubeData {"title": "<under 100 chars, no < >, end with #Shorts>", "type":"short", "privacy":"public", "category":"EDUCATION" (or SCIENCE_TECHNOLOGY for AI news), "madeForKids": false, "tags":[...]}. Text = description with #Shorts.

## 5. Links
~10 min after the publish time call getScheduledPosts (brandId 7498096, today, Asia/Calcutta). `providers[0].publicUrl` = live link, status PUBLISHED. Retry once after a few minutes if pending.

## 6. Report
Message Bharath (SendUserMessage and PushNotification if available): topic + Instagram link + YouTube link, or the exact error.
