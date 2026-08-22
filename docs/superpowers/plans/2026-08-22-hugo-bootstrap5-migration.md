# Hugo Bootstrap 5 Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the blog to Hugo extended `0.165.0` and the maintained `filipecarneiro/hugo-bootstrap-theme` Bootstrap 5 theme without changing published content routes or the GitHub Pages deployment model.

**Architecture:** Keep the existing Hugo site and `themes/hugo-bootstrap` submodule path, replacing only the submodule remote and pinned gitlink. Use site-local templates for the article page and footer where the new theme has no equivalent for the current blog presentation; leave content bundles and shortcodes in place. Keep the source-only GitHub Actions deployment job, changing its tool/action versions and build flags.

**Tech Stack:** Hugo extended `0.165.0`, Git submodules, Bootstrap 5.3 via `filipecarneiro/hugo-bootstrap-theme`, GitHub Actions, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-08-22-hugo-bootstrap5-migration-design.md`

## Global Constraints

- Hugo must be extended `0.165.0` in local verification and CI.
- The replacement theme must remain pinned to `cc21e8101c23dfa1803f3d15a68ebb8de60fed0e` unless a build failure requires a different reviewed commit.
- Preserve `https://npatta01.github.io/`, `/post/:year/:month/:title/`, existing menu destinations, taxonomies, content, shortcode names, and static files.
- Keep deployment triggered only by pushes to `source`, publishing `public/` to `master`.
- Do not add a GA4 measurement ID or any other tracker without a user-supplied value.
- Do not commit `public/`, Hugo resources, caches, credentials, or temporary audit files.

---

### Task 1: Capture the pre-migration route baseline

**Files:**
- Read: `config.toml`
- Read: `.gitmodules`
- Read: `.github/workflows/build.yaml`
- Test output: temporary directory under `/home/npatta01/data/`

**Interfaces:**
- Consumes: the merged `source` branch and the current `themes/hugo-bootstrap` submodule.
- Produces: a disposable baseline route list and key-page checks used by Task 6.

- [ ] **Step 1: Confirm the branch starts at the merged article.**

Run:

~~~bash
git status --short --branch
git log -1 --oneline
git submodule status
~~~

Expected: clean `blog/hugo-bootstrap5-migration` branch except the committed design and plan documents, HEAD includes the merged GNOME RDP post, and the old theme gitlink is initialized.

- [ ] **Step 2: Build the current site with the workflow’s old Hugo version.**

Download the Linux amd64 Hugo `0.71.1` archive into a task-specific temporary directory, then run:

~~~bash
"$OLD_HUGO" --source . --destination "$BASELINE_DIR/public"
~~~

Expected: exit code `0`, with only the existing `Page.RSSLink` and `Page.URL` deprecation warnings.

- [ ] **Step 3: Record the baseline routes without adding them to the repository.**

Run:

~~~bash
find "$BASELINE_DIR/public" -type f -printf '/%P\n' | sort > "$BASELINE_DIR/routes.txt"
~~~

Confirm the baseline includes `/index.html`, `/about/index.html`, `/projects/index.html`, `/presentations/index.html`, `/post/2026/08/fixing-a-black-screen-with-macos-windows-app-and-ubuntu-gnome-remote-login/index.html`, `/tags/index.html`, `/categories/index.html`, `/index.xml`, `/sitemap.xml`, and the actual legacy artifact route `/post/2017/09/guide-to-elastic-search/static/index.html`.

- [ ] **Step 4: Commit no generated baseline files.**

Run:

~~~bash
git status --short
~~~

Expected: no `public/`, `resources/`, or temporary audit paths appear in the repository status.

### Task 2: Replace and pin the theme submodule

**Files:**
- Modify: `.gitmodules:1-3`
- Modify: `themes/hugo-bootstrap` gitlink

**Interfaces:**
- Consumes: `https://github.com/filipecarneiro/hugo-bootstrap-theme.git` at `cc21e8101c23dfa1803f3d15a68ebb8de60fed0e`.
- Produces: the same `themes/hugo-bootstrap` path backed by the maintained Bootstrap 5 theme.

