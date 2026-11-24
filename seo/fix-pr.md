# Clarify Dotted’s app overview and link it from the launch post

## SEO Roast fixes

Verdict: Crawling works; Dotted’s overview needed a clearer product explanation and a link from its launch story.

### Fatal

No confirmed fatal issue found. All 15 live sitemap URLs returned 200 with matching canonical URLs; crawl rules and real 404 behavior passed. Actual search indexation remains unverified without Search Console.

### Revenue fixes

- The app overview’s title now identifies Dotted Line and time progress/countdown widgets. A short visible paragraph explains the app and its free/Premium split, verified against the official App Store listing. The approved personal story remains intact.
- The launch post’s Dotted heading now leads to the local overview. Its direct download link remains. Unique main-content pages linking to the overview increase from 2 to 3.
- Records include a prioritized roadmap, live HTTP/crawler evidence, and before/after link graphs. No regional dollar price, schema claims, dependencies, or new tracking were introduced.

### Verify

From the repository root:

```sh
python3 site/scripts/build.py
python3 -m unittest discover -s site/scripts -p 'test_*.py' -q
python3 -m http.server 8080 --directory site/dist
```

Inspect `http://localhost:8080/apps/dotted/` for the product summary and App Store link. Inspect `http://localhost:8080/blog/2026-11-21-comeback/` for the local Dotted heading link and the retained direct download link. The local checks confirmed canonical URLs and every generated local link/asset/anchor resolve. All 30 tests passed.

Live baseline commands (run November 24, 2026; these do not deploy the patch):

```sh
curl -sS -A Bingbot https://novarac.com/robots.txt
curl -sS https://novarac.com/sitemap.xml
curl -sS -A OAI-SearchBot https://novarac.com/apps/dotted/
curl -sS -o /dev/null -w '%{http_code}\n' https://novarac.com/no-such-page-seo-roast-20261124/
```

Expected baseline: default-allow robots.txt, XML sitemap, full app HTML, and HTTP 404 for the unknown page. After deployment the app HTML should also contain the new title, product summary, and Premium explanation.

### Limits and rollout

Browser preview tools were unavailable; desktop/phone pixel placement was not visually checked. Search Console and Ahrefs were not connected, so rankings, actual indexation, link authority, downloads, and revenue changes are not claimed. The product subdomain’s code is outside this checkout; suggested work there stays on the roadmap.

This is a prepared PR description for local changes. No branch was pushed and no PR or deployment was created. A push to `master` runs the existing deployment workflow, so publication remains with the user as recorded in AGENTS.md.
