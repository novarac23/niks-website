# Nik’s Website

<!-- impeccable:product-schema 1 -->

## Platform

web

## Product Purpose

Nikola's personal home on the web: introduce his background, show software he has built, and share his thoughts through a blog. The canonical domain is `https://novarac.com`; the visible name is **Nik’s Website**. Visitors should be able to understand who Nikola is, explore an app, read a post, or contact him directly.

## Positioning

Nikola is a software engineer, data scientist, and independent app developer. The homepage states 10 years building software and 5+ years working in data science. The voice is first person, straightforward, personal, and modest. Do not add unverified employers, achievements, revenue, customer counts, testimonials, or service offerings.

## Operating Context

The site is a static replacement for the existing Jekyll-based `niks-website` repository. It uses a dependency-free Python builder, HTML templates, CSS, and Markdown posts. GitHub Actions builds and deploys on `master`; the live host serves static files. A local HTTP server is only an optional preview tool.

The redesign began as a small company website under Nova Software LLC, with an astronomical nova motif. Nikola preferred Sindre Sorhus's personal independent-developer approach, while wanting a fuller homepage and a blog. The identity shifted to **Nik’s Website**, and company branding and the nova illustration were removed. Subsequent Impeccable cleanup simplified the visual hierarchy: plain app rows, compact recent posts, deliberate dividers, fewer buttons, no ornamental header star, and no custom favicon. These are completed decisions, not a request to recreate earlier versions.

The old site's nine posts and their five referenced images were migrated without copying its visual theme. Its About portrait was subsequently reused. Dotted's feature list was replaced with original app screenshots. The user approved the current site and intends to transfer the source ZIP into the existing GitHub checkout.

## Capabilities and Constraints

| Route | Purpose |
| --- | --- |
| `/` | Personal introduction, app listing, three recent posts |
| `/apps/` | App catalog; subtitle: “Here is the software I’ve built.” |
| `/apps/dotted/` | Personal app story, marketing/App Store links, screenshots |
| `/blog/` | Published writing and RSS link |
| `/blog/<slug>/` | Individual Markdown article |
| `/about/` | Portrait, biography, X profile, email contact |
| `/feed.xml` | RSS 2.0 with full published posts |
| `/sitemap.xml` | Canonical page inventory |

Directory index pages, a 404 page, and 20 legacy redirect pages support static hosting. New posts enter the homepage, Blog page, RSS, and sitemap after rebuilding. Draft and future-dated posts are excluded. Blog code is highlighted during the build. The native hamburger and screenshot scrolling require no JavaScript.

Contact is `nikola.novakovic@proton.me`. X is `https://x.com/novica93`. Keep these configurable or explicitly authored; do not invent replacements.

## Brand Commitments

Keep the site centered on Nikola and his actual work. No visible Nova Software/company attribution. The footer is the site name plus `@ YEAR`. Do not revive removed sections or marketing language as incidental “polish.” The approved palette, layout, and component details are in DESIGN.md.

Homepage introduction:

> I’ve spent 10 years building software and 5+ years working in data science. Here you’ll find what I’m currently working on and my thoughts on different subjects.

Dotted story:

> After my son was born, I quickly realized how little time we have on this earth and how quickly it passes. I built Dotted to remind myself of that and to live each day with intention.

## Evidence on Hand

- Dotted's real icon: `site/src/assets/dotted-icon.png`.
- Four original iPhone screenshots: `site/src/assets/dotted/`; source paths and hashes are recorded in `sources.json`. They show time progress, countdowns, daily intentions, and Home Screen widgets.
- Dotted marketing URL: `https://dotted.novarac.com`; future domain/service setup is separate from this website.
- App Store URL: `https://apps.apple.com/app/id6760857931`, sourced from Dotted's existing share-link code and checked against its official listing during the redesign.
- Portrait: unmodified 340 × 340 `site/src/assets/img/8-0-2.jpg`, originally used by the old About page.
- Nine migrated posts, image assets, and compatibility metadata: see `site/MIGRATION.md`.

## Product Principles

1. Make the personal connection clear before presenting the apps and writing.
2. Let real software, screenshots, and articles carry the site.
3. Keep publishing straightforward: write Markdown, commit, and push.
4. Preserve static hosting and portable source; avoid unnecessary infrastructure.
5. Keep accessibility and responsive behavior intact as the content grows.
