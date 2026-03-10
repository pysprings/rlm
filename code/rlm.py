# ~/~ begin <<docs/04-implementation.md#code/rlm.py>>[init]
# ~/~ begin <<docs/04-implementation.md#rlm-source>>[init]
"""
rlm.py — A complete Recursive Language Model in one function.
Requires: pip install openai
"""

import re
from openai import OpenAI

client = OpenAI()  # uses OPENAI_API_KEY env var

SYSTEM = """You answer queries using a Python REPL. \
The variable `context` holds your input data.
You have `llm_query(prompt)` to call a sub-LLM (~500K char capacity).
Call `FINAL(value)` inside a code block to return your answer — \
in the same block where you produce the final answer.
Wrap all code in ```repl ... ``` blocks. \
Use print() to inspect intermediate values. \
Output from print() and errors are returned as your next message.
Always explore context before answering.

Example:
```repl
chunks = [context[i:i+10000] for i in range(0, len(context), 10000)]
results = [llm_query(f"Summarize: {c}") for c in chunks]
answer = llm_query(f"Combine summaries: {results}")
FINAL(answer)
``` """


class _Done(Exception):
    """Raised by FINAL() to unwind exec and deliver the answer."""
    def __init__(self, value): self.value = value


def rlm(query, context, model="gpt-5.4", sub_model="gpt-5-mini",
        max_iters=30, verbose=False, reasoning_effort="low"):
    output = []

    def final(v): raise _Done(str(v))

    ns = {
        "context": context,
        "FINAL": final,
        "print": lambda *a: output.append(
            " ".join(str(x) for x in a)),
        "llm_query": lambda p: client.chat.completions.create(
            model=sub_model,
            messages=[{"role": "user",
                       "content": p if isinstance(p, str) else str(p)}]
        ).choices[0].message.content,
    }

    msgs = [{"role": "system", "content": SYSTEM}]
    resp = None

    for _ in range(max_iters):
        msgs.append({"role": "user",
                      "content": f"Query: {query}"})

        kwargs = {"model": model, "messages": msgs}
        if reasoning_effort:
            kwargs["reasoning_effort"] = reasoning_effort
        resp = client.chat.completions.create(
            **kwargs
        ).choices[0].message.content
        msgs.append({"role": "assistant", "content": resp})

        for code in re.findall(
            r'```repl\s*\n(.*?)\n```', resp, re.DOTALL
        ):
            output.clear()
            if verbose:
                print(f"\n```repl\n{code}\n```")
            try:
                exec(code, ns)
            except _Done as d:
                return d.value
            except Exception as e:
                output.append(f"Error: {e}")
            out = "\n".join(output) or "(no output)"
            if len(out) > 50000:
                out = out[:50000] + "...[truncated]"
            if verbose:
                print(out)
            msgs.append({"role": "user",
                          "content": f"REPL output:\n{out}"})

    return resp
# ~/~ end
# ~/~ end
