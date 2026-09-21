# Famous Qur'an — Recitation & Study Library

A static, source-first Qur'an recitation and study site built around a curated set of 30 passages with strong recitation arcs (setup → rise → climax).

## What is included

- Top 30 curated recitation passages with featured reciters and direct recitation searches/links.
- English, Bangla and Hindi interface.
- Ayah-by-ayah Arabic text and Mishary Rashid Alafasy audio from **AlQuran Cloud**.
- Qur'an translations from **QuranEnc**:
  - English: Rowwad Translation Center (`english_rwwad`)
  - Bangla: Dr. Abu Bakr Muhammad Zakaria (`bengali_zakaria`)
  - Hindi: Azizul Haq Umari (`hindi_omari`)
- Explanations / tafsir:
  - Bangla: QuranEnc Al-Mukhtasar (`bengali_mokhtasar`)
  - Hindi: QuranEnc Al-Mukhtasar (`hindi_mokhtasar`)
  - English: Tafsir Ibn Kathir via **Al Furqan API**, with a Quran.com Ibn Kathir link on every ayah.
- Qur'an-related hadith explorer from **HadeethEnc**, showing the source grade and explanation returned by the service.
- Original **eQuran Institute scanned Mushaf** links to preserve the exact visual reading style of the reference image.
- Favorites and personal notes stored locally in the browser.

## Why there is no database yet

The site is currently personal/static: favorites, language preference and notes are stored with `localStorage`. A hosted database would add cost, privacy surface and complexity without improving the core reading experience. A database (for example Supabase) becomes useful when cross-device sync, accounts or shared notes are requested.

## Sources

- eQuran Institute: https://www.equraninstitute.com/quranreading/index.htm
- QuranEnc: https://quranenc.com/ and https://quranenc.com/en/home/api
- AlQuran Cloud API/CDN: https://alquran.cloud/api and https://alquran.cloud/cdn
- HadeethEnc: https://hadeethenc.com/
- Al Furqan Quran API: https://alfurqan.online/docs
- Quran.com Ibn Kathir reference links: https://quran.com/

Translations and explanations remain the work of their respective publishers and are displayed with attribution. QuranEnc content is consumed directly from its API and should not be edited or paraphrased in the application.

## Deploy

The project is plain static HTML/CSS/JS. Vercel can deploy it without a build step.
