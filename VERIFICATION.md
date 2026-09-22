# Repair verification - 22 September 2026

## Feature checks

The source for the requested Al-Furqan recording is Wycombe Mosque's YouTube upload `K1cA-E6MoBU`, titled **Qari Ibrahim Idris - Surah Furqan: 61 - 77**. YouTube oEmbed returned that title and author. It is featured first, with five other source recordings. The existing study range remains 25:63-77 to preserve existing notes.

Chromium regression checks passed: 30 passages, persistent light/dark theme, visible correctly addressed iframe, English/Bangla/Japanese, a 390px mobile viewport without horizontal page overflow, original Mushaf tab, page zoom, wide mode, back navigation, and existing notes preservation. No JavaScript exceptions were recorded in those flows. These tests use declared network fixtures and do not prove external video playback.

## Live source checks

Real-browser checks separately loaded all five original eQuran scans for the selected source section: p363.gif, p364.gif, p365.gif, p366.gif, p367_1.gif. All five were saved into the offline scan cache. They are original publisher images, not a newly typeset or generated imitation.

Real audio playback advanced for Mishary Alafasy, Sudais and Luhaidan. Al-Ossi also advanced in an earlier test, but individual recordings may load at different speeds. The selected Alafasy MP3 was saved (16.8 MB), then played from a local blob with the browser offline. Yasser is matched by both first and family name to exclude Yasser Salamah and Ibrahim Aldosari; the publisher entry is ID92 at server11.mp3quran.net/yasser/025.mp3.

## Open limitation: YouTube playback

The original Ibrahim source returns successful metadata, but the live automated browser returned YouTube player error150. The interface reports this rather than leaving a blank player or claiming playback succeeded. A metadata response, thumbnail or Vercel build success is not proof of video playback. The workflow additionally records individual attempts for all source videos in embed-audit.json. No provider restriction is bypassed.

YouTube videos have not been converted into MP4/MP3 downloads. Publisher-authorized direct MP3 saving and permitted local media imports are separate features; they are not advertised as the original viral video audio.

## Supabase

The free famous-quran project was created in the owner-confirmed blackchoco organization, Tokyo region (project ref qzamdjcguksgzqcdaosd). Owner-only fq_backups row security was applied. A two-user transactional isolation test passed and rolled back its temporary records. The security advisor reported no database lints. Google OAuth, production email delivery and redirect configuration are not yet activated, and the site does not pretend otherwise.

## Real screenshots

GitHub Actions artifacts named verified-source contain actual light/dark recordings views, the original Mushaf reader and live test reports. The earlier generated promotional dashboard is a concept, not a screenshot of this deployed application.
