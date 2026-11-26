# Ayah Daily: daily batch runbook

Channel: **Ayah Daily | Quran** (@AyahDaily365), YouTube channel `UCFJ33lQM6lHEOyYgtBMn3sg`, Google account `ayahdaily365@gmail.com` (authuser=1 in the built-in browser).
Goal each run: **make 5 Shorts and schedule them into the next free slots** (07:30, 13:30, 20:30 Africa/Lagos), so the calendar stays several days ahead. Find the last scheduled slot in YouTube Studio (Shorts tab, Scheduled rows) and on publish.buffer.com/schedule?tab=queue, then fill forward from the next slot. Put each video in `queue/<its date>/<n>-<slot>_<name>.mp4`. Buffer's free plan allows max 10 queued posts per channel: if a video would exceed that, schedule it on YouTube only, keep a copy in `queue/buffer/`, and add it to Buffer on a later run once slots free up.
**Style update (user, 26 Nov, overrides older notes): calm, soothing qira'ah, and surreal animation scenes.**
Content focus (user, 25 Nov): verses that **comfort the soul in hard times**, and verses about **the oppressed and the weak** (Allah's justice for them, the oppressor's end). Mix in a little warning (Day of Judgement) where it supports that theme.

## Hard rules
- Visuals (26 Nov): **surreal, dreamlike scenes** (e.g. a lone figure on a staircase into the clouds, a door standing open in a calm sea, floating lanterns over a desert, a giant moon over still water, a tree growing from an open hand of light), still soft anime painted style, sharp and clean, one clear subject. Older guidance: **sharp and clean, relatable everyday scenes** (a tired person on a bus at night, someone sitting on a bed by a window, a worker walking home, a mother at a kitchen table), **simple uncluttered backgrounds with one clear subject**, little background detail. Put "sharp focus, clean simple background, minimal detail, uncluttered" in every image and Veo prompt. People are **always seen from behind or far away, no faces**. Never depict prophets, companions, angels or Allah. No gore. No text inside images.
- Text: Uthmani Arabic (api.quran.com `text_uthmani`) + **Sahih International** (translation id 20). Strip `<sup>` footnotes; drop bracketed words only when the meaning is unchanged.
- Length 10–30 s of recitation. Never reuse a verse listed in `posted.md`.
- Each video opens with **one animated Veo 3.1 Lite hook clip** (8 s), followed by 1–2 still images (Ken Burns).

## Network facts (important)
- My shell and the user's Mac shell **cannot** reach api.quran.com / everyayah.com / flow.google.com. Only the **built-in browser** can. Fetch text/audio in the browser with `fetch()` and return base64 in chunks of ≤230,000 characters per `javascript_tool` call (bigger results get cut off by the device bridge). Store the joined string in `window.__x` first, then pull the slices.
- Audio, one file per verse: `https://everyayah.com/data/<Reciter>/<SSSAAA>.mp3`. Folders that work: `Yasser_Ad-Dussary_128kbps`, `Maher_AlMuaiqly_64kbps`, `Alafasy_128kbps`, `Nasser_Alqatami_128kbps`, `Abdul_Basit_Murattal_192kbps`.
- **Reciters (user, 26 Nov): calm, soothing qira'ah.** Prefer gentle, slow, melodic murattal voices (e.g. Maher Al-Muaiqly `Maher_AlMuaiqly_64kbps`, Hani Ar-Rifai `Hani_Rifai_192kbps`, Muhammad Jibreel, Minshawi Murattal `Minshawy_Murattal_128kbps`, Abu Bakr Ash-Shaatree `Abu_Bakr_Ash-Shaatree_128kbps`, Saad Al-Ghamdi `Ghamadi_40kbps`); still avoid Alafasy/Abdul Basit. Older note (25 Nov, superseded where it conflicts): use trending, highly emotional voices. Rotate mainly: Yasser Al-Dosari (`Yasser_Ad-Dussary_128kbps`), Nasser Al-Qatami (`Nasser_Alqatami_128kbps`), Hani Ar-Rifai (`Hani_Rifai_192kbps`), Fares Abbad (`Fares_Abbad_64kbps`), Muhammad Jibreel (`Muhammad_Jibreel_128kbps`), Ahmed Al-Ajamy (`ahmed_ibn_ali_al_ajamy_128kbps`), Minshawi Mujawwad (`Minshawy_Mujawwad_192kbps`). Listen-check is not possible, so prefer these over calm/teaching styles. Avoid Alafasy and Abdul Basit (Content ID claims).
- Downloads: synthetic `<a download>` clicks only work from an **everyayah.com tab** (fetch same-origin there, then click). From flow.google.com, bundle images into one blob and click a real on-page link with the computer tool.
- Text: `https://api.quran.com/api/v4/verses/by_key/S:A?fields=text_uthmani&translations=20`.
- Flow **images**: tile `<img>` src is `https://flow.google.com/asb/<ID>=...`; fetch `.../asb/<ID>=s1376-rj?authuser=1` from a flow.google.com tab (CORS ok), then pass the base64 across in chunks.
- Flow **video clips** can't be fetched (googlevideo blocks it). Download them with Flow's ⋮ → Download → 720p. They land in `~/Downloads` with descriptive names (`Storm_wall_rolling_closer_xxxx.mp4`), so move them to `~/Downloads/Ayah Daily/clips/` with `device_bash` and pull them in with `device_stage_files`.
- **Publishing**: commit finished videos to this repo (`queue/<YYYY-MM-DD>/`). From a studio.youtube.com tab, `fetch('https://raw.githubusercontent.com/ayahdaily365/ayah-daily-media/main/queue/...')` works with CORS. Inject the file into the upload dialog's `input[type=file][name=Filedata]` with `DataTransfer`, then run `pipeline/yt_upload.js`. Known issues: the title box sometimes isn't set (it keeps the file name) and the date field typing lands in the time field. After each upload, check the title, set the date by clicking the day in the calendar with the computer tool, and **keep the channel's default description footer** (put the caption above it, don't replace it). Run (`ytUpload({url, filename, title, desc, date:'Nov 26, 2026', time:'7:30 AM'})`). Time items in the dropdown use U+202F narrow spaces, which the script normalises.

