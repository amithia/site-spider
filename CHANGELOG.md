# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

Nothing published yet — everything below has landed on `main` but hasn't been
tagged or released to PyPI.

### Changed
- `project.license` now uses the PEP 639 SPDX form (`license = "MIT"` plus
  `license-files`). The old TOML-table form was deprecated and stops being
  supported after 2027-02-18.
- **Renamed to `site-spider`.** The old name was generic and already taken on
  PyPI, so the project could never have been published under it. The
  distribution, the console command and the default User-Agent are all
  `site-spider` now. The import package is `sitespider` (Python module names
  cannot contain a hyphen) and `sitespider` also works as a command alias.
  `crawl_sitemap.py` still works for anyone running from a checkout.

- PyPI packaging metadata: keywords and trove classifiers, and a
  `Release` workflow that publishes to PyPI on a `v*` tag via trusted
  publishing (OIDC, no stored API token). The workflow refuses to publish
  if the tag and `pyproject.toml` version disagree, runs `twine check
  --strict`, and verifies the HTML template is present in both the wheel
  and the sdist.
- Python 3.13 added to the CI matrix, and declared in the classifiers.

### Added
- `--keep-query`: keeps query strings instead of stripping them, for sites
  that address distinct pages through parameters (`?id=`, `?page=`).
  Parameters are sorted so `?a=1&b=2` and `?b=2&a=1` are one URL.
- `--fail-on-removed` and `--fail-on-gaps`: exit `3` when a diff shows pages
  have disappeared, or when coverage verification finds unexplained gaps.
  `--diff-against` and `--verify` previously always exited `0`, so a
  scheduled crawl could report a problem but never fail a build. `3` rather
  than `2` keeps a tripped gate distinguishable from an argparse usage error.
- Installable CLI: `pyproject.toml` with a `sitemap-generator` console_scripts
  entry point (`pip install .` / `pipx install .`), instead of requiring a
  git clone. `crawl_sitemap.py` at the repo root remains as a
  backward-compatible shim for anyone still running from a checkout.
- `--version` flag.
- Automated test suite (`tests/test_cli.py`, stdlib `unittest`) and a CI
  workflow (GitHub Actions) running it across Python 3.10–3.12 plus `ruff`
  linting on every push/PR.
- SSRF hardening: every fetch — including each redirect hop — now refuses
  hosts that resolve to a private/loopback/link-local/reserved address
  unless `--allow-private-ips` is passed.
- `--max-duration SECONDS`: an optional wall-clock cap on a crawl, on top of
  the existing `--max-pages`/`--max-depth`.
- `--sitemap-xml FILE`: writes a standards-compliant `sitemap.xml` from crawl
  results (`noindex` pages excluded).
- `--diff-against FILE`: compares this crawl's URLs against a previous
  `--json` snapshot and reports what was added/removed since then.
- `--render-js` (optional `js` extra): fetches pages through a headless
  Chromium instance instead of raw HTTP, so JavaScript-injected links are
  discoverable. `--chromium-path` points it at an existing Chrome/Chromium
  install instead of downloading one.

### Fixed
- Sites that redirect apex to `www` (or vice versa) returned "No URLs
  discovered". The two spellings are now treated as one site, and the crawl
  adopts whichever host the base URL actually lands on — so later requests
  skip the redirect hop and a generated `sitemap.xml` carries the canonical
  host.
- The interactive map escaped link *text* but not link *URLs*, so a URL
  containing a quote could break out of an `href="..."` attribute and inject
  markup into the map. URLs are now escaped and restricted to
  `http`/`https`/`mailto`/`tel`.
- `--serve`'s re-crawl progress always reported 0 pages: the live crawl state
  the status endpoint reads was declared but never assigned.
- When `robots.txt` advertised several sitemaps, only the first one that
  returned any URLs was parsed and the rest were silently dropped. All
  advertised sitemaps are now read, with the well-known paths kept as a
  fallback.

## [0.1.0] - unreleased

The original crawler: sitemap.xml discovery with BFS-crawl fallback and
cross-checking (`auto`/`sitemap`/`crawl`/`hybrid` modes), politeness controls
(robots.txt, rate limiting, retry/backoff), checkpointed resumable crawls,
concurrent workers over keep-alive connections, ETag/Last-Modified caching
(`--fresh`), `noindex` detection, per-page outbound link capture, coverage
verification (`--verify`), and the interactive HTML map (`--html`/`--serve`)
with edit mode, drag-to-reparent, and export.
