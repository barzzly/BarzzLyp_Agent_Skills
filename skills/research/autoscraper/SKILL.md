---
name: autoscraper
version: 1.0.0
source: https://github.com/alirezamika/autoscraper
source_commit: 68a818158c673bf320a8569da10a8b979c1d23fe
---

# AutoScraper Notes

AutoScraper is a Python library that learns extraction rules from sample values in HTML. Use it for static or server-rendered pages where representative wanted values exist.

## API

- `AutoScraper().build(url, wanted_list, ...)` learns rules from URL content.
- `build(html=html_string, wanted_list=...)` learns without fetching a URL.
- `wanted_dict` maps aliases to target values; aliases are retained in learned rules.
- `get_result_similar(url)` extracts related elements.
- `get_result_exact(url)` returns results in wanted-item order.
- `get_results(url)` returns exact and similar result sets.
- `save(path)` serializes learned `stack_list` JSON; `load(path)` restores it.
- `remove_rules(...)` and `keep_rules(...)` prune learned rules.
- `request_args` passes custom requests arguments such as headers or proxies.
- `text_fuzz_ratio` controls fuzzy matching; default `1.0` means exact matching.

## How it works

1. Fetch HTML with `requests`, or accept supplied HTML.
2. Normalize/unescape HTML and parse with BeautifulSoup `lxml`.
3. Find DOM nodes whose text, non-recursive text, attributes, or resolved `href`/`src` match wanted samples.
4. Learn stack rules from matching nodes and ancestors.
5. Deduplicate results and learned rules while preserving order.

## Constraints

- It is not a browser automation tool and does not execute JavaScript. Use browser or API endpoint when content is client-rendered.
- Learning quality depends on representative sample values. Multiple wanted samples improve rule precision.
- Exact mode preserves wanted-item ordering; similar mode can return related matches.
- `request_args` is mutated when headers are popped internally; pass disposable dictionary.
- Keep credentials, cookies, proxies, and private endpoints outside public source files.
- Respect site terms, robots policies, rate limits, and access permissions.
- Validate parser behavior on target page before relying on learned rules.

## Relevant implementation details

- Default User-Agent is Chrome-like and can be overridden through `request_args["headers"]`.
- `build` requires `wanted_list` or non-empty `wanted_dict`.
- `normalize` uses Unicode NFKD and strips strings.
- Fuzzy matching uses `difflib.SequenceMatcher`.
- Package dependencies: `requests`, `beautifulsoup4`, and `lxml`.

## Practical workflow

```python
from autoscraper import AutoScraper

scraper = AutoScraper()
scraper.build(url, wanted_list=["sample title"], update=False)
results = scraper.get_result_similar(url)
scraper.save("scraper-rules.json")
```

For structured records, use `wanted_dict` aliases and verify outputs against known fixtures before production use. For dynamic pages, obtain rendered HTML first, then pass `html=` or use an API.