- [ ] **Step 1: Change only the submodule remote URL.**

Edit `.gitmodules` to:

~~~ini
[submodule "themes/hugo-bootstrap"]
    path = themes/hugo-bootstrap
    url = https://github.com/filipecarneiro/hugo-bootstrap-theme.git
~~~

- [ ] **Step 2: Synchronize the local submodule remote and fetch the reviewed commit.**

Run:

~~~bash
git submodule sync --recursive
git -C themes/hugo-bootstrap fetch --depth 1 origin cc21e8101c23dfa1803f3d15a68ebb8de60fed0e
git -C themes/hugo-bootstrap checkout --detach cc21e8101c23dfa1803f3d15a68ebb8de60fed0e
git add .gitmodules themes/hugo-bootstrap
git diff --cached --check
~~~

Expected: the staged gitlink resolves to the reviewed theme commit and no source files inside the submodule are staged.

- [ ] **Step 3: Verify the staged submodule metadata before moving on.**

Run:

~~~bash
git config -f .gitmodules --get submodule.themes/hugo-bootstrap.url
git diff --cached --submodule=log -- .gitmodules themes/hugo-bootstrap
git -C themes/hugo-bootstrap rev-parse HEAD
~~~

Expected: the staged URL is `https://github.com/filipecarneiro/hugo-bootstrap-theme.git`, the staged gitlink points to `cc21e8101c23dfa1803f3d15a68ebb8de60fed0e`, and the local submodule is checked out at that full commit. A clean-clone check is deferred to Task 6 after the final migration commit, when the new metadata is in `HEAD`.

### Task 3: Modernize site configuration

**Files:**
- Modify: `config.toml:1-65`

**Interfaces:**
- Consumes: the new theme’s `main` menu, `params.options`, `params.languageISO`, and current Hugo locale keys.
- Produces: a config that loads without deprecated `languageCode`/`languageName` warnings and preserves existing routes/menu targets.

- [ ] **Step 1: Replace deprecated locale keys and remove inactive Universal Analytics.**

Change the top-level and language blocks to:

~~~toml
baseURL = "https://npatta01.github.io/"
title = "My Blog"
locale = "en-US"

paginate = 3
paginatePath = "page"
theme = "hugo-bootstrap"

defaultContentLanguage = "en"

[languages.en]
  label = "English"
  locale = "en-US"
  weight = 10
  [languages.en.params]
    languageISO = "EN"
~~~

Remove `languageCode`, `languageName`, and `googleAnalytics = "UA-47268287-3"`. Do not add `[params.googleTag]` because no valid GA4 measurement ID has been supplied.

- [ ] **Step 2: Preserve the existing menu and permalink definitions.**

Keep the five `languages.en.menu.main` entries with their current URLs and weights, the `tag` and `category` taxonomies, and:

~~~toml
[permalinks]
  post = "/post/:year/:month/:title/"
~~~

If the new theme does not receive the language-scoped menu, move the same five entries to `[[menus.main]]` without changing any URL or weight; verify the generated header before choosing that fallback.

- [ ] **Step 3: Add only the new theme’s required parameters and Hugo security exception.**

Add:

~~~toml
[security]
  allowContent = ["text/html", "text/markdown"]

[markup.goldmark.renderer]
  unsafe = true

[params.options]
  bootStrapJs = true
  breadCrumb = true
  listCategoryFilter = true
  listTagFilter = true
~~~

Retain `params.mainSections = ["post"]`, `params.author = "Nidhin Pattaniyil"`, and the existing `params.sidebar` block. Do not copy the theme demo’s organization, event, local-business, contact, or social configuration.

- [ ] **Step 4: Build immediately to expose configuration/template errors.**

Run:

~~~bash
hugo --gc --minify --logLevel info
~~~

Expected at this checkpoint: no old internal-template error, no locale deprecation warnings, and any remaining failures identify a specific local override or content compatibility issue for Task 4.

### Task 4: Adapt the site-local presentation templates

