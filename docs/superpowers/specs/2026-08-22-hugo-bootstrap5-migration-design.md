# Hugo Bootstrap 5 Migration Design

**Date:** 2026-08-22  
**Status:** Proposed

## Goal

Move the blog from the abandoned 2018 `Xzya/hugo-bootstrap` theme and Hugo `0.71.1` to Hugo `0.165.0` with the maintained `filipecarneiro/hugo-bootstrap-theme` Bootstrap 5 theme, while preserving the existing content, navigation, canonical URLs, and GitHub Pages deployment model.

## Context

The current theme is pinned as a Git submodule at `dec099d40eb6144b4f6b1e32ef45c505db9e8e11` and calls removed Hugo internal templates. A disposable build with Hugo `0.165.0` fails before rendering on `_internal/google_analytics_async.html`; the site also contains an intentional HTML artifact at `content/post/2017/elastic/static/index.html`, which current Hugo blocks unless the content security policy explicitly allows HTML.

The replacement theme is Bootstrap 5 based, actively maintained, and documents Hugo `0.158.0+` plus the extended build as prerequisites. A disposable build reached the content-security check with Hugo `0.165.0`, confirming that the theme itself is compatible with the current Hugo version.

## Chosen approach

Use `filipecarneiro/hugo-bootstrap-theme` as the existing `themes/hugo-bootstrap` submodule path. Keeping the path stable minimizes configuration and repository-layout churn while pinning the submodule to a reviewed upstream commit. The visual language remains Bootstrap-based, but the replacement theme may change spacing, typography, navigation markup, and responsive behavior; the content model and URLs remain stable.

Alternative approaches considered:

1. **Repair the old theme locally.** Lowest visual change, but retains an unmaintained 2018/2019 template set and makes future Hugo upgrades the site’s responsibility.
2. **Use `razonyang/hugo-theme-bootstrap`.** Feature-rich and maintained for compatibility, but its own README places it in maintenance mode and recommends a separate incompatible successor for new sites.
3. **Use a non-Bootstrap modern blog theme.** Could provide a cleaner redesign, but would create the largest visual and template migration risk for this site.

## Scope

### Site configuration

- Set the site locale using current Hugo keys: `locale = "en-US"` and `languages.en.label = "English"`.
- Keep `baseurl`, the current menu destinations, taxonomies, pagination, and `/post/:year/:month/:title/` permalink structure.
- Add `[security] allowContent = ["text/html", "text/markdown"]` to preserve the existing published HTML artifact under `content/post/2017/elastic/static/` while allowing the site’s Markdown sources to render.
- Remove the obsolete Universal Analytics `UA-47268287-3` configuration rather than emitting a nonfunctional tracker. Do not add a GA4 tracker without a user-supplied `G-...` measurement ID.
- Add the replacement theme’s minimal Bootstrap, SEO, and menu parameters without copying unrelated demo-site settings.

### Theme and local overrides

- Change the Git submodule URL to `https://github.com/filipecarneiro/hugo-bootstrap-theme.git` and pin it to the reviewed release commit.
- Retain existing local overrides only where the new theme exposes the equivalent hook: brand/header, footer, head customizations, post date, and shortcodes.
- Adapt override markup to Bootstrap 5 classes and the new theme’s partial names; do not copy the entire theme into the site.
- Preserve existing page assets, content bundles, shortcode names, and static files.

### Build and deployment

- Pin CI to Hugo extended `0.165.0` using the current `peaceiris/actions-hugo` major and update checkout/GitHub Pages actions to supported major versions.
- Keep deployment on pushes to `source`, publishing the generated `public/` directory to `master` through the existing GitHub Pages workflow.
- Do not add a public preview service, change the Pages repository/branch model, or publish from pull requests.

## Compatibility and error handling

- Any content path that disappears, changes URL, or fails to render is a migration failure; the branch must not be presented as ready until the generated route inventory is compared with the pre-migration build.
- Build warnings from deprecated configuration or removed theme APIs must be resolved or explicitly classified. The target build should have no template errors and no unexpected deprecation warnings.
- If a custom partial is not compatible with the replacement theme, prefer a small site-local override or hook adaptation over copying all upstream templates.
- If the replacement theme cannot preserve the current navigation and content routes without broad rewrites, stop and report the mismatch rather than silently redesigning the site.

## Verification

The migration is ready for review only when all of the following pass on Hugo `0.165.0` extended:

1. `hugo --gc --minify` completes successfully.
2. The generated article route for the GNOME RDP post exists and contains the documented `use redirection server name:i:1` fix.
3. Existing high-value routes exist: `/`, `/about/`, `/projects/`, `/presentations/`, `/notes/`, at least one older post, tag/category pages, RSS, sitemap, and the static HTML artifact.
4. No generated internal links point to missing pages, and the canonical URL prefix remains `https://npatta01.github.io/`.
5. The working tree diff contains no generated `public/`, resources, caches, credentials, or unrelated content changes.
6. The GitHub Actions workflow parses and uses Hugo extended `0.165.0` while retaining source-only deployment.

## Rollback

The migration will be isolated on its own branch. Reverting the migration commit restores the old submodule URL, config, overrides, and workflow. The article commit already merged into `source` is independent and must not be reverted as part of this migration.
