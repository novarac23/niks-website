# SEO Roast Roadmap: novarac.com (2026-11-24)

Verdict: Crawling works. Dotted’s local overview under-explained the product, and its launch post bypassed that overview.

This is a personal maker site, not a SaaS sales funnel. The primary conversion audited is a visit to Dotted’s App Store listing; downloads, purchases, and revenue were not measured. The pages that matter most are `/apps/dotted/`, the external product homepage at `https://dotted.novarac.com/`, and the latest post at `/blog/2026-11-21-comeback/`.

No confirmed fatal crawl blocker was found. This does not establish that Google or Bing has indexed the pages. Local fixes below have not been pushed or deployed, and no PR has been opened. The product subdomain was inspected read-only because its source is outside this repository.

## Prioritized work

Rows are ordered by the first practical action that can improve or diagnose the path to an app download. “Revenue impact” describes the opportunity; it is not a measured loss or forecast.

| # | Tier | Issue | Revenue impact | Fix / first action | Owner | Status |
|---|---|---|---|---|---|---|
| 1 | REVENUE | Actual indexation and search demand for the two app pages are unverified. The search tool returned no matches for the app-specific `site:` queries. | If an app page is not indexed, it cannot bring search visitors to the download link; its actual status is unknown. | Inspect both URLs in Search Console, confirm the selected canonical and last crawl, submit each host’s sitemap, and export 90 days of page/query data. Use URL Inspection results rather than treating an empty search result as proof of deindexation. | Nikola | Next; needs Search Console access |
| 2 | REVENUE | The app overview used the vague title “Dotted — Time in dots” and only the personal story and screenshot captions to explain the app. | Visitors arriving without product knowledge had less text explaining whether Dotted met their needs. | Changed the title to “Dotted Line — Time Progress & Countdown Widgets”; added a short factual product summary and the free/Premium distinction, with a matching description. | Codex | Fixed locally; deploy through the existing workflow |
| 3 | REVENUE | The launch post’s Dotted heading linked straight to Apple. Only the homepage and app catalog linked to the local overview in main content. | Readers who wanted more detail had no contextual path to the site’s app overview from the launch story. | Pointed the heading at `/apps/dotted/`; retained the separate direct download link. Unique main-content source pages increased from 2 to 3. | Codex | Fixed locally; deploy through the existing workflow |
| 4 | REVENUE | The external marketing homepage shows widgets and Mac support without explaining the free/Premium split there. Its support page explains Premium, and the App Store explains the free tier. | Someone interested in a widget has to leave the landing page to learn it requires a purchase. | In the product website’s own repository, add a short free/Premium explanation beside its download action, matching the App Store and the English/German support pages. Keep exact regional prices on Apple unless price maintenance is explicitly owned. | Nikola | Next; outside this repository |
| 5 | COMPOUNDING | No verified backlink or ranking baseline exists in this audit. | Outreach spend could target the wrong bottleneck before indexation and relevant search demand are understood. | Connect Ahrefs, compare the three product peers below, and count unique dofollow, editorial, in-content referring domains with referring-page traffic above 10. Exclude farms and sitewide links; calculate a link gap only after obtaining the numbers. | Nikola | Unmeasured; Ahrefs available but not connected |
| 6 | COMPOUNDING | The marketing homepage’s observed links do not identify the maker site as the author’s home. | Product discovery has a weaker path back to Nikola’s other work and writing. | Consider one useful branded author link from the product website to the existing About page; review the App Store Connect marketing URL. Do this in the relevant product/account, without adding keyword-stuffed badges or fake public share pages here. | Nikola | Optional; outside this repository |
| 7 | COMPOUNDING | Search-led content opportunities have not been validated against real queries. | Broad new articles could consume writing time without attracting people who want this app. | After the Search Console export, choose one relevant task, such as adding a countdown widget, and improve the existing product support guide with real steps/screenshots. Do not turn historical personal posts into unrelated product pitches. | Nikola | After measurement; candidate topic, not verified demand |

The three-inlink check is an audit heuristic, not a Google ranking requirement. These changes provide clearer content and navigation; they do not guarantee rankings or purchases. The first row is a measurement gap, not a confirmed fatal issue.

## Six-point audit evidence

### 1. Crawl, locales, SafeSearch, and real 404s

- `https://novarac.com/robots.txt` returns 200 and default-allows crawling. Its sitemap line points to valid XML containing 15 URLs.
- All 15 live sitemap URLs returned HTTP 200, with exactly their own canonical URL and no observed `noindex` directive. This includes all 10 published posts; there was no need to invent a 20-page sample.
- An unknown path on both `novarac.com` and `dotted.novarac.com` returned 404. The app subdomain’s sitemap and robots.txt also returned XML/text respectively, not a homepage fallback.
- HTTP and `www` each normalize to `https://novarac.com/` in one HTTP redirect. A query variant of the app overview retains the clean canonical URL.
- The maker site has one language. The product website has English and German, with three reciprocal sets for home, support, and privacy. Both pages in each pair returned 200 and emitted matching `en`, `de`, and `x-default` alternates. The observed German content is translated; there is no locale sprawl requiring removal.
- The repository publishes app screenshots, a portrait, a sunrise, and historical article figures. It has no user-upload system or obvious adult media. A controlled SafeSearch on/off comparison was unavailable, so the site’s SafeSearch classification is unverified.

