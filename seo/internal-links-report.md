# Internal links report

Run: 2026-11-24. One post edited; one existing link retargeted; no callouts added.

| Target | Before: unique main-content sources | After, local | Added source |
|---|---|---|---|
| `/apps/dotted/` | 2 | 3 | `/blog/2026-11-21-comeback/` |

The launch post’s “Dotted Line” heading now links to the local app overview instead of directly to Apple. Its separate “download the app” link still goes directly to the App Store. The existing heading and prose were retained. This is the one relevant product target, so no unrelated link or generic callout was added to meet a quota.

Existing sources are `/` and `/apps/`; the target is one click from the homepage. All three links are real HTML anchors without `nofollow`. No historical article was rewritten, no category/hub pages were added, and no generic marketing blocks were inserted.

Counts use the built production sitemap and rendered HTML, which captures Python-generated links and relative Markdown URLs. The generic Node/MDX graph recipe was adapted to a standard-library HTML pass because this project deliberately has no Node requirement. Only links inside `<main>` and outside headers, footers, and navigation count. Each source counts once; self links, drafts, and redirects are excluded.

The two graph snapshots record the complete set of canonical pages, including ordinary posts with fewer than three inbound sources. That threshold was evaluated only for the app overview; it is an audit heuristic, not a Google rule. The target has no remaining gap under that heuristic. Search Console traffic was unavailable, so this change was selected for direct topical relevance, not claimed traffic volume.

The source graphs are `internal-link-graph.before.json` and `internal-link-graph.json`. Local link/asset checks pass. The third source link is not live until the user deploys these changes.
