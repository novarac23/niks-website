# Nik’s Website

The personal maker site includes apps at `/apps/`, a Markdown blog at `/blog/`, and an about page. The generated static website is in [`site/dist/`](site/dist/). See [`site/README.md`](site/README.md) for writing posts, editing, and hosting instructions.

All nine existing blog posts from `niks-website` are migrated with their original dates and five referenced images. See [migration details](site/MIGRATION.md). The canonical domain is `https://novarac.com`.

For future contributors and coding agents, start with [AGENTS.md](AGENTS.md). [PRODUCT.md](PRODUCT.md) records the site's purpose, approved content, and redesign history; [DESIGN.md](DESIGN.md) records the current style and responsive behavior. Impeccable's design sidecar is in `.impeccable/design.json`. These files are included in the source ZIP and are repository documentation, not published pages.

To preview from this directory:

```sh
python3 site/scripts/build.py
python3 -m http.server 8080 --directory site/dist
```

## Publish through the existing niks-website repository

The replacement workflow is `.github/workflows/github-pages.yml`. It checks the site, builds it with Python, and publishes `site/dist` to GitHub Pages whenever you push to `master`, matching the existing repository's branch. It also supports a manual run from the Actions tab. The GitHub runner handles Python; the published website is static.

1. Extract **`novarac-source.zip`** into the root of your existing `niks-website` checkout. The archive includes `.github/`, `site/`, and the contributor/design documentation, with Git metadata and generated files excluded. This replaces the old Jekyll workflow at the same filename. Keep the existing checkout's own `.git` directory.
2. In the repository's **Settings → Pages**, set **Build and deployment → Source** to **GitHub Actions**. Keep the custom domain set to **novarac.com** and HTTPS enabled.
3. Commit and push to `master`. The new workflow deploys the site automatically using GitHub's built-in token; it does not use `JEKYLL_PAT`.

Keep the `site/` folder at the repository root as packaged. Old Jekyll source files can remain in the repository: the new workflow publishes only the generated `site/dist/` output.

For future posts, edit Markdown under `site/content/posts/`, set `draft: false`, and push. GitHub builds and publishes the update for you.

`novarac-static.zip` contains only the prebuilt website for manual uploading. Use `novarac-source.zip` for this GitHub Actions workflow.
