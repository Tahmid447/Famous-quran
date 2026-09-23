# Famous Quran: resumable community release checkpoint

## Working branch and production status

Continue from feature/community-learning-native-media. Do not restart the application. Inspect main and the branch's latest verification run before claiming a production release. A Vercel success on a feature branch is only a preview.

## Implemented changes

- Original passage IDs 1-30 and existing notes/favorites preserved.
- 36 short English/Bangla/Japanese source-based guides, explicitly labelled as paraphrases rather than quotations or independent scholarly tafsir.
- Six complete-surah cards: Ya-Sin, Ar-Rahman, Al-Waqiah, As-Sajdah, Al-Mulk, Al-Fatihah.
- Existing per-verse translations, explanations, four reciter choices and original eQuran scan reader retained. Ossi/Dosari remain full-surah when reliable verse timing is absent.
- Practice notes link to Muslim 804a, Bukhari 891 and Tirmidhi 2891. No authenticated fixed-time Yasin/Waqiah wealth claim is invented.
- Native MP4/audio import, audio-only playback of the same supplied file, native timeline/volume controls, local save and standard/WebKit PiP API calls.
- Native players stay mounted across navigation. Duplicate progress work removed, hidden-page YouTube UI updates skipped, publisher audio preloading reduced.
- Additional source-identified YouTube videos for Ya-Sin, Ar-Rahman and Al-Fatihah. Their full-surah ranges are not presented as exact excerpts. No global viral rank or live view count is claimed.

## Verification recovery

The earlier CI failed waiting for video readiness before a Play click in bundled Chromium. The revised test uses installed Chrome/Chromium where available, explicitly clicks Play, records codec support/errors, and still requires real H.264/AAC playback, advancing time, seek, audio-only switching, and local save. An isolated browser check of the actual application decoded a synthetic MP4 successfully. CI remains the production gate.

Build: node build.mjs && node upgrade.mjs && node community-build.mjs
Unit checks: node --test tests/community.test.cjs tests/repair.test.cjs
Browser checks: tests/browser.py, tests/ios-webkit.py, tests/community-browser.py, tests/embed-audit.py

## Honest remaining work

- The exact permitted Ibrahim Idris video has NOT been uploaded to this conversation. Ask for one MP4 with its sound; a separate MP3 is optional. No YouTube audio has been extracted or rehosted.
- Local import is private to the device, not public hosting for other visitors. Public distribution requires the supplied file and a suitable hosting step.
- Physical iPhone lock-screen/background/PiP testing has NOT been performed. Do not present emulation or a PiP method spy as proof of OS behavior.
- YouTube embedding remains subject to YouTube/browser/account restrictions. In-page floating is not operating-system PiP.
- The full-surah video expansion is not a complete video catalogue for all 30 passages. Some entries still use source/search links.
- Exact publisher translation text is kept separate from editorial guide summaries. Do not label the summaries as verbatim tafsir.

## Sources

https://quranenc.com/
https://www.equraninstitute.com/quranreading/index.htm
https://sunnah.com/muslim:804a
https://sunnah.com/bukhari:891
https://sunnah.com/tirmidhi:2891
https://surahquran.com/video-sheikh-127-sora-36-en.html
https://surahquran.com/video-sheikh-127-sora-55-en.html
https://surahquran.com/video-sheikh-127-sora-1-en.html
