# SnagR knowledge base

Documentation site for SnagR, built with [Mintlify](https://mintlify.com). The content was migrated from the Helpjuice knowledge base (export in `helpjuice-export/`, migration notes in `helpjuice-export/migration-report.md`).

## Layout

- `docs.json` - site configuration and navigation (one `languages` entry per language).
- `en/`, `nl/`, `de/`, `it/`, `zh-hant/`, `cn/` - one folder per language, then one folder per category and subcategory. Each article is an MDX file.
- `images/` - all images referenced by the articles (`uploads/` and `direct/` came from Helpjuice, `guidde/` from embedded Guidde walkthroughs).

## Local preview

```bash
npm i -g mint
mint dev
```

Then open `http://localhost:3000`.

## Checks

```bash
mint validate
mint broken-links
mint a11y
```