**Files:**
- Create: `layouts/_default/single.html`
- Create: `layouts/partials/footer/footer.html`
- Delete after verification: `layouts/partials/brand.html`
- Delete after verification: `layouts/partials/footer.html`
- Delete after verification: `layouts/partials/head-custom.html`
- Delete after verification: `layouts/partials/post-date.html`
- Preserve: `layouts/shortcodes/gdocs.html`
- Preserve: `layouts/shortcodes/include-text.html`
- Preserve: `layouts/shortcodes/slideshare.html`

**Interfaces:**
- Consumes: Hugo page metadata and the replacement theme’s `baseof.html` blocks.
- Produces: visible article titles/dates/taxonomies, a Bootstrap 5 footer, and unchanged shortcode names.

- [ ] **Step 1: Add an article template because the replacement theme’s default single template renders only `.Content`.**

Create `layouts/_default/single.html` with this structure:

~~~go-html-template
{{ define "main" }}
<article class="container py-3">
  <header class="mb-4">
    <h1>{{ .Title }}</h1>
    <div class="text-muted">
      {{ with .Date }}<time datetime="{{ .Format "2006-01-02" }}">{{ .Format "Jan 2, 2006" }}</time>{{ end }}
      {{ with .Params.categories }}
        <span class="ms-3">Category:
          {{ range . }}<a href="{{ (printf "/categories/%s/" (. | urlize)) | relLangURL }}">{{ . }}</a>{{ end }}
        </span>
      {{ end }}
    </div>
  </header>
  <div class="content">{{ .Content }}</div>
</article>
{{ end }}
~~~

The generated HTML must show the front-matter title for posts that do not repeat the title in Markdown, including the GNOME RDP post.

- [ ] **Step 2: Add the site footer at the replacement theme’s actual hook.**

Create `layouts/partials/footer/footer.html` with a Bootstrap 5-compatible footer that keeps the existing back-to-top behavior but removes credits to the abandoned theme:

~~~go-html-template
<footer class="blog-footer w-100">
  <nav class="navbar navbar-light bg-light">
    <p class="w-100 text-center mb-0">
      <a href="#content">Back to top</a>
    </p>
  </nav>
</footer>
~~~

- [ ] **Step 3: Remove obsolete root-level overrides only after confirming they are not called by the replacement theme.**

Confirm the theme partial calls with:

~~~bash
rg -n "brand|head-custom|post-date|partials.*footer" themes/hugo-bootstrap/layouts
~~~

Then delete the four old root-level overrides listed above. Do not delete the three shortcodes or any content/static asset.

- [ ] **Step 4: Build and inspect representative HTML.**

Run:

~~~bash
hugo --gc --minify --logLevel info
rg -n "Fixing a Black Screen|Back to top|Nidhin Pattaniyil|use redirection server name:i:1" public/post/2026/08/fixing-a-black-screen-with-macos-windows-app-and-ubuntu-gnome-remote-login/index.html
~~~

Expected: the article title, date/metadata, fix text, and footer are present; no old Xzya/Bootstrap 4 credit is present.

### Task 5: Upgrade the GitHub Actions build and deployment workflow

**Files:**
- Modify: `.github/workflows/build.yaml:1-42`
- Modify: `readme.md:8-27`

**Interfaces:**
- Consumes: the checked-in theme submodule and Hugo extended binary.
- Produces: a source-only GitHub Pages deployment using current action majors and the same `master` publish branch.

- [ ] **Step 1: Update the workflow action versions and Hugo pin.**

Keep the existing `push` trigger on `source`, `submodules: true`, and `fetch-depth: 0`. Change the relevant steps to:

~~~yaml
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: true
          fetch-depth: 0

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: '0.165.0'
          extended: true

      - name: Build
        run: hugo --gc --minify
~~~

Keep `peaceiris/actions-gh-pages@v4`, `publish_dir: ./public`, `publish_branch: master`, and `force_orphan: true` in the deploy step.

- [ ] **Step 2: Document the local build command and current CI behavior.**

Update `readme.md` so Development says:

~~~text
Install Hugo extended 0.165.0, then run:
hugo server -D
~~~

Update Deployment to describe GitHub Actions building on pushes to `source` and publishing `public/` to `master`; remove the obsolete Travis CI reference.

- [ ] **Step 3: Validate the workflow text without deploying.**

