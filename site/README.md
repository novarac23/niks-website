# Nik’s Website

A personal website for Nikola, named “Nik’s Website,” with a homepage, app catalog, Dotted product page, about page, and Markdown blog. The design uses white, navy, and blue, with plain headings, compact app listings, and readable articles.

The published site is static HTML, CSS, and image assets. Its content and navigation work without JavaScript; the user-authorized Plausible analytics snippet loads asynchronously from the shared page template. No application server, database, or external fonts are needed. Building requires Python 3.9+ and its standard library only. There are no dependencies to install.

Contact Me follows About in the navigation and opens an email to `nikola.novakovic@proton.me`. At phone widths, a native HTML disclosure replaces the desktop navigation with a keyboard-accessible hamburger menu. Opening it reveals the same links beneath the site name; the icon changes to a close button.

All pages, including legacy redirects, declare an empty icon URL (`data:,`). No favicon images are shipped. The footer shows only the year beside the site name.

## Build and preview

From `site/`:

```sh
python3 scripts/build.py
python3 -m http.server 8080 --directory dist
```

Visit http://localhost:8080. Rebuild and refresh after editing source or posts.

## Write a blog post

1. Copy `content/posts/first-post.md` to a descriptive filename, such as `content/posts/building-dotted.md`. The filename becomes `/blog/building-dotted/`; use lowercase letters, numbers, and hyphens.
2. Update the title, date (`YYYY-MM-DD`), and description at the top. Keep `draft: true` while writing. Front matter uses one key/value per line; optional surrounding quotes are supported. Multiline values, tags, and other YAML features are not supported.
3. Write your post below the closing `---` in Markdown.
4. Preview drafts separately from the deployable output:

   ```sh
   python3 scripts/build.py --drafts --output .preview
   python3 -m http.server 8081 --directory .preview
   ```

   Open http://localhost:8081/blog/. Drafts have a visible label; all draft preview pages have `noindex,nofollow` metadata. This is a local editing preview, not access control—keep `.preview` off your host.

5. To publish, set `draft: false`, choose today's date or an earlier date, rebuild normally, and deploy `dist/`. The post automatically appears on the blog and in the homepage's latest three posts. Future-dated posts remain excluded until you build on or after their date. Removing a post or changing it back to a draft removes its generated page on the next build.

The nine existing posts from novarac.com are imported and published in the generated site. `first-post.md` remains an unpublished writing template. See [the migration notes](MIGRATION.md) for the source inventory and compatibility URLs.

### Supported Markdown

Paragraphs, headings (with linkable IDs), **bold**, *italics* using asterisks or underscores, inline code, links, images, flat ordered/unordered lists, blockquotes, horizontal rules, escaped punctuation, and triple-backtick code fences. Raw HTML is escaped. Tables, nested lists, footnotes, embedded HTML, and full CommonMark syntax are outside the small renderer's supported subset.

Put post images in `content/images/`. They are copied to `dist/assets/blog/`. Reference them from a post with `![Useful description](../../assets/blog/my-image.jpg)`.

### Code examples

Use a fence labeled `python` (or `py` / `python3`) for Python examples. The standard-library Python lexer adds syntax colors during the build. Use a `text` fence for program output; other language labels currently display escaped plain code. All code blocks have a language label, a readable monospace font, and horizontal scrolling that also works with a keyboard. There are no highlighting scripts or external assets to load in the browser.

## Routes

| URL | Content |
| --- | --- |
| `/` | Introduction, experience, featured app, and latest writing |
| `/apps/` | App catalog |
| `/apps/dotted/` | Dotted product page |
| `/blog/` | Published posts |
| `/blog/<filename>/` | Individual post |
| `/about/` | Background and contact |
| `/feed.xml` | RSS feed with the full published posts |
| `/sitemap.xml` | Canonical URLs for search engines |

All routes are generated as real directory index files, so direct links and browser refresh work on ordinary static hosting. The main domain hosts the app catalog; individual app websites can use separate subdomains.

### Separate app websites

