## Demo: The Time Machine

Hand the model a novel, let it write code to break the book into pieces, summarize them with a cheaper model, and assemble one timeline.

Run it with `uv run python code/demo.py`. The first run downloads and caches the text; later runs reuse `data/the-time-machine.txt`.

At roughly 100K characters, it runs in about a minute.

Verbose mode prints each `repl` block and its output as the model works.

```python
#| id: demo-source
from pathlib import Path
from urllib.request import urlopen

from rlm import rlm

URL = "https://www.gutenberg.org/files/35/35-0.txt"
CACHE = Path("data/the-time-machine.txt")
QUERY = "Give me a chronological timeline of the major events in this novel."


def load_the_time_machine():
    CACHE.parent.mkdir(exist_ok=True)
    if not CACHE.exists():
        with urlopen(URL) as resp:
            CACHE.write_text(resp.read().decode("utf-8"), encoding="utf-8")
    text = CACHE.read_text(encoding="utf-8")
    start = "*** START OF THE PROJECT GUTENBERG EBOOK THE TIME MACHINE ***"
    end = "*** END OF THE PROJECT GUTENBERG EBOOK THE TIME MACHINE ***"
    return text.split(start, 1)[-1].split(end, 1)[0].strip()


print(
    rlm(
        QUERY,
        load_the_time_machine(),
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
