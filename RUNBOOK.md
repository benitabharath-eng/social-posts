# Daily post runbook (Instagram + YouTube Shorts)

Owner: Bharath Kumar (@bh_arath1843). Metricool brand blogId **7498096**, timezone **Asia/Calcutta**.
Post DIRECTLY (no approval). Share the links with Bharath every time.

## 1. Topic (TWO posts a day since 10 Nov 2026 — pick by run time, IST)
- **Morning run (~8:23 AM)** – Excel or TallyPrime tip for accountants (formulas, shortcuts, GST, reconciliation, Power Query). Must be accurate. Check `videos/*/spec.json` so you never repeat a tip; number tips in sequence (EXCEL TIP #N / TALLY TIP #N). Folder: `videos/YYYY-MM-DD-am/`.
- **Evening run (~6:41 PM)** – Mon–Sat: one AI news item from the last 48–72 h, confirmed by a reliable source (official blog/release notes, Reuters, The Verge, TechCrunch); say why it matters for office/finance workers in India and put the source in captions. Sunday: a simple "automate your office work with AI" idea. Folder: `videos/YYYY-MM-DD/`.
- Best performers so far (Nov 2026): practical "AI at work" (payment reminder prompt, security/updates). Prefer practical takeaways.
- End the cta scene / caption with a question to invite comments (e.g. "Which Tally problem should I solve next? Comment below").

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
- **YouTube** (separate post): providers [youtube], media [short.mp4 URL], youtubeData {"title": "<under 100 chars, no < >, end with #Shorts>", "type":"short", "privacy":"public", "category":"EDUCATION" (or SCIENCE_TECHNOLOGY for AI news), "madeForKids": false, "tags":[...]}. Text = description with #Shorts. NEVER use the characters < or > anywhere in the YouTube title or description (YouTube rejects the upload: "invalid video description"). Write "Data, then Remove Duplicates" instead of "Data > Remove Duplicates".

## 4b. Comments
Read YouTube comments without a browser: firecrawl_scrape alexandria provider "youtube-com", capability "videos/video_comments", options {"video_id": ID} for the last ~7 Shorts (IDs from getScheduledPosts publicUrl). Reply as Bharath only via a browser already signed in to his YouTube (Chrome extension or built-in browser) — never type passwords. If no signed-in browser, send Bharath the suggested reply text instead. Reply only to genuine questions; skip spam/abuse; never delete comments.

## 5. Links
~10 min after the publish time call getScheduledPosts (brandId 7498096, today, Asia/Calcutta). `providers[0].publicUrl` = live link, status PUBLISHED. Retry once after a few minutes if pending.

## 6. Report
Message Bharath (SendUserMessage and PushNotification if available): topic + Instagram link + YouTube link, or the exact error.
