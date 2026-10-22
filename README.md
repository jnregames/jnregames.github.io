# Galaxiga — JNR Games

Bilingual, responsive game page for https://jnregames.github.io/.

## Local preview

Run `python3 -m http.server 8765` from this directory, then open http://localhost:8765/ (English) or http://localhost:8765/es/ (Spanish).

## Editing

- Page copy/markup: `tools/build_site.py`. Run `python3 tools/build_site.py` to regenerate both pages.
- Design: `assets/style.css`.
- Image assets: compressed WebP versions of the game's existing October marketing art and development screenshots.
- Video: the existing eight-second silent Unity Editor capture. No autoplay; native playback controls; preload disabled.
- Press kit: `assets/galaxiga-press-kit.zip`, with actual development screenshots and separately identified promotional art.
- `robots.txt` and `sitemap.xml` use the existing GitHub Pages hostname.

No Node build, subscriptions, tracking scripts, account system, social SDK, external font provider, or custom domain is required. Root HTML is served directly by GitHub Pages; the Spanish version is at `/es/`.

## Preserved resources

`app-ads.txt` is unchanged. Footer privacy links keep the existing working public URL `https://jnregames.github.io/game/privacy-policy.txt`; that path is outside this checkout and must remain available. Support email matches the public Google Play listing. No privacy text was rewritten.

## Release information

Upcoming changes are explicitly marked as in development. There is no promised date, update cadence, claimed full in-game Spanish localization, new-download statistic, or invented testimonial. After a tested release, update both languages together and refresh footage/screenshots as needed.

The preview clip is 1080x1920 H.264, eight seconds, silent. Its source motion was captured at 15fps and exported at 30fps with repeated frames; it is not a 30fps device-performance demonstration. Existing screenshots also show a development build. New key art/icon are promotional artwork, not gameplay captures.

## Publishing

Prepared on local branch `prepare-bilingual-game-page`, based on the repository default `JNR-Galaxiga`. Nothing has been committed, pushed, or deployed by this work.

Before publishing, sign into GitHub using a local authenticated tool or connected account with write access to `jnregames/jnregames.github.io`. Do not send a password or access token through chat. Check Settings > Pages for the actual configured source branch/folder; the public repository's default branch is not proof of the Pages publishing source. Review the prepared page, then push/merge into the configured source and verify the resulting Pages deployment. No paid hosting is needed.

Reference: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Validation performed

Both language pages rendered in Chromium, with English desktop (1440x1100) and Spanish phone (390x844) screenshots inspected. Internal file links, one H1 per page, and language attributes were checked. Existing privacy URL returned HTTP 200. `app-ads.txt` matches the checked-out original. Final Android browser playback and live Google Play navigation should be checked after deployment; no deployment or private Pages configuration access occurred.