`/apps/` remains the catalog on novarac.com. An app's own website can live separately, for example at `dotted.novarac.com` pointing to the existing Render service.

`apps.dotted.website_url` in `site.json` is currently `https://dotted.novarac.com`. The “Visit Dotted’s website” link on `/apps/dotted/` uses this setting. Beside it, “View on the App Store” uses `apps.dotted.app_store_url`, taken from the Dotted app's existing share link (`https://apps.apple.com/app/id6760857931`). Each URL can be set to `null` to hide its link. The cards on the homepage and Apps page lead to the local `/apps/dotted/` overview.

The custom subdomain is configured separately: add it to the Dotted service in Render, then add a `dotted` CNAME record pointing to the hostname Render provides at the domain's active DNS provider. This does not require hosting Dotted within the personal website. DNS and Render settings have not been changed.

## Edit the site

- `site.json`: site name (`site_name`, currently Nik’s Website), personal name (`person_name`, currently Nikola), canonical domain (`url`, currently `https://novarac.com`), and contact email (`nikola.novakovic@proton.me`).
- `scripts/build.py`: page copy, layouts, app information, and post generation.
- `scripts/highlight.py`: build-time Python syntax highlighting and code block markup.
- `src/templates/base.html`: shared header, navigation, footer, and metadata.
- `src/styles.css`: visual design and responsive layout.
- `src/assets/`: app icon and shared assets.
- `src/assets/dotted/`: original iPhone screenshots used on Dotted’s page, with their source paths recorded in `sources.json`.
- `content/posts/`: blog posts.
- `src/assets/img/`: original images used in the migrated posts, kept at their old `/assets/img/` URLs.
- `src/assets/img/8-0-2.jpg`: unmodified 340 × 340 portrait from `niks-website/assets/img/8-0-2.jpg`, used in that repository’s `about.md` and now on the About me page.
- `content/novarac-migration.json`: original source hashes, metadata, image inventory, RSS identifiers, and legacy URL mappings.

Edit the source and rebuild; `dist/` is generated and replaced on each successful build. `src/assets/dotted-icon.png` is the actual app icon, copied from the Dotted Line project's asset catalog. The app description and App Store link are based on that project.

Layout dividers use one shared `--divider` style: the header and footer mark the page boundaries; app and post lists have a top boundary and separators between items. There is no rule below the homepage introduction or around article headings and navigation. Rules written inside blog posts and code block borders retain their content-specific purpose. Dotted’s page uses a four-column screenshot gallery that scrolls horizontally on smaller screens, with keyboard access and no JavaScript.

## Checks

```sh
python3 -m unittest discover -s scripts -p 'test_*.py' -v
```

Checks cover draft publication, future dates, ordering, article generation, Markdown escaping, stale post removal, static links, content-only import, canonical URLs, RSS, legacy redirects, and failure handling.

## Host anywhere

Upload the **contents of `dist/`**. No server or client-side router is needed. Configure your host's normal directory index behavior and use `404.html` for its custom error page if supported.

The output includes `CNAME` for `novarac.com` and `.nojekyll` for GitHub Pages compatibility. Upload `.nojekyll` along with the other output files if hosting on GitHub Pages. These files do not change DNS or replace your live site automatically.

For a Git-based static host connected to the workspace root, use build command `python3 site/scripts/build.py` and publish directory `site/dist`. If connected to this `site/` directory, use `python3 scripts/build.py` and `dist` respectively. Python is only needed during the build; you can also build locally and upload the result.

For the existing `niks-website` GitHub repository, use the workflow and transfer instructions in the [root README](../README.md). It runs the build and deploys automatically on pushes to `master`. The repository's Pages publishing source must be set to **GitHub Actions**; the custom domain is configured in those settings, because custom Actions deployments do not use the output `CNAME` file to select a domain.

The optional `.openai/hosting.json` manifest retains the registered Sites project identity in this workspace. It is omitted from the GitHub source export. Private Sites preview publication remains blocked because the environment cannot resolve its source repository host. Other static hosts need only `dist/`.
