## Demo

Hand the model a novel, let it write code to break the book into pieces, summarize them with a cheaper model, and assemble one timeline.

Pass a Project Gutenberg ID, a URL, or a local file path:

```
uv run python code/demo.py 35          # The Time Machine
uv run python code/demo.py 84          # Frankenstein
uv run python code/demo.py path/to/book.txt
```

The first run downloads and caches the text under `data/`; later runs reuse the cache. At roughly 100K characters, The Time Machine runs in about a minute.

```python
#| id: demo-source
import sys
from pathlib import Path
from urllib.request import urlopen

from rlm import rlm

QUERY = """
Give me a chronological timeline of the major events in this novel.

Format using Unicode box drawing and emoji only — no ANSI escape codes. Output will be rendered via Python `print()`.

Structure:
- Vertical spine: │
- Connectors: ├── and └──
- Markers: 🔶 major turning points, 🔹 secondary, ○ minor
- Group by part/act with ▐ PART NAME ▌ headers
- Chapter refs in 「Ch. N」 brackets
- Title box: double-line box drawing (╔═╗║╚═╝)

Example:

╔══════════════════════════════════╗
║   📖  TIMELINE: [NOVEL TITLE]    ║
╚══════════════════════════════════╝

  ▐ PART ONE ▌
  │
  ├── 🔹 Event description 「Ch. 1」
  ├── 🔶 Major turning point 「Ch. 4」
  │
  ▐ PART TWO ▌
  │
  ├── 🔹 Event description 「Ch. 5」
  └── 🔶 Final event 「Ch. 12」
"""


def strip_gutenberg(text: str) -> str:
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    if start_marker in text:
        text = text.split(start_marker, 1)[-1].split("***", 1)[-1]
    if end_marker in text:
        text = text.split(end_marker, 1)[0]
    return text.strip()


def load_book(source: str) -> str:
    path = Path(source)
    if path.exists():
        return path.read_text(encoding="utf-8")

    if source.isdigit():
        book_id = source
        url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
        cache = Path(f"data/gutenberg-{book_id}.txt")
    else:
        url = source
        cache = Path("data") / Path(url.rstrip("/").split("/")[-1])

    cache.parent.mkdir(exist_ok=True)
    if not cache.exists():
        with urlopen(url) as resp:
            cache.write_text(resp.read().decode("utf-8"), encoding="utf-8")

    return strip_gutenberg(cache.read_text(encoding="utf-8"))


if len(sys.argv) < 2:
    print("usage: demo.py <gutenberg-id|url|file>", file=sys.stderr)
    sys.exit(1)

print(
    rlm(
        QUERY,
        load_book(sys.argv[1]),
        model="gpt-5.4",
        sub_model="gpt-5-mini",
        max_iters=30,
        verbose=True,
        reasoning_effort="low",
    )
)
```

The point is not that the model memorized Wells - it is that it built its own reading strategy.

```python
#| file: code/demo.py
<<demo-source>>
```