Crawl eligibility is not the same as inclusion in results. [Google’s technical requirements](https://developers.google.com/search/docs/essentials/technical) distinguish access and indexable content; [URL Inspection and sitemap submission](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl) are the appropriate next checks. Reciprocal alternates follow [Google’s localized-page guidance](https://developers.google.com/search/docs/specialty/international/localized-versions).

### 2. Programmatic traps and conflicting counts

This repository builds fixed pages and Markdown posts with Python’s standard library. There are no search/filter result pages, entity-ID routes, database-generated location pages, dynamic locale middleware, or FAQ/count factories. Date-prefixed article filenames are descriptive post slugs, not opaque entity IDs; renaming them would create needless migration work.

All current posts were represented in the sitemap, while the writing template stayed excluded. The 20 historical compatibility pages remain outside the sitemap. Existing RSS identifiers and imported article bodies were preserved.

### 3. Layout and demo access

The source places the app title, story, app description, real download links, and screenshots in HTML. No login, demo booking, map, or hero video blocks the download path. No replacement calculator, signup flow, badges, or new JavaScript was warranted.

Browser preview tools were unavailable. Placement at 1366 × 768 and 390 × 844 was therefore **not visually verified**. Source and CSS checks confirm the existing shell, 700px phone breakpoint, wrapping action buttons, and the existing four-column/horizontally scrolling screenshot gallery; they do not prove above-the-fold pixel positions. One desktop/phone review after deployment remains a manual check.

### 4. Authority and competitor reality

No connected Ahrefs, DataForSEO, or Search Console data was available. Plugin discovery found Ahrefs available but not connected; no paid query, subscription, outreach, or account change was performed. **DR, organic keyword totals, clean referring-domain counts, and the numerical link gap are unknown.** There is no evidence here that the site has inflated authority or that buying links is the answer.

Three verified product peers for a later comparison:

| Peer | Official page | Useful comparison | Authority data |
|---|---|---|---|
| Pretty Progress | [prettyprogress.app](https://prettyprogress.app/) | Explicit countdown/widget positioning and a real widget setup guide. | Not measured |
| Day Progress | [sindresorhus.com/day-progress](https://sindresorhus.com/day-progress) | A personal maker page explains its menu-bar use case, purchase model, and limitations. It is a Mac-focused adjacent product. | Not measured; distinguish this page from its author’s much broader domain |
| TimeDots | [Official App Store listing](https://apps.apple.com/us/app/timedots-countdown-widget/id6758563521) | Closely related dot-based time progress and countdown widgets. | Not measured; identify its own marketing domain before comparing backlinks, rather than using apple.com’s DR |

These pages establish relevant peers, not their ranking positions. Product share cards are image outputs, not public indexable web pages; a generic “Powered by” embed would not create a useful backlink loop for this site.

### 5. AI access, product identity, and pricing

Googlebot, Bingbot, GPTBot, OAI-SearchBot, PerplexityBot, and ClaudeBot user-agent probes received 200 and byte-identical HTML for the local app page. Four AI user-agent probes also received byte-identical HTML from the product homepage. This tests access from the audit network, not verified crawler IPs, crawl history, or actual AI citations.

The local overview now names the app, its time progress/countdown use, daily intentions, widgets, and the free/Premium split in visible HTML. The [official App Store listing](https://apps.apple.com/us/app/visual-time-dotted-line/id6760857931), checked November 24, 2026, says the core app is free on iPhone/iPad and a one-time Premium purchase unlocks widgets, custom colors, and Mac. The existing [public product support page](https://dotted.novarac.com/support/) also explains Premium and widget setup without login.

No regional dollar price was hard-coded, no review/rating claims were added, and no separate pricing page or `llms.txt` file was needed to fix the observed navigation and product-description issues. Structured data is optional follow-up, not a substitute for the visible explanation or verified indexation.

### 6. Indexation and internal links

Both app URLs are in their own host’s sitemap, return 200, and self-canonicalize. The maker homepage links directly to `/apps/dotted/`; that overview has real anchors to the marketing site and Apple. The launch post now links to the local overview as well as its existing direct download link.

| Target | Before: unique main-content source pages | After, local | Sources after |
|---|---|---|---|
| `/apps/dotted/` | 2 | 3 | `/`, `/apps/`, `/blog/2026-11-21-comeback/` |

Navigation, headers, footers, self links, redirect pages, and drafts are excluded. Repeated links from the same source count once. These are site-structure counts, not traffic-weighted link values; there is no evidence that the latest post is the highest-traffic article.

## Verification and handoff

- Normal build: 16 canonical/error pages, 10 published posts, 20 preserved legacy redirects; 15 sitemap entries.
- All 30 existing tests passed. Generated canonical URLs, local links, image paths, anchor targets, and draft exclusion were checked.
- Impeccable’s scan of the changed builder and post returned no deterministic findings. The existing identity, personal story, screenshot assets, portrait, favicon policy, analytics, and layout were preserved.
- Full before/after graph: `internal-link-graph.before.json` and `internal-link-graph.json`. Measurement snapshot: `roast-evidence.json`. Reviewable PR description: `fix-pr.md`. The described changes are local; no push, PR, deployment, DNS edit, or external app-site change occurred.

After the user’s normal deployment, fetch the app page and launch post again, confirm the new title/summary/internal link, inspect both app URLs in Search Console, and record a baseline. Do not report an uplift until there are actual clicks/download data.

## Fluff

Optional social preview imagery, article/author structured data, and small metadata refinements can wait; they were not used to distract from product clarity, navigation, and the missing search-performance evidence.