## Instagram, Facebook and TikTok via Buffer (free plan)
- Buffer account: ayahdaily365@gmail.com (publish.buffer.com, already signed in to the built-in browser). Free plan = 3 channels, max 10 queued posts per channel. Channels: Instagram professional `ayahdaily365`, TikTok `ayah.daily86`, Facebook Page `Ayah Daily Quran`.
- Facebook, Meta Business Suite and TikTok web block fetching from GitHub (CSP); **publish.buffer.com allows it**, so schedule IG/FB/TikTok through Buffer.
- For each of the 3 daily videos: on publish.buffer.com click **New Post** (all 3 channels are preselected). Inject the video from raw.githubusercontent.com into `input[type=file]` with DataTransfer and wait ~12 s.
- **Type the caption with real keystrokes** (computer `type`, after clicking inside the editor area, not on the "Templates" link). `execCommand('insertText')` does NOT save into Buffer's editor state. Use max **5 hashtags** (Instagram limit).
- Time: open the "Next Available" dropdown → **Set Date and Time** → click the time field → click the 15-minute slot (7:30 AM / 1:30 PM / 8:30 PM; time zone is Africa/Lagos) → Done → **Customize**.
- In Customize: TikTok AI-Generated switch ON; expand Instagram (button aria-label starts `Instagram:`), check Reel is selected, AI-Generated ON; expand Facebook, select radio `facebook_reel`, then replace the **Reel Title** (defaults to the file name) with the YouTube title minus "#shorts". Click **Schedule**. Verify on publish.buffer.com/schedule?tab=queue.

## Download workaround (26 Nov)
- Browser-pane downloads stopped landing in ~/Downloads on 26 Nov (synthetic clicks, real clicks and Flow's own Download menu all failed). What works: build the bytes in the page (fetch same-origin on everyayah.com / flow.google.com `asb/<ID>=s1376-rj`), base64 into `window.__x`, and pull slices of 230,000 chars per `javascript_tool` call returned as `'TAG<n>:'+slice`. Large results are saved to the session's tool-results folder; join them with a small script (match prefix `TAG<n>:`, sort by n, base64-decode).
- Flow **video clips** cannot be pulled this way (googlevideo redirect; captureStream is blocked as cross-origin). If downloads are still broken, skip Veo (don't spend credits) and open each video on a still image with Ken Burns. Check ~/Downloads after one test download first.

## Flow limits (free plan)
- 50 credits/day, refreshing about 24 h after the first generation. Veo 3.1 **Lite** = 10 credits → **5 hook clips/day**. Use the Flow **agent panel** (right side) and click its send arrow; long prompts don't send on Enter. Approve the "N credits" prompt.
- Nano Banana Pro ≈ 20 images/day, then switch to Nano Banana 2.1. Ask for "SEPARATE vertical 9:16 images (not a collage)" and "upright portrait orientation".

## Steps
1. `git clone` this repo and `pip install` nothing extra (PIL+raqm, numpy, ffmpeg already exist). Fonts are in `pipeline/fonts`; `render.py` expects them at `<render.py dir>/fonts/`.
2. Pick 5 new verses (check `posted.md`), rotating reciters. Fetch text and audio in the browser. Build per-video audio with ffmpeg concat.
3. Split each verse into phrases at its waqf marks; time them with `pauses.py` energy dips (split at the nearest dip). Write a spec JSON like those in `pipeline/specs/` (fields: audio, out, surah_en, surah_ar, ref, reciter_en, hook, segments, scenes). The **hook** is a short scroll-stopping line (e.g. "Why were you created?").
4. In Flow (project "Ayah Daily Islamic Ani…", account ayahdaily365, URL flow.google.com/u/1/...), generate 3 images per video, then animate the first image of each with Veo 3.1 Lite (5 clips). Check every image with a contact sheet before use, and reject faces, odd figures or sideways images.
5. `python3 render.py spec.json` (about 25 s per video). Check frames at 1.5 s, mid and end.
6. Commit the 3 for tomorrow to `queue/<date>/` and the other 2 to `queue/buffer/`, then push. Schedule the 3 in YouTube Studio. Titles: `<Hook-ish title> <emoji> Surah X (S:A) | Reciter #shorts`. Description: 2–3 line caption, reference + reciter, then the standard footer and hashtags (see `posted.md` examples). Not made for kids; paid promotion No; altered content No (stylised animation isn't realistic).
7. Append each verse to `posted.md` with date, slot and the YouTube link. Delete queue files older than 2 days from the repo (`git rm`).
8. Schedule the same 3 videos to Instagram, TikTok and Facebook through Buffer (section above).
9. Report to the user: what's scheduled, the buffer, credits used and any Content ID claims.

## Known notes
- Mishary Alafasy recitations receive Content ID audio claims (no reach impact, no strike; claimant gets monetisation). Track claims per reciter in `posted.md`.
