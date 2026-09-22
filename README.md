# Famous Qur'an - v2

A static, local-first recitation and study library. Primary languages: English, Bangla and Japanese. Build with `node build.mjs` (Node 20+). Deploy only `public/`.

## Features

- Existing 30 passage collection and existing local favorite/note keys retained.
- Verse-by-verse pronunciation with Alafasy, Husary and Minshawi; repeat and sequential playback.
- Translations: QuranEnc `english_rwwad`, `bengali_zakaria`, `japanese_saeedsato`. Source notes are shown separately from translations.
- Bangla Al-Mukhtasar; English Ibn Kathir through Al Furqan API; Japanese uses the translator's explanatory notes, not falsely labelled Ibn Kathir.
- MP3Quran full-surah reciter catalogue, with Luhaidan, Yasser Al-Dosari and Mishary prioritized when available. These are not advertised as cropped excerpts or identical social-video performances.
- Al-Furqan source embeds for Muhammad Al-Luhaidan and Omar Hisham Al Arabi. Existing YouTube recordings retained.
- MP3Quran's general publisher video catalogue is explicitly separate from exact-passage clips.
- On-device media downloads; complete responses only; 100 MB cap; repeat saves reuse existing bytes. Audio-only playback from a video does NOT convert it to MP3.
- Local import of permitted audio/MP4/WebM without uploading to any server.
- HadeethEnc category and page browsing, shuffle batches, individual favorites, Save all six, and saved source details for offline reading. Availability varies by language.
- Versioned service-worker app shell, explicit reading/audio saves, offline inventory, export/delete, storage estimates and optional persistent-storage request.
- SVG logo, PNG home-screen icons, 1200 x 630 sharing image, manifest and Open Graph metadata.
- Local JSON export/import of notes and favorite IDs. Restore merges without overwriting existing notes. Media and hadith full-text snapshots are not included in this small notes backup.

## Offline operation

Open online first, save reading/audio, then reopen the installed site or its bookmarked URL. Unsaved remote content, social embeds, account login and first-time downloads require a connection. Offline storage is per browser/device/origin and may be cleared by the user or browser. External Mushaf pages remain online links. Public JSON is cached separately from private authentication responses. Close existing site tabs and reopen to activate a newly installed worker.

## Authentication: prepared, not yet activated

The Supabase connection has no project yet. Do not show a pretend login state. Without the public build variables below, Account displays a truthful setup notice and working local backup tools.

1. Obtain owner approval for the Supabase organization and project cost.
2. Create the approved project; apply `supabase/schema.sql`; inspect RLS advisors.
3. Configure Site URL and redirect allowlist for the actual Vercel production URL. Configure email delivery and rate limits suitable for production.
4. Set `PUBLIC_SUPABASE_URL` and `PUBLIC_SUPABASE_PUBLISHABLE_KEY` in Vercel and rebuild. Never use service_role or secret keys.
5. Google sign-in additionally requires the owner's Google OAuth client configuration in Supabase. Set `PUBLIC_GOOGLE_SIGN_IN=true` only after that provider is configured.
6. Test email delivery, PKCE return, sign-out, two-user row isolation and explicit cloud backup/restore before declaring auth live. Authenticator-app MFA is not implemented in this release.

Cloud backups are explicit, not silent cross-account synchronization. Local browser data remains local when signing out.

## Source integrity and media rights

QuranEnc: https://quranenc.com/en/home/api
HadeethEnc: https://hadeethenc.com/en/home
AlQuran Cloud: https://alquran.cloud/api
MP3Quran: https://www.mp3quran.net/eng/api
Original scan source: https://www.equraninstitute.com/quranreading/index.htm

Source translations are not generated or rewritten. Publisher attribution is retained. No AI-written religious text is substituted when an API fails. The pre-existing collection's editorial English recitation notes are explicitly labelled. Historic unverified popularity metrics are not displayed in v2.

Social uploads are embedded, not copied or redistributed. Download controls use provider media URLs or files supplied by the user. Source download permission and browser CORS determine whether saving succeeds. No YouTube/TikTok/Instagram ripping service, DRM bypass or paywall bypass is included. Public video catalogue entries are not claimed to match the selected verses unless independently identified.

## Verification

Each build fails on invalid JavaScript, missing required language strings, invalid/missing passage ranges or missing local assets. It also runs service-worker logic tests in a Node VM, including offline shell fallback and authentication exclusions. This is NOT a substitute for a live browser/network/media/authentication integration test. `public/release.json` reports the deployed commit and checks. Browser navigation and external networking were restricted in the authoring environment; do not mislabel mock tests as live API validation.
