## Step 1: The REPL is just a dictionary

A REPL environment sounds fancy. It isn't. Python's `exec()` runs a string of code inside a namespace, and a namespace is just a dict:

~~~python
ns = {"context": my_big_document}
exec('print(len(context))', ns)
# prints: 4382917
~~~

That's it. The variable `context` lives in `ns`. Any code we `exec()` with that namespace can see it. Variables the code creates land there too. It's a persistent scratch space — same as Jupyter cells sharing state.
