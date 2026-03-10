## Step 5: Capturing print output without touching sys.stdout

The model writes `print()` calls to see intermediate results. We need to capture that output to feed it back. The standard approach is redirecting `sys.stdout` to a `StringIO` buffer — but that mutates global interpreter state and requires a `finally` block to clean up.

Simpler: shadow `print` in the namespace.

~~~python
output = []
ns["print"] = lambda *a: output.append(" ".join(str(x) for x in a))

exec(code, ns)

result = "\n".join(output)
~~~

The model calls `print()`. Our lambda catches it. No global state, no cleanup, no `import sys`, no `import io`. The REPL is now *entirely* defined by what's in the namespace dict.