Run:

~~~bash
rg -n "actions/checkout@v4|peaceiris/actions-hugo@v3|hugo-version: '0.165.0'|extended: true|actions-gh-pages@v4|branches:|source|publish_branch" .github/workflows/build.yaml
git diff --check
~~~

Expected: all required settings are present, the trigger remains source-only, and no generated files are staged.

### Task 6: Run the full migration verification gate

**Files:**
- Test: generated `public/` only; do not commit it.
- Compare: temporary baseline route list from Task 1.

**Interfaces:**
- Consumes: the completed migration tree and the pre-migration route list.
- Produces: fresh evidence that the new theme, content, routes, and workflow are ready for review.

- [ ] **Step 1: Run the full minified build with the installed extended Hugo.**

Run:

~~~bash
hugo version
hugo --gc --minify --logLevel info
~~~

Expected: Hugo `0.165.0` extended, exit code `0`, no template errors, and no unexpected deprecation warnings.

- [ ] **Step 2: Check required generated routes and article content.**

Run:

~~~bash
test -s public/index.html
test -s public/about/index.html
test -s public/projects/index.html
test -s public/presentations/index.html
test -s public/post/2026/08/fixing-a-black-screen-with-macos-windows-app-and-ubuntu-gnome-remote-login/index.html
test -s public/tags/index.html
test -s public/categories/index.html
test -s public/index.xml
test -s public/sitemap.xml
test -s public/post/2017/09/guide-to-elastic-search/static/index.html
rg -q "use redirection server name:i:1" public/post/2026/08/fixing-a-black-screen-with-macos-windows-app-and-ubuntu-gnome-remote-login/index.html
rg -q "https://npatta01.github.io/" public/sitemap.xml
~~~

- [ ] **Step 3: Compare route inventories.**

Run:

~~~bash
find public -type f -printf '/%P\n' | sort > "$MIGRATION_DIR/routes.txt"
comm -23 "$BASELINE_DIR/routes.txt" "$MIGRATION_DIR/routes.txt"
comm -13 "$BASELINE_DIR/routes.txt" "$MIGRATION_DIR/routes.txt"
~~~

Expected: no lost HTML/XML routes; any new theme assets are classified as expected, and no existing post route is silently renamed.

- [ ] **Step 4: Check the final repository diff and generated-file exclusions.**

Run:

~~~bash
git diff --check
git status --short
git diff --stat
~~~

Expected: only intended source/config/theme/workflow/readme/spec/plan files are changed; `public/`, resources, caches, credentials, and temporary route lists are absent.

### Task 7: Commit the implementation for review

**Files:**
- Add/modify/delete: all files from Tasks 2–5
- Preserve: `docs/superpowers/specs/2026-08-22-hugo-bootstrap5-migration-design.md`
- Preserve: `docs/superpowers/plans/2026-08-22-hugo-bootstrap5-migration.md`

**Interfaces:**
- Consumes: fresh passing verification from Task 6.
- Produces: a reviewable local migration commit on `blog/hugo-bootstrap5-migration`.

- [ ] **Step 1: Review the complete diff.**

Run:

~~~bash
git diff --check
git diff --stat
git diff -- .gitmodules config.toml .github/workflows/build.yaml readme.md layouts
git diff --submodule=log -- themes/hugo-bootstrap
~~~

Confirm that the article content is unchanged from the merged `source` branch and the only content change is the already-live GNOME RDP post.

- [ ] **Step 2: Commit the migration.**

Run:

~~~bash
git add .gitmodules config.toml .github/workflows/build.yaml readme.md layouts docs/superpowers/specs/2026-08-22-hugo-bootstrap5-migration-design.md docs/superpowers/plans/2026-08-22-hugo-bootstrap5-migration.md themes/hugo-bootstrap
git commit -m "Upgrade blog to Hugo 0.165 and Bootstrap 5 theme"
~~~

- [ ] **Step 3: Verify the commit is clean.**

Run:

~~~bash
git status --short --branch
git show --stat --oneline HEAD
~~~

Expected: the migration branch is clean and the commit contains no generated output or unrelated content changes.
