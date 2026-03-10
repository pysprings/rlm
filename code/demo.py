# ~/~ begin <<docs/05-demo.md#code/demo.py>>[init]
# ~/~ begin <<docs/05-demo.md#demo-source>>[init]
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
# ~/~ end
# ~/~ end
