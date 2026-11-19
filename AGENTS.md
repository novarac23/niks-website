# Working on Nik’s Website

Read [PRODUCT.md](PRODUCT.md), [DESIGN.md](DESIGN.md), and [site/README.md](site/README.md) before changing the site. These files record decisions Nikola made during the redesign. The user's current instructions take precedence; update the records when an intentional decision changes.

## Project and implementation

This is Nikola's personal website at `https://novarac.com`, with independent apps, writing, and an About page. The displayed name is **Nik’s Website**. It is a personal maker site, not an agency landing page.

- Build from the repository root: `python3 site/scripts/build.py`.
- Run checks: `python3 -m unittest discover -s site/scripts -p 'test_*.py' -q`.
- Optional local preview: `python3 -m http.server 8080 --directory site/dist`.
- Python 3.9+ and its standard library are sufficient. Python builds the site; the deployed pages require no Python server.
- Edit `site/scripts/build.py` for page content and markup, `site/src/templates/base.html` for the shared shell, `site/src/styles.css` for styling, and `site/site.json` for configuration.
- Write posts in `site/content/posts/`. `site/dist/` is generated; never make source changes there. Preserve the content-based stylesheet version in the builder/template so browsers refresh changed CSS.
- Keep the published site static. The hamburger uses native `<details>` and needs no JavaScript. Do not introduce a framework, runtime, database, dependencies, analytics, or hosted form service without a concrete user requirement.

## Design workflow and Impeccable

Use the installed **Impeccable** skill for substantial interface work. Its installation path is machine-specific; discover it from the current skills catalog rather than hard-coding a path from the original workspace. Follow its setup and relevant playbook, then read its craft floor before UI edits. If it is unavailable, say so and use DESIGN.md as the project-specific fallback.

Preserve the approved design for refinements. A request to adjust copy, spacing, or one component does not authorize a new visual identity. Use real app assets and the existing portrait. Prefer typography, alignment, spacing, and useful content over decoration. Avoid generic marketing copy, repeated cards, ornamental icons, oversized statistics, gradient text, or unnecessary animation.

Check the affected desktop and phone layouts in one bounded pass when browser preview is available, fix observed issues together, and stop after confirmation. If browser tools are unavailable, validate the build, generated markup, links/assets, and responsive CSS; report that visual verification was unavailable. Do not claim a browser check occurred. Do not install or improvise preview infrastructure merely to repeat a failed browser attempt.

## Decisions to preserve

- No company branding, astronomical art, header star, welcome slogan, or custom favicon. Every HTML page, including legacy redirects, declares `<link rel="icon" href="data:,">`.
- Header navigation: Home, Apps, Blog, About, Contact Me. Contact Me is a normal menu item after About and uses `mailto:`. On phones the hamburger reveals the same links and changes to a close icon.
- All contact links use the configured address, currently `nikola.novakovic@proton.me`. The user accepted publishing it. Do not replace it with an alias or form without being asked.
- Footer: site name on the left; `@ YEAR` on the right, generated from the current year. The literal `@` is intentional. No footer Email link, personal name, or company attribution.
- Homepage: introduction, Apps, Recent posts. No hero buttons, rule beneath the introduction, decorative illustration, or “how I work” section.
- Recent posts: date left, title right, three latest posts. No subtitles, categories, or reading times in this homepage list. The full Blog page retains its summaries and metadata.
- App rows link to local `/apps/dotted/`; no redundant “View app” label. Dotted's detail page links to both its marketing site and the App Store, and shows four real screenshots instead of a feature list.
- About: heading above the layout, portrait left and all biography/contact copy right on desktop. At 700px and below, the portrait may stack above the text. Preserve the X link.
- Avoid diminutive filler such as “little” in new general site copy. The user's approved Dotted story intentionally says “how little time we have”; retain that exception and do not silently rewrite author content.

## Content and migration

Nine published posts were migrated from the previous Jekyll site, using its content rather than its theme. Preserve original dates, article content, image paths, feed identifiers, and legacy redirects. See `site/MIGRATION.md` and `site/content/novarac-migration.json`. Do not rerun the importer against edited posts unless asked.

For new posts, copy `first-post.md`, update front matter, write Markdown, and set `draft: false` when ready. Drafts and future-dated posts stay out of production. Python code fences receive build-time highlighting; `text` fences represent output. The renderer supports a documented Markdown subset, not all CommonMark or arbitrary HTML.

## Deployment and handoff

The user deploys through the existing `niks-website` GitHub repository. `.github/workflows/github-pages.yml` tests, builds, and publishes `site/dist/` on pushes to `master`. Pages must use GitHub Actions and the custom domain `novarac.com`. Retain the destination checkout's `.git`. Old Jekyll files can remain because the workflow publishes only the new output.

Do not push, change DNS, or deploy merely because local edits are complete. The user has been handling publication separately. Preserve real app URLs in `site.json`; configuring `dotted.novarac.com` is a separate hosting/DNS task.

When asked for ZIPs, refresh `novarac-source.zip` with root documentation (including this file, PRODUCT.md, DESIGN.md, and `.impeccable/design.json`), `.github/`, `.gitignore`, and `site/` source/configuration. Exclude all `.git` directories, `.openai`, generated output, caches, previews, and ZIPs. `novarac-static.zip` contains the contents of `site/dist/`, including `.nojekyll`, but excludes the builder marker. The older `nova-software-static.zip` filename is a compatibility copy, not website branding. Verify archives and, for source handoffs, check that an extracted copy builds independently of sibling repositories.
