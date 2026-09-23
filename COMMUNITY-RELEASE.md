# Community study release

## Source-first reading

The original thirty passage IDs and local notes keys remain unchanged. Seven complete-surah entries use separate IDs 101-107: Ya-Sin, Ar-Rahman, Al-Waqiah, As-Sajdah, Al-Mulk, Al-Kahf and Al-Insan. Full-surah reading is paginated in groups of twenty ayahs.

Introductions use brief editorial theme headings and selected **publisher translation text**, not generated tafsir. Each excerpt links to its exact surah, ayah and edition. Extended explanations are loaded only when expanded. QuranEnc editions: English Rowwad, Bengali Zakaria, Japanese Saeed Sato; Bengali and Japanese Al-Mukhtasar explanations. English Ibn Kathir remains sourced via Al Furqan API. Text and footnotes are not rewritten.

Recitation guidance is labelled as source-based editorial notes, with named grading sources. General encouragement to learn is not presented as a special reward for every passage. Yasin-after-Fajr claims and the weak Waqiah-poverty report are not advertised as established guarantees. Friday Fajr As-Sajdah/Al-Insan refers to the prayer itself. Al-Kahf and Al-Mulk evidence is attributed to the named reports; a virtue is not an obligation. HadeethEnc supplies hadith text and explanation when that language exists; unavailable-language responses are shown as unavailable, not translated anonymously.

## Media

The new native player accepts a permitted MP4 or audio file, keeps its media element permanently mounted, uses standard browser/Safari native PiP methods for video, and supports the same file's audio track. File import is **local**, not a public upload. Public exact-performance media is pending the owner's permitted source file. This release does not download, extract or rehost the Ibrahim Idris YouTube performance.

Native OS PiP is not the same as a floating YouTube iframe. iPhone device-volume controls, lock-screen continuity, codec support, publisher embed restrictions and device temperature are not guaranteed by desktop or emulated tests. There are no silent loops to bypass browser suspension. Timers for visual progress stop in the background. Audio elements are no longer reparented when a reading window closes.

More video choices are discovered only on fixed publisher pages and checked against primary YouTube oEmbed titles/reciter information. No universal viral ranking or invented view counts are added. Source recordings may cover a full chapter, not the exact selected ayah range.

## Verification

- Build checks: all 37 guide maps, bounds, three language dictionaries, public assets and original note IDs.
- `tests/community-browser.py`: controlled source fixtures and a real 20-minute synthetic H.264/AAC test file. Tests native playback, seek to minute 15, same-source continuity, audio-only mode, paging and mobile width. Synthetic media is not a Quran recording and is not deployed.
- `tests/community-sources.mjs`: read-only publisher availability audit across translation editions, explanation samples, hadith language availability, original scan manifests and additional video metadata.
- Existing browser/WebKit tests remain in CI. Physical iPhone PiP/lock-screen/thermal behavior still requires real-device validation.

## Primary references

- https://quranenc.com/en/home/api
- https://quranenc.com/en/browse/japanese_mokhtasar
- https://hadeethenc.com/en/browse/hadith/10113
- https://hadeethenc.com/en/browse/hadith/6260
- https://hadeethenc.com/en/browse/hadith/6265
- https://sunnah.com/bukhari:891
- https://dorar.net/h/j6ZoctCR
- https://dorar.net/h/BNYuAeoR
- https://islamqa.info/ar/answers/366252
- https://islamqa.org/hanafi/mahmoodiyah/53323/
- https://developer.apple.com/documentation/webkitjs/adding_picture_in_picture_to_your_safari_media_controls
