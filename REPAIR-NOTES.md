# Famous Quran v3 repair

The requested featured recording is Qari Ibrahim Idris, Al-Furqan 25:61-77, YouTube `K1cA-E6MoBU`. The second Ibrahim prayer recording is `z0KNzQCA8d4`, starting at 13:20. The saved study range remains 25:63-77 so existing notes are preserved. Video ranges are separately labelled.

## Changes

- Visible 16:9 YouTube player with poster, explicit origin/referrer and reported player errors.
- Removed the unrelated general publisher video collection from passage view.
- Requested full-surah reciters resolved from actual MP3Quran metadata: Mishary, Sudais, Al-Ossi, Yasser Al-Dosari and Al-Luhaidan.
- Added Sudais and Maher to verse-by-verse playback using published edition identifiers.
- In-site original Mushaf images with zoom, wide mode, page selection, back and offline scan saving.
- Light/dark/system theme with persistent choice. Existing notes, hadith favorites and offline data retained.

## Media

YouTube video playback is online; it is not a downloadable MP4. Publisher MP3 saving and user-supplied permitted video/audio imports remain separate. A different studio MP3 must never be described as the audio of a viral video. No ripping service or access-control bypass is included.

## Supabase

The owner-approved free project `famous-quran` was created in `blackchoco`, Tokyo region. `fq_backups` and owner-only row security were applied. A transactional two-user test verified isolation, blocked cross-user writes, and allowed owner updates; test data was rolled back. The security advisor returned no database lints.

Google/email sign-in is not declared live: Google OAuth provider credentials, production redirect allowlist and production email delivery still need account-level configuration. Do not commit Google client secrets, SMTP passwords, service_role keys or access tokens. Google callback: https://qzamdjcguksgzqcdaosd.supabase.co/auth/v1/callback

## Verification

Build validation and unit tests are distinct from browser regression fixtures. The workflow separately records a real public-source HTTP audit and a real browser attempt. A successful build or HTTP 200 does not prove YouTube playback. Read the individual reports before claiming completion.

The previously generated dashboard artwork was a concept, not a screenshot of shipped functionality. No generated Quran page is used in the reader.
