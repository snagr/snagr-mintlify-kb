# Documentation project instructions

## About this project

- This is the SnagR support knowledge base, built on [Mintlify](https://mintlify.com)
- Content was migrated from Helpjuice; the raw export and `migration-report.md` live in `helpjuice-export/`
- Pages are MDX files with YAML frontmatter, organised as `<language>/<category>/<subcategory>/<article>.mdx`
- Languages: `en`, `nl`, `de`, `it`, `zh-hant`, `cn`, each a `languages` entry in `docs.json`
- Images live in `images/`; reference them with root-relative paths such as `/images/uploads/123669-icon.png`
- Configuration lives in `docs.json`
- Use the Mintlify MCP server, `https://mcp.mintlify.com`, to edit content and settings via MCP
- Use the Mintlify docs MCP server, `https://www.mintlify.com/docs/mcp`, to query information about using Mintlify via MCP

## Terminology

- "issue" for a snag or defect pin on a drawing (the app has an issue mode and a form mode)
- "form" for an inspection form or checklist
- "device" for the mobile app, "website" for the web app and Plan Viewer
- "company level" and "project level" for the two admin areas

## Style preferences

{/* Add any project-specific style rules below */}

- Use active voice and second person ("you")
- Keep sentences concise — one idea per sentence
- Use sentence case for headings
- Bold for UI elements: Click **Settings**
- Code formatting for file names, commands, paths, and code references

## Content boundaries

- `en/aahk-trd/`, `en/aahk-cwd/` and `en/power-bi-integration/` were login-only on Helpjuice and are excluded via `.mintignore`; do not add them to the public navigation without confirmation
- Articles that were unpublished on Helpjuice were not migrated
