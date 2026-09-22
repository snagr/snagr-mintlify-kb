# Migration scripts

Scripts used to convert the Helpjuice export into this Mintlify site. They only use the Python standard library and cache crawled pages in `crawl/` (re-fetched from snagr.helpjuice.com if missing).

Run order, from this directory:

1. `python3 crawl.py` - crawls category pages for article order (writes `mapping.json`)
2. `python3 crawl_q.py` - reads category and language of every published article from the live site (writes `qmap.json`)
3. `python3 media.py` - downloads images into `../../images/` (writes `media_map.json`)
4. `python3 build.py` - converts HTML to MDX, writes the language folders and `docs.json`
5. `python3 report.py` - regenerates `../migration-report.md`

`convert.py` holds the HTML to MDX converter. `linkcache.json` records old article links resolved against the live site.
