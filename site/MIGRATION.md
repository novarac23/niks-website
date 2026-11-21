# novarac.com blog migration

Imported from the local `niks-website` Jekyll repository on November 18, 2026. This is a content-only migration into the existing Nik’s Website design. No old theme, stylesheets, navigation, or page templates were copied. The source repository is read-only and remains unchanged.

## Imported posts

| Original date | Original title | New URL |
| --- | --- | --- |
| 2023-08-06 | Simple And Practical NLP | `/blog/simple-and-practical-nlp/` |
| 2023-06-24 | Survive Grad School while working full time | `/blog/guide-on-surviving-grad-school/` |
| 2022-12-22 | Lessons Learned In 2022 | `/blog/lessons-learned/` |
| 2021-11-18 | Back To The Basics - Statistics | `/blog/back-to-basics-stats/` |
| 2021-01-01 | Lessons Learned In 2020 | `/blog/lessons-learned-2020/` |
| 2020-12-26 | Tweetanator Updates | `/blog/tweetanator-updates/` |
| 2020-02-15 | Prevent Overengineering | `/blog/overengineering-solutions/` |
| 2020-01-24 | Feedback Loops | `/blog/feedback-loops/` |
| 2019-12-30 | Lessons Learned In 2019 | `/blog/lessons-from-2019/` |

All nine source posts are included. Original titles, descriptions (including existing typos), prose, code blocks, links, and image alt text are retained. Dates come from the original Jekyll filenames. Categories were retained during the initial import and removed from active posts, pages, and RSS on November 21, 2026. Historical migration metadata and legacy URLs remain intact. The unpublished new-post template remains a draft.

Five referenced image files are copied byte-for-byte under `src/assets/img/`. They keep their original `/assets/img/` URLs. The old repository's four unused images and theme assets were not imported.

## Adaptations for the new static site

- Added explicit `date` and `draft: false` fields to the post front matter. The importer now omits categories from generated post front matter while recording their original values for migration provenance and legacy URLs.
- Replaced Jekyll's `{{ site.url }}` image prefix with local relative paths.
- Updated the existing internal link to Feedback Loops to its new local `/blog/` location. External links, including historical Tweetanator and social links, are preserved as written; their destinations were not independently checked.
- Added renderer support for the source posts' escaped apostrophes and quotes, underscore italics, Unicode bullets, and stable heading IDs.
- Added static Python syntax highlighting. The two result blocks in Simple And Practical NLP are labeled `text` instead of `python` so their output is displayed without misleading syntax colors. The contents of all code blocks are unchanged. Target hashes in the migration manifest record the initial import, before this formatting-only edit.
- Generated a feed at `/feed.xml` using the original post dates. Categories are no longer emitted. Imported posts retain identifiers derived from the old feed's URL configuration and Jekyll permalink pattern; item links point to the new pages. Feed content uses absolute image and link URLs.
- Set canonical metadata and the sitemap to `https://novarac.com`.

## Older links

The build creates 20 static compatibility pages: one short root-level alias and one original Jekyll date/category alias per imported post, plus `/archive/` and `/archive.html` leading to `/blog/`. Visiting `/archive` also works with normal directory-index hosting.

Date/category paths are derived from the source repository's default Jekyll permalink configuration. Root-level aliases support the older short URL style used in the source posts' own links. The live archive could not be fetched to independently compare its rendered URLs.

Compatibility pages use an HTML refresh, a canonical URL, and a normal clickable link. They work on static hosts without a server redirect configuration. The alias files are omitted when a post is removed or returned to draft.

## Provenance and repeatability

`content/novarac-migration.json` records the source Git commit, SHA-256 hashes of each source post and copied image, original metadata, destination paths, and compatibility URLs.

The original import command, run from `site/`, was:

```sh
python3 scripts/import_jekyll.py /Users/novarac23/Projects/niks-website
```

The importer refuses to overwrite different existing post or image content, protecting subsequent edits. Edit the migrated Markdown directly for normal writing; importing is a one-time migration step. The build no longer depends on the old checkout or on Jekyll.
