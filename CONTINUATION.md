# Community reading and native media checkpoint

## This release

- Existing passage IDs 1-30 and storage keys retained.
- Source-based short reading guides in English, Bangla and Japanese. These are labelled paraphrases, not quotations or independent scholarly tafsir.
- Separate complete-surah cards: Ya-Sin, Ar-Rahman, Al-Waqiah, As-Sajdah, Al-Mulk and Al-Fatihah.
- Existing per-verse text, translation, explanation and reciter integrations reused; Al-Ossi and Al-Dosari remain clearly labelled full-surah audio where verse timing is unavailable.
- Original eQuran scan sections linked in the existing reader.
- Practice notes distinguish Quran-wide encouragement (Muslim 804a) from specific reports: As-Sajdah in Friday Fajr prayer (Bukhari 891), and Al-Mulk intercession (Tirmidhi 2891, Hasan/Darussalam).
- No unverified after-Fajr Ya-Sin or after-Maghrib Al-Waqiah wealth promise is presented as an authenticated instruction.
- User-permitted local MP4/audio input, permanently mounted native players, audio-only mode, standard/WebKit system-PiP calls, local save, native seek and volume controls. Files are not silently uploaded or published.
- Stable audio node during navigation; duplicate UI progress callbacks removed; hidden-page YouTube UI refresh skipped; publisher audio no longer preloads every track. These are performance changes, not a guarantee about device temperature.

## Not completed / must not be misrepresented

- The requested Ibrahim Idris performance has not been supplied as a permitted MP4 file. No YouTube recording has been extracted or rehosted. Request one permitted source MP4 from the user; ffmpeg can produce the audio copy once supplied.
- Local file import does not make a recording available to other visitors. Public hosting requires the actual permitted file and an explicit publication decision.
- A physical iPhone screen-lock/background/PiP test has not been performed. Browser profiles and synthetic fixtures are not physical-device tests.
- The YouTube player cannot be forced into system PiP by a parent page. In-site floating mode is not OS-level PiP.
- New full-surah cards use identified publisher audio and YouTube search links. Additional popular-video IDs for other surahs have not been individually researched in this release.
- Native audio-only MP4 playback does not create an exported MP3 file.

## Build and tests

Run `node build.mjs && node upgrade.mjs && node community-build.mjs`, then both Node test files. The final build layer makes checked patches to generated public files and updates the service-worker revision.

CI preserves existing browser/source checks and adds `tests/community-browser.py`. That test distinguishes controlled data fixtures, synthetic H.264/AAC decoding, and actual-device verification.

## Sources

- https://quranenc.com/ (translation titles and verse-level sources remain shown in the reader)
- https://www.equraninstitute.com/quranreading/index.htm
- https://sunnah.com/muslim:804a
- https://sunnah.com/bukhari:891
- https://sunnah.com/tirmidhi:2891
