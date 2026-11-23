# Smart Seller Lab — Single Release Gate

Current status: HOLD (not Amazon-ready, not indexable). No automatic release authorization.

## Current production preview
- Cloudflare Pages URL: https://smart-seller-lab.pages.dev/
- Git branch: feat/affiliate-site-v1; PR #1 Draft
- Existing Cloudflare configuration deploys static source root, not generated dist.
- Do not change Cloudflare output directory or deploy generated release artifacts without Owner approval.

## One-command offline QA on Mac
```bash
python3 scripts/check_site.py
python3 scripts/build_site.py --site-url https://smart-seller-lab.pages.dev --output dist
python3 scripts/check_site.py
```
This generates a **preview** dist folder with robots Disallow and noindex retained. It does not deploy.

## Release artifact only after final content/legal QA and explicit Owner GO
```bash
python3 scripts/build_site.py --site-url https://smart-seller-lab.pages.dev --output dist --release
```
Before deployment, validate generated dist contains 15 HTML pages, a sitemap, canonical URLs and robots Allow. Deploy **dist** only after updating Cloudflare Pages output directory in an approved release operation. Avoid deploying the raw source root after release or SEO will revert to noindex.

## Hard gates
1. Review every article for sufficient original depth, accurate sources and absence of fabricated testing.
2. Verify contact email works and legal/privacy disclosures match actual Cloudflare hosting and any tracking integrations.
3. Check local and hosted 320/390/768/1536px layouts, Safari, Chromium, keyboard, links and screenshots.
4. Confirm Cloudflare deployment full SHA equals the intended commit, HTTPS and 200 responses for all pages.
5. Confirm the live HTML no longer has noindex and live robots allows indexing; verify sitemap and canonical host.
6. Only then set up Google Search Console and start Amazon Associates registration with real Vietnamese identity, tax interview and payout methods shown in the account.

No Amazon Associates enrollment, payouts, or Google indexing have been performed by these code changes.
